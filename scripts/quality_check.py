"""
quality_check.py — проверяет explanations/*.md на 7 классов ошибок точности.

Финиш-критерий: `✅ 0 issues`. Вызывается pre-build hook'ом в plan_html.py.

Usage:
    python scripts/quality_check.py                 # human-readable
    python scripts/quality_check.py --json          # machine-readable
    python scripts/quality_check.py --strict        # exit 1 даже если только warnings
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EXPLANATIONS = ROOT / "explanations"


@dataclass
class Issue:
    file: str
    line: int
    cls: str
    severity: str  # "error" | "warn"
    snippet: str
    suggestion: str


@dataclass
class Rule:
    cls: str
    severity: str
    pattern: re.Pattern
    suggestion: str
    # optional guard: skip match if this regex also matches the line (anti-FP)
    guard_skip: re.Pattern | None = None


# ---------- RULES ----------------------------------------------------------

RULES: list[Rule] = [
    # 1. РФ-РЕГУЛЯТОРЫ И РФ-ОС (курс для банков/госов Казахстана)
    Rule(
        cls="RU_REGULATOR",
        severity="error",
        pattern=re.compile(r"\bФСТЭК\b"),
        suggestion="заменить на ЦАРКА / КИБ РК либо нейтральное «национальный регулятор»",
    ),
    Rule(
        cls="RU_OS",
        severity="error",
        pattern=re.compile(r"Astra\s+Linux(\s+Special\s+Edition)?", re.IGNORECASE),
        suggestion="для курса в РК заменить на нейтральное «сертифицированная Linux-сборка» либо удалить",
    ),
    Rule(
        cls="RU_REGULATOR",
        severity="error",
        pattern=re.compile(r"\bРоскомнадзор|Роспотребнадзор\b"),
        suggestion="удалить — регулятор РФ, не РК",
    ),
    Rule(
        cls="RU_OS",
        severity="warn",
        pattern=re.compile(r"\bРЕД\s*ОС\b"),
        suggestion="если не подтверждено заказчиком — убрать или заменить на «сертифицированный дистрибутив»",
    ),
    # 2. ROADMAP-ДАТЫ (Dynatrace не публикует публичных дат)
    Rule(
        cls="ROADMAP_DATE",
        severity="error",
        pattern=re.compile(
            r"(Grail|DQL|Notebooks|Workflows|Apps\s*platform).{0,40}(в\s+Managed|в\s+managed).{0,40}20\d\d",
            re.IGNORECASE,
        ),
        suggestion="заменить на «сроки в публичных roadmap Dynatrace не зафиксированы»",
    ),
    Rule(
        cls="ROADMAP_DATE",
        severity="error",
        pattern=re.compile(
            r"(Grail|DQL).{0,30}(запланирован|появится|ожидается).{0,30}20\d\d",
            re.IGNORECASE,
        ),
        suggestion="удалить дату — Dynatrace не публикует публичных roadmap-дат",
    ),
    Rule(
        cls="ROADMAP_DATE",
        severity="warn",
        pattern=re.compile(r"(DQL|Grail)\s+следом", re.IGNORECASE),
        suggestion="удалить — спекуляция о порядке релизов",
    ),
    # 3. MARKETING / SALES BATTLE CARD (не обучение)
    Rule(
        cls="MARKETING",
        severity="error",
        pattern=re.compile(r"не\s+вкладывает(ся|ются)"),
        suggestion="удалить — субъективная оценка стратегии конкурента",
    ),
    Rule(
        cls="MARKETING",
        severity="error",
        pattern=re.compile(r"выбирают\s+чаще"),
        suggestion="удалить — marketing-оценка без источника",
    ),
    Rule(
        cls="MARKETING",
        severity="error",
        pattern=re.compile(r"слабый\s+APM"),
        suggestion="удалить — marketing-оценка",
    ),
    Rule(
        cls="MARKETING",
        severity="error",
        pattern=re.compile(r"теряют\s+трейс"),
        suggestion="удалить — marketing-оценка без источника",
    ),
    Rule(
        cls="MARKETING",
        severity="error",
        pattern=re.compile(r"3[-–]5\s+инженер", re.IGNORECASE),
        suggestion="удалить — выдуманная метрика Open Source-стека",
    ),
    Rule(
        cls="MARKETING",
        severity="warn",
        pattern=re.compile(r"\bAppDynamics\b|\bSplunk\b", re.IGNORECASE),
        suggestion="упоминание конкурента — проверить, нужен ли в курсе обучения (vs battle card)",
        guard_skip=re.compile(
            r"Splunk\s+SPL|синтаксис.*Splunk"
        ),  # пример в usql.md для аналогии синтаксиса — ок
    ),
    # 4. SUPPORT-ИНСТРУКЦИИ (курс учит работе с платформой, не эскалации)
    Rule(
        cls="SUPPORT_INSTRUCTION",
        severity="error",
        pattern=re.compile(r"через\s+интегратора"),
        suggestion="удалить — support-инструкция, не часть курса",
    ),
    Rule(
        cls="SUPPORT_INSTRUCTION",
        severity="error",
        pattern=re.compile(
            r"поддержке\s+Dynatrace|в\s+поддержку\s+Dynatrace|поддержк[аеу]?\s+Dynatrace"
        ),
        suggestion="удалить или переформулировать без упоминания процесса эскалации",
    ),
    Rule(
        cls="SUPPORT_INSTRUCTION",
        severity="warn",
        pattern=re.compile(r"открыть\s+тикет"),
        suggestion="проверить контекст — если это support-инструкция, убрать",
        guard_skip=re.compile(
            r"тикет\s+в\s+(Jira|ServiceNow|Remedy)"
        ),  # интеграция с внешним ITSM — ок
    ),
    # 5. ВЫДУМАННЫЕ SUCCESS-STORIES (конкретные цифры без источника)
    Rule(
        cls="FAKE_SUCCESS_STORY",
        severity="error",
        pattern=re.compile(r"MTTR\s*\d+\s*[→\-]+\s*\d+"),
        suggestion="удалить конкретные до/после цифры — нет источника",
    ),
    Rule(
        cls="FAKE_SUCCESS_STORY",
        severity="error",
        pattern=re.compile(r"алертов?\s+в\s+\d+\s+раз(а)?\s+меньше"),
        suggestion="удалить — выдуманная метрика",
    ),
    Rule(
        cls="FAKE_SUCCESS_STORY",
        severity="warn",
        pattern=re.compile(r"\d{3,}\s+серверов"),
        suggestion="конкретные цифры серверов — проверить, что это generic-пример с подписью «типично», а не выдуманный кейс",
    ),
    Rule(
        cls="FAKE_SUCCESS_STORY",
        severity="warn",
        pattern=re.compile(r"цена\s*\+\d+\s*%"),
        suggestion="конкретный прирост цены без источника — удалить или пометить «иллюстративно»",
    ),
    # 6. UNSOURCED ПРОЦЕНТЫ (overhead / CPU / память)
    Rule(
        cls="UNSOURCED_PERCENT",
        severity="warn",
        pattern=re.compile(
            r"\d+\s*[-–]\s*\d+\s*%\s*(CPU|нагрузк|overhead|процессор)", re.IGNORECASE
        ),
        suggestion="numeric claim про overhead — верифицировать в dtkb; если не подтверждается, смягчить («заметной доли не тратит»)",
    ),
    Rule(
        cls="UNSOURCED_PERCENT",
        severity="warn",
        pattern=re.compile(
            r"до\s+\d+\s*%\s*(CPU|нагрузк|overhead|процессор)", re.IGNORECASE
        ),
        suggestion="верхняя граница overhead без источника — верифицировать в dtkb",
    ),
    # 7. RPS-CLAIMS (нагрузочные характеристики без источника)
    Rule(
        cls="UNSOURCED_RPS",
        severity="warn",
        pattern=re.compile(
            r"\d{3,}\s*(rps|RPS|req/s|запросов\s+в\s+секунду)", re.IGNORECASE
        ),
        suggestion="нагрузочная цифра без источника — либо привязать к docs, либо переформулировать без числа",
    ),
    # 8. SaaS-ONLY ФИЧИ, ПОДАННЫЕ КАК ДОСТУПНЫЕ В MANAGED (курс — air-gapped Managed)
    # Grail / DQL / Notebooks / Workflows / Apps platform / DPS и т.п. живут только в SaaS.
    # Легитимны ТОЛЬКО как пояснение «в Managed этого нет». guard_skip снимает строки
    # с exclusion-контекстом; остальное = кандидат на протечку (warn, ручной ревью).
    # Pattern регистрозависим: ловит продукты (Workflows/Apps), не общий «workflow».
    Rule(
        cls="SAAS",
        severity="warn",
        pattern=re.compile(
            r"\bGrail\b|\bDQL\b|\bNotebooks?\b|\bWorkflows\b|\bAutomationEngine\b"
            r"|\bOpenPipeline\b|\bDPS\b|Apps[\s\-]?(?:platform|платформ|интерфейс)"
            r"|Experience\s+Vitals|Latest\s+Dynatrace"
        ),
        suggestion=(
            "SaaS-only фича, в air-gapped Managed её нет. Допустимо только как пояснение, "
            "что в Managed недоступно. Если подаётся как рабочая в Managed, переписать на "
            "классический аналог. Легитимную строку пометить <!-- qc:ignore=SAAS -->"
        ),
        guard_skip=re.compile(
            r"недоступ|не\s*(?:доступ|активн|активир|работа|включ|целев|выполн|показыв|поддерж|относят)"
            r"|Managed[^.\n]{0,30}\bнет\b|\bнет\b[^.\n]{0,20}(?:Grail|DQL|Managed)"
            r"|\bSaaS\b|air-?gapped|классическ|\bClassic\b|пока\s+не|экран\s+пуст|пуст(?:ой|ая|ое)\b",
            re.IGNORECASE,
        ),
    ),
]


# ---------- SCAN -----------------------------------------------------------

# Строки, помеченные комментарием `<!-- qc:ignore -->` или `<!-- qc:ignore=CLASS -->`,
# чекер пропускает (allowlist для known-good фраз).
IGNORE_RE = re.compile(r"<!--\s*qc:ignore(?:=([A-Z_,]+))?\s*-->")


# Source-required детектор.
# Строки, которые выглядят как "hard tech-spec про Managed" (RAM ГБ, HU, vCPU,
# retention N дней с явным "по умолчанию" / "default"), должны иметь source-маркер
# в ±SRC_WINDOW строках: либо `docs.dynatrace.com/...`, либо markdown-ссылка,
# либо inline-комментарий `<!-- source: ... -->`, либо секция "Источник:".

TECH_SPEC_RE = re.compile(
    r"(\d+\s*(?:[-–]\s*\d+\s*)?)"
    r"(?:"
    r"ГиБ|GiB|ГБ\s*RAM|ГБ\s*памяти|GB\s*RAM|vCPU|HU|Host\s*Unit"
    r"|IOPS|Гбит/с|мс\s*между|ядер\s*процессора"
    r")",
    re.IGNORECASE,
)

SOURCE_MARKER_RE = re.compile(
    r"docs\.dynatrace\.com|<!--\s*source:|\[источник\]|\[source\]|Источник:|Source:",
    re.IGNORECASE,
)
SRC_WINDOW = 10  # строк ± (в размер секции/таблицы)


# ---------- ROUTE DETECTORS ------------------------------------------------
# Курс должен быть воспроизводим: ученик обязан суметь повторить показанное,
# не догадываясь, где живёт объект и что нажать. Два дефекта, из-за которых
# это ломается (правка 2026-07-30 по замечанию владельца курса):
#   ROUTE_SCENARIO_NO_STEPS (error) — сценарий пересказан прозой, без шагов.
#   ROUTE_NO_ADDRESS        (error) — объект/клик описан без адреса рядом.
# Оба сняты с реальных дефектов ui-overview.md: «Карточка сервиса. Клик по
# имени» (где именно имя, что откроется, какой URL?) и «Типичный сценарий.
# Инженер ищет payment-service…» (сервис выдуман, повторить нельзя).

# Заголовок или лид-абзац, который обещает сценарий/маршрут.
SCENARIO_INTRO_RE = re.compile(
    r"^(?:#{2,6}\s*|\*\*|[-*]\s*\*\*)?"
    r"(?:Типичный|Типовой|Практический)?\s*"
    r"(?:сценари[йя]|маршрут)\b",
    re.IGNORECASE,
)
# Нумерованный шаг: «1. …». Ищем именно начало списка.
STEP_START_RE = re.compile(r"^\s*1\.\s+\S")
SCENARIO_WINDOW = 14  # строк вперёд, в которых обязан начаться список шагов

# Детектор бьёт только по сценариям, которые показывают в интерфейсе. Слово
# «сценарий» в курсе значит ещё и «вариант конфигурации» (нарезка окружения на
# Production/Staging/Dev), там нумерованные шаги были бы неуместны. Отличаем по
# наличию навигации в теле блока.
NAVIGATION_MARKER_RE = re.compile(
    r"клик|нажат|открыва|перехо|провалива|экран|карточк|drilldown|/ui/",
    re.IGNORECASE,
)

# Объект или действие, требующие адреса: «Карточка X», «Клик по … открывает».
OBJECT_INTRO_RE = re.compile(
    r"(?:^|\*\*)Карточка\s+[а-яёa-z]+"
    r"|Клик(?:\s+по|\s+на|аю)?\b[^.]{0,80}?(?:открывает|раскрывает|ведёт|проваливается)",
    re.IGNORECASE,
)
# Что считается адресом: URL тенанта, маршрут /ui/, строка «Путь:»,
# явный блок «Как открыть» либо путь по меню со стрелкой между пунктами.
ADDRESS_RE = re.compile(
    r"https?://[^\s`]*dynatrace\.com/(?:ui|#)"
    r"|/ui/[a-z#]"
    r"|Путь(?:\s+в\s+меню)?:"
    r"|Как\s+открыть"
    r"|Что\s+нажать"
    r"|\*\*[^*]{3,40}\s+→\s+[^*]{3,40}\*\*",
    re.IGNORECASE,
)
ADDR_WINDOW = 12  # строк ± (лид-абзац секции обычно держит путь выше блока)

# Абзацы-определения: перечисление терминов, глоссарий, «X (путь): это …».
# Там клик упоминается как пример, а не как действие на экране.
DEFINITION_GUARD_RE = re.compile(
    r"Термины\s+темы"
    r"|^\s*[-*]\s*\*\*[^*]+\s*\((?:путь|воронка)\)\*\*"
    r"|Настраивается\s+через",
    re.IGNORECASE,
)


def _in_code_fence(lines: list[str]) -> list[bool]:
    """Маска: True для строк внутри ``` … ``` (детекторы их не трогают)."""
    inside = False
    mask: list[bool] = []
    for line in lines:
        if line.lstrip().startswith("```"):
            inside = not inside
            mask.append(True)
            continue
        mask.append(inside)
    return mask


def scan_routes(rel: str, lines: list[str]) -> list[Issue]:
    """Детекторы воспроизводимости: сценарий без шагов, объект без адреса."""
    issues: list[Issue] = []
    fence = _in_code_fence(lines)

    for idx, line in enumerate(lines):
        if fence[idx]:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        ignored = _ignored_classes(line)
        if "*" in ignored:
            continue

        # 1. Сценарий обязан разворачиваться в нумерованные шаги.
        if "ROUTE_SCENARIO_NO_STEPS" not in ignored and SCENARIO_INTRO_RE.match(stripped):
            window = lines[idx + 1 : idx + 1 + SCENARIO_WINDOW]
            navigational = NAVIGATION_MARKER_RE.search(stripped) or NAVIGATION_MARKER_RE.search(
                "\n".join(window)
            )
            if navigational and not any(STEP_START_RE.match(w) for w in window):
                issues.append(
                    Issue(
                        file=rel,
                        line=idx + 1,
                        cls="ROUTE_SCENARIO_NO_STEPS",
                        severity="error",
                        snippet=stripped[:160],
                        suggestion=(
                            "сценарий пересказан прозой — развернуть в нумерованные шаги "
                            "(где я → что делаю → что вижу → почему дальше туда), "
                            "пример: explanations/day-1/ui-overview.md"
                        ),
                    )
                )

        # 2. Объект или клик обязан иметь адрес рядом.
        if "ROUTE_NO_ADDRESS" in ignored or DEFINITION_GUARD_RE.search(stripped):
            continue
        if not OBJECT_INTRO_RE.search(stripped):
            continue
        lo = max(0, idx - ADDR_WINDOW)
        hi = min(len(lines), idx + ADDR_WINDOW + 1)
        if ADDRESS_RE.search("\n".join(lines[lo:hi])):
            continue
        issues.append(
            Issue(
                file=rel,
                line=idx + 1,
                cls="ROUTE_NO_ADDRESS",
                severity="error",
                snippet=stripped[:160],
                suggestion=(
                    "объект описан без адреса — добавить рядом «Как открыть»: "
                    "путь по меню, что нажать, куда попадаешь "
                    "(URL брать из ui_elements.json / study_plan.yaml, не выдумывать)"
                ),
            )
        )
    return issues


def scan_file(path: Path) -> list[Issue]:
    rel = path.relative_to(ROOT).as_posix()
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig", errors="replace")

    lines = text.splitlines()

    for lineno, line in enumerate(lines, start=1):
        m_ignore = IGNORE_RE.search(line)
        ignored_classes: set[str] = set()
        if m_ignore:
            raw = m_ignore.group(1)
            if raw is None:
                ignored_classes = {"*"}
            else:
                ignored_classes = {c.strip() for c in raw.split(",") if c.strip()}

        # Стандартные regex-детекторы
        for rule in RULES:
            if "*" in ignored_classes or rule.cls in ignored_classes:
                continue
            m = rule.pattern.search(line)
            if not m:
                continue
            if rule.guard_skip and rule.guard_skip.search(line):
                continue
            snippet = line.strip()
            if len(snippet) > 160:
                start = max(m.start() - 40, 0)
                end = min(m.end() + 40, len(line))
                snippet = "…" + line[start:end].strip() + "…"
            issues.append(
                Issue(
                    file=rel,
                    line=lineno,
                    cls=rule.cls,
                    severity=rule.severity,
                    snippet=snippet,
                    suggestion=rule.suggestion,
                )
            )

        # Source-required: tech-spec должен иметь docs-ссылку рядом
        if "NO_SOURCE" in ignored_classes or "*" in ignored_classes:
            continue
        if TECH_SPEC_RE.search(line):
            window_start = max(0, lineno - 1 - SRC_WINDOW)
            window_end = min(len(lines), lineno + SRC_WINDOW)
            window = "\n".join(lines[window_start:window_end])
            if not SOURCE_MARKER_RE.search(window):
                snippet = line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:157] + "…"
                issues.append(
                    Issue(
                        file=rel,
                        line=lineno,
                        cls="NO_SOURCE",
                        severity="warn",
                        snippet=snippet,
                        suggestion=(
                            "tech-spec без источника — добавить рядом ссылку на "
                            "docs.dynatrace.com или пометить <!-- qc:ignore=NO_SOURCE --> "
                            "если это generic-иллюстрация"
                        ),
                    )
                )

    issues.extend(scan_routes(rel, lines))
    return issues


def scan_all() -> list[Issue]:
    if not EXPLANATIONS.is_dir():
        print(f"ERROR: {EXPLANATIONS} not found", file=sys.stderr)
        sys.exit(2)
    all_issues: list[Issue] = []
    for md in sorted(EXPLANATIONS.rglob("*.md")):
        all_issues.extend(scan_file(md))
    return all_issues


# ---------- CARD DETECTORS (Ф2.3, spec.md раздел 10) -----------------------
# Сканируют cards/<day>/<topic>.md. Включаются флагом --cards (или из plan_html
# при сборке v2). Дефолтный quality_check (только explanations) не затрагивается,
# чтобы незавершённость карточек не блокировала сборку v1.
#   CARD_MISSING            (warn)  — темы без карточки (инфо, не блокирует)
#   CARD_EMDASH             (error) — длинное тире в карточке
#   CARD_BANNED_CATEGORY    (error) — запрещённая категория контент-политики в карточке
#   CARD_UNSOURCED_NUMBER   (error) — число, которого нет в explanation той же темы

CARDS_DIR = ROOT / "cards"
PLAN_FILE = ROOT / "study_plan.yaml"
CARD_NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")


def _ignored_classes(line: str) -> set[str]:
    """Классы из inline-маркера <!-- qc:ignore[=A,B] -->; {'*'} = все."""
    m = IGNORE_RE.search(line)
    if not m:
        return set()
    raw = m.group(1)
    return {"*"} if raw is None else {c.strip() for c in raw.split(",") if c.strip()}


def _frontmatter_end(lines: list[str]) -> int:
    """1-based номер строки, закрывающей YAML-шапку (второй '---'); 0 если шапки нет."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0


