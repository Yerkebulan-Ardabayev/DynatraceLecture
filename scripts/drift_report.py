"""
drift_report.py: детектор дрейфа UI живого тенанта относительно эталона ui_elements.json.

Часть A ("Freshness Pipeline") из spec.md (v2-presenter, раздел 10, пакет Ф3.1).
Заново открывает роуты тем kind: live из study_plan.yaml в ОДНОЙ тёплой сессии
playwright (авторизация через state/storage_state.json, подход как в auth.py /
crawler.py / plan_runner.py), извлекает main_title и headings ТОЙ ЖЕ функцией,
что extract_ui_elements.py (extract_from_html, импортируется без изменения
оригинального файла), и сравнивает результат с эталоном ui_elements.json.

Транзиентные счётчики в заголовках ("Problems (12)" -> "Problems (7)") нормализуются
(\\d+ -> "#") перед сравнением: если разница только в цифрах, это НЕ дрейф, а
info-строка "счётчик изменился".

Критичные грабли этого тенанта (не убирать, иначе ложный дрейф или битая сессия):
  - НЕ ставить кастомный user_agent, НЕ добавлять --disable-blink-features в
    chromium.launch(): оба ломают SSO-логин (см. auth.py/crawler.py: launch()
    вызывается без дополнительных args, здесь так же).
  - networkidle на этом тенанте практически не наступает (фоновый поллинг
    Dynatrace SPA), поэтому реальный контент ждём через wait_for_function по
    длине document.body.innerText, а не через wait_for_load_state("networkidle").
  - Если storage_state протух (редирект на SSO/логин), скрипт НЕ пытается
    перелогиниться сам (частые перелогины троттлятся), а честно останавливается
    с инструкцией: перелогинься headed-режимом (python auth.py) и запусти заново.

Выход: drift_report.md (по умолчанию в корне репозитория), 5 секций:
  1. сводная таблица (маршрут / статус / вердикт)
  2. изменённые экраны (дифф заголовков)
  3. битые роуты (403 / 404 / пустой центр / ошибка навигации)
  4. info: транзиентные счётчики
  5. затронутые темы (day/topic: что перепроверить)

Exit code: 0, если дрейфа нет (только OK/COUNTER/NO_BASELINE); 1, если есть
CHANGED и/или BROKEN роуты.

Использование (после `pip install -r requirements.txt && playwright install chromium`,
см. spec.md раздел 8):
    python scripts/drift_report.py                    # полный прогон, все live-роуты
    python scripts/drift_report.py --limit 3           # смоук: первые 3 роута плана
    python scripts/drift_report.py --routes day-1      # только day-1
    python scripts/drift_report.py --routes settings   # роуты с "settings" в пути
    python scripts/drift_report.py --output out/drift.md
    python scripts/drift_report.py --no-headless       # показать браузер (дебаг/перелогин)
"""
from __future__ import annotations

import argparse
import asyncio
import io
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# drift_report.py лежит в scripts/, а crawler.py / extract_ui_elements.py на
# уровень выше (корень репозитория). Добавляем корень в sys.path, чтобы
# переиспользовать их код напрямую, без копипаста и риска расхождения логики.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Playwright и bs4 (через extract_ui_elements): мягкий импорт, как в crawler.py.
# чистая логика сравнения (diff_headings/compare_route/build_report) должна
# импортироваться и тестироваться даже без установленных браузерных зависимостей.
try:
    from playwright.async_api import async_playwright
except ImportError:  # pragma: no cover
    async_playwright = None

try:
    # extract_ui_elements.py НЕ трогаем: просто переиспользуем его функцию,
    # чтобы live-извлечение main_title/headings шло ТОЙ ЖЕ логикой, что эталон.
    from extract_ui_elements import extract_from_html
except ImportError:  # pragma: no cover
    extract_from_html = None

import yaml  # тот же PyYAML, что и в crawler.py; лёгкая зависимость, уже в venv

from crawler import TENANT_URL, STATE_FILE, CONFIG, log, normalize_url, same_host

PLAN_FILE = ROOT / "study_plan.yaml"
BASELINE_FILE = ROOT / "ui_elements.json"
DEFAULT_OUTPUT = ROOT / "drift_report.md"

