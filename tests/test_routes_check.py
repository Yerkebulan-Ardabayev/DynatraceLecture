"""Тесты routes_check: адрес курса обязан существовать в ground truth.

Как и для ROUTE-детекторов, зелёный прогон репозитория ничего не доказывает:
проверяем классификацию на заведомо плохом адресе и заодно на хорошем, чтобы
детектор не оказался ни слепым, ни истеричным.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import routes_check as rc  # noqa: E402

KNOWN = {"/ui/services", "/ui/settings/builtin:alerting.maintenance-window"}


def test_known_route_passes():
    assert rc.classify("/ui/services", KNOWN)[0] == "known"


def test_typo_route_is_unknown():
    """Реальный дефект 2026-07-30: в тексте был адрес без суффикса -rule."""
    assert rc.classify("/ui/settings/builtin:maintenance-window", KNOWN)[0] == "unknown"


def test_query_string_ignored():
    assert rc.classify("/ui/services?gf=all&gtf=-2h", KNOWN)[0] == "known"


def test_allowlisted_route_passes_with_reason():
    kind, why = rc.classify("/#newhosts", KNOWN)
    assert kind == "allowlisted" and why


def test_entity_card_prefix_allowlisted():
    kind, why = rc.classify("/ui/nav/SERVICE-4B770D7846DE018B", KNOWN)
    assert kind == "allowlisted" and why


def test_unverified_route_is_separate_bucket(monkeypatch):
    """Не сверенное не выдаём ни за подтверждённое, ни за ошибку.

    Реестр UNVERIFIED сейчас пуст (оба адреса разрешены 2026-07-30: схема
    подтверждена Managed-докой, недоказуемый URL убран из текста). Механизм
    проверяем на синтетической записи, чтобы тест не гнил вместе с реестром.
    """
    monkeypatch.setitem(rc.UNVERIFIED, "/ui/some-unproven-screen", "нет подтверждения")
    assert rc.classify("/ui/some-unproven-screen", KNOWN)[0] == "unverified"


def test_unverified_routes_are_handed_to_drift_report():
    """Адрес без офлайн-подтверждения обязан попадать в браузерную проверку."""
    import drift_report as dr

    monkey = dict(rc.UNVERIFIED)
    rc.UNVERIFIED["/ui/some-unproven-screen"] = "нет подтверждения"
    try:
        routes = {t["route"] for t in dr.unverified_tasks()}
        assert "/ui/some-unproven-screen" in routes
    finally:
        rc.UNVERIFIED.clear()
        rc.UNVERIFIED.update(monkey)


def test_allowlist_entries_all_carry_justification():
    for path, why in {**rc.ALLOWLIST, **rc.PREFIX_ALLOWLIST, **rc.UNVERIFIED}.items():
        assert why.strip(), f"{path} внесён без обоснования"


# ---------- подтверждение по живому тенанту (Settings API v2) ---------------

LIVE = {
    "checked_at": "2026-07-30T06:00:00+00:00",
    "schemas": ["builtin:alerting.maintenance-window", "builtin:oneagent.features"],
    "entity_types": ["HOST", "SERVICE"],
}


def test_live_schema_confirms_route():
    kind, why = rc.classify("/ui/settings/builtin:oneagent.features", set(), LIVE)
    assert kind == "live" and "2026-07-30" in why


def test_schema_absent_on_tenant_is_error_even_if_crawler_saw_it():
    """Главный смысл живой сверки: снапшот устаревает, тенант — нет."""
    stale_known = {"/ui/settings/builtin:process.old-schema"}
    kind, _ = rc.classify("/ui/settings/builtin:process.old-schema", stale_known, LIVE)
    assert kind == "unknown"


def test_classic_settings_page_not_treated_as_schema():
    """/ui/settings/applications-web — не Settings 2.0, в API схем его нет."""
    kind, _ = rc.classify("/ui/settings/applications-web", set(), LIVE)
    assert kind == "allowlisted"


def test_entity_type_confirmed_and_missing():
    assert rc.classify("/ui/entity/list/HOST", set(), LIVE)[0] == "live"
    assert rc.classify("/ui/entity/list/QUEUE", set(), LIVE)[0] == "unknown"


def test_without_live_cache_behaviour_is_unchanged():
    """Офлайн-прогон должен работать точно так же, как до появления флага."""
    assert rc.classify("/ui/services", KNOWN, {})[0] == "known"
    assert rc.classify("/ui/settings/builtin:oneagent.features", KNOWN, {})[0] == "unknown"


def test_lecturer_cards_are_scanned_too():
    """Карточки едут в v2 и тоже называют адреса — проверка обязана их видеть."""
    places = [p for places in rc.collect_used().values() for p in places]
    assert any(p.startswith("cards/") for p in places)


def test_repository_has_no_unknown_routes():
    """Живая сверка текущего состояния курса."""
    known = rc.load_known()
    unknown = [
        path for path in rc.collect_used() if rc.classify(path, known)[0] == "unknown"
    ]
    assert unknown == [], f"адреса вне ground truth: {unknown}"


# ---------- анти-флак drift_report --------------------------------------------


def _entry(headings):
    return {"ui": {"headings": [{"level": lv, "text": tx} for lv, tx in headings]}}


class _Cap:
    def __init__(self, headings):
        self.headings = [{"level": lv, "text": tx} for lv, tx in headings]


def test_missing_headings_trigger_retry():
    """Пропавшая панель фильтров — повод переснять, а не объявлять дрейф."""
    import drift_report as dr

    base = _entry([("h3", "Analysis over time"), ("h3", "Applications")])
    live = _Cap([("h3", "Analysis over time")])
    assert dr._has_missing_headings(base, live) is True


def test_added_headings_do_not_trigger_retry():
    """Добавления разметка не выдумывает, пересъёмка тут не нужна."""
    import drift_report as dr

    base = _entry([("h3", "Analysis over time")])
    live = _Cap([("h3", "Analysis over time"), ("h3", "Strict firewall policy?")])
    assert dr._has_missing_headings(base, live) is False


def test_counter_change_does_not_trigger_retry():
    """«244Services» -> «251Services» — транзиентный счётчик, не пропажа."""
    import drift_report as dr

    assert dr._has_missing_headings(_entry([("h2", "244Services")]), _Cap([("h2", "251Services")])) is False


def test_no_baseline_no_retry():
    import drift_report as dr

    assert dr._has_missing_headings(None, _Cap([])) is False
