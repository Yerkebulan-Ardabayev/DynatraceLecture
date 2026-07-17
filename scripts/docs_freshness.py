"""
docs_freshness.py — автообновление информации курса по официальной документации.

Следит за страницами docs.dynatrace.com, на которые ссылаются explanations/*.md.
Когда основной текст страницы меняется:
  1) находит темы курса, цитирующие этот URL;
  2) через claude -p (подписка, Sonnet) решает, устарело ли утверждение курса;
  3) применяет минимальные правки: качественный русский, ровно в месте старого
     утверждения, числа только из новой версии доки, без длинных тире;
  4) гейт scripts/quality_check.py --cards; при провале правки запуска откатываются;
  5) пересборка v1+v2 и отчёт output/freshness_report.md + уведомление.

Первый запуск лишь снимает базовую линию (без LLM и без правок).
Правки НЕ коммитятся: git остаётся за владельцем (git-controller пушит только
уже закоммиченное, поэтому автоправки в рабочем дереве безопасны).

Usage:
    python scripts/docs_freshness.py                 # полный цикл (для launchd)
    python scripts/docs_freshness.py --dry-run       # только дифф-отчёт, без LLM и правок
    python scripts/docs_freshness.py --no-llm        # зафиксировать диффы в отчёт, не править
    python scripts/docs_freshness.py --limit N       # не больше N URL (смоук)
    python scripts/docs_freshness.py --url SUBSTR    # только URL, содержащие подстроку
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_check  # noqa: E402  (переиспользуем extract_urls)

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
TEXTS_DIR = STATE_DIR / "docs_texts"
BAK_DIR = STATE_DIR / "freshness_bak"
SNAPSHOT_FILE = STATE_DIR / "docs_snapshot.json"
MANUAL_FILE = STATE_DIR / "freshness_manual.json"
LOCK_FILE = STATE_DIR / "freshness.lock"
REPORT_FILE = ROOT / "output" / "freshness_report.md"
ARCHIVE_DIR = ROOT / "logs" / "freshness"
STORAGE_STATE = STATE_DIR / "storage_state.json"

WATCH_HOSTS = ("docs.dynatrace.com",)   # следим только за официальной документацией
MAX_LLM_PER_RUN = 12                    # защита от всплеска: остальное в следующий запуск
MAX_ATTEMPTS_PER_DIFF = 2               # после двух неудачных LLM-попыток — в ручной разбор
FETCH_TIMEOUT = 25.0
CLAUDE_TIMEOUT = 600
CLAUDE_MODEL = "sonnet"                 # фоновые LLM-задачи = Sonnet (политика маршрутизации)
DIFF_MAX_CHARS = 9000
EM_DASH = "—"

DIGIT_TOKEN_RE = re.compile(r"\d+(?:[.,]\d+)?")


def log(msg: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


# ---------------------------------------------------------------- lock

def acquire_lock() -> bool:
    STATE_DIR.mkdir(exist_ok=True)
    if LOCK_FILE.exists():
        try:
            data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            age = time.time() - data.get("ts", 0)
            if age < 2 * 3600:
                log(f"lock занят (pid={data.get('pid')}, {int(age)}s) — выхожу")
                return False
            log("lock протух (>2ч) — перехватываю")
        except Exception:
            pass
    LOCK_FILE.write_text(json.dumps({"pid": os.getpid(), "ts": time.time()}), encoding="utf-8")
    return True


def release_lock() -> None:
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except OSError:
        pass


# ---------------------------------------------------------------- fetch + extract

def fetch_html(url: str) -> tuple[int, str]:
    """GET страницы. Возвращает (status, html); status=0 при сетевой ошибке."""
    last_err = ""
    for attempt in (1, 2):
        try:
            req = Request(url, method="GET", headers={
                "User-Agent": "Mozilla/5.0 (dt-crawler docs_freshness)",
                "Accept": "text/html,*/*",
            })
            with urlopen(req, timeout=FETCH_TIMEOUT) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                return resp.status, raw.decode(charset, errors="replace")
        except HTTPError as e:
            return e.code, ""
        except (URLError, OSError) as e:
            last_err = str(e)
            time.sleep(1.5 * attempt)
    log(f"  сеть: {url} — {last_err[:120]}")
    return 0, ""


def extract_main_text(html: str) -> str:
    """Основной текст страницы: <main>/<article>, без навигации и скриптов."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "header", "footer",
                     "aside", "svg", "button", "form"]):
        tag.decompose()
    node = soup.find("main") or soup.find("article") or soup.body or soup
    lines = []
    for raw in node.get_text("\n").splitlines():
        s = " ".join(raw.split())
        if not s:
            continue
        # служебные строки, меняющиеся без смысла для контента
        if re.match(r"^(Was this page helpful|Last updated|Feedback|Table of contents)\b", s, re.I):
            continue
        lines.append(s)
    return "\n".join(lines)


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def unified_diff(old: str, new: str, max_chars: int = DIFF_MAX_CHARS) -> str:
    diff = "\n".join(difflib.unified_diff(
        old.splitlines(), new.splitlines(),
        fromfile="старая версия", tofile="новая версия", lineterm="", n=6,
    ))
    if len(diff) > max_chars:
        diff = diff[:max_chars] + "\n… (дифф обрезан)"
    return diff


