"""
link_check.py — проверяет что все внешние URL в explanations/*.md отвечают 200 OK.

Блокирует сборку если найден broken link. Кэш (7 дней) в .link_check_cache.json,
чтобы не дёргать сеть на каждом rebuild.

Usage:
    python scripts/link_check.py                  # human-readable
    python scripts/link_check.py --json           # machine-readable
    python scripts/link_check.py --no-cache       # игнор кэша, проверить всё заново
    python scripts/link_check.py --allowlist URL  # пометить URL как known-good
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EXPLANATIONS = ROOT / "explanations"
CACHE_FILE = ROOT / ".link_check_cache.json"
CACHE_TTL_SEC = 7 * 24 * 3600  # 7 дней

# URL pattern: markdown-link (...)(url), bare https://, inline-code `docs.dynatrace.com/...`
URL_PATTERNS = [
    re.compile(r"\]\((https?://[^\s)]+)\)"),            # [text](https://...)
    re.compile(r"(?<![(\w])(https?://[^\s`\)>]+)"),     # bare https://...
    re.compile(r"`(docs\.dynatrace\.com/[^\s`]+)`"),    # `docs.dynatrace.com/...` inline code
]

# URL, которые не нужно проверять (placeholder'ы / illustrative / auth-walled)
SKIP_PATTERNS = [
    re.compile(r"[<>{}]"),                              # <P-NNN>, {{var}} — template placeholders
    re.compile(r"\bexample\.(com|org|net)\b"),          # RFC 2606 reserved: illustrative
    re.compile(r"\*"),                                  # wildcard в path/host
    re.compile(r"^https?://<"),                         # "<наш-кластер>" etc.
    re.compile(r"\bguu84124\.live\.dynatrace\.com"),    # captured-tenant — auth-required, пропускать
    re.compile(r"\bcustomers\.dynatrace\.com"),         # customer portal — auth-required
]


@dataclass
class LinkCheckResult:
    url: str
    status: int  # HTTP status или 0 при URLError
    ok: bool
    error: str = ""
    sources: list[str] = None  # where this URL is used: file:line


def load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        # Prune stale entries
        now = time.time()
        return {url: e for url, e in data.items() if now - e.get("ts", 0) < CACHE_TTL_SEC}
    except Exception:
        return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def is_skipped(url: str) -> bool:
    return any(rx.search(url) for rx in SKIP_PATTERNS)


def extract_urls() -> dict[str, list[str]]:
    """Вернуть {url: [file:line, ...]} по всем explanations/*.md, исключая placeholder'ы."""
    out: dict[str, list[str]] = {}
    for md in sorted(EXPLANATIONS.rglob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        text = md.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for rx in URL_PATTERNS:
                for m in rx.finditer(line):
                    url = m.group(1)
                    if not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    url = url.rstrip(".,;:!?)")
                    if is_skipped(url):
                        continue
                    out.setdefault(url, []).append(f"{rel}:{lineno}")
    return out


def check_one(url: str, timeout: float = 10.0) -> tuple[int, str]:
    """Вернёт (status_code, error_message). status=0 при сетевой ошибке."""
    try:
        req = Request(url, method="HEAD", headers={
            "User-Agent": "Mozilla/5.0 (dt-crawler link_check)",
            "Accept": "*/*",
        })
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, ""
    except HTTPError as e:
        # Некоторые сервера не любят HEAD — попробуем GET для пограничных случаев
        if e.code in (405, 403, 400):
            try:
                req = Request(url, method="GET", headers={
                    "User-Agent": "Mozilla/5.0 (dt-crawler link_check)",
                    "Accept": "text/html,*/*",
                })
                with urlopen(req, timeout=timeout) as resp:
                    return resp.status, ""
            except HTTPError as e2:
                return e2.code, str(e2)
            except URLError as e2:
                return 0, str(e2.reason)
        return e.code, str(e)
    except URLError as e:
        return 0, str(e.reason)
    except Exception as e:
        return 0, str(e)


def main() -> int:
    ap = argparse.ArgumentParser(description="Link checker for dt-crawler explanations.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--allowlist", nargs="+", default=[], help="URL(s) to mark as known-good without checking")
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()

    url_to_sources = extract_urls()
    if not url_to_sources:
        print("✅ 0 URL в explanations — нечего проверять.")
        return 0

    cache = {} if args.no_cache else load_cache()
    results: list[LinkCheckResult] = []

    for allow in args.allowlist:
        cache[allow] = {"status": 200, "ok": True, "ts": time.time(), "allowlisted": True}

    total = len(url_to_sources)
    print(f"→ link_check: {total} уникальных URL…")

    for i, (url, sources) in enumerate(sorted(url_to_sources.items()), start=1):
        if url in cache:
            entry = cache[url]
            results.append(LinkCheckResult(
                url=url, status=entry["status"], ok=entry["ok"],
                error=entry.get("error", ""), sources=sources,
            ))
            continue

        status, err = check_one(url, args.timeout)
        ok = 200 <= status < 400
        print(f"  [{i}/{total}] {status or 'ERR'} {url}")
        cache[url] = {"status": status, "ok": ok, "error": err, "ts": time.time()}
        results.append(LinkCheckResult(
            url=url, status=status, ok=ok, error=err, sources=sources,
        ))

    save_cache(cache)

    broken = [r for r in results if not r.ok]

    if args.json:
        payload = {
            "total": len(results),
            "broken": len(broken),
            "results": [asdict(r) for r in results],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print()
        if not broken:
            print(f"✅ {len(results)} URL — все 200 OK.")
        else:
            print(f"❌ {len(broken)} broken из {len(results)}:\n")
            for r in broken:
                print(f"  ❌ [{r.status or 'NET-ERR'}] {r.url}")
                if r.error:
                    print(f"     error: {r.error[:140]}")
                for src in r.sources[:3]:
                    print(f"     used in: {src}")
                if len(r.sources) > 3:
                    print(f"     ... и ещё {len(r.sources) - 3} мест")
                print()

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
