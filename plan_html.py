"""
Generate single-file HTML viewer for the training course.
Output: output/training.html (double-click to open in browser).

Reads:
    study_plan.yaml    — structure (days, topics)
    explanations/{day_id}/{topic_id}.md  — markdown content
    output/data/pages.jsonl  — screenshots (filtered by source=plan)
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import yaml
import markdown as md

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
PLAN_FILE = ROOT / "study_plan.yaml"
DATA_FILE = ROOT / "output" / "data" / "pages.jsonl"
EXPL_DIR = ROOT / "explanations"
OUT_FILE = ROOT / "output" / "training.html"
QC_SCRIPT = ROOT / "scripts" / "quality_check.py"
LC_SCRIPT = ROOT / "scripts" / "link_check.py"


def pre_build_quality_check() -> None:
    """Вызывает scripts/quality_check.py. Если найдены errors — блокирует сборку.

    Можно отключить переменной окружения SKIP_QC=1 (для отладки только). Warnings
    не блокируют — они в логе quality_check для ручного ревью.
    """
    if os.environ.get("SKIP_QC") == "1":
        print("⚠️  SKIP_QC=1 — quality_check пропущен (отладка; не коммитить так).")
        return
    if not QC_SCRIPT.exists():
        print(f"⚠️  {QC_SCRIPT} не найден — quality_check пропущен.")
        return
    print("→ quality_check…")
    result = subprocess.run(
        [sys.executable, str(QC_SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    # Print the checker's own report so user sees what failed
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        print(
            "\n❌ BUILD BLOCKED: quality_check обнаружил errors. "
            "Исправь нарушения CONTENT_POLICY.md или добавь inline-комментарий "
            "<!-- qc:ignore=CLASS --> на легитимных строках, затем повтори сборку.",
            file=sys.stderr,
        )
        sys.exit(result.returncode)
    print("✓ quality_check: ✅ 0 errors\n")


def pre_build_link_check() -> None:
    """Валидирует все URL в explanations через HTTP. Кэш 7 дней."""
    if os.environ.get("SKIP_LC") == "1":
        print("⚠️  SKIP_LC=1 — link_check пропущен (отладка; не коммитить так).")
        return
    if not LC_SCRIPT.exists():
        print(f"⚠️  {LC_SCRIPT} не найден — link_check пропущен.")
        return
    print("→ link_check…")
    result = subprocess.run(
        [sys.executable, str(LC_SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        print(
            "\n❌ BUILD BLOCKED: link_check нашёл broken URL. "
            "Исправь ссылки в explanations (или убери битые), затем повтори сборку. "
            "Если ссылка работает, но стоит за auth — добавь паттерн в SKIP_PATTERNS "
            "в scripts/link_check.py.",
            file=sys.stderr,
        )
        sys.exit(result.returncode)
    print("✓ link_check: все URL 200 OK\n")


def compute_build_id() -> str:
    """Короткий идентификатор сборки — sha1 от всех explanations + timestamp.

    Отображается в UI и title, чтобы после rebuild юзер видел «это новая версия»,
    даже если браузер закешировал predыдущий HTML (лечится Ctrl+F5, но видимый
    маркер помогает диагностике).
    """
    h = hashlib.sha1()
    for md_file in sorted(EXPL_DIR.rglob("*.md")):
        h.update(md_file.read_bytes())
    sha_short = h.hexdigest()[:8]
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"{ts} · {sha_short}"


def load_plan():
    return yaml.safe_load(PLAN_FILE.read_text(encoding="utf-8"))


def load_pages():
    if not DATA_FILE.exists():
        return []
    out = []
    with DATA_FILE.open(encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                if rec.get("source") == "plan":
                    out.append(rec)
            except Exception:
                pass
    return out


def status_marker(p):
    title = (p.get("title") or "").lower()
    if "404" in title:
        return "❌ 404"
    if "403" in title:
        return "🔒 403"
    return "✅"


def md_to_html(text: str) -> str:
    if not text:
        return ""
    return md.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        output_format="html5",
    )


def build_topics_data(plan, pages):
    """Build {day_id: {title, topics: [{id, name, html, screenshots, notes}]}}"""
    by_topic_pages = defaultdict(list)
    seen = defaultdict(set)
    for p in pages:
        tid = p.get("topic_id")
        if not tid:
            continue
        if p["url"] in seen[tid]:
            continue
        seen[tid].add(p["url"])
        by_topic_pages[tid].append(p)

    result = []
    for d in plan["days"]:
        day_data = {
            "id": d["id"],
            "title": d["title"],
            "objectives": d.get("objectives", "").strip(),
            "topics": [],
        }
        for t in d["topics"]:
            expl_file = EXPL_DIR / d["id"] / f"{t['id']}.md"
            md_text = expl_file.read_text(encoding="utf-8") if expl_file.exists() else ""
            shots = []
            for p in by_topic_pages.get(t["id"], []):
                sc = p.get("screenshot", "")
                if sc:
                    rel = sc.split("output/", 1)[1] if "output/" in sc else sc
                    short = p["title"].split(" - ")[0] if " - " in p["title"] else p["title"]
                    shots.append({
                        "title": short,
                        "route": p.get("plan_route", ""),
                        "src": rel,
                        "status": status_marker(p),
                    })
            day_data["topics"].append({
                "id": t["id"],
                "name": t["name"],
                "kind": t.get("kind", "live"),
                "notes": t.get("notes", ""),
                "html": md_to_html(md_text),
                "has_explanation": bool(md_text),
                "screenshots": shots,
                "routes_planned": t.get("routes", []),
            })
        result.append(day_data)
    return result


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="dt-build-id" content="__BUILD_ID__">
<title>Обучение Dynatrace Managed · __BUILD_ID__</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#07080c;--card:#0c0f18;--border:#161b26;--text:#bfc5d2;
  --muted:#6b7280;--accent:#6fa0e8;--accentDim:rgba(111,160,232,.12);
  --green:#34d399;--greenDim:rgba(52,211,153,.12);
  --orange:#f59e0b;--red:#ef4444;--redDim:rgba(239,68,68,.12);
  --surface:#10131d;--hover:#141825;--bright:#e2e8f0;
  --tip:#fbbf24;--tipDim:rgba(251,191,36,.12);
}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--text);font-family:'Source Sans 3',sans-serif;font-size:16px}
::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--muted)}

#app{display:flex;height:100vh;overflow:hidden}

/* Sidebar */
#sidebar{width:340px;min-width:340px;background:var(--card);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden}
#sidebar-header{padding:18px 18px 14px;border-bottom:1px solid var(--border)}
#sidebar-header .brand{font-size:13px;font-weight:700;color:var(--accent);letter-spacing:1.5px;text-transform:uppercase}
#sidebar-header .sub{font-size:11px;color:var(--muted);margin-top:3px}

#search-wrap{padding:10px 14px;border-bottom:1px solid var(--border)}
#search{width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 12px;color:var(--text);font-size:13px;font-family:inherit;outline:none}
#search:focus{border-color:var(--accent)}

#nav-list{flex:1;overflow-y:auto;padding:8px 0}

.nav-day{padding:14px 18px 6px;font-size:11px;font-weight:700;color:var(--accent);letter-spacing:1.5px;text-transform:uppercase;border-top:1px solid var(--border);margin-top:4px;background:rgba(111,160,232,.04)}
.nav-day:first-child{border-top:none;margin-top:0}
.nav-day .day-objective{display:block;font-size:11px;color:var(--muted);margin-top:4px;font-weight:400;letter-spacing:0;text-transform:none;line-height:1.4}

.nav-btn{display:flex;align-items:flex-start;gap:8px;width:100%;padding:9px 18px 9px 26px;background:transparent;border:none;cursor:pointer;text-align:left;color:var(--text);font-size:13px;font-family:inherit;transition:all .12s;border-left:3px solid transparent;line-height:1.35}
.nav-btn:hover{background:var(--hover)}
.nav-btn.active{background:var(--accentDim);color:var(--accent);border-left-color:var(--accent)}
.nav-mark{flex-shrink:0;font-size:10px;color:var(--muted);min-width:14px}
.nav-mark.has-content{color:var(--green)}
.nav-mark.no-content{color:var(--orange)}

/* Main */
#main{flex:1;display:flex;flex-direction:column;overflow:hidden}
#topbar{display:flex;align-items:center;gap:12px;padding:12px 24px;border-bottom:1px solid var(--border);background:var(--card)}
#breadcrumb{flex:1;color:var(--muted);font-size:13px}
#breadcrumb b{color:var(--bright)}
.nav-btns{display:flex;gap:6px}
.nav-arrow{border:1px solid var(--border);border-radius:6px;padding:6px 14px;font-size:13px;font-family:inherit;cursor:pointer;background:var(--accentDim);color:var(--accent);transition:all .15s}
.nav-arrow:hover:not(:disabled){background:var(--accent);color:var(--bg)}
.nav-arrow:disabled{background:var(--bg);color:var(--muted);cursor:default}

#content{flex:1;overflow-y:auto;padding:28px 36px 60px}
#content-inner{max-width:920px;margin:0 auto}

.topic-header h1{font-size:30px;color:var(--bright);margin-bottom:8px;line-height:1.3}
.topic-meta{font-size:12px;color:var(--muted);margin-bottom:24px}
.topic-meta .pill{display:inline-block;padding:2px 8px;border-radius:10px;background:var(--accentDim);color:var(--accent);font-size:11px;margin-right:6px}
.topic-meta .pill.warn{background:rgba(251,191,36,.12);color:var(--tip)}

.topic-notes{background:rgba(251,191,36,.08);border-left:3px solid var(--tip);padding:12px 16px;margin-bottom:18px;border-radius:0 6px 6px 0;color:var(--text);font-size:13px;line-height:1.5}

.theory{font-size:18px;line-height:1.75}
.theory h1{display:none}
.theory h2{font-size:26px;color:var(--bright);margin:32px 0 14px;padding-bottom:10px;border-bottom:1px solid var(--border)}
.theory h3{font-size:22px;color:var(--accent);margin:26px 0 12px}
.theory h4{font-size:18px;color:var(--bright);margin:18px 0 10px}
.theory p{margin:12px 0;color:var(--text)}
.theory strong{color:var(--bright);font-weight:600}
.theory em{color:var(--accent)}
.theory ul, .theory ol{margin:12px 0 12px 26px;color:var(--text)}
.theory li{margin:6px 0}
.theory code{background:rgba(111,160,232,.14);color:var(--accent);padding:2px 7px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:.92em;word-break:break-word;overflow-wrap:anywhere}
.theory pre{background:#080a12;border:1px solid var(--border);border-radius:6px;padding:16px 18px;overflow-x:auto;margin:16px 0;font-size:15px;line-height:1.55}
.theory pre code{background:none;color:#93c5fd;padding:0;font-size:15px;word-break:normal;overflow-wrap:normal}
.theory blockquote{background:var(--tipDim);border-left:3px solid var(--tip);padding:12px 18px;margin:16px 0;border-radius:0 6px 6px 0;color:var(--text);font-style:normal}
.theory blockquote p{margin:5px 0}
.theory blockquote strong{color:var(--tip)}
.theory table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px;font-family:'JetBrains Mono',monospace;table-layout:fixed;word-break:break-word;overflow-wrap:anywhere}
.theory table th{text-align:left;padding:9px 14px;border-bottom:2px solid var(--accent);color:var(--accent);font-weight:600;background:var(--accentDim)}
.theory table td{padding:7px 14px;color:var(--text);border-bottom:1px solid var(--border);word-break:break-word;overflow-wrap:anywhere}
.theory table tr:hover{background:var(--hover)}
.theory hr{border:none;border-top:1px solid var(--border);margin:24px 0}
.theory a{color:var(--accent);text-decoration:underline;text-decoration-style:dotted;word-break:break-word;overflow-wrap:anywhere}
.theory a:hover{text-decoration-style:solid;color:var(--bright)}
.theory a.ext-link{position:relative;padding-right:22px}
.theory a.ext-link::after{content:"↗";font-size:.8em;opacity:.65;margin-left:3px}
.theory a.ext-link .copy-btn{position:absolute;right:-26px;top:50%;transform:translateY(-50%);opacity:0;pointer-events:none;transition:opacity .15s;background:var(--tipDim);border:1px solid var(--border);border-radius:4px;padding:2px 6px;font-size:11px;cursor:pointer;color:var(--text);user-select:none}
.theory a.ext-link:hover .copy-btn,.theory a.ext-link .copy-btn:hover{opacity:1;pointer-events:auto}
.theory a.ext-link .copy-btn.ok{color:var(--accent)}
.theory .source-note{font-size:.88em;color:#7c8aa8;margin-top:8px;padding:6px 10px;background:rgba(111,160,232,.06);border-left:2px solid var(--accent);border-radius:0 4px 4px 0}
.theory .source-note a{text-decoration:none}
.theory img{display:block;width:100%;max-width:100%;max-height:700px;object-fit:contain;background:#000;border:1px solid var(--border);border-radius:8px;margin:14px 0;cursor:zoom-in;transition:max-height .25s}
.theory img.zoomed{max-height:none;cursor:zoom-out;object-fit:initial}

.no-explanation{background:rgba(251,191,36,.08);border:1px dashed var(--tip);padding:18px 20px;border-radius:8px;color:var(--tip);font-size:13px;margin:18px 0}
.no-explanation b{color:var(--bright)}
.no-explanation code{background:rgba(0,0,0,.3);padding:2px 6px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent)}

/* Top "Where to find" block (path + main screenshot ABOVE theory) */
.location-block{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:18px 20px;margin-bottom:20px}
.location-block h3{color:var(--accent);font-size:14px;text-transform:uppercase;letter-spacing:1.1px;margin-bottom:10px;font-weight:700}
.location-block .path-row{display:flex;align-items:flex-start;gap:10px;margin:6px 0;font-size:14px;line-height:1.5}
.location-block .path-row .label{color:var(--muted);min-width:70px;font-size:12px;padding-top:2px}
.location-block .path-row .value{color:var(--bright);flex:1}
.location-block code{background:var(--bg);color:var(--accent);padding:2px 8px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:12px;word-break:break-all;overflow-wrap:anywhere}

.main-screenshot{margin:18px 0 24px;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:#000}
.main-screenshot-caption{padding:10px 16px;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.main-screenshot-caption .ms-status{font-size:14px}
.main-screenshot-caption .ms-title{flex:1;color:var(--bright);font-weight:600;font-size:14px}
.main-screenshot-caption .ms-route{color:var(--muted);font-size:11px;font-family:'JetBrains Mono',monospace;word-break:break-all;overflow-wrap:anywhere}

/* Universal screenshot toggle — click to enlarge to natural size, click again to restore */
.screenshot-img{display:block;width:100%;height:auto;max-height:700px;object-fit:contain;cursor:zoom-in;background:#000;transition:max-height .25s}
.screenshot-img.zoomed{max-height:none;cursor:zoom-out;object-fit:initial}
.zoom-hint{position:absolute;bottom:8px;right:12px;background:rgba(0,0,0,.7);color:var(--accent);padding:3px 8px;border-radius:3px;font-size:11px;pointer-events:none}
.shot-wrap{position:relative}

.shots-section{margin-top:36px;padding-top:24px;border-top:1px solid var(--border)}
.shots-section h2{font-size:16px;color:var(--muted);text-transform:uppercase;letter-spacing:1.2px;font-weight:600;margin-bottom:18px}
.shot{margin-bottom:28px;border:1px solid var(--border);border-radius:8px;overflow:hidden;background:var(--card)}
.shot-header{padding:12px 16px;border-bottom:1px solid var(--border);background:var(--surface);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.shot-status{font-size:13px}
.shot-title{flex:1;color:var(--bright);font-weight:600;font-size:13px}
.shot-route{color:var(--muted);font-size:11px;font-family:'JetBrains Mono',monospace;word-break:break-all;overflow-wrap:anywhere}
.shot-img{display:block;width:100%;height:auto;cursor:zoom-in;background:#000}
.shot-img.zoomed{cursor:zoom-out}

.missing-shots{background:rgba(251,191,36,.08);border:1px dashed var(--tip);padding:12px 16px;border-radius:6px;color:var(--tip);font-size:13px;margin:14px 0}
.missing-shots b{color:var(--bright)}

#topic-default{text-align:center;color:var(--muted);padding:80px 20px}
#topic-default h2{font-size:18px;color:var(--bright);margin-bottom:8px}
#topic-default p{margin:6px 0;font-size:14px}

@media (max-width:900px){
  #sidebar{width:280px;min-width:280px}
  #content{padding:18px 20px 40px}
}
</style>
</head>
<body>
<div id="app">
  <aside id="sidebar">
    <div id="sidebar-header">
      <div class="brand">DYNATRACE MANAGED</div>
      <div class="sub">Обучающий курс — 5 дней, 44 темы</div>
    </div>
    <div id="search-wrap">
      <input id="search" type="text" placeholder="Поиск по темам / контенту..." autocomplete="off">
    </div>
    <nav id="nav-list"></nav>
  </aside>
  <main id="main">
    <div id="topbar">
      <div id="breadcrumb">Выберите тему слева</div>
      <div class="nav-btns">
        <button class="nav-arrow" id="prev-btn" disabled>← Пред</button>
        <button class="nav-arrow" id="next-btn" disabled>След →</button>
      </div>
    </div>
    <div id="content">
      <div id="content-inner">
        <div id="topic-default">
          <h2>Обучение Dynatrace Managed — JUSAN</h2>
          <p>Полный материал курса с теорией и скриншотами тенанта.</p>
          <p>Выбери тему слева, чтобы начать.</p>
        </div>
      </div>
    </div>
  </main>
</div>
<script>
const DATA = __DATA_PLACEHOLDER__;

const navList = document.getElementById('nav-list');
const contentInner = document.getElementById('content-inner');
const breadcrumb = document.getElementById('breadcrumb');
const searchInput = document.getElementById('search');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');

// Flatten all topics for prev/next navigation
const FLAT = [];
DATA.forEach(d => d.topics.forEach(t => FLAT.push({day: d, topic: t})));

let currentIdx = -1;

function buildNav(filter='') {
  navList.innerHTML = '';
  const f = filter.toLowerCase().trim();
  let visibleCount = 0;
  DATA.forEach(d => {
    const matchedTopics = d.topics.filter(t => {
      if (!f) return true;
      if (t.name.toLowerCase().includes(f)) return true;
      if (t.html.toLowerCase().includes(f)) return true;
      return false;
    });
    if (matchedTopics.length === 0) return;
    const dayDiv = document.createElement('div');
    dayDiv.className = 'nav-day';
    const dayLabel = d.id.replace('day-', 'День ');
    dayDiv.innerHTML = `${dayLabel} — ${escapeHtml(d.title)}<span class="day-objective">${escapeHtml(d.objectives.split('\\n')[0])}</span>`;
    navList.appendChild(dayDiv);
    matchedTopics.forEach(t => {
      const idx = FLAT.findIndex(x => x.topic.id === t.id && x.day.id === d.id);
      const btn = document.createElement('button');
      btn.className = 'nav-btn';
      btn.dataset.idx = idx;
      const mark = t.has_explanation ? '●' : '○';
      const markClass = t.has_explanation ? 'has-content' : 'no-content';
      btn.innerHTML = `<span class="nav-mark ${markClass}">${mark}</span><span class="nav-name">${escapeHtml(t.name)}</span>`;
      btn.onclick = () => showTopic(idx);
      navList.appendChild(btn);
      visibleCount++;
    });
  });
  if (visibleCount === 0) {
    navList.innerHTML = '<div style="padding:20px;color:var(--muted);font-size:12px;text-align:center">Ничего не найдено</div>';
  }
}

function escapeHtml(s) {
  return (s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function showTopic(idx) {
  if (idx < 0 || idx >= FLAT.length) return;
  currentIdx = idx;
  const {day, topic} = FLAT[idx];

  document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', +b.dataset.idx === idx));
  const activeBtn = document.querySelector(`.nav-btn[data-idx="${idx}"]`);
  if (activeBtn) activeBtn.scrollIntoView({block:'nearest'});

  const dayLabel2 = day.id.replace('day-', 'День ');
  breadcrumb.innerHTML = `<span style="color:var(--muted)">${dayLabel2} — ${escapeHtml(day.title)}</span> &nbsp;›&nbsp; <b>${escapeHtml(topic.name)}</b>`;

  let html = `<div class="topic-header"><h1>${escapeHtml(topic.name)}</h1>`;
  html += `<div class="topic-meta">`;
  html += `<span class="pill">${dayLabel2} — ${escapeHtml(day.title)}</span>`;
  if (topic.kind === 'concept') html += `<span class="pill">Концепт</span>`;
  if (!topic.has_explanation) html += `<span class="pill warn">Объяснение не написано</span>`;
  html += `</div></div>`;

  // (Внутренние planning-notes из study_plan.yaml пользователю не показываем)

  // === TOP: путь "Где найти" + главный скриншот ===
  // Filter: only OK screenshots (no 404/403). Pick first as "main".
  const okShots = (topic.screenshots || []).filter(s => !s.status.includes('404') && !s.status.includes('403'));
  const badShots = (topic.screenshots || []).filter(s => s.status.includes('404') || s.status.includes('403'));
  const mainShot = okShots[0] || null;
  const restShots = okShots.slice(1);

  if (topic.routes_planned && topic.routes_planned.length) {
    html += `<div class="location-block">`;
    html += `<h3>📍 Где найти в интерфейсе</h3>`;
    topic.routes_planned.forEach(r => {
      html += `<div class="path-row"><span class="label">URL:</span><span class="value"><code>${escapeHtml(r)}</code></span></div>`;
    });
    html += `</div>`;
  }

  if (badShots.length) {
    html += `<div class="missing-shots">⚠️ <b>${badShots.length}</b> запланированных страниц недоступны на этом тенанте (404 / 403). Объясняется концептуально.</div>`;
  }

  // === MIDDLE: theory (с встроенными скриншотами через markdown) ===
  if (topic.has_explanation) {
    html += `<div class="theory">${topic.html}</div>`;
  } else {
    html += `<div class="no-explanation">⚠️ <b>Объяснение пока не написано.</b><br><br>Создай файл <code>explanations/${day.id}/${topic.id}.md</code> и регенерируй HTML командой <code>python plan_html.py</code>.</div>`;
    // Для placeholder-тем — показываем все доступные скриншоты как preview
    if (okShots.length) {
      html += `<div class="shots-section"><h2>📸 Доступные скриншоты (${okShots.length}) — нет deep-описаний</h2>`;
      okShots.forEach(s => {
        html += `<div class="shot">`;
        html += `<div class="shot-header"><span class="shot-status">${s.status}</span><span class="shot-title">${escapeHtml(s.title)}</span><span class="shot-route">${escapeHtml(s.route)}</span></div>`;
        html += `<div class="shot-wrap"><img class="screenshot-img" src="${s.src}" alt="${escapeHtml(s.title)}" onclick="this.classList.toggle('zoomed')" title="Клик — увеличить / уменьшить"><span class="zoom-hint">клик для зума</span></div>`;
        html += `</div>`;
      });
      html += `</div>`;
    }
  }

  contentInner.innerHTML = html;
  enhanceExternalLinks(contentInner);
  contentInner.parentElement.scrollTop = 0;

  prevBtn.disabled = idx <= 0;
  nextBtn.disabled = idx >= FLAT.length - 1;

  try { localStorage.setItem('dt-jusan-last', String(idx)); } catch(e){}
}

// Внешние ссылки: открывать в новой вкладке + кнопка "copy URL" при hover.
// Работает и для ссылок, которые рендерит markdown-парсер, и для inline-code,
// который мы пост-процессим (если это чистый `docs.dynatrace.com/...` — сделаем ссылкой).
function enhanceExternalLinks(root) {
  // 1) inline-code вида `docs.dynatrace.com/...` или `https://docs.dynatrace.com/...`
  //    превращаем в настоящий <a> — чтобы можно было кликнуть и скопировать.
  const codes = root.querySelectorAll('code');
  codes.forEach(c => {
    if (c.closest('pre')) return; // не трогать блоки кода
    const t = c.textContent.trim();
    const m = t.match(/^(https?:\/\/)?(docs\.dynatrace\.com\/[^\s`]+)$/);
    if (!m) return;
    const href = (m[1] ? m[1] : 'https://') + m[2];
    const a = document.createElement('a');
    a.href = href;
    a.textContent = m[2];
    c.replaceWith(a);
  });

  // 2) для всех внешних <a> добавить target=_blank + копирующую кнопку
  const links = root.querySelectorAll('a[href]');
  links.forEach(a => {
    const href = a.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href)) return;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.classList.add('ext-link');
    a.title = 'Открыть в новой вкладке · наведите для копирования URL';
    // Copy button (rendered on hover via CSS)
    if (!a.querySelector('.copy-btn')) {
      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.type = 'button';
      btn.textContent = '⧉';
      btn.title = 'Скопировать URL';
      btn.addEventListener('click', ev => {
        ev.preventDefault();
        ev.stopPropagation();
        const url = a.href;
        const done = () => {
          const old = btn.textContent;
          btn.textContent = '✓';
          btn.classList.add('ok');
          setTimeout(() => { btn.textContent = old; btn.classList.remove('ok'); }, 1200);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done).catch(() => {
            fallbackCopy(url); done();
          });
        } else {
          fallbackCopy(url); done();
        }
      });
      a.appendChild(btn);
    }
  });
}

function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); } catch(e){}
  document.body.removeChild(ta);
}

prevBtn.onclick = () => showTopic(currentIdx - 1);
nextBtn.onclick = () => showTopic(currentIdx + 1);

searchInput.addEventListener('input', e => buildNav(e.target.value));

// Universal img click toggle (для inline-картинок из markdown)
contentInner.addEventListener('click', e => {
  if (e.target.tagName === 'IMG' && (e.target.closest('.theory') || e.target.classList.contains('screenshot-img'))) {
    e.target.classList.toggle('zoomed');
  }
});

document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowLeft' && !prevBtn.disabled) prevBtn.click();
  else if (e.key === 'ArrowRight' && !nextBtn.disabled) nextBtn.click();
  else if (e.key === '/' || (e.ctrlKey && e.key === 'f')) { e.preventDefault(); searchInput.focus(); }
});

buildNav();
const last = parseInt(localStorage.getItem('dt-jusan-last') || '-1');
if (last >= 0 && last < FLAT.length) showTopic(last);
</script>
</body>
</html>
"""


def main():
    pre_build_quality_check()
    pre_build_link_check()
    plan = load_plan()
    pages = load_pages()
    data = build_topics_data(plan, pages)
    data_json = json.dumps(data, ensure_ascii=False)
    build_id = compute_build_id()
    html = (
        HTML_TEMPLATE
        .replace("__DATA_PLACEHOLDER__", data_json)
        .replace("__BUILD_ID__", build_id)
    )
    OUT_FILE.write_text(html, encoding="utf-8")
    total_topics = sum(len(d["topics"]) for d in data)
    with_expl = sum(1 for d in data for t in d["topics"] if t["has_explanation"])
    total_shots = sum(len(t["screenshots"]) for d in data for t in d["topics"])
    print(f"OK  ->  {OUT_FILE}")
    print(f"     build-id: {build_id}")
    print(f"     {len(data)} days, {total_topics} topics ({with_expl} with explanation), {total_shots} screenshots")
    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"     {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
