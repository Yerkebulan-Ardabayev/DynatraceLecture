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
        pattern=re.compile(r"(Grail|DQL|Notebooks|Workflows|Apps\s*platform).{0,40}(в\s+Managed|в\s+managed).{0,40}20\d\d", re.IGNORECASE),
        suggestion="заменить на «сроки в публичных roadmap Dynatrace не зафиксированы»",
    ),
    Rule(
        cls="ROADMAP_DATE",
        severity="error",
        pattern=re.compile(r"(Grail|DQL).{0,30}(запланирован|появится|ожидается).{0,30}20\d\d", re.IGNORECASE),
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
        guard_skip=re.compile(r"Splunk\s+SPL|синтаксис.*Splunk"),  # пример в usql.md для аналогии синтаксиса — ок
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
        pattern=re.compile(r"поддержке\s+Dynatrace|в\s+поддержку\s+Dynatrace|поддержк[аеу]?\s+Dynatrace"),
        suggestion="удалить или переформулировать без упоминания процесса эскалации",
    ),
    Rule(
        cls="SUPPORT_INSTRUCTION",
        severity="warn",
        pattern=re.compile(r"открыть\s+тикет"),
        suggestion="проверить контекст — если это support-инструкция, убрать",
        guard_skip=re.compile(r"тикет\s+в\s+(Jira|ServiceNow|Remedy)"),  # интеграция с внешним ITSM — ок
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
        pattern=re.compile(r"\d+\s*[-–]\s*\d+\s*%\s*(CPU|нагрузк|overhead|процессор)", re.IGNORECASE),
        suggestion="numeric claim про overhead — верифицировать в dtkb; если не подтверждается, смягчить («заметной доли не тратит»)",
    ),
    Rule(
        cls="UNSOURCED_PERCENT",
        severity="warn",
        pattern=re.compile(r"до\s+\d+\s*%\s*(CPU|нагрузк|overhead|процессор)", re.IGNORECASE),
        suggestion="верхняя граница overhead без источника — верифицировать в dtkb",
    ),

    # 7. RPS-CLAIMS (нагрузочные характеристики без источника)
    Rule(
        cls="UNSOURCED_RPS",
        severity="warn",
        pattern=re.compile(r"\d{3,}\s*(rps|RPS|req/s|запросов\s+в\s+секунду)", re.IGNORECASE),
        suggestion="нагрузочная цифра без источника — либо привязать к docs, либо переформулировать без числа",
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
            issues.append(Issue(
                file=rel,
                line=lineno,
                cls=rule.cls,
                severity=rule.severity,
                snippet=snippet,
                suggestion=rule.suggestion,
            ))

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
                issues.append(Issue(
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
                ))
    return issues


def scan_all() -> list[Issue]:
    if not EXPLANATIONS.is_dir():
        print(f"ERROR: {EXPLANATIONS} not found", file=sys.stderr)
        sys.exit(2)
    all_issues: list[Issue] = []
    for md in sorted(EXPLANATIONS.rglob("*.md")):
        all_issues.extend(scan_file(md))
    return all_issues


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

    print(f"Найдено: {len(errors)} ошибок, {len(warns)} предупреждений по {len(by_class)} классам.\n")

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
    ap = argparse.ArgumentParser(description="Quality check for dt-crawler explanations.")
    ap.add_argument("--json", action="store_true", help="JSON output for hooks/CI")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    args = ap.parse_args()

    issues = scan_all()

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