# Сколько ждать реальный контент через wait_for_function (см. докстринг файла:
# networkidle на этом тенанте не наступает из-за поллинга). Таймаут не фатален:
# не дождались нужной длины текста, значит, скорее всего, экран реально пуст,
# это увидим ниже через classify_status(), а не свалимся с исключением.
CONTENT_READY_TIMEOUT_MS = 15000
CONTENT_READY_MIN_CHARS = 40

# Порог "пустого центра": меньше стольки символов видимого текста на странице.
EMPTY_TEXT_MIN_CHARS = 40

NUMBER_RE = re.compile(r"\d+")


# ---------- данные ----------

@dataclass
class LiveCapture:
    """Результат живого снятия одного роута."""
    day_id: str
    topic_id: str
    topic_name: str
    route: str
    url: str
    status: str                      # ok | 403 | 404 | empty | http_NNN | error | session_expired
    http_status: int | None = None
    main_title: str = ""
    headings: list[dict] = field(default_factory=list)  # [{"level":.., "text":..}, ...]
    error: str = ""


@dataclass
class DriftEntry:
    """Результат сравнения одного роута с эталоном (единица отчёта)."""
    day_id: str
    topic_id: str
    topic_name: str
    route: str
    verdict: str                     # OK | COUNTER | CHANGED | BROKEN | NO_BASELINE
    status: str
    http_status: int | None = None
    error: str = ""
    title_before: str = ""
    title_after: str = ""
    title_counter_only: bool = False
    headings_added: list[tuple[str, str]] = field(default_factory=list)
    headings_removed: list[tuple[str, str]] = field(default_factory=list)
    heading_counter_changes: list[tuple[str, str, str]] = field(default_factory=list)
    note: str = ""


# ---------- план и эталон ----------

def load_plan() -> dict:
    return yaml.safe_load(PLAN_FILE.read_text(encoding="utf-8"))


def load_baseline() -> dict[tuple[str, str, str], dict]:
    """Эталон ui_elements.json, ключ (day_id, topic_id, plan_route) -> запись."""
    data = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    lookup: dict[tuple[str, str, str], dict] = {}
    for entry in data:
        key = (entry.get("day_id"), entry.get("topic_id"), entry.get("plan_route"))
        lookup[key] = entry
    return lookup


def task_matches(task: dict, needle: str) -> bool:
    haystack = f"{task['day_id']}/{task['topic_id']}/{task['route']}".lower()
    return needle.lower() in haystack


def build_tasks(plan: dict, routes_filter: str | None, limit: int | None) -> list[dict]:
    """Плоский список задач (day_id, topic_id, topic_name, route) по темам kind: live.

    Темы kind: concept (например day-1/architecture) в дрейф-проверку не входят:
    у них нет своего живого экрана, это слайды (см. заметку в study_plan.yaml).
    """
    tasks: list[dict] = []
    for day in plan["days"]:
        for t in (day.get("topics") or []):
            if t.get("kind") != "live":
                continue
            for r in (t.get("routes") or []):
                tasks.append({
                    "day_id": day["id"],
                    "topic_id": t["id"],
                    "topic_name": t["name"],
                    "route": r.strip(),
                })
    tasks += unverified_tasks()
    if routes_filter:
        tasks = [t for t in tasks if task_matches(t, routes_filter)]
    if limit is not None:
        tasks = tasks[:limit]
    return tasks


def unverified_tasks() -> list[dict]:
    """Адреса, которые routes_check не смог подтвердить офлайн.

    Часть адресов курса не проверить ни снапшотом, ни Settings API v2: это
    UI-маршруты без своей схемы и без типа сущности (например /ui/technologies).
    Единственный способ узнать, живы ли они, открыть их в сессии. Раз этот
    скрипт всё равно ходит по тенанту, пусть заодно отвечает и на этот вопрос:
    иначе адрес остаётся вечной сноской «не сверено» в отчёте routes_check.
    """
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from routes_check import UNVERIFIED
    except ImportError:  # pragma: no cover — скрипт должен работать и без него
        return []
    return [
        {
            "day_id": "—",
            "topic_id": "routes_check",
            "topic_name": "адреса без офлайн-подтверждения",
            "route": route.strip(),
        }
        for route in sorted(UNVERIFIED)
        if route.startswith("/ui/")
    ]


