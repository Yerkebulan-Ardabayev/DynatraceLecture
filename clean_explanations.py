"""
Post-process explanation .md files:
1. Drop leading "## Title" line (plan_docs.py adds the topic title separately)
2. Convert mkdocs admonitions (???+ tip "X" / ???+ note "X" / etc.) to plain markdown blockquotes
"""
import re
from pathlib import Path

EXPL_DIR = Path(__file__).parent / "explanations"

ICONS = {
    "tip": "💡",
    "note": "📝",
    "info": "ℹ️",
    "warning": "⚠️",
    "danger": "🚨",
    "example": "🎬",
    "success": "✅",
    "question": "❓",
}


def convert_admonitions(text: str) -> str:
    """Convert ???+ tip "Title"\\n    body  -> > 💡 **Title**\\n> body"""
    pattern = re.compile(
        r'^(\?\?\?\+?|!!!)\s+(\w+)\s+"([^"]*)"\s*\n((?:[ \t]{4}.*(?:\n|$))+)',
        re.MULTILINE,
    )

    def replace(m):
        kind = m.group(2).lower()
        title = m.group(3)
        body = m.group(4)
        # Strip 4-space indent from body lines
        body_lines = [re.sub(r'^[ \t]{4}', '', ln) for ln in body.rstrip().split('\n')]
        icon = ICONS.get(kind, "▸")
        # Build blockquote
        out = [f"> {icon} **{title}**", ">"]
        for ln in body_lines:
            if ln.strip():
                out.append(f"> {ln}")
            else:
                out.append(">")
        return "\n".join(out) + "\n"

    return pattern.sub(replace, text)


def clean_file(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text

    # 1. Drop leading "## ..." line (we don't need duplicate title)
    text = re.sub(r"^##\s+[^\n]+\n+", "", text, count=1)

    # 2. Convert admonitions
    text = convert_admonitions(text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    count = 0
    for md in sorted(EXPL_DIR.rglob("*.md")):
        if clean_file(md):
            print(f"  cleaned: {md.relative_to(EXPL_DIR)}")
            count += 1
        else:
            print(f"  unchanged: {md.relative_to(EXPL_DIR)}")
    print(f"\nDONE. {count} files cleaned.")


if __name__ == "__main__":
    main()
