"""
Dynatrace tenant crawler.

Modes:
    discovery — visit each top-level route, screenshot + DOM, depth=1
    deep      — recursive crawl from a section, depth from config
    docs      — generate docs.md from collected data

Usage:
    python crawler.py discovery
    python crawler.py discovery --headed
    python crawler.py deep --section settings
    python crawler.py deep --section settings/preferences
    python crawler.py docs
"""
import os
import re
import json
import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import yaml
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent
CONFIG = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
TENANT_URL = os.getenv("DT_TENANT", CONFIG["tenant_url"]).rstrip("/")
STATE_FILE = ROOT / CONFIG["state_file"]
OUT = ROOT / CONFIG["output_dir"]
LOGS = ROOT / CONFIG["logs_dir"]
CHECKPOINTS = ROOT / "checkpoints"

for d in (CHECKPOINTS, LOGS, OUT / "screenshots", OUT / "pages", OUT / "data"):
    d.mkdir(parents=True, exist_ok=True)

VISITED_FILE = CHECKPOINTS / "visited.json"
DATA_FILE = OUT / "data" / "pages.jsonl"

SKIP_PATTERNS = [re.compile(p, re.IGNORECASE) for p in CONFIG["crawl"]["url_skip_patterns"]]


# ---------- helpers ----------

def slugify(text: str, max_len: int = 80) -> str:
    if not text:
        return "unnamed"
    text = text.replace("|", "-").replace("/", "-")
    text = re.sub(r"[^\w\s\-\.]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s\-]+", "-", text).strip("-_.")
    return (text[:max_len] or "unnamed").strip("-_.")


def url_to_folder(url: str) -> str:
    """Map URL path to a readable folder hierarchy."""
    m = re.search(r"/(ui|apps)/(.+?)(\?|#|$)", url)
    if not m:
        return "_root"
    path = m.group(2).rstrip("/")
    parts = [slugify(p) for p in path.split("/") if p]
    return "/".join(parts) or "_root"


