"""
Извлечь реальные UI-элементы из сохранённых HTML-дампов тенанта.
Для каждой страницы: заголовки, кнопки, поля форм, sidebar items.
Выход: ui_elements.json — основа для переписки demo-сценариев под реальный контент.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "output" / "data" / "pages.jsonl"
OUT_FILE = ROOT / "ui_elements.json"


def extract_from_html(html_text: str) -> dict:
    """Из HTML вытащить структурированные UI-элементы."""
    soup = BeautifulSoup(html_text, "html.parser")

    # Удалить скрипты и стили — они зашумляют текст
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Заголовки
    headings = []
    for h in soup.find_all(["h1", "h2", "h3", "h4"]):
        text = h.get_text(strip=True)
        if text and len(text) < 200:
            headings.append({"level": h.name, "text": text})

    # Главный заголовок страницы (первый h1, либо title)
    main_title = ""
    h1 = soup.find("h1")
    if h1:
        main_title = h1.get_text(strip=True)
    elif soup.title:
        main_title = soup.title.get_text(strip=True)

    # Sidebar items — все ссылки с /ui/ в href
    sidebar_links = []
    seen_links = set()
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        text = a.get_text(strip=True)
        if not text or len(text) > 80:
            continue
        # Только internal /ui/ ссылки
        if "/ui/" not in href:
            continue
        # Очистить query string для де-дупа
        clean_href = re.sub(r"[?#].*", "", href)
        if (clean_href, text) in seen_links:
            continue
        seen_links.add((clean_href, text))
        sidebar_links.append({"text": text, "href": clean_href})

    # Кнопки (видимые тексты)
    buttons = []
    seen_buttons = set()
    for b in soup.find_all(["button"]):
        text = b.get_text(strip=True)
        aria = b.get("aria-label", "")
        if not text and not aria:
            continue
        label = text or aria
        if len(label) > 100:
            continue
        if label in seen_buttons:
            continue
        seen_buttons.add(label)
        buttons.append(label)
    buttons = buttons[:30]  # ограничить

    # Поля форм (input/select labels)
    fields = []
    for inp in soup.find_all(["input", "select", "textarea"]):
        ftype = inp.get("type", inp.name)
        name = inp.get("name", "") or inp.get("id", "")
        placeholder = inp.get("placeholder", "")
        aria = inp.get("aria-label", "")
        label = placeholder or aria or name
        if label and len(label) < 100:
            fields.append({"type": ftype, "label": label})
    # де-дуп
    seen = set()
    fields = [f for f in fields if not (f["label"] in seen or seen.add(f["label"]))][:30]

    # Tabs
    tabs = []
    for el in soup.select('[role="tab"], [data-testid*="tab" i], [data-testid*="Tab"]'):
        text = el.get_text(strip=True) or el.get("aria-label", "")
        if text and len(text) < 80 and text not in tabs:
            tabs.append(text)
    tabs = tabs[:20]

    # Body text — для контекста, первые 1500 chars
    body = soup.find("body")
    body_text = ""
    if body:
        body_text = body.get_text(separator=" ", strip=True)
        # Сжать множественные пробелы
        body_text = re.sub(r"\s+", " ", body_text)[:2000]

    return {
        "main_title": main_title,
        "headings": headings[:30],
        "sidebar_links": sidebar_links[:60],
        "buttons": buttons,
        "fields": fields,
        "tabs": tabs,
        "body_preview": body_text,
    }


def main():
    # Загружаем pages.jsonl чтобы знать пары (route, html_path, topic_id)
    pages = []
    with DATA_FILE.open(encoding="utf-8") as f:
        for line in f:
            try:
                pages.append(json.loads(line))
            except Exception:
                pass

    # Только plan-tagged
    pages = [p for p in pages if p.get("source") == "plan"]
    print(f"Pages to process: {len(pages)}")

    result = []
    for p in pages:
        html_path = ROOT / p.get("html", "")
        if not html_path.exists():
            print(f"  SKIP (no html): {p['url']}")
            continue
        try:
            text = html_path.read_text(encoding="utf-8")
            ui = extract_from_html(text)
            entry = {
                "day_id": p.get("day_id"),
                "topic_id": p.get("topic_id"),
                "topic_name": p.get("topic_name"),
                "plan_route": p.get("plan_route"),
                "url": p.get("url"),
                "title": p.get("title"),
                "screenshot": p.get("screenshot"),
                "ui": ui,
            }
            result.append(entry)
            print(f"  OK: {p['plan_route']}  ({len(ui['headings'])} headings, {len(ui['sidebar_links'])} sidebar, {len(ui['buttons'])} buttons)")
        except Exception as e:
            print(f"  ERROR on {p['url']}: {e}")

    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDONE -> {OUT_FILE}  ({len(result)} pages)")


if __name__ == "__main__":
    main()