def _card_numbers(text: str) -> set[str]:
    """Множество числовых токенов (запятая->точка для единообразия)."""
    return {n.replace(",", ".") for n in CARD_NUM_RE.findall(text or "")}


def scan_cards() -> list[Issue]:
    import yaml

    issues: list[Issue] = []
    plan = yaml.safe_load(PLAN_FILE.read_text(encoding="utf-8"))
    for day in plan["days"]:
        for t in day.get("topics", []):
            day_id, topic_id = day["id"], t["id"]
            cf = CARDS_DIR / day_id / f"{topic_id}.md"
            rel = f"cards/{day_id}/{topic_id}.md"
            if not cf.exists():
                issues.append(Issue(rel, 0, "CARD_MISSING", "warn",
                                    f"{day_id}/{topic_id}",
                                    "карточка лектора ещё не создана (Ф2.2)"))
                continue

            text = cf.read_text(encoding="utf-8")
            lines = text.splitlines()
            fm_end = _frontmatter_end(lines)

            expl = EXPLANATIONS / day_id / f"{topic_id}.md"
            expl_nums = _card_numbers(expl.read_text(encoding="utf-8")) if expl.exists() else None

            for lineno, line in enumerate(lines, start=1):
                ignored = _ignored_classes(line)
                if "*" in ignored:
                    continue

                # CARD_EMDASH: только U+2014 (короткое тире '–' в списках допустимо)
                if "—" in line and "CARD_EMDASH" not in ignored:
                    issues.append(Issue(rel, lineno, "CARD_EMDASH", "error",
                                        line.strip()[:160],
                                        "длинное тире запрещено: заменить на «,» «:» или «·»"))

                # CARD_BANNED_CATEGORY: переиспользуем error-правила контент-политики
                if "CARD_BANNED_CATEGORY" not in ignored:
                    for rule in RULES:
                        if rule.severity != "error" or rule.cls in ignored:
                            continue
                        if rule.pattern.search(line) and not (
                            rule.guard_skip and rule.guard_skip.search(line)
                        ):
                            issues.append(Issue(rel, lineno, "CARD_BANNED_CATEGORY", "error",
                                                line.strip()[:160],
                                                f"{rule.cls}: {rule.suggestion}"))

                # CARD_UNSOURCED_NUMBER: число тела карточки обязано быть в explanation
                if expl_nums is not None and lineno > fm_end and "CARD_UNSOURCED_NUMBER" not in ignored:
                    for num in CARD_NUM_RE.findall(line):
                        if num.replace(",", ".") not in expl_nums:
                            issues.append(Issue(rel, lineno, "CARD_UNSOURCED_NUMBER", "error",
                                                line.strip()[:160],
                                                f"число «{num}» не найдено в explanation темы "
                                                f"({day_id}/{topic_id}); цифры карточки берутся "
                                                f"только из explanation"))
    return issues


