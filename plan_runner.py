"""
Crawl Dynatrace по study_plan.yaml — точечно по темам учебного плана.

Usage:
    python plan_runner.py                  # все дни
    python plan_runner.py --day day-1      # только день 1
    python plan_runner.py --day day-3-4    # только дни 3-4
    python plan_runner.py --headed         # с открытым браузером
"""
import os
import sys
import asyncio
import argparse
from pathlib import Path
import yaml
from playwright.async_api import async_playwright

from crawler import (
    TENANT_URL, STATE_FILE, CONFIG, OUT, LOGS, ROOT,
    capture_page, log, load_visited, save_visited,
    should_skip_url, normalize_url, url_to_folder,
)

PLAN_FILE = ROOT / "study_plan.yaml"


def load_plan():
    return yaml.safe_load(PLAN_FILE.read_text(encoding="utf-8"))


async def crawl_plan(day_filter: str | None = None, headless: bool = True):
    if not STATE_FILE.exists():
        log(f"ERROR: storage state missing at {STATE_FILE}. Run: python auth.py")
        sys.exit(2)

    plan = load_plan()
    days = plan["days"]
    if day_filter:
        days = [d for d in days if d["id"] == day_filter]
        if not days:
            log(f"ERROR: day '{day_filter}' not found in plan. Available: {[d['id'] for d in plan['days']]}")
            sys.exit(2)

    # Build flat task list: (day, topic, route)
    tasks = []
    for d in days:
        for t in d["topics"]:
            for r in t.get("routes", []):
                tasks.append({
                    "day_id": d["id"],
                    "day_title": d["title"],
                    "topic_id": t["id"],
                    "topic_name": t["name"],
                    "topic_kind": t.get("kind", "live"),
                    "topic_notes": t.get("notes", ""),
                    "route": r.strip(),
                })

    log(f"=== plan crawl ===  days={len(days)}  tasks={len(tasks)}")

    visited = load_visited()
    nav_wait = CONFIG["crawl"]["navigation_wait_ms"]
    page_timeout = CONFIG["crawl"]["page_timeout_ms"]
    vw = CONFIG["crawl"]["viewport_width"]
    vh = CONFIG["crawl"]["viewport_height"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            storage_state=str(STATE_FILE),
            viewport={"width": vw, "height": vh},
        )
        page = await context.new_page()

        crawled = 0
        errors = 0
        skipped = 0

        for i, task in enumerate(tasks, 1):
            url = TENANT_URL + task["route"]
            url = normalize_url(url)
            if should_skip_url(url):
                skipped += 1
                continue
            # NB: don't skip if visited — same URL may be referenced from multiple topics,
            #     we need a copy of the record per topic for docs.
            try:
                log(f"[{i}/{len(tasks)}] {task['day_id']} / {task['topic_id']}  ->  {task['route']}")
                await page.goto(url, wait_until="domcontentloaded", timeout=page_timeout)
                await page.wait_for_timeout(nav_wait)
                try:
                    await page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass

                folder = f"{task['day_id']}/{task['topic_id']}/{url_to_folder(page.url)}"
                meta = {
                    "day_id": task["day_id"],
                    "day_title": task["day_title"],
                    "topic_id": task["topic_id"],
                    "topic_name": task["topic_name"],
                    "topic_kind": task["topic_kind"],
                    "topic_notes": task["topic_notes"],
                    "plan_route": task["route"],
                    "source": "plan",
                }
                await capture_page(page, page.url, 0, folder, extra_meta=meta)
                visited.add(url)
                crawled += 1

                if crawled % 5 == 0:
                    save_visited(visited)
            except Exception as e:
                errors += 1
                log(f"  ERROR: {type(e).__name__}: {str(e)[:200]}")

        save_visited(visited)
        await browser.close()
        log(f"=== done ===  crawled={crawled}  errors={errors}  skipped={skipped}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", help="day-1 / day-2 / day-3-4 / day-5 — пропустить чтобы крутить все")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()
    asyncio.run(crawl_plan(day_filter=args.day, headless=not args.headed))


if __name__ == "__main__":
    main()
