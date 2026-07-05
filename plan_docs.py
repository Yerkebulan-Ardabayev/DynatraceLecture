"""
Сгенерировать документацию по структуре учебного плана.
Читает output/data/pages.jsonl + study_plan.yaml.
Пишет:
    output/docs/index.md          — оглавление по всем дням
    output/docs/day-1.md          — день 1
    output/docs/day-2.md
    output/docs/day-3-4.md
    output/docs/day-5.md
"""
import json
from pathlib import Path
from collections import defaultdict
import yaml

ROOT = Path(__file__).parent
PLAN_FILE = ROOT / "study_plan.yaml"
DATA_FILE = ROOT / "output" / "data" / "pages.jsonl"
DOCS_DIR = ROOT / "output" / "docs"
EXPLANATIONS_DIR = ROOT / "explanations"


def load_explanation(day_id: str, topic_id: str) -> str | None:
    f = EXPLANATIONS_DIR / day_id / f"{topic_id}.md"
    if f.exists():
        return f.read_text(encoding="utf-8").strip()
    return None


def load_plan():
    return yaml.safe_load(PLAN_FILE.read_text(encoding="utf-8"))


def load_pages():
    if not DATA_FILE.exists():
        return []
    out = []
    with DATA_FILE.open(encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def status_marker(p):
    # Приоритет: реальный HTTP-статус ответа (пишется краулером в http_status).
    # Подстрока "404" в title была ненадёжной: страница про коды ошибок HTTP
    # с "404" в заголовке ложно помечалась как битая, а реальный 404 без слова
    # "404" в title, наоборот, как рабочий.
    status = p.get("http_status")
    if isinstance(status, int):
        if status == 404:
            return "❌ 404"
        if status == 403:
            return "🔒 403"
        if status >= 400:
            return f"❌ {status}"
        return "✅"
    # Fallback для старых записей без http_status: прежняя эвристика по title.
    title = (p.get("title") or "").lower()
    if "404" in title:
        return "❌ 404"
    if "403" in title:
        return "🔒 403"
    return "✅"


def write_day(day, pages_for_day):
    day_id = day["id"]
    f = DOCS_DIR / f"{day_id}.md"
    out = []
    out.append(f"# {day['title']}\n\n")
    out.append(f"**Цели дня:**\n\n{day['objectives'].strip()}\n\n")
    out.append(f"_Тем: {len(day['topics'])}._\n\n")
    out.append("## Содержание\n\n")
    for t in day["topics"]:
        anchor = t["id"]
        out.append(f"- [{t['name']}](#{anchor})\n")
    out.append("\n---\n\n")

    # Group records by topic_id
    by_topic = defaultdict(list)
    for p in pages_for_day:
        by_topic[p.get("topic_id")].append(p)

    for t in day["topics"]:
        anchor = t["id"]
        out.append(f'<a id="{anchor}"></a>\n')
        out.append(f"## {t['name']}\n\n")

        if t.get("notes"):
            out.append(f"> **Примечание:** {t['notes']}\n\n")

        # === Главное: explanation из explanations/{day_id}/{topic_id}.md ===
        explanation = load_explanation(day["id"], t["id"])
        if explanation:
            out.append(explanation)
            out.append("\n\n")
        else:
            out.append(f"> ⚠️ **Объяснение не написано.** Создай `explanations/{day['id']}/{t['id']}.md` "
                       f"со структурой: «Что это / Где найти / Куда нажать / Как настроить».\n\n")

        if t.get("kind") == "concept" and not t.get("routes"):
            out.append("---\n\n")
            continue

        recs = by_topic.get(t["id"], [])
        seen = set()
        recs = [r for r in recs if (r["url"] not in seen and not seen.add(r["url"]))]

        if recs:
            out.append("### Скриншоты UI\n\n")
            for p in recs:
                mark = status_marker(p)
                short_title = p['title'].split(' - ')[0] if ' - ' in p['title'] else p['title']
                out.append(f"**{mark} {short_title}** — `{p.get('plan_route', '?')}`\n\n")
                sc = p.get("screenshot", "")
                if sc:
                    rel = "../" + sc.split("output/", 1)[1] if "output/" in sc else sc
                    out.append(f"![{short_title}]({rel})\n\n")
        elif t.get("routes"):
            out.append(f"_⚠️ Crawler не зафиксировал скриншотов — запусти `python plan_runner.py --day {day['id']}`_\n\n")
            for r in t.get("routes", []):
                out.append(f"- `{r}`\n")
            out.append("\n")

        out.append("---\n\n")

    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("".join(out), encoding="utf-8")
    print(f"  -> {f}  ({len(pages_for_day)} pages, {len(day['topics'])} topics)")


def write_index(plan, all_pages):
    f = DOCS_DIR / "index.md"
    out = ["# Обучение Dynatrace — оглавление\n\n"]
    out.append(f"Тенант: `{plan.get('tenant_url', 'guu84124.live.dynatrace.com')}`. Всего страниц: {len(all_pages)}.\n\n")
    out.append("## План\n\n")
    for d in plan["days"]:
        topics_count = len(d["topics"])
        pages_count = sum(1 for p in all_pages if p.get("day_id") == d["id"])
        out.append(f"### [{d['title']}]({d['id']}.md)\n\n")
        out.append(f"_Тем: {topics_count} · Страниц зафиксировано: {pages_count}_\n\n")
        out.append(f"{d['objectives'].strip()}\n\n")
        for t in d["topics"]:
            t_pages = sum(1 for p in all_pages if p.get("topic_id") == t["id"])
            mark = "✅" if t_pages else "⚪"
            out.append(f"- {mark} [{t['name']}]({d['id']}.md#{t['id']}) — {t_pages} стр.\n")
        out.append("\n")
    f.write_text("".join(out), encoding="utf-8")
    print(f"  -> {f}")


def main():
    plan = load_plan()
    all_pages = [p for p in load_pages() if p.get("source") == "plan"]
    print(f"Loaded {len(all_pages)} plan-tagged pages")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    write_index(plan, all_pages)
    for d in plan["days"]:
        day_pages = [p for p in all_pages if p.get("day_id") == d["id"]]
        write_day(d, day_pages)

    print(f"\nDONE. open: {DOCS_DIR / 'index.md'}")


if __name__ == "__main__":
    main()