def load_visited():
    if VISITED_FILE.exists():
        try:
            return set(json.loads(VISITED_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()


def save_visited(visited):
    VISITED_FILE.write_text(
        json.dumps(sorted(visited), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def append_data(record: dict):
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log_file = LOGS / f"crawl-{datetime.now().strftime('%Y-%m-%d')}.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def should_skip_url(url: str) -> bool:
    if not url.startswith(TENANT_URL):
        return True
    return any(p.search(url) for p in SKIP_PATTERNS)


def normalize_url(url: str) -> str:
    return url.split("#")[0].rstrip("/")


# ---------- capture ----------

async def capture_page(page, url: str, depth: int, folder: str, extra_meta: dict | None = None):
    title = (await page.title()) or "untitled"
    title_slug = slugify(title)

    sc_dir = OUT / "screenshots" / folder
    sc_dir.mkdir(parents=True, exist_ok=True)
    sc_path = sc_dir / f"{title_slug}.png"

    html_dir = OUT / "pages" / folder
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / f"{title_slug}.html"

    # screenshot — full page
    try:
        await page.screenshot(path=str(sc_path), full_page=True)
    except Exception as e:
        log(f"  screenshot failed: {e} — try viewport only")
        try:
            await page.screenshot(path=str(sc_path), full_page=False)
        except Exception as e2:
            log(f"  screenshot fully failed: {e2}")

    # rendered HTML
    try:
        html_path.write_text(await page.content(), encoding="utf-8")
    except Exception as e:
        log(f"  html save failed: {e}")

    body_text = ""
    try:
        body_text = await page.evaluate("() => (document.body && document.body.innerText) || ''")
    except Exception:
        pass

    links = []
    try:
        links = await page.evaluate(
            """() => Array.from(document.querySelectorAll('a[href]'))
                .map(a => a.href)
                .filter(h => h && (h.startsWith(window.location.origin)))"""
        )
    except Exception:
        pass

    tabs = []
    try:
        tabs = await page.evaluate(
            """() => Array.from(document.querySelectorAll('[role="tab"], [data-testid*="tab" i], [data-testid*="Tab"]'))
                .map(t => ({
                    text: (t.innerText || '').trim().slice(0, 100),
                    aria: t.getAttribute('aria-label') || ''
                }))
                .filter(t => t.text || t.aria)
                .slice(0, 50)"""
        )
    except Exception:
        pass

    headings = []
    try:
        headings = await page.evaluate(
            """() => Array.from(document.querySelectorAll('h1, h2, h3'))
                .map(h => ({lvl: h.tagName, text: (h.innerText||'').trim().slice(0,200)}))
                .filter(h => h.text)
                .slice(0, 80)"""
        )
    except Exception:
        pass

    record = {
        "url": url,
        "title": title,
        "folder": folder,
        "depth": depth,
        "screenshot": str(sc_path.relative_to(ROOT)).replace("\\", "/"),
        "html": str(html_path.relative_to(ROOT)).replace("\\", "/"),
        "text_preview": body_text[:1500],
        "text_full_length": len(body_text),
        "links_count": len(links),
        "tabs": tabs,
        "headings": headings,
        "captured_at": datetime.now().isoformat(timespec="seconds"),
    }
    if extra_meta:
        record.update(extra_meta)
    append_data(record)
    log(f"  ok: {title}")
    return links


# ---------- crawl ----------

async def crawl(mode: str, section: str | None, headless: bool):
    if not STATE_FILE.exists():
        log(f"ERROR: storage state missing at {STATE_FILE}. Run: python auth.py")
        sys.exit(2)

    if mode == "discovery":
        seeds = [TENANT_URL + r for r in CONFIG["seed_routes"]]
        max_depth = CONFIG.get("discovery", {}).get("depth", 1)
        max_pages = CONFIG.get("discovery", {}).get("max_pages", CONFIG["crawl"]["max_pages"])
    elif mode == "deep":
        if not section:
            log("ERROR: --section required for deep mode (e.g. settings, settings/preferences)")
            sys.exit(2)
        seeds = [f"{TENANT_URL}/ui/{section.strip('/')}"]
        max_depth = CONFIG.get("deep", {}).get("depth", CONFIG["crawl"]["max_depth"])
        max_pages = CONFIG.get("deep", {}).get("max_pages", CONFIG["crawl"]["max_pages"])
    else:
        log(f"ERROR: unknown mode {mode}")
        sys.exit(2)

    visited = load_visited()
    nav_wait = CONFIG["crawl"]["navigation_wait_ms"]
    page_timeout = CONFIG["crawl"]["page_timeout_ms"]
    vw = CONFIG["crawl"]["viewport_width"]
    vh = CONFIG["crawl"]["viewport_height"]

    log(f"start: mode={mode} headless={headless} max_pages={max_pages} already_visited={len(visited)} seeds={len(seeds)}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            storage_state=str(STATE_FILE),
            viewport={"width": vw, "height": vh},
        )
        page = await context.new_page()

        queue: list[tuple[str, int]] = [(normalize_url(u), 0) for u in seeds]
        in_queue = {u for u, _ in queue}
        crawled = 0
        errors = 0

        while queue and crawled < max_pages:
            url, depth = queue.pop(0)
            in_queue.discard(url)
            if url in visited or should_skip_url(url):
                continue

            try:
                log(f"[{crawled+1}] depth={depth} {url}")
                await page.goto(url, wait_until="domcontentloaded", timeout=page_timeout)
                await page.wait_for_timeout(nav_wait)
                # extra wait for Angular/SPA settle
                try:
                    await page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass

                folder = url_to_folder(page.url)  # use ACTUAL URL (after redirects)
                links = await capture_page(page, page.url, depth, folder)
                visited.add(url)
                visited.add(normalize_url(page.url))
                crawled += 1

                if crawled % 5 == 0:
                    save_visited(visited)

                if depth < max_depth:
                    for link in links:
                        clean = normalize_url(link)
                        if (
                            clean
                            and clean not in visited
                            and clean not in in_queue
                            and not should_skip_url(clean)
                            and ("/ui/" in clean or "/apps/" in clean)
                        ):
                            queue.append((clean, depth + 1))
                            in_queue.add(clean)

            except Exception as e:
                errors += 1
                log(f"  ERROR: {type(e).__name__}: {str(e)[:200]}")

        save_visited(visited)
        await browser.close()
        log(f"done. crawled={crawled} errors={errors} total_visited={len(visited)} queue_remaining={len(queue)}")


# ---------- docs ----------

def generate_docs():
    if not DATA_FILE.exists():
        print("No data yet — run crawler first.")
        return

    pages = []
    with DATA_FILE.open(encoding="utf-8") as f:
        for line in f:
            try:
                pages.append(json.loads(line))
            except Exception:
                pass

    by_url = {}
    for p in pages:
        by_url[p["url"]] = p
    pages = sorted(by_url.values(), key=lambda x: (x["folder"] or "", x["url"]))

    groups = defaultdict(list)
    for p in pages:
        top = (p["folder"] or "_root").split("/")[0]
        groups[top].append(p)

    out = [
        "# Dynatrace Tenant — карта сайта и страниц\n\n",
        f"_Автогенерация. Страниц: {len(pages)}. Тенант: `{TENANT_URL}`._\n\n",
        "## Содержание\n\n",
    ]
    for g in sorted(groups):
        out.append(f"- [{g}](#{g.lower().replace('/', '').replace(' ', '-')}) — {len(groups[g])} страниц\n")
    out.append("\n---\n")

    for g in sorted(groups):
        out.append(f"\n## {g}\n\n")
        for p in groups[g]:
            out.append(f"### {p['title']}\n\n")
            out.append(f"- **URL:** `{p['url']}`\n")
            out.append(f"- **Папка:** `{p['folder']}`\n")
            out.append(f"- **Глубина:** {p['depth']}\n")
            if p.get("tabs"):
                tab_list = " · ".join(t["text"] or t["aria"] for t in p["tabs"] if (t["text"] or t["aria"]))
                if tab_list:
                    out.append(f"- **Табы:** {tab_list}\n")
            if p.get("headings"):
                heads = " · ".join(h["text"] for h in p["headings"][:10])
                out.append(f"- **Заголовки:** {heads}\n")
            out.append(f"- **Скриншот:** [{p['screenshot']}]({p['screenshot']})\n")
            out.append(f"- **HTML:** [{p['html']}]({p['html']})\n\n")
            out.append(f"![{p['title']}]({p['screenshot']})\n\n")
            preview = (p.get("text_preview") or "").strip()
            if preview:
                out.append("<details><summary>Текст страницы (превью)</summary>\n\n```\n")
                out.append(preview)
                out.append("\n```\n\n</details>\n\n")
            out.append("---\n")

    docs_file = OUT / "docs.md"
    docs_file.write_text("".join(out), encoding="utf-8")
    print(f"OK -> {docs_file} ({len(pages)} pages, {len(groups)} sections)")


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description="Dynatrace tenant crawler")
    ap.add_argument("mode", choices=["discovery", "deep", "docs"])
    ap.add_argument("--section", help="for deep mode, e.g. 'settings' or 'settings/preferences'")
    ap.add_argument("--headed", action="store_true", help="show browser (default headless)")
    args = ap.parse_args()

    if args.mode == "docs":
        generate_docs()
        return
    asyncio.run(crawl(mode=args.mode, section=args.section, headless=not args.headed))


if __name__ == "__main__":
    main()