# ---------------------------------------------------------------- snapshot

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path)


def store_text(text: str, sha: str) -> str:
    TEXTS_DIR.mkdir(parents=True, exist_ok=True)
    name = sha[:16] + ".txt"
    p = TEXTS_DIR / name
    if not p.exists():
        p.write_text(text, encoding="utf-8")
    return name


def prune_texts(snapshot: dict) -> None:
    """Убрать тексты, на которые снапшот больше не ссылается."""
    if not TEXTS_DIR.is_dir():
        return
    keep = {e.get("text_file") for e in snapshot.values()}
    for p in TEXTS_DIR.iterdir():
        if p.name not in keep:
            p.unlink(missing_ok=True)


# ---------------------------------------------------------------- LLM

def find_claude() -> str | None:
    cand = shutil.which("claude")
    if cand:
        return cand
    fallback = Path.home() / ".local" / "bin" / "claude"
    return str(fallback) if fallback.exists() else None


PROMPT_TEMPLATE = """Ты обновляешь русскоязычный обучающий курс «Dynatrace Managed (закрытый контур, air-gapped) для инженеров банка». Официальная страница документации изменилась. Определи, затрагивает ли изменение утверждения курса, ссылающиеся на эту страницу, и если да, дай МИНИМАЛЬНЫЕ правки.

ЖЁСТКИЕ ПРАВИЛА:
1. Правь только то, что противоречит новой версии документации. Стиль, структуру и объём не трогай.
2. Числа и факты в новом тексте бери ТОЛЬКО из новой версии страницы. Ничего не выдумывай.
3. Пиши естественным русским, тем же тоном и в том же месте, где стояло старое утверждение. Дословные английские цитаты UI (заголовки экранов, кнопки, пути в меню) и названия фич НЕ переводи.
4. НИКОГДА не используй длинное тире «—»: заменяй запятой, двоеточием или скобками.
5. Курс только про Managed: SaaS-функции (DQL, Grail, Notebooks, Workflows, Apps) можно упоминать только как «есть в SaaS, в Managed недоступно».
6. Если дока добавила новый важный факт, которого в курсе не было, НЕ вставляй его в текст: опиши его в поле "new_fact_proposal" (иначе оставь это поле null).
7. Если изменение страницы не затрагивает утверждения этого файла, верни verdict "no_impact" и пустой список edits.

URL: {url}

ДИФФ СТРАНИЦЫ (унифицированный, старое → новое):
{diff}

ФАЙЛ КУРСА {relpath} (полностью):
<<<FILE
{file_text}
FILE>>>
{card_block}
ОТВЕТ: строго один JSON-объект, без пояснений и без markdown-ограждений:
{{"verdict":"update"|"no_impact","edits":[{{"file":"{relpath}","old":"<точный фрагмент из файла>","new":"<замена>","reason":"<1 фраза>"}}],"summary":"<1-2 фразы: что изменилось в доке и что сделано>","new_fact_proposal":null}}
Поле "old" обязано встречаться в файле ровно один раз: копируй его посимвольно, включая пробелы."""