# ---------- сравнение (чистая логика, без браузера) ----------

def normalize_counters(text: str) -> str:
    """Заменить все числа на "#": тогда "Problems (12)" и "Problems (7)" совпадают."""
    return NUMBER_RE.sub("#", text or "")


def diff_headings(
    baseline: list[tuple[str, str]],
    live: list[tuple[str, str]],
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str, str]]]:
    """Сравнить заголовки эталона и живого снятия.

    Возвращает (real_added, real_removed, counter_changes):
      - real_added / real_removed: реальный дрейф, заголовок появился/пропал;
      - counter_changes: (level, было, стало) там, где (level, текст) совпадают
        с точностью до чисел, это транзиентный счётчик, не дрейф.
    """
    base_left = list(baseline)
    live_left = list(live)

    # 1. точные совпадения (level, text) выкидываем: тут точно ничего не менялось.
    for pair in list(base_left):
        if pair in live_left:
            base_left.remove(pair)
            live_left.remove(pair)

    # 2. среди оставшихся ищем пары "тот же level, тот же текст с точностью до цифр".
    counter_changes: list[tuple[str, str, str]] = []
    for pair in list(base_left):
        level, text = pair
        norm = (level, normalize_counters(text))
        match = next(
            (lp for lp in live_left if (lp[0], normalize_counters(lp[1])) == norm),
            None,
        )
        if match is not None:
            counter_changes.append((level, text, match[1]))
            base_left.remove(pair)
            live_left.remove(match)

    real_added, real_removed = live_left, base_left
    return real_added, real_removed, counter_changes


def _has_missing_headings(baseline_entry: dict | None, cap: "LiveCapture") -> bool:
    """Есть ли заголовки, которые были в эталоне и не попали в живое снятие.

    Признак для анти-флак-повтора: пропажа заголовков почти всегда означает, что
    снимок сделан до конца отрисовки, а не что элемент убрали из продукта.
    """
    if not baseline_entry:
        return False
    base = [
        (h.get("level", ""), h.get("text", ""))
        for h in (baseline_entry.get("ui") or {}).get("headings") or []
    ]
    live = [(h.get("level", ""), h.get("text", "")) for h in cap.headings or []]
    _added, removed, _counters = diff_headings(base, live)
    return bool(removed)


def compare_route(task: dict, baseline_entry: dict | None, cap: LiveCapture) -> DriftEntry:
    """Свести живое снятие (cap) и эталон (baseline_entry) к одному вердикту."""
    identity = dict(
        day_id=task["day_id"], topic_id=task["topic_id"],
        topic_name=task["topic_name"], route=task["route"],
    )

    # Битый роут важнее эталона: даже если эталона вообще нет, статус решает.
    if cap.status != "ok":
        return DriftEntry(
            **identity, verdict="BROKEN", status=cap.status, http_status=cap.http_status,
            error=cap.error, title_before=(baseline_entry or {}).get("ui", {}).get("main_title", ""),
        )

    if baseline_entry is None:
        live_headings = [(h.get("level", ""), h.get("text", "")) for h in cap.headings]
        return DriftEntry(
            **identity, verdict="NO_BASELINE", status=cap.status, http_status=cap.http_status,
            title_after=cap.main_title, headings_added=live_headings,
            note="роута нет в эталоне ui_elements.json (новый в study_plan.yaml, нужен первый снимок)",
        )

    base_ui = baseline_entry.get("ui") or {}
    base_title = base_ui.get("main_title") or ""
    base_headings = [(h.get("level", ""), h.get("text", "")) for h in (base_ui.get("headings") or [])]
    live_headings = [(h.get("level", ""), h.get("text", "")) for h in cap.headings]

    title_changed = base_title != (cap.main_title or "")
    title_counter_only = title_changed and normalize_counters(base_title) == normalize_counters(cap.main_title or "")

    added, removed, counters = diff_headings(base_headings, live_headings)

    real_drift = (title_changed and not title_counter_only) or bool(added) or bool(removed)
    counter_only = (not real_drift) and (title_counter_only or bool(counters))

    if real_drift:
        verdict = "CHANGED"
    elif counter_only:
        verdict = "COUNTER"
    else:
        verdict = "OK"

    return DriftEntry(
        **identity, verdict=verdict, status=cap.status, http_status=cap.http_status,
        title_before=base_title, title_after=cap.main_title or "",
        title_counter_only=title_counter_only,
        headings_added=added, headings_removed=removed, heading_counter_changes=counters,
    )


