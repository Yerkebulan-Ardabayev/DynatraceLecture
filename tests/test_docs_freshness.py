"""Тесты решающей логики docs_freshness (без сети и без LLM)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import docs_freshness as df  # noqa: E402


def test_extract_main_text_strips_chrome():
    html = """
    <html><head><script>var x=1;</script><style>.a{}</style></head>
    <body><nav>Menu Home</nav><header>Top</header>
    <main><h1>OneAgent limits</h1>
    <p>Maximum   500 metrics per environment.</p>
    <p>Was this page helpful?</p><p>Last updated Jan 1</p></main>
    <footer>(c) Dynatrace</footer></body></html>"""
    text = df.extract_main_text(html)
    assert "OneAgent limits" in text
    assert "Maximum 500 metrics per environment." in text  # пробелы схлопнуты
    assert "Menu Home" not in text and "(c) Dynatrace" not in text
    assert "Was this page helpful" not in text and "Last updated" not in text


def test_extract_main_text_fallback_body():
    text = df.extract_main_text("<body><p>plain body only</p></body>")
    assert text == "plain body only"


def _mk_file(tmp_path, monkeypatch, rel="explanations/day-1/demo.md",
             body="Лимит: 500 метрик на окружение.\nВторая строка.\n"):
    root = tmp_path
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    monkeypatch.setattr(df, "ROOT", root)
    monkeypatch.setattr(df, "BAK_DIR", root / "state" / "freshness_bak")
    return p


def test_validate_edit_ok(tmp_path, monkeypatch):
    _mk_file(tmp_path, monkeypatch)
    edit = {"file": "explanations/day-1/demo.md",
            "old": "Лимит: 500 метрик на окружение.",
            "new": "Лимит: 600 метрик на окружение."}
    ok, why = df.validate_edit(edit, new_page_text="Maximum 600 metrics per environment")
    assert ok, why


def test_validate_edit_rejects_hallucinated_digit(tmp_path, monkeypatch):
    _mk_file(tmp_path, monkeypatch)
    edit = {"file": "explanations/day-1/demo.md",
            "old": "Лимит: 500 метрик на окружение.",
            "new": "Лимит: 999 метрик на окружение."}
    ok, why = df.validate_edit(edit, new_page_text="Maximum 600 metrics per environment")
    assert not ok and "999" in why


def test_validate_edit_rejects_emdash_and_dup_and_path(tmp_path, monkeypatch):
    _mk_file(tmp_path, monkeypatch, body="строка\nстрока\n")
    bad_dash = {"file": "explanations/day-1/demo.md", "old": "строка\n",
                "new": "строка — новая\n"}
    ok, why = df.validate_edit(bad_dash, "")
    assert not ok and "тире" in why
    dup = {"file": "explanations/day-1/demo.md", "old": "строка", "new": "стр"}
    ok, why = df.validate_edit(dup, "")
    assert not ok and "раз" in why
    escape = {"file": "../outside.md", "old": "a", "new": "b"}
    ok, why = df.validate_edit(escape, "")
    assert not ok


def test_apply_and_rollback_preserve_manual_edits(tmp_path, monkeypatch):
    p = _mk_file(tmp_path, monkeypatch,
                 body="ручная правка владельца\nЛимит: 500 метрик.\n")
    edit = {"file": "explanations/day-1/demo.md",
            "old": "Лимит: 500 метрик.", "new": "Лимит: 600 метрик."}
    df.apply_edit(edit, run_id="testrun")
    assert "600" in p.read_text(encoding="utf-8")
    restored = df.rollback_run("testrun")
    text = p.read_text(encoding="utf-8")
    assert "500" in text and "ручная правка владельца" in text
    assert restored == ["explanations/day-1/demo.md"]


def test_card_for(tmp_path, monkeypatch):
    _mk_file(tmp_path, monkeypatch)
    card = tmp_path / "cards" / "day-1" / "demo.md"
    card.parent.mkdir(parents=True)
    card.write_text("x", encoding="utf-8")
    assert df.card_for("explanations/day-1/demo.md") == card
    assert df.card_for("explanations/day-1/nope.md") is None


def test_snapshot_roundtrip_and_prune(tmp_path, monkeypatch):
    monkeypatch.setattr(df, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(df, "TEXTS_DIR", tmp_path / "state" / "docs_texts")
    snap_file = tmp_path / "state" / "snap.json"
    name = df.store_text("hello", df.text_sha("hello"))
    stale = df.store_text("stale", df.text_sha("stale"))
    snap = {"https://docs.dynatrace.com/x": {"sha": df.text_sha("hello"), "text_file": name}}
    df.save_json(snap_file, snap)
    assert df.load_json(snap_file) == snap
    df.prune_texts(snap)
    assert (df.TEXTS_DIR / name).exists()
    assert not (df.TEXTS_DIR / stale).exists()


def test_unified_diff_truncates():
    old = "\n".join(f"line {i}" for i in range(400))
    new = "\n".join(f"line {i} changed" for i in range(400))
    d = df.unified_diff(old, new, max_chars=500)
    assert len(d) <= 530 and "обрезан" in d
