"""
insert_source_links.py — одноразовая утилита. Вставляет блок `> 📚 **Источники:**`
сразу после `## 🎓 ТЕОРИЯ` (или после блок-цитаты день/тема, если она идёт первой)
в темы, у которых есть подтверждённая страница docs.dynatrace.com.

URL-ы ниже прошли `link_check.py` — все отвечают 200 OK.

Запуск: `python scripts/insert_source_links.py`. Идемпотентный (не вставляет дважды).
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EXPL = ROOT / "explanations"


# Mapping: explanations/<day>/<file>.md → [(Название раздела, URL), ...]
# URL-ы верифицированы 2026-04-24 через WebFetch.
SOURCES: dict[str, list[tuple[str, str]]] = {
    "day-1/oneagent-principles.md": [
        ("OneAgent — capabilities и monitoring modes", "https://docs.dynatrace.com/docs/shortlink/oneagent"),
    ],
    "day-1/smartscape.md": [
        ("Smartscape — auto-discovered topology", "https://docs.dynatrace.com/docs/shortlink/smartscape"),
    ],
    "day-1/problems-feature.md": [
        ("Davis AI — root-cause analysis", "https://docs.dynatrace.com/docs/observe/problem-detection-and-analysis"),
    ],
    "day-1/dashboards.md": [
        ("Dashboards", "https://docs.dynatrace.com/docs/shortlink/dashboards"),
    ],
    "day-1/key-objects.md": [
        ("Smartscape — топология сущностей", "https://docs.dynatrace.com/docs/shortlink/smartscape"),
        ("Management Zones — разграничение доступа", "https://docs.dynatrace.com/docs/shortlink/management-zones"),
    ],
    "day-1/dem.md": [
        ("Digital Experience Monitoring (DEM)", "https://docs.dynatrace.com/docs/observe/digital-experience"),
    ],
    "day-2/services-overview.md": [
        ("Services — мониторинг приложений", "https://docs.dynatrace.com/docs/shortlink/services"),
    ],
    "day-2/service-cards.md": [
        ("Services — детальные карточки", "https://docs.dynatrace.com/docs/shortlink/services"),
    ],
    "day-2/hosts-processes.md": [
        ("Hosts — инфраструктурный мониторинг", "https://docs.dynatrace.com/docs/shortlink/hosts"),
    ],
    "day-2/containers.md": [
        ("Containers — мониторинг контейнеров", "https://docs.dynatrace.com/docs/shortlink/containers"),
    ],
    "day-2/kubernetes.md": [
        ("Kubernetes monitoring", "https://docs.dynatrace.com/docs/shortlink/kubernetes"),
    ],
    "day-2/oneagent-infra.md": [
        ("OneAgent Infrastructure mode", "https://docs.dynatrace.com/docs/shortlink/oneagent"),
    ],
    "day-2/problems-navigation.md": [
        ("Problems — навигация и обработка", "https://docs.dynatrace.com/docs/observe/problem-detection-and-analysis"),
    ],
    "day-3-4/service-object.md": [
        ("Services — сущность сервиса", "https://docs.dynatrace.com/docs/shortlink/services"),
    ],
    "day-3-4/service-flow.md": [
        ("Service flow — карта зависимостей", "https://docs.dynatrace.com/docs/shortlink/services"),
    ],
    "day-3-4/sli-slo-sla.md": [
        ("Service-Level Objectives (SLO)", "https://docs.dynatrace.com/docs/shortlink/service-level-objectives"),
    ],
    "day-3-4/reliability-config.md": [
        ("Service-Level Objectives (SLO)", "https://docs.dynatrace.com/docs/shortlink/service-level-objectives"),
    ],
    "day-3-4/thresholds.md": [
        ("Metric events — alerting на метрики", "https://docs.dynatrace.com/docs/shortlink/metric-events"),
    ],
    "day-3-4/instrumentation.md": [
        ("OneAgent — инструментация", "https://docs.dynatrace.com/docs/shortlink/oneagent"),
    ],
    "day-5/rum.md": [
        ("Real User Monitoring (RUM)", "https://docs.dynatrace.com/docs/shortlink/rum"),
    ],
    "day-5/ux-metrics.md": [
        ("Real User Monitoring — метрики UX", "https://docs.dynatrace.com/docs/shortlink/rum"),
    ],
    "day-5/journeys.md": [
        ("Real User Monitoring — user journeys", "https://docs.dynatrace.com/docs/shortlink/rum"),
    ],
    "day-5/session-replay.md": [
        ("Session Replay", "https://docs.dynatrace.com/docs/shortlink/session-replay"),
    ],
    "day-5/app-segments.md": [
        ("Real User Monitoring — applications", "https://docs.dynatrace.com/docs/shortlink/rum"),
    ],
    "day-5/synthetic.md": [
        ("Synthetic Monitoring", "https://docs.dynatrace.com/docs/shortlink/synthetic-monitoring"),
    ],
    "day-5/alerting-logic.md": [
        ("Metric events — условия алертов", "https://docs.dynatrace.com/docs/shortlink/metric-events"),
    ],
    "day-5/alerting-profiles.md": [
        ("Metric events — alerting profile scope", "https://docs.dynatrace.com/docs/shortlink/metric-events"),
    ],
}


SECTION_HDR = re.compile(r"^## 🎓 ТЕОРИЯ")
MARKER = "📚 **Источники"  # для идемпотентности


def format_block(entries: list[tuple[str, str]]) -> str:
    lines = ["> 📚 **Источники (официальная документация Dynatrace):**"]
    lines.append(">")
    for label, url in entries:
        lines.append(f"> - [{label}]({url})")
    lines.append("")
    return "\n".join(lines)


def process_file(rel_path: str, sources: list[tuple[str, str]]) -> str:
    p = EXPL / rel_path
    if not p.exists():
        return f"  ✗ skip (file not found): {rel_path}"
    text = p.read_text(encoding="utf-8")
    if MARKER in text:
        return f"  · already has source block: {rel_path}"

    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    for i, line in enumerate(lines):
        out.append(line)
        if not inserted and SECTION_HDR.match(line):
            # Вставим блок после ## 🎓 ТЕОРИЯ, пропустив возможные подзаголовки/описание
            # следующих 1-2 строк.
            look = 1
            while i + look < len(lines) and lines[i + look].strip() == "":
                out.append(lines[i + look])
                look += 1
            # Поглотим пустую строку уже — теперь вставляем блок
            out.append(format_block(sources))
            # Следующий цикл уйдёт с i = i (forward), но мы уже съели `look` строк.
            # Простейший путь — помечаем и пропускаем эти строки в дальнейшей копии.
            # Вместо этого перепишем через срез:
            rest = lines[i + look:]
            p.write_text("\n".join(out + rest) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
            return f"  ✓ inserted in {rel_path} ({len(sources)} link(s))"
    return f"  ✗ no '## 🎓 ТЕОРИЯ' section in {rel_path}"


def main() -> int:
    for rel, srcs in SOURCES.items():
        print(process_file(rel, srcs))
    print(f"\n→ обработано {len(SOURCES)} файлов")
    return 0


if __name__ == "__main__":
    sys.exit(main())