def call_claude(prompt: str, claude_bin: str) -> tuple[dict | None, str]:
    """Вернёт (parsed_json | None, raw_output). Оба потока в лог (причина ошибки в stdout)."""
    try:
        p = subprocess.run(
            [claude_bin, "-p", "--model", CLAUDE_MODEL],
            input=prompt, capture_output=True, text=True, timeout=CLAUDE_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None, "timeout"
    raw = (p.stdout or "") + (("\nSTDERR: " + p.stderr) if p.stderr.strip() else "")
    if p.returncode != 0:
        return None, f"rc={p.returncode}: {raw[:800]}"
    m = re.search(r"\{.*\}", p.stdout, re.S)
    if not m:
        return None, raw[:800]
    try:
        return json.loads(m.group(0)), raw
    except json.JSONDecodeError as e:
        return None, f"json: {e}: {raw[:800]}"


# ---------------------------------------------------------------- edits

ALLOWED_PREFIXES = ("explanations/", "cards/")


def validate_edit(edit: dict, new_page_text: str) -> tuple[bool, str]:
    """Детеминированный предохранитель поверх LLM-вывода."""
    rel = edit.get("file", "")
    old, new = edit.get("old", ""), edit.get("new", "")
    if not rel.startswith(ALLOWED_PREFIXES) or ".." in rel:
        return False, f"файл вне разрешённых папок: {rel}"
    path = ROOT / rel
    if not path.is_file():
        return False, f"файла нет: {rel}"
    if not old or not new or old == new:
        return False, "пустая или тождественная правка"
    if EM_DASH in new:
        return False, "длинное тире в новом тексте"
    content = path.read_text(encoding="utf-8")
    n = content.count(old)
    if n != 1:
        return False, f"old встречается {n} раз (нужно ровно 1)"
    # каждая цифра нового текста обязана существовать в новой доке либо в старом фрагменте
    page_tokens = set(DIGIT_TOKEN_RE.findall(new_page_text))
    old_tokens = set(DIGIT_TOKEN_RE.findall(old))
    for tok in DIGIT_TOKEN_RE.findall(new):
        if tok not in page_tokens and tok not in old_tokens:
            return False, f"цифра «{tok}» отсутствует и в новой доке, и в старом фрагменте"
    return True, ""


def apply_edit(edit: dict, run_id: str) -> None:
    rel = edit["file"]
    path = ROOT / rel
    bak = BAK_DIR / run_id / rel
    if not bak.exists():
        bak.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, bak)
    content = path.read_text(encoding="utf-8")
    path.write_text(content.replace(edit["old"], edit["new"], 1), encoding="utf-8")


def rollback_run(run_id: str) -> list[str]:
    """Вернуть файлы к состоянию до этого запуска (ручные правки владельца в них сохраняются,
    потому что бэкап снимался с диска непосредственно перед нашей правкой)."""
    restored = []
    base = BAK_DIR / run_id
    if not base.is_dir():
        return restored
    for bak in base.rglob("*.md"):
        rel = bak.relative_to(base)
        shutil.copy2(bak, ROOT / rel)
        restored.append(str(rel))
    return restored


def card_for(rel: str) -> Path | None:
    """explanations/day-X/topic.md → cards/day-X/topic.md (если есть)."""
    p = Path(rel)
    if len(p.parts) == 3 and p.parts[0] == "explanations":
        c = ROOT / "cards" / p.parts[1] / p.parts[2]
        if c.is_file():
            return c
    return None


# ---------------------------------------------------------------- gates + build

def run_gate() -> tuple[bool, str]:
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "quality_check.py"), "--cards"],
                       capture_output=True, text=True, cwd=ROOT, timeout=300)
    out = (p.stdout + p.stderr).strip()
    return p.returncode == 0, out[-1500:]


def rebuild() -> tuple[bool, str]:
    msgs = []
    for args in ([], ["--v2"]):
        p = subprocess.run([sys.executable, str(ROOT / "plan_html.py"), *args],
                           capture_output=True, text=True, cwd=ROOT, timeout=600)
        tail = (p.stdout + p.stderr).strip()[-400:]
        msgs.append(f"plan_html.py {' '.join(args) or '(v1)'}: rc={p.returncode}\n{tail}")
        if p.returncode != 0:
            return False, "\n".join(msgs)
    return True, "\n".join(msgs)


def run_drift() -> str:
    """Дрейф живого тенанта, только если есть свежая сессия (< 20 часов)."""
    if not STORAGE_STATE.exists():
        return "пропущен: нет живой сессии тенанта (python auth.py --manual)"
    age_h = (time.time() - STORAGE_STATE.stat().st_mtime) / 3600
    if age_h > 20:
        return f"пропущен: сессия старше 20 ч ({age_h:.0f} ч), перелогинься: python auth.py --manual"
    try:
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "drift_report.py")],
                           capture_output=True, text=True, cwd=ROOT, timeout=1800)
        tail = (p.stdout + p.stderr).strip()[-600:]
        verdict = {0: "дрейфа нет", 1: "ЕСТЬ ДРЕЙФ, см. drift_report.md", 2: "ошибка прогона"}
        return f"{verdict.get(p.returncode, f'rc={p.returncode}')}\n{tail}"
    except subprocess.TimeoutExpired:
        return "прерван по таймауту 30 мин"