# ---------- живое снятие (нужен playwright) ----------

def session_expired(url: str) -> bool:
    """True, если после навигации мы оказались не на тенанте, а на SSO/логин-странице.

    Та же эвристика, что в auth.py (там ждут "live.dynatrace.com" без sso/login
    в адресе); здесь достаточно "явно sso/login в адресе или чужой хост".
    """
    low = url.lower()
    if "sso" in low or "/login" in low or "signin" in low:
        return True
    return not same_host(url, TENANT_URL)


def classify_status(http_status: int | None, body_text: str) -> str:
    if http_status == 403:
        return "403"
    if http_status == 404:
        return "404"
    if http_status is not None and http_status >= 400:
        return f"http_{http_status}"
    if len((body_text or "").strip()) < EMPTY_TEXT_MIN_CHARS:
        return "empty"
    return "ok"


RENDER_POLL_MS = 1000  # шаг опроса (заголовок, число h1-h4)
RENDER_STABLE_SAMPLES = 3  # столько одинаковых замеров подряд считаем «дорисовалось»
RENDER_MIN_SETTLE_MS = 4000  # раньше не снимаем даже при «стабильных» замерах
RENDER_STABLE_TIMEOUT_MS = 20000  # верхняя граница ожидания
RENDER_RETRY_SETTLE_MS = 6000  # доп. пауза при повторном снятии подозрительного роута


async def wait_render_stable(page) -> str:
    """Ждёт, пока SPA догрузит экран: заголовок И число подзаголовков перестают меняться.

    Зачем отдельное ожидание. Прежнее условие готовности (innerText длиннее 40
    символов) выполняется мгновенно одной навигационной оболочкой, поэтому
    заголовок и подзаголовки снимались до отрисовки контент-зоны. Итог: все
    Settings-страницы попадали в отчёт как CHANGED с вырожденным заголовком
    «Settings - <окружение>», то есть отчёт кричал о дрейфе на каждом прогоне.
    Тревога, которая срабатывает всегда, ничего не значит и приучает её
    игнорировать.

    Замер 2026-07-30 на `/ui/settings/builtin:deployment.oneagent.updates`: при
    прямой загрузке правильный заголовок появляется за 3 секунды и дальше не
    меняется, то есть дело было в моменте снятия, а не в тенанте.

    Одного заголовка мало. На `/ui/user-sessions` он становится «Session List»
    почти сразу, а панель фильтров подтягивается позже, поэтому в отчёте
    «пропадали» все 12 её заголовков разом на шести маршрутах. Прямая проверка
    2026-07-30 показала, что на живой странице они на месте. Поэтому ждём
    стабилизации пары (заголовок, число h1-h4): пока разметка достраивается,
    второе значение растёт, и снимок не делается.

    Двух одинаковых замеров подряд тоже мало: оболочка успевает застыть на доли
    секунды, пока панель фильтров ещё не пришла. Прямая проверка 2026-07-30: в
    сериализованном HTML все 12 заголовков появляются примерно к 9-й секунде.
    Поэтому требуем RENDER_STABLE_SAMPLES одинаковых замеров подряд и не снимаем
    раньше RENDER_MIN_SETTLE_MS, даже если замеры уже совпали.
    """
    last: tuple[str, int] | None = None
    same = 0
    waited = 0
    while waited < RENDER_STABLE_TIMEOUT_MS:
        try:
            current = (await page.title(), await page.locator("h1,h2,h3,h4").count())
        except Exception:
            return last[0] if last else ""
        same = same + 1 if current == last else 0
        last = current
        if current[0] and same >= RENDER_STABLE_SAMPLES and waited >= RENDER_MIN_SETTLE_MS:
            return current[0]
        try:
            await page.wait_for_timeout(RENDER_POLL_MS)
        except Exception:
            return last[0] if last else ""
        waited += RENDER_POLL_MS
    return last[0] if last else ""


