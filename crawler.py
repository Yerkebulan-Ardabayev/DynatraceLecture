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
import errno
import hashlib
import asyncio
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from urllib.parse import urlsplit, urlunsplit
import yaml
from dotenv import load_dotenv

# Playwright грузим мягко: чистые хелперы (slugify/normalize_url/frontier)
# импортируются и тестируются без установленного браузера. Нужен он только в
# момент реального обхода (crawl); там проверяем и просим установить.
try:
    from playwright.async_api import async_playwright
except ImportError:  # pragma: no cover
    async_playwright = None

# fcntl is POSIX-only; on Windows the single-instance lock is skipped (best effort).
try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None

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
FRONTIER_FILE = CHECKPOINTS / "frontier.json"
EXTRACTED_LINKS_FILE = CHECKPOINTS / "extracted_links.json"
LOCK_FILE = CHECKPOINTS / "crawler.lock"
DATA_FILE = OUT / "data" / "pages.jsonl"

# Сколько раз вернуть упавший URL во фронтир прежде чем окончательно бросить.
MAX_RETRIES = CONFIG["crawl"].get("max_retries", 2)

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


def _atomic_write_json(path: Path, payload) -> None:
    """Записать JSON атомарно (tmp + os.replace), чтобы kill посреди записи
    не оставил битый чекпоинт."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(tmp, path)


def save_visited(visited):
    _atomic_write_json(VISITED_FILE, sorted(visited))


def load_frontier():
    """Восстановить BFS-очередь из чекпоинта.

    Возвращает список пар [url, depth]. Пусто, если файла нет или он битый:
    вызывающий тогда стартует с seeds.
    """
    if FRONTIER_FILE.exists():
        try:
            raw = json.loads(FRONTIER_FILE.read_text(encoding="utf-8"))
            out = []
            for item in raw:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    out.append((str(item[0]), int(item[1])))
            return out
        except Exception:
            return []
    return []


def load_extracted_links():
    """Восстановить накопленные исходящие ссылки (url -> список ссылок)."""
    if EXTRACTED_LINKS_FILE.exists():
        try:
            data = json.loads(EXTRACTED_LINKS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            return {}
    return {}


def save_checkpoint(visited, queue, extracted_links):
    """Единый чекпоинт: visited + frontier (очередь) + извлечённые ссылки.

    Вызывается после КАЖДОЙ страницы, поэтому kill теряет максимум текущую
    страницу, а не последние N (раньше чекпоинт был раз в 5 страниц).
    """
    save_visited(visited)
    _atomic_write_json(FRONTIER_FILE, [[u, d] for (u, d) in queue])
    _atomic_write_json(EXTRACTED_LINKS_FILE, extracted_links)


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


def _host_of(url: str) -> str:
    return urlsplit(url).netloc.lower()


def same_host(url: str, base: str) -> bool:
    """True, если url на том же хосте, что base.

    Через urlparse, а не startswith: startswith(TENANT_URL) пропускал
    fooguu84124.live.dynatrace.com.evil.com (граница хоста не проверялась).
    """
    return bool(_host_of(url)) and _host_of(url) == _host_of(base)


def should_skip_url(url: str) -> bool:
    if not same_host(url, TENANT_URL):
        return True
    return any(p.search(url) for p in SKIP_PATTERNS)


def normalize_url(url: str) -> str:
    """Канонизировать URL для дедупа.

    Отбрасываем фрагмент (#...) И query-строку (?gtf=-2h и т.п.): в UI это
    транзиентные фильтры времени/состояния, из-за которых одна и та же страница
    попадала во фронтир многократно как «разные» URL.
    """
    parts = urlsplit(url)
    cleaned = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return cleaned.rstrip("/")


def _url_hash(url: str, length: int = 8) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:length]


def unique_filename(title_slug: str, url: str, ext: str) -> str:
    """Имя файла скриншота/HTML с коротким хэшем URL.

    Раньше файлы звались только по slugify(title): две разные страницы с
    одинаковым <title> (частое в SPA) молча перезаписывали друг друга. Хэш URL
    делает имя уникальным на URL.
    """
    return f"{title_slug}-{_url_hash(url)}{ext}"


# ---------- frontier (BFS): чистая логика, тестируется без браузера ----------

def is_crawlable_link(url: str) -> bool:
    """Ссылка достойна фронтира: тот же хост, не skip-паттерн, в /ui/ или /apps/."""
    return not should_skip_url(url) and ("/ui/" in url or "/apps/" in url)


def build_initial_frontier(seeds, restored_frontier, visited):
    """Собрать стартовую очередь.

    Приоритет: восстановленный из чекпоинта фронтир. Если он пуст (первый
    запуск или битый файл), берём seeds на depth=0. Уже посещённые URL в
    очередь не кладём.
    """
    queue: list[tuple[str, int]] = []
    in_queue: set[str] = set()

    source = restored_frontier if restored_frontier else [(normalize_url(u), 0) for u in seeds]
    for url, depth in source:
        clean = normalize_url(url)
        if clean and clean not in visited and clean not in in_queue:
            queue.append((clean, depth))
            in_queue.add(clean)
    return queue, in_queue


def enqueue_links(links, depth, max_depth, visited, in_queue, queue):
    """Добавить исходящие ссылки во фронтир (BFS), с дедупом.

    Мутирует queue и in_queue на месте. Возвращает число реально добавленных.
    Вынесено из главного цикла, чтобы покрыть дедуп юнит-тестом.
    """
    if depth >= max_depth:
        return 0
    added = 0
    for link in links:
        clean = normalize_url(link)
        if (
            clean
            and clean not in visited
            and clean not in in_queue
            and is_crawlable_link(clean)
        ):
            queue.append((clean, depth + 1))
            in_queue.add(clean)
            added += 1
    return added


# ---------- capture ----------

async def capture_page(page, url: str, depth: int, folder: str, extra_meta: dict | None = None):
    title = (await page.title()) or "untitled"
    title_slug = slugify(title)

    sc_dir = OUT / "screenshots" / folder
    sc_dir.mkdir(parents=True, exist_ok=True)
    sc_path = sc_dir / unique_filename(title_slug, url, ".png")

    html_dir = OUT / "pages" / folder
    html_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / unique_filename(title_slug, url, ".html")

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

def acquire_single_instance_lock():
    """Межпроцессный lock через fcntl.flock.

    Два параллельных краулера гонялись на visited.json / pages.jsonl / чекпоинтах
    (дубли, битый state). Держим эксклюзивный lock на весь прогон; хэндл файла
    возвращаем наружу, чтобы он жил до конца процесса.
    """
    if fcntl is None:  # pragma: no cover - Windows
        return None
    fh = open(LOCK_FILE, "w")
    try:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as e:
        fh.close()
        if e.errno in (errno.EACCES, errno.EAGAIN):
            log(f"ERROR: another crawler is already running (lock held on {LOCK_FILE}).")
            sys.exit(3)
        raise
    fh.write(f"{os.getpid()}\n")
    fh.flush()
    return fh


async def crawl(mode: str, section: str | None, headless: bool):
    if async_playwright is None:
        log("ERROR: playwright is not installed. Run: pip install -r requirements.txt && playwright install chromium")
        sys.exit(2)
    if not STATE_FILE.exists():
        log(f"ERROR: storage state missing at {STATE_FILE}. Run: python auth.py")
        sys.exit(2)

    lock_handle = acquire_single_instance_lock()

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
    restored_frontier = load_frontier()
    extracted_links = load_extracted_links()
    nav_wait = CONFIG["crawl"]["navigation_wait_ms"]
    page_timeout = CONFIG["crawl"]["page_timeout_ms"]
    vw = CONFIG["crawl"]["viewport_width"]
    vh = CONFIG["crawl"]["viewport_height"]

    queue, in_queue = build_initial_frontier(seeds, restored_frontier, visited)
    if restored_frontier:
        log(f"Restored frontier with {len(queue)} pages from checkpoint (visited={len(visited)})")

    retries: dict[str, int] = {}

    log(f"start: mode={mode} headless={headless} max_pages={max_pages} already_visited={len(visited)} frontier={len(queue)} seeds={len(seeds)}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            storage_state=str(STATE_FILE),
            viewport={"width": vw, "height": vh},
        )
        page = await context.new_page()

        crawled = 0
        errors = 0

        while queue and crawled < max_pages:
            url, depth = queue.pop(0)
            in_queue.discard(url)
            if url in visited or should_skip_url(url):
                # Пропуск ничего не добавляет во фронтир, чекпоинт не нужен:
                # при рестарте такой URL просто повторно отсеется (идемпотентно).
                continue

            try:
                log(f"[{crawled+1}] depth={depth} {url}")
                response = await page.goto(url, wait_until="domcontentloaded", timeout=page_timeout)
                http_status = response.status if response is not None else None
                await page.wait_for_timeout(nav_wait)
                # extra wait for Angular/SPA settle
                try:
                    await page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass

                folder = url_to_folder(page.url)  # use ACTUAL URL (after redirects)
                links = await capture_page(
                    page, page.url, depth, folder, extra_meta={"http_status": http_status}
                )
                visited.add(url)
                visited.add(normalize_url(page.url))
                crawled += 1

                # Персистим исходящие ссылки страницы (раньше в pages.jsonl был
                # только links_count, восстановить фронтир было нельзя).
                extracted_links[url] = links
                enqueue_links(links, depth, max_depth, visited, in_queue, queue)

                # Чекпоинт после КАЖДОЙ страницы: visited + очередь + ссылки.
                save_checkpoint(visited, queue, extracted_links)

            except Exception as e:
                errors += 1
                log(f"  ERROR: {type(e).__name__}: {str(e)[:200]}")
                # Ретрай: вернуть URL в конец очереди до MAX_RETRIES раз, чтобы
                # временный сбой (таймаут/сеть) не терял страницу навсегда.
                attempts = retries.get(url, 0)
                if attempts < MAX_RETRIES:
                    retries[url] = attempts + 1
                    queue.append((url, depth))
                    in_queue.add(url)
                    log(f"  retry scheduled ({retries[url]}/{MAX_RETRIES}) for {url}")
                else:
                    log(f"  giving up on {url} after {MAX_RETRIES} retries")
                save_checkpoint(visited, queue, extracted_links)

        save_checkpoint(visited, queue, extracted_links)
        await browser.close()
        log(f"done. crawled={crawled} errors={errors} total_visited={len(visited)} queue_remaining={len(queue)}")
    if lock_handle is not None:
        lock_handle.close()


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