# ---------------------------------------------------------------- notify

def notify(title: str, message: str) -> None:
    try:
        subprocess.run(["osascript", "-e",
                        f'display notification "{message[:180]}" with title "{title}"'],
                       capture_output=True, timeout=10)
    except Exception:
        pass
    tok, chat = os.environ.get("FRESHNESS_TG_TOKEN"), os.environ.get("FRESHNESS_TG_CHAT")
    if not (tok and chat):  # опционально: ключи можно положить в .env проекта
        env = load_env()
        tok, chat = env.get("FRESHNESS_TG_TOKEN"), env.get("FRESHNESS_TG_CHAT")
    if tok and chat:
        try:
            import urllib.parse
            data = urllib.parse.urlencode({"chat_id": chat, "text": f"{title}\n{message[:3500]}"}).encode()
            urlopen(Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=data), timeout=15)
        except Exception as e:
            log(f"telegram не отправился: {e}")


def load_env() -> dict:
    env = {}
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Автообновление курса по официальной документации.")
    ap.add_argument("--dry-run", action="store_true", help="без LLM и правок, только дифф")
    ap.add_argument("--no-llm", action="store_true", help="диффы в отчёт, файлы не править")
    ap.add_argument("--limit", type=int, default=0, help="обработать не больше N URL")
    ap.add_argument("--url", default="", help="только URL с этой подстрокой")
    ap.add_argument("--no-drift", action="store_true", help="не запускать тенант-дрейф")
    args = ap.parse_args()

    if not acquire_lock():
        return 0
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        return run_cycle(args, run_id)
    finally:
        release_lock()


