"""tenant_facts.py: единый источник живых чисел тенанта для курса.

Зачем. Счётчики тенанта (сколько сервисов, баз, дашбордов, релизов) были вписаны
в текст 12 раз в 9 темах и разъехались: в одной теме «244 Services», в другой
«239 Services», в третьей «241 Services» — все три числа сняты с одного экрана в
разные моменты. Такой текст устаревает молча, и заметить это можно только глазами.

Решение. Число живёт в одном месте (`state/tenant_facts.json`), в explanations
стоит плейсхолдер `{{tenant:services}}`, подстановка происходит при сборке. Чтобы
обновить курс, достаточно обновить JSON и пересобрать: ни модель, ни браузер для
этого не нужны.

Три способа наполнить JSON, от самого дешёвого к самому точному:

    python scripts/tenant_facts.py --from-snapshot
        Берёт счётчики из заголовков `ui_elements.json` (то, что уже лежит в репо
        после обхода краулером). Ноль сети, ноль зависимостей, работает всегда.

    python scripts/tenant_facts.py --from-api
        Обновляет по Dynatrace Environment API v2 токеном из .env (DT_API_TOKEN,
        права entities.read + problems.read + ReadConfig). Только stdlib
        urllib, без playwright и без LLM. Печатает дифф со старыми значениями:
        применяются только те ключи, которые реально ответили.

    python scripts/tenant_facts.py --set services=244
        Ручная правка одного ключа, когда число снято глазами с экрана.

Проверка свежести (для джобы и для человека):

    python scripts/tenant_facts.py --check --max-age-days 30

Exit code: 0 — всё в порядке; 1 — есть протухшие или отсутствующие факты.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FACTS_FILE = ROOT / "state" / "tenant_facts.json"
SNAPSHOT_FILE = ROOT / "ui_elements.json"
ENV_FILE = ROOT / ".env"

PLACEHOLDER_RE = re.compile(r"\{\{tenant:([a-z0-9_]+)\}\}")
DEFAULT_MAX_AGE_DAYS = 45
API_TIMEOUT_S = 20


class FactsError(RuntimeError):
    """Отсутствующий ключ или битый файл фактов — повод уронить сборку."""


# ---------------------------------------------------------------------------
# Каталог фактов
#
# snapshot_route/snapshot_re — откуда взять число из ui_elements.json.
# api — как спросить у Environment API v2. Селекторы помечены verified=False,
# пока их паритет с числом на экране не подтверждён живым прогоном: первый
# `--from-api` печатает дифф, человек сверяет с UI и только потом доверяет.
# ---------------------------------------------------------------------------

CATALOG: dict[str, dict] = {
    "services": {
        "label": "Services",
        "snapshot_route": "/ui/services",
        "snapshot_re": r"^(\d[\d\s,]*)\s*Services$",
        "api": {"kind": "entities", "selector": 'type("SERVICE")'},
        "verified": False,
    },
    "databases": {
        "label": "Databases",
        "snapshot_route": "/ui/databases",
        "snapshot_re": r"^(\d[\d\s,]*)\s*Databases$",
        "api": {"kind": "entities", "selector": 'type("SERVICE"),serviceType("DATABASE_SERVICE")'},
        "verified": False,
    },
    "hosts": {
        "label": "Hosts",
        "api": {"kind": "entities", "selector": 'type("HOST")'},
        "verified": False,
    },
    "applications": {
        "label": "Applications",
        "api": {"kind": "entities", "selector": 'type("APPLICATION")'},
        "verified": False,
    },
    "problems_open": {
        "label": "открытых проблем",
        "api": {"kind": "problems", "selector": 'status("OPEN")'},
        "verified": False,
    },
    "dashboards": {
        "label": "Dashboards",
        "api": {"kind": "dashboards"},
        "verified": False,
    },
}


# ---------------------------------------------------------------------------
# Чтение и запись
# ---------------------------------------------------------------------------


def load_raw() -> dict:
    if not FACTS_FILE.exists():
        return {"tenant": "", "facts": {}}
    try:
        return json.loads(FACTS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # битый файл лучше видеть сразу
        raise FactsError(f"{FACTS_FILE} повреждён: {exc}") from exc


def load_values() -> dict[str, str]:
    """{ключ: значение-строка} для подстановки в текст."""
    return {k: str(v["value"]) for k, v in load_raw().get("facts", {}).items()}


def save_raw(data: dict) -> None:
    FACTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    FACTS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def substitute(text: str, values: dict[str, str] | None = None, *, where: str = "") -> str:
    """Подставляет {{tenant:key}}. Неизвестный ключ — исключение, не тихий пропуск."""
    if values is None:
        values = load_values()
    missing: list[str] = []

    def repl(m: re.Match) -> str:
        key = m.group(1)
        if key not in values:
            missing.append(key)
            return m.group(0)
        return values[key]

    out = PLACEHOLDER_RE.sub(repl, text)
    if missing:
        where_s = f" ({where})" if where else ""
        raise FactsError(
            f"нет значения для плейсхолдера: {', '.join(sorted(set(missing)))}{where_s}. "
            f"Заполнить: python scripts/tenant_facts.py --from-snapshot "
            f"(или --set {sorted(set(missing))[0]}=<число>)"
        )
    return out


def _stamp(data: dict, key: str, value, source: str) -> None:
    data.setdefault("facts", {})[key] = {
        "value": value,
        "label": CATALOG.get(key, {}).get("label", key),
        "source": source,
        "observed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verified_against_ui": CATALOG.get(key, {}).get("verified", False),
    }


# ---------------------------------------------------------------------------
# Источник 1: снапшот ui_elements.json (без сети)
# ---------------------------------------------------------------------------


def collect_from_snapshot() -> dict[str, int]:
    """Самые свежие счётчики из заголовков обхода.

    В снапшоте один маршрут встречается несколько раз (несколько тем ходят на
    /ui/services), и числа отличаются: экран живой. Берём последнее вхождение,
    оно соответствует последнему обходу.
    """
    if not SNAPSHOT_FILE.exists():
        raise FactsError(f"нет {SNAPSHOT_FILE}")
    entries = json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
    found: dict[str, int] = {}
    for key, spec in CATALOG.items():
        route, pattern = spec.get("snapshot_route"), spec.get("snapshot_re")
        if not route or not pattern:
            continue
        rx = re.compile(pattern)
        for entry in entries:
            if entry.get("plan_route") != route:
                continue
            for heading in entry.get("ui", {}).get("headings") or []:
                m = rx.match(heading.get("text", "").strip())
                if m:
                    found[key] = int(re.sub(r"[\s,]", "", m.group(1)))
    return found


# ---------------------------------------------------------------------------
# Источник 2: Environment API v2 (только stdlib, без браузера и без модели)
# ---------------------------------------------------------------------------


def read_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if k.startswith("DT_")})
    return env


def _api_get(base: str, path: str, params: dict, token: str) -> dict:
    url = f"{base.rstrip('/')}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Api-Token {token}"})
    with urllib.request.urlopen(req, timeout=API_TIMEOUT_S) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


def collect_from_api(base: str, token: str) -> tuple[dict[str, int], list[str]]:
    """Возвращает (значения, список ошибок по ключам). Частичный успех допустим."""
    values: dict[str, int] = {}
    errors: list[str] = []
    for key, spec in CATALOG.items():
        api = spec.get("api")
        if not api:
            continue
        try:
            if api["kind"] == "entities":
                body = _api_get(
                    base,
                    "/api/v2/entities",
                    {"entitySelector": api["selector"], "pageSize": 1},
                    token,
                )
                values[key] = int(body["totalCount"])
            elif api["kind"] == "problems":
                body = _api_get(
                    base,
                    "/api/v2/problems",
                    {"problemSelector": api["selector"], "pageSize": 1},
                    token,
                )
                values[key] = int(body["totalCount"])
            elif api["kind"] == "dashboards":
                body = _api_get(base, "/api/config/v1/dashboards", {}, token)
                values[key] = len(body.get("dashboards", []))
        except (urllib.error.URLError, KeyError, ValueError, TypeError) as exc:
            errors.append(f"{key}: {type(exc).__name__}: {exc}")
    return values, errors


# ---------------------------------------------------------------------------
# Команды
# ---------------------------------------------------------------------------


def cmd_apply(values: dict[str, int], source: str) -> int:
    data = load_raw()
    before = {k: v.get("value") for k, v in data.get("facts", {}).items()}
    for key, value in sorted(values.items()):
        was = before.get(key)
        mark = "нов." if was is None else ("=" if was == value else f"было {was}")
        print(f"  {key:16s} {value:>8}  ({mark})")
        _stamp(data, key, value, source)
    if not values:
        print("  ничего не получено")
        return 1
    data["tenant"] = data.get("tenant") or read_env().get("DT_TENANT", "")
    data["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_raw(data)
    print(f"→ {FACTS_FILE.relative_to(ROOT)}")
    return 0


def cmd_check(max_age_days: int) -> int:
    data = load_raw()
    facts = data.get("facts", {})
    used = used_keys()
    missing = sorted(used - set(facts))
    limit = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    stale = []
    for key, entry in sorted(facts.items()):
        try:
            observed = datetime.fromisoformat(entry["observed_at"])
        except (KeyError, ValueError):
            stale.append((key, "нет даты наблюдения"))
            continue
        age = (datetime.now(timezone.utc) - observed).days
        flag = "ПРОТУХ" if observed < limit else "ок"
        unverified = "" if entry.get("verified_against_ui") else "  (паритет с UI не сверен)"
        print(f"  {key:16s} {str(entry['value']):>8}  {entry['source']:9s} {age:>3}д  {flag}{unverified}")
        if observed < limit:
            stale.append((key, f"{age} дней"))
    for key in missing:
        print(f"  {key:16s} {'—':>8}  ОТСУТСТВУЕТ (используется в explanations)")
    if stale or missing:
        print(f"\n❌ протухших: {len(stale)}, отсутствующих: {len(missing)}")
        return 1
    print(f"\n✅ все факты свежее {max_age_days} дней")
    return 0


def used_keys() -> set[str]:
    """Ключи, реально встречающиеся в explanations."""
    keys: set[str] = set()
    expl = ROOT / "explanations"
    if expl.is_dir():
        for md in expl.rglob("*.md"):
            keys |= set(PLACEHOLDER_RE.findall(md.read_text(encoding="utf-8")))
    return keys


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--from-snapshot", action="store_true", help="взять числа из ui_elements.json")
    ap.add_argument("--from-api", action="store_true", help="обновить по Environment API v2")
    ap.add_argument("--set", metavar="KEY=VALUE", action="append", default=[])
    ap.add_argument("--check", action="store_true", help="отчёт о свежести")
    ap.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS)
    args = ap.parse_args()

    if args.check:
        return cmd_check(args.max_age_days)

    if args.set:
        values = {}
        for pair in args.set:
            if "=" not in pair:
                print(f"ERROR: ожидался KEY=VALUE, получено {pair!r}", file=sys.stderr)
                return 2
            k, v = pair.split("=", 1)
            values[k.strip()] = int(v.strip())
        print("Ручная правка:")
        return cmd_apply(values, "manual")

    if args.from_api:
        env = read_env()
        base, token = env.get("DT_TENANT", ""), env.get("DT_API_TOKEN", "")
        if not base or not token:
            print(
                "ERROR: нужны DT_TENANT и DT_API_TOKEN в .env.\n"
                "Токен создаётся в тенанте: Access tokens → Generate new token,\n"
                "права entities.read, problems.read, ReadConfig.",
                file=sys.stderr,
            )
            return 2
        print(f"Environment API v2 → {base}")
        values, errors = collect_from_api(base, token)
        for err in errors:
            print(f"  ! {err}", file=sys.stderr)
        return cmd_apply(values, "api")

    if args.from_snapshot:
        print(f"Снапшот {SNAPSHOT_FILE.name}:")
        return cmd_apply(collect_from_snapshot(), "snapshot")

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
