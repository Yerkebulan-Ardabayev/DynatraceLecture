"""routes_check.py: сверка адресов курса с ground truth. Без сети, без модели.

Зачем. Курс переведён в формат «маршрут»: у каждого объекта написано, где он
живёт и по какому адресу открывается. Такой текст полезен ровно настолько,
насколько адреса настоящие. Проверка глазами не масштабируется на 148 адресов,
а платформа их меняет.

Что делает. Достаёт каждый адрес тенанта из `explanations/*.md` и сверяет с
двумя источниками правды, которые уже лежат в репозитории:

  * `study_plan.yaml` — маршруты, по которым реально ходил краулер;
  * `ui_elements.json` — то, что при обходе открылось (URL и заголовок страницы).

Адрес, которого нет ни там ни там, либо опечатка, либо выдумка, либо экран, на
который краулер не заходил. Первые два, дефект; третий заносится в ALLOWLIST
ниже с обоснованием, а не молча игнорируется.

Проверка нашла три реальных расхождения (2026-07-30): один и тот же экран
указывался в разных темах разными адресами, и версия из study_plan (та, что
открывалась вживую) отличалась от версии в тексте.

Подтверждение по живому тенанту, без браузера и без модели. 100 из 144 адресов
курса это страницы Settings (`/ui/settings/builtin:<схема>`), ещё 5 — типизированные
списки (`/ui/entity/list/<ТИП>`). И схемы, и типы сущностей отдаются обычным REST
по токену, поэтому две трети адресов проверяются против живого тенанта, а не
против июньского снапшота:

    python scripts/routes_check.py --confirm-live

Результат кладётся в `state/routes_live.json` и используется всеми последующими
офлайн-прогонами: схема, которой на тенанте нет, становится ошибкой сборки, а не
строчкой «не сверено». Нужны DT_TENANT и DT_API_TOKEN в .env (права
`settings.read` и `entities.read`).

ВАЖНО про демо-тенант guu84124.live.dynatrace.com: токен там выпустить НЕЛЬЗЯ.
Проверено 2026-07-30: на `/ui/settings/builtin:tokens.token-settings` стоит
«Your user does not have the necessary write permissions», кнопка «Generate new
token» на `/ui/access-tokens` неактивна, тумблер personal access tokens выключен
и недоступен. Это демо-окружение Dynatrace, права только на чтение интерфейса.
Поэтому `--confirm-live` рассчитан на тенант, где права есть (например кластер
заказчика), и НЕ является условием работоспособности курса: офлайн-сверка со
снапшотом и Managed-докой закрывает все адреса сама. Не предлагать владельцу
выпустить токен на демо-тенанте повторно.

Запуск:
    python scripts/routes_check.py            # отчёт, exit 0 при чистом прогоне
    python scripts/routes_check.py --strict   # неизвестный адрес = exit 1
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPLANATIONS = ROOT / "explanations"
PLAN_FILE = ROOT / "study_plan.yaml"
SNAPSHOT_FILE = ROOT / "ui_elements.json"

TENANT_HOST = "guu84124.live.dynatrace.com"
URL_RE = re.compile(re.escape(TENANT_HOST) + r"(/[^\s`)\]<>\"']*)")
# Карточки лектора пишут адреса без хоста и в бэктиках: `/ui/services`, `/#newhosts`.
# Без этого шаблона их адреса не проверялись вовсе (найдено 2026-07-30).
BARE_ROUTE_RE = re.compile(r"`(/(?:ui/|#)[^\s`]*)`")

# Адреса вне снапшота, у каждого обоснование. Ключ — точный путь или префикс
# (см. PREFIX_ALLOWLIST). Без обоснования запись сюда не добавляется: смысл
# файла в том, чтобы «неизвестный адрес» оставался видимым, а не растворялся.
ALLOWLIST: dict[str, str] = {
    "/": "корень тенанта, используется как пример базового URL",
    "/api": "префикс REST API, а не экран интерфейса (тема day-5/api)",
    "/#newhosts": "классический адрес пункта Hosts, сверен вживую 2026-07-28",
    "/#uemapplications": "классический адрес списка приложений, сверен вживую 2026-07-28",
    "/#smartscape": "классический адрес Smartscape, сверен вживую 2026-07-28",
    "/#deploy": "классический адрес Deploy Dynatrace, сверен вживую 2026-07-28",
    "/#settings/server/requestattributes": "классический адрес Request attributes (есть в study_plan)",
    "/ui/entity/list/HOST": "типизированный список хостов, заменил /ui/entity/list (404)",
    "/ui/entity/list/CONTAINER_GROUP": "типизированный список контейнеров",
    "/ui/entity/list/CLOUD_APPLICATION": "типизированный список Kubernetes workloads",
    "/ui/entity/list/KUBERNETES_CLUSTER": "типизированный список кластеров",
    "/ui/entity/list/QUEUE": "типизированный список очередей",
    "/ui/entity/list/PROCESS_GROUP": (
        "список Process Groups, сверен вживую 2026-07-30 (заголовок «Process Groups»); "
        "заменил /ui/technologies, который отдаёт пустую оболочку"
    ),
    "/ui/settings/applications-web": "Application settings, экран настроек RUM-приложений",
    "/ui/deployment": "маршрут снапшота Deploy Dynatrace, в тексте помечен как таковой",
    "/ui/settings": "корень Settings, пункт меню Manage → Settings",
    "/ui/technologies": (
        "упоминается в тексте как НЕрабочий адрес: сверено вживую 2026-07-30, "
        "отдаёт пустую оболочку без заголовка; рабочий заменитель "
        "/ui/entity/list/PROCESS_GROUP"
    ),
    "/ui/settings/builtin:custom-metrics": (
        "схема Settings 2.0 «User session custom metrics», подтверждена Managed-докой "
        "2026-07-30: docs.dynatrace.com/managed/discover-dynatrace/references/"
        "dynatrace-api/environment-api/settings/schemas/builtin-custom-metrics"
    ),
    "/ui/settings/builtin:metric.metadata": (
        "схема Settings 2.0, подтверждена Managed-докой 2026-07-30: "
        "docs.dynatrace.com/managed/discover-dynatrace/references/dynatrace-api/"
        "environment-api/settings/schemas/builtin-metric-metadata"
    ),
}

# Префиксы: адрес конкретной сущности, идентификатор у каждого тенанта свой.
PREFIX_ALLOWLIST: dict[str, str] = {
    "/ui/nav/SERVICE-": "карточка сервиса, шаблон адреса из sidebar_links снапшота",
    "/ui/nav/HOST-": "карточка хоста, тот же шаблон",
    "/#services/serviceOverview": "канонический адрес карточки сервиса, сверен вживую 2026-07-28",
}

# Адреса, которые не подтверждены ничем: ни снапшотом, ни живой сверкой.
# Держим отдельным списком, чтобы они были на виду и уходили по мере проверки.
UNVERIFIED: dict[str, str] = {}


LIVE_FILE = ROOT / "state" / "routes_live.json"
SETTINGS_PREFIX = "/ui/settings/"  # дальше идёт schemaId целиком, вместе с «builtin:»
ENTITY_LIST_PREFIX = "/ui/entity/list/"


def load_live() -> dict:
    """Кэш подтверждения по живому тенанту; пусто, если --confirm-live не гоняли."""
    if not LIVE_FILE.exists():
        return {}
    try:
        return json.loads(LIVE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def confirm_live() -> int:
    """Тянет список схем настроек и типов сущностей. Только stdlib, без браузера."""
    import urllib.error
    import urllib.parse
    import urllib.request

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from tenant_facts import read_env  # переиспользуем разбор .env, не дублируем

    env = read_env()
    base, token = env.get("DT_TENANT", "").rstrip("/"), env.get("DT_API_TOKEN", "")
    if not base or not token:
        print(
            "ERROR: нужны DT_TENANT и DT_API_TOKEN в .env.\n"
            "Токен: Access tokens → Generate new token, права settings.read и entities.read.",
            file=sys.stderr,
        )
        return 2

    def get(path: str, params: dict) -> dict:
        url = f"{base}{path}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"Authorization": f"Api-Token {token}"})
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))

    live: dict = {"checked_at": None, "schemas": [], "entity_types": [], "errors": []}
    try:
        body = get("/api/v2/settings/schemas", {})
        live["schemas"] = sorted(
            {i["schemaId"] for i in body.get("items", []) if "schemaId" in i}
        )
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        live["errors"].append(f"schemas: {type(exc).__name__}: {exc}")

    try:
        types: list[str] = []
        params = {"pageSize": 500}
        while True:
            body = get("/api/v2/entityTypes", params)
            types += [t["type"] for t in body.get("types", []) if "type" in t]
            nxt = body.get("nextPageKey")
            if not nxt:
                break
            params = {"nextPageKey": nxt}
        live["entity_types"] = sorted(set(types))
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        live["errors"].append(f"entityTypes: {type(exc).__name__}: {exc}")

    if not live["schemas"] and not live["entity_types"]:
        for err in live["errors"]:
            print(f"  ! {err}", file=sys.stderr)
        print("ERROR: тенант не ответил, кэш не обновлён.", file=sys.stderr)
        return 2

    from datetime import datetime, timezone

    live["checked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    LIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LIVE_FILE.write_text(json.dumps(live, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"подтверждено по тенанту: схем {len(live['schemas'])}, "
        f"типов сущностей {len(live['entity_types'])} → {LIVE_FILE.relative_to(ROOT)}"
    )
    for err in live["errors"]:
        print(f"  ! {err}", file=sys.stderr)
    return 0


def load_known() -> set[str]:
    known: set[str] = set()
    import yaml

    plan = yaml.safe_load(PLAN_FILE.read_text(encoding="utf-8"))
    for day in plan["days"]:
        for topic in day["topics"]:
            for route in topic.get("routes") or []:
                known.add(route)
    for entry in json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8")):
        url = entry.get("url", "")
        if TENANT_HOST in url:
            known.add(url.split(TENANT_HOST, 1)[1].split("?")[0])
        if entry.get("plan_route"):
            known.add(entry["plan_route"])
    return known


def collect_used() -> dict[str, list[str]]:
    """{адрес: [file:line, …]} по explanations и карточкам лектора.

    Карточки (`cards/*.md`) едут в окно докладчика сборки v2 и тоже называют
    адреса. Первая версия проверки их не смотрела, и там пережил правку адрес,
    убранный из explanations (найдено 2026-07-30 сверкой собранного HTML, а не
    доверием к чекеру).
    """
    used: dict[str, list[str]] = {}
    sources = list(EXPLANATIONS.rglob("*.md")) + list((ROOT / "cards").rglob("*.md"))
    for md in sorted(sources):
        rel = md.relative_to(ROOT).as_posix()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for path in URL_RE.findall(line) + BARE_ROUTE_RE.findall(line):
                path = path.rstrip(".,;:").rstrip("/") or "/"
                used.setdefault(path, []).append(f"{rel}:{lineno}")
    return used


def classify(path: str, known: set[str], live: dict | None = None) -> tuple[str, str]:
    bare = path.split("?")[0]
    live = live or {}

    # Живой тенант старше снапшота: если схемы/типа там нет, адрес мёртв,
    # даже когда краулер когда-то по нему ходил. Это и есть дрейф платформы.
    schema = bare[len(SETTINGS_PREFIX) :].split("/")[0] if bare.startswith(SETTINGS_PREFIX) else ""
    # Только Settings 2.0 (`builtin:<схема>`). Классические страницы настроек вида
    # /ui/settings/applications-web схемами не являются и в этом API не значатся.
    if schema.startswith("builtin:") and live.get("schemas"):
        if schema in live["schemas"]:
            return "live", f"схема есть на тенанте (сверка {live.get('checked_at', '?')})"
        return "unknown", f"схемы {schema!r} нет на тенанте (сверка {live.get('checked_at', '?')})"
    if bare.startswith(ENTITY_LIST_PREFIX) and live.get("entity_types"):
        etype = bare[len(ENTITY_LIST_PREFIX) :].split("/")[0]
        if etype in live["entity_types"]:
            return "live", f"тип сущности есть на тенанте (сверка {live.get('checked_at', '?')})"
        return "unknown", f"типа сущности {etype!r} нет на тенанте"

    if bare in known or bare + "/" in known:
        return "known", ""
    if bare in ALLOWLIST:
        return "allowlisted", ALLOWLIST[bare]
    for prefix, why in PREFIX_ALLOWLIST.items():
        if bare.startswith(prefix):
            return "allowlisted", why
    if bare in UNVERIFIED:
        return "unverified", UNVERIFIED[bare]
    return "unknown", ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--strict", action="store_true", help="неизвестный адрес = ошибка")
    ap.add_argument(
        "--confirm-live",
        action="store_true",
        help="подтвердить схемы и типы сущностей по Settings API v2 (нужен токен)",
    )
    args = ap.parse_args()

    if args.confirm_live:
        rc = confirm_live()
        if rc != 0:
            return rc

    known = load_known()
    live = load_live()
    used = collect_used()
    buckets: dict[str, list[tuple[str, str]]] = {
        "live": [],
        "known": [],
        "allowlisted": [],
        "unverified": [],
        "unknown": [],
    }
    for path, places in sorted(used.items()):
        kind, why = classify(path, known, live)
        buckets[kind].append((path, why or f"{len(places)} упом., первое {places[0]}"))

    live_note = f", {len(buckets['live'])} подтверждены живым тенантом" if buckets["live"] else ""
    print(
        f"routes_check: {len(used)} уникальных адресов — "
        f"{len(buckets['known'])} в ground truth, "
        f"{len(buckets['allowlisted'])} в allowlist, "
        f"{len(buckets['unverified'])} не сверено, "
        f"{len(buckets['unknown'])} неизвестных" + live_note
    )
    if not live:
        print(
            "  ℹ️  подтверждение по живому тенанту не запускалось: "
            "python scripts/routes_check.py --confirm-live (нужен DT_API_TOKEN)"
        )

    for path, why in buckets["unverified"]:
        print(f"  ⚠️  {path}\n      {why}")
    for path, why in buckets["unknown"]:
        print(f"  ❌ {path}\n      {why}")
        print("      → сверить с study_plan.yaml / ui_elements.json, либо внести в ALLOWLIST с обоснованием")

    if buckets["unknown"]:
        return 1 if args.strict else 0
    if not buckets["unverified"]:
        print("✅ все адреса подтверждены")
    return 0


if __name__ == "__main__":
    sys.exit(main())