def run_cycle(args, run_id: str) -> int:
    started = datetime.now()
    url_map = {u: srcs for u, srcs in link_check.extract_urls().items()
               if any(h in u for h in WATCH_HOSTS)}
    if args.url:
        url_map = {u: s for u, s in url_map.items() if args.url in u}
    urls = sorted(url_map)
    if args.limit:
        dropped = max(0, len(urls) - args.limit)
        urls = urls[: args.limit]
        if dropped:
            log(f"--limit: пропускаю {dropped} URL (обработаются в следующий запуск)")

    snapshot = load_json(SNAPSHOT_FILE)
    manual = load_json(MANUAL_FILE)
    claude_bin = None
    baseline_mode = not snapshot  # самый первый запуск: только базовая линия

    stats = {"same": 0, "new": 0, "changed": 0, "net_err": 0, "http_err": 0}
    changed_entries = []   # для отчёта
    applied_edits = []     # [{file, reason, url}]
    proposals = []         # summary с новыми фактами
    llm_used = 0

    log(f"старт run={run_id} URL={len(urls)} baseline={baseline_mode} "
        f"dry_run={args.dry_run} no_llm={args.no_llm}")

    for url in urls:
        status, html = fetch_html(url)
        entry = snapshot.get(url, {})
        if status == 0:
            stats["net_err"] += 1
            continue
        if status >= 400:
            stats["http_err"] += 1
            entry["fail_count"] = entry.get("fail_count", 0) + 1
            snapshot[url] = entry
            changed_entries.append({"url": url, "kind": f"HTTP {status} (подряд: {entry['fail_count']})",
                                    "files": url_map[url], "action": "проверить ссылку-источник"})
            continue

        text = extract_main_text(html)
        sha = text_sha(text)
        entry.pop("fail_count", None)

        if not entry:  # новый URL
            snapshot[url] = {"sha": sha, "text_file": store_text(text, sha),
                             "fetched_at": started.isoformat(timespec="seconds")}
            stats["new"] += 1
            continue
        if entry.get("sha") == sha:
            stats["same"] += 1
            snapshot[url] = entry
            continue

        # --- страница изменилась ---
        stats["changed"] += 1
        old_text = ""
        old_file = TEXTS_DIR / entry.get("text_file", "")
        if old_file.is_file():
            old_text = old_file.read_text(encoding="utf-8")
        diff = unified_diff(old_text, text)
        files = sorted({s.split(":")[0] for s in url_map[url]})
        rec = {"url": url, "kind": "изменилась", "files": files, "action": "", "summary": ""}

        if args.dry_run or args.no_llm:
            rec["action"] = "правки не выполнялись (режим без LLM)"
            changed_entries.append(rec)
            continue  # снапшот НЕ обновляем: обработаем в боевом запуске

        diff_key = f"{url}#{sha}"
        attempts = entry.get("attempts", {}).get(diff_key, 0)
        if attempts >= MAX_ATTEMPTS_PER_DIFF:
            rec["action"] = "в ручной разбор (2 неудачные LLM-попытки)"
            manual[diff_key] = {"url": url, "files": files, "diff": diff[:4000],
                                "added": started.isoformat(timespec="seconds")}
            snapshot[url] = {"sha": sha, "text_file": store_text(text, sha),
                             "fetched_at": started.isoformat(timespec="seconds")}
            changed_entries.append(rec)
            continue
        if llm_used >= MAX_LLM_PER_RUN:
            rec["action"] = f"отложено: лимит {MAX_LLM_PER_RUN} LLM-вызовов за запуск"
            changed_entries.append(rec)
            continue  # снапшот не трогаем — вернёмся в следующий запуск

        if claude_bin is None:
            claude_bin = find_claude()
            if not claude_bin:
                log("claude CLI не найден: правки невозможны, только отчёт")
        ok_all = True
        deferred = False
        summaries = []
        if claude_bin:
            for rel in files:
                fpath = ROOT / rel
                if not fpath.is_file():
                    continue
                if llm_used >= MAX_LLM_PER_RUN:
                    deferred = True  # бюджет LLM исчерпан посреди URL: дообработаем в следующий запуск
                    break
                card = card_for(rel)
                card_block = ""
                if card:
                    card_rel = card.relative_to(ROOT).as_posix()
                    card_block = (f"\nКАРТОЧКА ЛЕКТОРА {card_rel} (полностью; если правишь цифру "
                                  f"в explanation, поправь и карточку, если она цитирует эту цифру):\n"
                                  f"<<<CARD\n{card.read_text(encoding='utf-8')}\nCARD>>>\n")
                prompt = PROMPT_TEMPLATE.format(url=url, diff=diff, relpath=rel,
                                                file_text=fpath.read_text(encoding="utf-8"),
                                                card_block=card_block)
                llm_used += 1
                parsed, raw = call_claude(prompt, claude_bin)
                if parsed is None:
                    log(f"  LLM не ответил валидно по {rel}: {raw[:200]}")
                    ok_all = False
                    continue
                verdict = parsed.get("verdict")
                s = str(parsed.get("summary") or "")
                if s and s not in summaries:
                    summaries.append(s)
                if parsed.get("new_fact_proposal"):
                    p = f"{url}: {parsed['new_fact_proposal']}"
                    if p not in proposals:
                        proposals.append(p)
                if verdict == "no_impact":
                    continue
                for edit in parsed.get("edits", []):
                    valid, why = validate_edit(edit, text)
                    if not valid:
                        log(f"  правка отклонена ({rel}): {why}")
                        ok_all = False
                        continue
                    apply_edit(edit, run_id)
                    applied_edits.append({"file": edit["file"], "reason": edit.get("reason", ""),
                                          "url": url})
        else:
            ok_all = False

        rec["summary"] = " | ".join(summaries)[:400]
        if deferred:
            snapshot[url] = entry  # sha старый, попытки не тратим: дообработаем в следующий запуск
            rec["action"] = "отложено: исчерпан бюджет LLM этого запуска"
        elif ok_all:
            snapshot[url] = {"sha": sha, "text_file": store_text(text, sha),
                             "fetched_at": started.isoformat(timespec="seconds")}
            rec["action"] = "обработано"
        else:
            att = entry.setdefault("attempts", {})
            att[diff_key] = attempts + 1
            snapshot[url] = entry  # sha старый: повторим в следующий запуск
            rec["action"] = f"частично, попытка {attempts + 1}/{MAX_ATTEMPTS_PER_DIFF}"
        changed_entries.append(rec)
        time.sleep(0.3)  # вежливость к docs-сайту

    # --- гейты и пересборка (только если что-то правили) ---
    gate_line = "не требовался (правок нет)"
    build_line = "не требовалась"
    if applied_edits:
        ok, out = run_gate()
        if ok:
            gate_line = "PASS (quality_check --cards: 0 errors)"
            built, bout = rebuild()
            build_line = ("OK\n" + bout) if built else ("FAIL\n" + bout)
        else:
            restored = rollback_run(run_id)
            gate_line = f"FAIL → откат {len(restored)} файлов. Вывод гейта:\n{out}"
            build_line = "пропущена (гейт не прошёл)"
            manual[f"gate-fail-{run_id}"] = {
                "files": [e["file"] for e in applied_edits],
                "urls": sorted({e["url"] for e in applied_edits}),
                "added": started.isoformat(timespec="seconds"),
                "note": "правки откатились из-за гейта, разобрать вручную",
            }
            applied_edits = [dict(e, rolled_back=True) for e in applied_edits]

    drift_line = "пропущен (--no-drift)" if args.no_drift else run_drift()

    save_json(SNAPSHOT_FILE, snapshot)
    save_json(MANUAL_FILE, manual)
    prune_texts(snapshot)

    # --- отчёт ---
    report = build_report(started, run_id, stats, changed_entries, applied_edits,
                          proposals, manual, gate_line, build_line, drift_line,
                          baseline_mode, len(urls))
    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    (ARCHIVE_DIR / f"report-{run_id}.md").write_text(report, encoding="utf-8")

    noteworthy = stats["changed"] or stats["http_err"] or applied_edits or manual
    if noteworthy and not args.dry_run:
        applied_n = len([e for e in applied_edits if not e.get("rolled_back")])
        notify("DT Freshness",
               f"изменений: {stats['changed']}, правок применено: {applied_n}, "
               f"ручной разбор: {len(manual)}. Отчёт: output/freshness_report.md")
    log(f"финиш: same={stats['same']} new={stats['new']} changed={stats['changed']} "
        f"net_err={stats['net_err']} http_err={stats['http_err']} edits={len(applied_edits)}")
    return 1 if stats["changed"] or stats["http_err"] else 0