# ---------- REPORT ---------------------------------------------------------

SEV_GLYPH = {"error": "❌", "warn": "⚠️"}


def print_human(issues: list[Issue]) -> None:
    if not issues:
        print("✅ 0 issues — все пояснения прошли quality_check.")
        return

    errors = [i for i in issues if i.severity == "error"]
    warns = [i for i in issues if i.severity == "warn"]

    by_class: dict[str, list[Issue]] = {}
    for i in issues:
        by_class.setdefault(i.cls, []).append(i)

    print(
        f"Найдено: {len(errors)} ошибок, {len(warns)} предупреждений по {len(by_class)} классам.\n"
    )

    for cls in sorted(by_class):
        group = by_class[cls]
        err_n = sum(1 for i in group if i.severity == "error")
        warn_n = sum(1 for i in group if i.severity == "warn")
        print(f"--- [{cls}]  errors={err_n} warns={warn_n} ---")
        for i in group:
            glyph = SEV_GLYPH[i.severity]
            print(f"  {glyph} {i.file}:{i.line}")
            print(f"     {i.snippet}")
            print(f"     → {i.suggestion}")
        print()

    total_err = len(errors)
    total_warn = len(warns)
    if total_err:
        print(f"❌ {total_err} error(s) — build должен быть заблокирован.")
    else:
        print(f"✅ 0 errors ({total_warn} warnings к просмотру).")


def print_json(issues: list[Issue]) -> None:
    payload = {
        "total": len(issues),
        "errors": sum(1 for i in issues if i.severity == "error"),
        "warnings": sum(1 for i in issues if i.severity == "warn"),
        "issues": [asdict(i) for i in issues],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Quality check for dt-crawler explanations."
    )
    ap.add_argument("--json", action="store_true", help="JSON output for hooks/CI")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--cards", action="store_true",
                    help="также проверять cards/*.md (CARD-детекторы, Ф2.3)")
    args = ap.parse_args()

    issues = scan_all()
    if args.cards:
        issues += scan_cards()

    if args.json:
        print_json(issues)
    else:
        print_human(issues)

    errors = [i for i in issues if i.severity == "error"]
    if errors:
        return 1
    if args.strict and issues:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
