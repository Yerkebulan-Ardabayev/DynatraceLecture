"""
Извлечь контент из dynatrace-platform.html (твой навигатор) → JSON.
Парсит pages = [...] массив с {id, part, title, sections: [{title, content}]}.
Выход: navigator_content.json со всеми страницами.
"""
import json
import re
from pathlib import Path

NAV_HTML = Path(r"C:\Users\yerke\Desktop\dynatrace-platform\dynatrace-platform.html")
OUT_FILE = Path(__file__).parent / "navigator_content.json"


def extract_pages():
    """Парсим pages = [...] массив. Каждая страница — {id, part, title, sections}."""
    text = NAV_HTML.read_text(encoding="utf-8")

    # Найти начало pages = [
    start_match = re.search(r"const pages\s*=\s*\[", text)
    if not start_match:
        raise RuntimeError("Не найден 'const pages = ['")

    pos = start_match.end()
    pages = []

    while pos < len(text):
        # Пропустить whitespace
        while pos < len(text) and text[pos] in " \t\n\r":
            pos += 1

        # Конец массива?
        if text[pos] == "]":
            break

        # Должен быть `{`
        if text[pos] != "{":
            # Пропустить запятую
            if text[pos] == ",":
                pos += 1
                continue
            break

        # Парсим один объект страницы — найти соответствующий `}`
        # с учётом nested {} и template literals (`...`)
        page_start = pos
        depth = 0
        in_backtick = False
        in_string = None  # ' или "

        while pos < len(text):
            c = text[pos]
            if in_backtick:
                if c == "\\" and pos + 1 < len(text):
                    pos += 2
                    continue
                if c == "`":
                    in_backtick = False
                pos += 1
                continue
            if in_string:
                if c == "\\" and pos + 1 < len(text):
                    pos += 2
                    continue
                if c == in_string:
                    in_string = None
                pos += 1
                continue
            if c == "`":
                in_backtick = True
                pos += 1
                continue
            if c in ("'", '"'):
                in_string = c
                pos += 1
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    pos += 1
                    break
            pos += 1

        page_text = text[page_start:pos]
        page = parse_page(page_text)
        if page:
            pages.append(page)

    return pages


def parse_page(page_text):
    """Из {id:"...",part:"...",title:"...",sections:[...]} → dict."""
    page = {}

    # id
    m = re.search(r'id:\s*["\']([^"\']+)["\']', page_text)
    if m:
        page["id"] = m.group(1)

    # part
    m = re.search(r'part:\s*["\']([^"\']+)["\']', page_text)
    if m:
        page["part"] = m.group(1)

    # title
    m = re.search(r'title:\s*["\']([^"\']+)["\']', page_text)
    if m:
        page["title"] = m.group(1)

    # icon
    m = re.search(r'icon:\s*["\']([^"\']+)["\']', page_text)
    if m:
        page["icon"] = m.group(1)

    # sections — массив объектов с title и content
    sections = []
    sec_start = page_text.find("sections:")
    if sec_start >= 0:
        # Пройти от sections:[ до соответствующего ]
        bracket_pos = page_text.find("[", sec_start)
        if bracket_pos >= 0:
            sections_text = extract_array_content(page_text, bracket_pos)
            sections = parse_sections(sections_text)

    page["sections"] = sections
    return page if page.get("id") else None


def extract_array_content(text, bracket_pos):
    """Из text[bracket_pos]='[' извлечь содержимое до соответствующего ']'."""
    pos = bracket_pos + 1
    depth = 1
    in_backtick = False
    in_string = None
    start = pos

    while pos < len(text):
        c = text[pos]
        if in_backtick:
            if c == "\\" and pos + 1 < len(text):
                pos += 2
                continue
            if c == "`":
                in_backtick = False
            pos += 1
            continue
        if in_string:
            if c == "\\" and pos + 1 < len(text):
                pos += 2
                continue
            if c == in_string:
                in_string = None
            pos += 1
            continue
        if c == "`":
            in_backtick = True
            pos += 1
            continue
        if c in ("'", '"'):
            in_string = c
            pos += 1
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return text[start:pos]
        pos += 1
    return text[start:pos]


def parse_sections(sections_text):
    """Из массива {title:"...",content:`...`} извлечь список секций."""
    sections = []
    pos = 0
    while pos < len(sections_text):
        # Пропустить whitespace и запятые
        while pos < len(sections_text) and sections_text[pos] in " \t\n\r,":
            pos += 1
        if pos >= len(sections_text):
            break
        if sections_text[pos] != "{":
            break

        # Найти соответствующий }
        obj_start = pos
        depth = 0
        in_backtick = False
        in_string = None
        while pos < len(sections_text):
            c = sections_text[pos]
            if in_backtick:
                if c == "\\" and pos + 1 < len(sections_text):
                    pos += 2
                    continue
                if c == "`":
                    in_backtick = False
                pos += 1
                continue
            if in_string:
                if c == "\\" and pos + 1 < len(sections_text):
                    pos += 2
                    continue
                if c == in_string:
                    in_string = None
                pos += 1
                continue
            if c == "`":
                in_backtick = True
                pos += 1
                continue
            if c in ("'", '"'):
                in_string = c
                pos += 1
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    pos += 1
                    break
            pos += 1

        obj_text = sections_text[obj_start:pos]

        # Извлечь title
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', obj_text)
        title = title_match.group(1) if title_match else ""

        # Извлечь content (между бэктиками)
        content = ""
        content_match = re.search(r"content:\s*`", obj_text)
        if content_match:
            c_start = content_match.end()
            c_pos = c_start
            while c_pos < len(obj_text):
                ch = obj_text[c_pos]
                if ch == "\\" and c_pos + 1 < len(obj_text):
                    c_pos += 2
                    continue
                if ch == "`":
                    break
                c_pos += 1
            content = obj_text[c_start:c_pos]
            # Unescape JS
            content = content.replace("\\`", "`").replace("\\$", "$").replace("\\\\", "\\")

        sections.append({"title": title, "content": content})

    return sections


def main():
    pages = extract_pages()
    OUT_FILE.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {OUT_FILE}")
    print(f"Извлечено страниц: {len(pages)}")
    print(f"Уникальные части:")
    parts = {}
    for p in pages:
        part = p.get("part", "(no part)")
        parts.setdefault(part, []).append(p["id"])
    for part, ids in parts.items():
        print(f"  {part}: {len(ids)} страниц")


if __name__ == "__main__":
    main()