def build_report(started, run_id, stats, changed, applied, proposals, manual,
                 gate_line, build_line, drift_line, baseline_mode, total) -> str:
    L = [f"# Отчёт свежести документации — {started:%Y-%m-%d %H:%M}",
         "",
         f"Запуск `{run_id}`. Проверено {total} URL официальной документации "
         f"(docs.dynatrace.com), на которые ссылается курс.",
         ""]
    if baseline_mode:
        L += ["**Первый запуск: снята базовая линия.** Сравнение начнётся со следующего запуска.", ""]
    L += ["## 1. Сводка", "",
          f"| Без изменений | Изменились | Новые URL | HTTP-ошибки | Сеть |",
          f"|---|---|---|---|---|",
          f"| {stats['same']} | {stats['changed']} | {stats['new']} | {stats['http_err']} | {stats['net_err']} |",
          ""]
    if changed:
        L += ["## 2. Изменившиеся страницы", ""]
        for c in changed:
            L.append(f"- **{c['url']}** ({c['kind']})")
            L.append(f"  - темы: {', '.join(c['files'])}")
            L.append(f"  - действие: {c['action']}")
            if c.get("summary"):
                L.append(f"  - суть: {c['summary']}")
        L.append("")
    if applied:
        L += ["## 3. Применённые правки", ""]
        for e in applied:
            mark = " (ОТКАЧЕНА гейтом)" if e.get("rolled_back") else ""
            L.append(f"- `{e['file']}`{mark}: {e['reason']} (источник: {e['url']})")
        L += ["", "Правки в рабочем дереве, НЕ закоммичены: посмотри `git diff` и закоммить сам.", ""]
    if proposals:
        L += ["## 4. Предложения (новые факты в доках, в курс не вносились)", ""]
        L += [f"- {p}" for p in proposals] + [""]
    if manual:
        L += ["## 5. Ручной разбор", ""]
        for k, m in manual.items():
            L.append(f"- {k}: файлы {', '.join(m.get('files', []))} (с {m.get('added', '?')})")
        L.append("")
    L += ["## Гейт и сборка", "",
          f"- quality_check --cards: {gate_line}",
          f"- пересборка v1+v2: {build_line}",
          f"- тенант-дрейф: {drift_line}",
          ""]
    return "\n".join(L)


if __name__ == "__main__":
    sys.exit(main())