async def capture_route(page, task: dict, extra_settle_ms: int = 0) -> LiveCapture:
    url = normalize_url(TENANT_URL + task["route"])
    identity = dict(
        day_id=task["day_id"], topic_id=task["topic_id"],
        topic_name=task["topic_name"], route=task["route"], url=url,
    )
    page_timeout = CONFIG["crawl"]["page_timeout_ms"]

    try:
        response = await page.goto(url, wait_until="domcontentloaded", timeout=page_timeout)
    except Exception as e:
        return LiveCapture(**identity, status="error", error=f"{type(e).__name__}: {str(e)[:200]}")

    http_status = response.status if response is not None else None

    if session_expired(page.url):
        return LiveCapture(**identity, status="session_expired", http_status=http_status)

    # networkidle здесь не наступает (см. докстринг файла): ждём реальный контент
    # по длине innerText. Таймаут не фатален, страница может быть реально пустой.
    try:
        await page.wait_for_function(
            "(n) => !!(document.body && document.body.innerText "
            "&& document.body.innerText.trim().length > n)",
            arg=CONTENT_READY_MIN_CHARS,
            timeout=CONTENT_READY_TIMEOUT_MS,
        )
    except Exception:
        pass

    # Оболочка уже отрисована, но экран маршрута может быть ещё пуст: дожидаемся,
    # пока заголовок и разметка перестанут меняться (см. докстринг wait_render_stable).
    await wait_render_stable(page)
    if extra_settle_ms:
        try:
            await page.wait_for_timeout(extra_settle_ms)
        except Exception:
            pass

    body_text = ""
    try:
        body_text = await page.evaluate("() => (document.body && document.body.innerText) || ''")
    except Exception:
        pass

    html = ""
    try:
        html = await page.content()
    except Exception:
        pass

    ui = extract_from_html(html) if html else {"main_title": "", "headings": []}
    status = classify_status(http_status, body_text)

    return LiveCapture(
        **identity, status=status, http_status=http_status,
        main_title=ui.get("main_title", ""), headings=ui.get("headings", []),
    )


async def run_capture(
    tasks: list[dict],
    headless: bool,
    baseline: dict[tuple[str, str, str], dict] | None = None,
) -> list[LiveCapture]:
    captures: list[LiveCapture] = []
    async with async_playwright() as p:
        # Специально БЕЗ дополнительных launch-args и БЕЗ user_agent: и то, и
        # другое ломает SSO на этом тенанте (см. докстринг файла и auth.py/
        # crawler.py, где launch() тоже вызывается без args).
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            storage_state=str(STATE_FILE),
            viewport={
                "width": CONFIG["crawl"]["viewport_width"],
                "height": CONFIG["crawl"]["viewport_height"],
            },
        )
        page = await context.new_page()

        for i, task in enumerate(tasks, 1):
            log(f"[{i}/{len(tasks)}] {task['day_id']}/{task['topic_id']} -> {task['route']}")
            cap = await capture_route(page, task)

            # Анти-флак: «пропавшие заголовки», это единственное направление, в
            # котором отчёт врёт. Ленивая отрисовка успевает не всё, и панель,
            # которая физически на месте, попадает в отчёт как удалённая (проверено
            # 2026-07-30 на /ui/user-sessions: в полном прогоне 12 фильтров
            # «исчезали», в точечном те же роуты чистые). Добавлений это не
            # касается: лишнего разметка не придумывает. Поэтому только при
            # пропажах снимаем роут повторно, с запасом по времени, и берём
            # вторую попытку. Стоимость: один лишний заход на подозрительный роут.
            baseline_entry = (baseline or {}).get(
                (task["day_id"], task["topic_id"], task["route"])
            )
            if cap.status == "ok" and _has_missing_headings(baseline_entry, cap):
                log("    пропали заголовки — повторное снятие с запасом")
                cap = await capture_route(page, task, extra_settle_ms=RENDER_RETRY_SETTLE_MS)

            if cap.status == "session_expired":
                await browser.close()
                log("ERROR: storage_state протух, редирект на SSO/логин.")
                log("Перелогинься руками (headed, частые перелогины троттлятся):")
                log("  python auth.py")
                log("Затем запусти drift_report.py заново.")
                sys.exit(2)

            captures.append(cap)

        await browser.close()
    return captures


