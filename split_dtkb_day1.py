"""
Split dtkb's day1-introduction.md into per-topic explanation files.
Source: dynatrace-docs-website (Managed-focused training).
Maps each ## N. <title> section to a topic_id from study_plan.yaml.
"""
import os
import re
from pathlib import Path

# Источник и назначение кросс-платформенно (через env / от домашней папки), а не
# Windows-хардкодом, который падал при импорте и на Mac. Переопределяется SRC_MD.
DEFAULT_SRC = (
    Path.home()
    / "Desktop" / "Projects" / "dynatrace-docs-website"
    / "docs" / "ru" / "training" / "day1-introduction.md"
)
SRC = Path(os.environ.get("SRC_MD", DEFAULT_SRC))
DST_DIR = Path(__file__).parent / "explanations" / "day-1"

# Section index (## N.) -> topic_id (matches study_plan.yaml day-1 topic ids)
MAPPING = {
    1: "architecture",
    2: "components",
    3: "oneagent-principles",
    4: "dem",
    5: "ui-overview",
    6: "smartscape",
    7: "key-objects",
    8: "data-explorer",
    9: "baselines",
    10: "problems-feature",
    11: "dashboards",
}

def main():
    DST_DIR.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")

    # Split by ## N. heading (preserving the heading)
    parts = re.split(r"\n(?=## \d+\. )", text)

    written = 0
    for part in parts:
        m = re.match(r"## (\d+)\. (.+)", part)
        if not m:
            continue
        idx = int(m.group(1))
        if idx not in MAPPING:
            print(f"  skip: section {idx} not in mapping")
            continue
        topic_id = MAPPING[idx]
        # Drop the "## N. " prefix from the first heading (becomes natural ## title)
        body = re.sub(r"^## \d+\. ", "## ", part, count=1)
        # Stop at "## Итоги" (last meta section)
        body = re.split(r"\n## Итоги ", body)[0].rstrip() + "\n"

        out_file = DST_DIR / f"{topic_id}.md"
        out_file.write_text(body, encoding="utf-8")
        print(f"  -> {out_file.name}  ({len(body)} chars, section {idx})")
        written += 1

    print(f"\nDONE. Wrote {written} explanation files to {DST_DIR}")


if __name__ == "__main__":
    main()
