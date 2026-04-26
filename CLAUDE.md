# CLAUDE.md — dt-crawler

Курс «Dynatrace Managed для Казахстана» на основе tenant-scrape. Главный артефакт — `training.html` (947 KB+), собирается через `plan_html.py` из `explanations/*.md`.

## ПРИОРИТЕТ №1 — фактологическая точность

Это не UI-рерайт, это технический обучающий курс. **Любая выдумка — дефект**.

### Источники правды (в порядке доверия)

1. **`ui_elements.json` + `pages.jsonl`** — UI-цитирование, headings/buttons/fields дословно. Это ground truth для того, что юзер видит.
2. **`dtkb` skill** — technical facts (настройки, лимиты, overhead, retention, поведение фич, air-gapped). FTS5 по всем Dynatrace docs. Использовать `mcp__dtkb__dtkb_search`.
3. **`docs.dynatrace.com/managed/`** — fallback, если в dtkb не нашлось.

Разделяй: «на captured экране X» vs «в production обычно Y». Никогда не смешивай.

### Запрещено в explanations/*

| Категория | Примеры | Почему |
|---|---|---|
| **RU_REGULATOR** | ФСТЭК, Astra Linux как обязательный | Курс для Казахстана, не РФ |
| **RU_OS** | «только на Astra», требования РФ | см. выше |
| **ROADMAP_DATE** | «Grail в 2027», «DQL следом» | Roadmap-даты устаревают; не обещать того, что вне Managed |
| **MARKETING** | таблицы сравнения конкурентов, «лучше чем X» | это обучение, не sales |
| **SUPPORT_INSTRUCTION** | «обратитесь в поддержку Dynatrace» | L1/L2 сами решают; не отправлять в support |
| **FAKE_SUCCESS_STORY** | «клиент X сократил MTTR с 60 до 15 мин» | выдуманные кейсы запрещены |
| **UNSOURCED_PERCENT / UNSOURCED_RPS** | «1-2% CPU», «800 RPS» без источника | цифры только с источником (dtkb / docs) |
| **DQL для Managed** | «используйте DQL в Advanced mode» | DQL/Grail только в SaaS. В Managed → Metrics Selector / USQL / UI-фильтры |
| **UI-баннеры из SaaS** | «Try the new…», «Leverage…» | в Managed этих баннеров нет; техсуть — одной фразой без цитирования |

## Обязательный workflow перед сборкой

```bash
# 1. Quality check (7 детекторов)
python scripts/quality_check.py
# должно быть: ✅ 0 errors

# 2. Extract tech claims для dtkb-верификации
python scripts/extract_tech_claims.py
# открыть tech_claims_verification.md, сверить numeric claims с dtkb

# 3. Build
python plan_html.py
# pre_build_quality_check() вызовется автоматически — упадёт при errors > 0
# escape (не использовать без явной просьбы): SKIP_QC=1 python plan_html.py
```

## Паттерны для explanations

### Первая тема дня/курса: контекст → UI, не UI → контекст

Шаблон `КАРТА → Что показать → ТЕОРИЯ` работает только на **последующих** темах. На первой — вводный блок теории («Что такое X и зачем он нужен») ВПЕРЕД, до `КАРТА`. Не переписывай шаблон для всех тем — точечное исключение.

### Структура explanation

```markdown
# <Тема>

## КАРТА
<navigation — откуда пришли, куда идём>

## Что показать / UI
<цитирование из ui_elements.json; headings дословно>

## ТЕОРИЯ
<объяснение; tech-claims со ссылкой на dtkb / docs>

## Практика / Чеклист
<шаги L1/L2 могут повторить>
```

## Build-id и cache

HTML собирается с `<meta name="dt-build-id">` + build-id в `title` (sha1 explanations + timestamp) + `extra.vN.css?sha=<SHA>`. Это автоматом в `plan_html.py`. Не трогай.

## Если что-то не находится

- Tech-факт не в dtkb и не в docs → **спроси пользователя**, не выдумывай.
- UI-элемент не в `ui_elements.json` → возможно, captured скрины устарели; не цитируй дословно, опиши обобщённо («в разделе Settings обычно есть поле X»).

## Не репозиторий

dt-crawler **НЕ git-репо**. «Пуш» = `python plan_html.py` — генерирует `training.html`. Нет коммитов, нет веток.

## Связанные правила (в memory/)

- `feedback_dt_managed_tech_accuracy.md` — это главное правило
- `feedback_ui_elements_ground_truth.md` — UI дословно
- `feedback_dql_only_saas.md` — DQL только SaaS
- `feedback_no_ui_banners_in_narration.md` — SaaS-баннеры не цитируй
- `feedback_first_topic_context_before_ui.md` — порядок на первой теме

## Команды

- `/status` — статус проекта
- `/quality` — полная проверка (verify-build + quality_check.py + dtkb-верификация)
- `/new-batch` — открыть новый батч
