"""Тесты ROUTE-детекторов quality_check (воспроизводимость курса).

Зелёный прогон explanations ничего не доказывает сам по себе: детектор,
который не срабатывает никогда, тоже даёт «0 issues». Поэтому здесь каждый
детектор проверяется заведомо плохим входом, а рядом, заведомо хорошим, чтобы
поймать и пропуск дефекта, и ложное срабатывание.

Эталонный плохой вход, реальный текст ui-overview.md до правки 2026-07-30:
владелец курса не смог по нему повторить показанное («не понял, что такое
карточка, где она и путь какой»).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import quality_check as qc  # noqa: E402


def classes(md: str) -> list[str]:
    return [i.cls for i in qc.scan_routes("t.md", md.splitlines())]


# ---------- ROUTE_SCENARIO_NO_STEPS ----------------------------------------

PROSE_SCENARIO = """\
**Типичный сценарий.** Жалоба «что-то тормозит на странице платежей».
Инженер ищет сервис `payment-service` в списке, открывает карточку, смотрит
Response time, проваливается в медленные запросы, оттуда в трейс (PurePath).
"""

STEPPED_SCENARIO = """\
**Сценарий «жалуются, что тормозит»: маршрут по шагам.**

1. **Экран Services.** Открываю `https://guu84124.live.dynatrace.com/ui/services`.
2. **Карточка.** Клик по имени в колонке **Name**.
"""


def test_prose_scenario_is_error():
    assert "ROUTE_SCENARIO_NO_STEPS" in classes(PROSE_SCENARIO)


def test_stepped_scenario_is_clean():
    assert "ROUTE_SCENARIO_NO_STEPS" not in classes(STEPPED_SCENARIO)


def test_non_navigational_scenario_is_not_flagged():
    """«Сценарий» в курсе значит ещё и «вариант конфигурации» — не маршрут."""
    md = """\
**Сценарий 1: Production / Staging / Dev.** Отдельная management zone на среду,
права выдаются по зонам, dev-команда не видит продуктив.
"""
    assert classes(md) == []


# ---------- ROUTE_NO_ADDRESS -----------------------------------------------

CARD_WITHOUT_ADDRESS = """\
**Карточка сервиса.** Клик по имени. В ней: всё для расследования: графики
отклика и пропускной способности, топ-10 медленных запросов, активные проблемы.
"""

CARD_WITH_ADDRESS = """\
**Карточка сервиса: как открыть.** Где: экран Services,
**Application Observability → Services** → `https://guu84124.live.dynatrace.com/ui/services`.
Что нажать: имя сервиса в колонке **Name**. Клик по имени открывает карточку.
"""


def test_card_without_address_is_error():
    assert "ROUTE_NO_ADDRESS" in classes(CARD_WITHOUT_ADDRESS)


def test_card_with_address_is_clean():
    assert "ROUTE_NO_ADDRESS" not in classes(CARD_WITH_ADDRESS)


def test_address_may_live_in_section_lead():
    """Путь задан выше по секции — блок ниже не обязан его повторять."""
    md = (
        "Путь: **Observe and explore → Problems** → "
        "`https://guu84124.live.dynatrace.com/ui/problems`.\n"
        + "\n" * 6
        + "**Карточка проблемы.** Клик по строке открывает хронологию событий.\n"
    )
    assert "ROUTE_NO_ADDRESS" not in classes(md)


def test_address_too_far_away_is_error():
    """За пределами окна путь читателю уже не помогает."""
    md = (
        "Путь: `https://guu84124.live.dynatrace.com/ui/problems`.\n"
        + "\n" * 40
        + "**Карточка проблемы.** Клик по строке открывает хронологию событий.\n"
    )
    assert "ROUTE_NO_ADDRESS" in classes(md)


def test_definitions_are_not_flagged():
    md = (
        "Термины темы: `Rage click / злой клик / многократный клик`, "
        "`Dead click / клик по неинтерактивному элементу`.\n"
    )
    assert classes(md) == []


# ---------- служебное -------------------------------------------------------


def test_code_fence_is_skipped():
    md = "```\n**Карточка сервиса.** Клик по имени открывает карточку.\n```\n"
    assert classes(md) == []


def test_qc_ignore_respected():
    md = CARD_WITHOUT_ADDRESS.replace(
        "**Карточка сервиса.**", "**Карточка сервиса.** <!-- qc:ignore=ROUTE_NO_ADDRESS -->"
    )
    assert "ROUTE_NO_ADDRESS" not in classes(md)


def test_regression_original_ui_overview_block():
    """Оба дефекта разом — тот самый блок, с которого началась правка."""
    found = set(classes(PROSE_SCENARIO + "\n" + CARD_WITHOUT_ADDRESS))
    assert {"ROUTE_SCENARIO_NO_STEPS", "ROUTE_NO_ADDRESS"} <= found