# ---------- отчёт ----------

def _fmt_heading(h: tuple[str, str]) -> str:
    level, text = h
    return f"({level}) {text}"


def build_report(entries: list[DriftEntry], tenant_url: str) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    counts = Counter(e.verdict for e in entries)
    drift = counts.get("CHANGED", 0) > 0 or counts.get("BROKEN", 0) > 0

    lines: list[str] = []
    lines.append("# Отчёт о дрейфе UI живого тенанта")
    lines.append("")
    lines.append(f"Сформирован: {generated_at}")
    lines.append(f"Тенант: `{tenant_url}`")
    lines.append(f"Роутов проверено: {len(entries)}")
    lines.append(
        f"OK: {counts.get('OK', 0)}, COUNTER (инфо): {counts.get('COUNTER', 0)}, "
        f"CHANGED: {counts.get('CHANGED', 0)}, BROKEN: {counts.get('BROKEN', 0)}, "
        f"без эталона: {counts.get('NO_BASELINE', 0)}"
    )
    lines.append(f"Итог: {'ЕСТЬ ДРЕЙФ' if drift else 'ДРЕЙФА НЕТ'}")
    lines.append("")

    # 1. сводная таблица
    lines.append("## 1. Сводная таблица")
    lines.append("")
    lines.append("| День / Тема | Маршрут | Статус | Вердикт |")
    lines.append("|---|---|---|---|")
    for e in entries:
        lines.append(f"| {e.day_id} / {e.topic_id} | `{e.route}` | {e.status} | {e.verdict} |")
    lines.append("")

    # 2. изменённые экраны
    lines.append("## 2. Изменённые экраны")
    lines.append("")
    changed = [e for e in entries if e.verdict == "CHANGED"]
    if not changed:
        lines.append("Изменений не найдено.")
    for e in changed:
        lines.append(f"### {e.day_id} / {e.topic_id}")
        lines.append(f"Маршрут: `{e.route}`")
        lines.append("")
        if e.title_before != e.title_after:
            lines.append(f'Заголовок: "{e.title_before}" -> "{e.title_after}"')
            lines.append("")
        if e.headings_added:
            lines.append("Заголовки, добавленные:")
            for h in e.headings_added:
                lines.append(f"- {_fmt_heading(h)}")
            lines.append("")
        if e.headings_removed:
            lines.append("Заголовки, удалённые:")
            for h in e.headings_removed:
                lines.append(f"- {_fmt_heading(h)}")
            lines.append("")

    no_baseline = [e for e in entries if e.verdict == "NO_BASELINE"]
    if no_baseline:
        lines.append("### Без эталона (новые роуты в study_plan.yaml)")
        lines.append("")
        for e in no_baseline:
            lines.append(f"- {e.day_id} / {e.topic_id} : `{e.route}` ({e.note})")
        lines.append("")

    # 3. битые роуты
    lines.append("## 3. Битые роуты (403 / 404 / пустой центр / ошибка)")
    lines.append("")
    broken = [e for e in entries if e.verdict == "BROKEN"]
    if not broken:
        lines.append("Битых роутов нет.")
    else:
        for e in broken:
            extra = f", {e.error}" if e.error else ""
            lines.append(f"- {e.day_id} / {e.topic_id} ({e.topic_name}) : `{e.route}` : статус {e.status}{extra}")
    lines.append("")

    # 4. info: транзиентные счётчики
    lines.append("## 4. Info: транзиентные счётчики")
    lines.append("")
    counters_only = [e for e in entries if e.verdict == "COUNTER"]
    if not counters_only:
        lines.append("Счётчиков не найдено.")
    else:
        for e in counters_only:
            lines.append(f"- {e.day_id} / {e.topic_id} : `{e.route}`")
            if e.title_counter_only:
                lines.append(f'  Заголовок (счётчик): "{e.title_before}" -> "{e.title_after}"')
            for level, before, after in e.heading_counter_changes:
                lines.append(f'  Счётчик в заголовке ({level}): "{before}" -> "{after}"')
    lines.append("")

    # 5. затронутые темы
    lines.append("## 5. Затронутые темы (перепроверить)")
    lines.append("")
    topics: dict[tuple[str, str], dict] = {}
    for e in entries:
        if e.verdict not in ("CHANGED", "BROKEN", "NO_BASELINE"):
            continue
        key = (e.day_id, e.topic_id)
        info = topics.setdefault(key, {"topic_name": e.topic_name, "reasons": []})
        if e.verdict == "BROKEN":
            info["reasons"].append(f"роут {e.route} сломан ({e.status})")
        elif e.verdict == "CHANGED":
            what = []
            if e.title_before != e.title_after and not e.title_counter_only:
                what.append("заголовок страницы")
            if e.headings_added:
                what.append(f"{len(e.headings_added)} новых подзаголовков")
            if e.headings_removed:
                what.append(f"{len(e.headings_removed)} пропавших подзаголовков")
            info["reasons"].append(f"на {e.route} изменились: {', '.join(what)}")
        elif e.verdict == "NO_BASELINE":
            info["reasons"].append(f"роут {e.route} без эталона, нужен первый снимок")

    if not topics:
        lines.append("Тем на переверификацию нет.")
    else:
        for (day_id, topic_id), info in sorted(topics.items()):
            reasons = "; ".join(info["reasons"])
            lines.append(f"- {day_id}/{topic_id} ({info['topic_name']}): {reasons}")
    lines.append("")

    return "\n".join(lines)


