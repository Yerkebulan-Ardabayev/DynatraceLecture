"""
extract_tech_claims.py — вытаскивает все numeric tech-claims из explanations/*.md.

Даёт исчерпывающий инвентарь утверждений вида «X% CPU», «N MB RAM», «N дней retention»,
«N запросов в секунду», «порт N», «до N хостов», для последующей верификации через dtkb.

Вывод: tech_claims.md — таблица file:line / class / claim / context. Это вход для
quality_check.py не является, это отдельный инструмент для ручного/полуручного review.

Usage:
    python scripts/extract_tech_claims.py
    python scripts/extract_tech_claims.py --json
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
class Claim:
    file: str
    line: int
    cls: str
    claim: str
    context: str


# Классы claim'ов с соответствующими regex. Ловим только те, где в строке есть цифра
# + единица измерения / ключевое слово из словаря Managed-specifics.

CLAIM_PATTERNS: list[tuple[str, re.Pattern]] = [
    # CPU / процессор overhead
    ("CPU_OVERHEAD", re.compile(
        r"\d+(?:[.,]\d+)?\s*[-–]?\s*\d*\s*%\s*(?:CPU|процессора|процессор|нагрузк|overhead)",
        re.IGNORECASE,
    )),
    # Память: MB / ГБ / мегабайт / гигабайт
    ("MEMORY", re.compile(
        r"\d+(?:[-–]\d+)?\s*(?:МБ|МБайт|MB|мегабайт(?:а|ов)?|ГБ|GB|гигабайт(?:а|ов)?)\s*(?:памяти|ОЗУ|RAM|heap)?",
        re.IGNORECASE,
    )),
    # Диск / retention
    ("DISK_RETENTION", re.compile(
        r"\d+\s*(?:ТБ|TB|терабайт|дн(?:ей|я|ь)|недел(?:и|ь|я)|месяц(?:ев|а|)|year|год(?:а|ов|)|час(?:ов|а|)|минут)",
        re.IGNORECASE,
    )),
    # Лимиты / counts (хосты, серверы, сессии, запросы, метрики)
    ("LIMIT_COUNT", re.compile(
        r"\d{2,}\s*(?:HU|DDU|host|хост(?:ов|а|)|сервер(?:ов|а|)|сессий|метрик|микросервис(?:ов|а|)|трейс(?:ов|а|))",
        re.IGNORECASE,
    )),
    # RPS / throughput
    ("THROUGHPUT", re.compile(
        r"\d+\s*(?:rps|RPS|req/s|запрос(?:ов|а)?\s*в\s*секунду|событий\s*в\s*секунду)",
        re.IGNORECASE,
    )),
    # Порты
    ("PORT", re.compile(r"\bпорт[ыу]?\s*(?:TCP|UDP)?\s*\d{2,5}\b", re.IGNORECASE)),
    ("PORT", re.compile(r"\b(?:8021|8443|9091|9200|9300|9042|7000|7001|443|80|53|4317|4318|9999)\b")),
    # Latency / таймаут
    ("LATENCY", re.compile(
        r"\d+(?:[.,]\d+)?\s*(?:мс|ms|секунд[аы]?|минут[аы]?|наносекунд)",
        re.IGNORECASE,
    )),
    # Проценты общие (baseline, deviation, confidence)
    ("PERCENT_GENERIC", re.compile(
        r"\b\d+(?:[.,]\d+)?\s*%\s*(?:доверит|отклонен|baseline|percentile|перцент|медиан)",
        re.IGNORECASE,
    )),
    # Сжатие / компрессия (cardinality)
    ("COMPRESSION", re.compile(r"\d+[-–]\d+×|\d+\s*раз(?:а)?\s*(?:сжат|меньше)", re.IGNORECASE)),
    # Интервалы сбора / frequency
    ("SAMPLING_INTERVAL", re.compile(
        r"(?:каждые|раз в|интервал)\s*\d+\s*(?:сек|мин|секунд|минут)",
        re.IGNORECASE,
    )),
    # Версии Dynatrace (для проверки актуальности)
    ("DYNATRACE_VERSION", re.compile(r"\b1\.\d{3}(?:\.\d+)?\b")),
]


# Некоторые классы шумны — отфильтруем заведомо нерелевантные контексты.
# Для LIMIT_COUNT — пропустить «N лет», «N часов», «N дней» (это в DISK_RETENTION).
SKIP_IN_CONTEXT = {
    "PORT": re.compile(r"(?:год|годов|лет|дней|месяц|тысяч|миллион)", re.IGNORECASE),
}


def scan_file(path: Path) -> list[Claim]:
    rel = path.relative_to(ROOT).as_posix()
    claims: list[Claim] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig", errors="replace")

    # Skip code blocks — там порты и версии программ как синтаксис, не claim'ы
    in_code = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Skip table separator lines
        if re.match(r"^\s*\|?\s*[-: |]+$", line):
            continue

        for cls, rx in CLAIM_PATTERNS:
            for m in rx.finditer(line):
                claim_text = m.group(0)
                # Apply class-specific skip filters
                skip_rx = SKIP_IN_CONTEXT.get(cls)
                if skip_rx and skip_rx.search(line):
                    continue
                # Build context window around match
                start = max(m.start() - 50, 0)
                end = min(m.end() + 50, len(line))
                context = line[start:end].strip()
                if start > 0:
                    context = "…" + context
                if end < len(line):
                    context = context + "…"
                claims.append(Claim(
                    file=rel,
                    line=lineno,
                    cls=cls,
                    claim=claim_text.strip(),
                    context=context,
                ))
    return claims


def scan_all() -> list[Claim]:
    if not EXPLANATIONS.is_dir():
        print(f"ERROR: {EXPLANATIONS} not found", file=sys.stderr)
        sys.exit(2)
    all_claims: list[Claim] = []
    for md in sorted(EXPLANATIONS.rglob("*.md")):
        all_claims.extend(scan_file(md))
    # Deduplicate identical claims at same line (regex pattern overlap)
    seen: set[tuple[str, int, str, str]] = set()
    uniq: list[Claim] = []
    for c in all_claims:
        key = (c.file, c.line, c.cls, c.claim.lower())
        if key in seen:
            continue
        seen.add(key)
        uniq.append(c)
    return uniq


def write_report(claims: list[Claim], out_path: Path) -> None:
    by_class: dict[str, list[Claim]] = {}
    for c in claims:
        by_class.setdefault(c.cls, []).append(c)

    lines: list[str] = []
    lines.append("# Tech-claims inventory для dtkb-верификации")
    lines.append("")
    lines.append(f"Всего: **{len(claims)} claims** по **{len(by_class)} классам**. "
                 "Сгенерировано `scripts/extract_tech_claims.py`.")
    lines.append("")
    lines.append("Для каждого claim — проверить через `dtkb search` (fallback: `docs.dynatrace.com/managed/`). "
                 "Занести в `tech_claims_verification.md` решение: **подтверждён** / **смягчён** / **удалён** "
                 "с ссылкой на источник.")
    lines.append("")

    for cls in sorted(by_class):
        group = by_class[cls]
        lines.append(f"## [{cls}]  — {len(group)} claims")
        lines.append("")
        lines.append("| file:line | claim | context |")
        lines.append("|---|---|---|")
        for c in group:
            ctx = c.context.replace("|", "\\|")
            claim = c.claim.replace("|", "\\|")
            lines.append(f"| `{c.file}:{c.line}` | `{claim}` | {ctx} |")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract numeric tech-claims from explanations/*.md")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--out", default="tech_claims.md", help="output path (default: tech_claims.md)")
    args = ap.parse_args()

    claims = scan_all()

    if args.json:
        payload = {"total": len(claims), "claims": [asdict(c) for c in claims]}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    out = (ROOT / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    write_report(claims, out)
    by_class: dict[str, int] = {}
    for c in claims:
        by_class[c.cls] = by_class.get(c.cls, 0) + 1
    print(f"✅ {len(claims)} claims → {out.relative_to(ROOT)}")
    for cls in sorted(by_class):
        print(f"   [{cls}] = {by_class[cls]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