# ---------- main ----------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Детектор дрейфа UI живого тенанта относительно эталона ui_elements.json "
            "(Ф3.1, spec.md раздел 10)."
        ),
    )
    ap.add_argument("--limit", type=int, default=None, help="первые N роутов плана (после --routes), для смоука")
    ap.add_argument(
        "--routes", type=str, default=None,
        help="подстрока фильтра по day_id/topic_id/route, например day-1 или settings",
    )
    ap.add_argument(
        "--output", type=str, default=str(DEFAULT_OUTPUT),
        help=f"путь к отчёту (по умолчанию {DEFAULT_OUTPUT.name} в корне репозитория)",
    )
    ap.add_argument(
        "--headless", action=argparse.BooleanOptionalAction, default=True,
        help="headless-режим браузера (--no-headless, чтобы посмотреть live)",
    )
    args = ap.parse_args()

    if async_playwright is None:
        log("ERROR: playwright не установлен. Установи: pip install -r requirements.txt && playwright install chromium")
        return 2
    if extract_from_html is None:
        log("ERROR: beautifulsoup4 не установлен (нужен для извлечения UI). Установи: pip install -r requirements.txt")
        return 2
    if not STATE_FILE.exists():
        log(f"ERROR: storage state не найден: {STATE_FILE}. Сначала: python auth.py")
        return 2

    plan = load_plan()
    baseline = load_baseline()
    tasks = build_tasks(plan, args.routes, args.limit)
    if not tasks:
        log("ERROR: после фильтра не осталось ни одного роута (проверь --routes/--limit).")
        return 2

    log(f"drift_report: тенант={TENANT_URL} роутов={len(tasks)} headless={args.headless}")

    captures = asyncio.run(run_capture(tasks, headless=args.headless, baseline=baseline))

    entries = [
        compare_route(task, baseline.get((task["day_id"], task["topic_id"], task["route"])), cap)
        for task, cap in zip(tasks, captures)
    ]

    report_text = build_report(entries, tenant_url=TENANT_URL)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")

    drift = any(e.verdict in ("CHANGED", "BROKEN") for e in entries)
    counts = Counter(e.verdict for e in entries)
    log(f"-> {output_path}")
    log(
        f"   роутов={len(entries)} OK={counts.get('OK', 0)} COUNTER={counts.get('COUNTER', 0)} "
        f"CHANGED={counts.get('CHANGED', 0)} BROKEN={counts.get('BROKEN', 0)} "
        f"NO_BASELINE={counts.get('NO_BASELINE', 0)}"
    )
    log("ЕСТЬ ДРЕЙФ" if drift else "Дрейфа нет.")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
