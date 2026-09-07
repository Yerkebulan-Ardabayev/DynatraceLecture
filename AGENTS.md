# AGENTS.md — dt-crawler

Курс «Dynatrace Managed для Казахстана» на основе tenant-scrape. Главный артефакт — `training.html` (947 KB+), собирается через `plan_html.py` из `explanations/*.md`.

## ПРИОРИТЕТ №1 — фактологическая точность

Это не UI-рерайт, это технический обучающий курс. **Любая выдумка — дефект**.

### Источники правды (в порядке доверия)

1. **`ui_elements.json` + `pages.jsonl`** — UI-цитирование, headings/buttons/fields дословно. Это ground truth для того, что юзер видит. Ограничение: контент-зона Settings-страниц и body_preview обрезаны, скриншоты на Mac отсутствуют.
2. **`docs.dynatrace.com/managed/` (живые страницы, WebFetch)** — авторитет для верификации tech-фактов: лимиты, retention, версии, поведение фич, air-gapped. Расхождение с любым локальным источником решает живая дока. Дрейф этих страниц автоматически ловит `scripts/docs_freshness.py` (см. README, «Автообновление»).
3. **`dtkb` skill** — вспомогательный локальный индекс (личные Dynatrace-заметки и выдержки, НЕ полное зеркало доков; проверено аудитом 2026-07-17). Годится для быстрого поиска, но отсутствие факта в dtkb ничего не доказывает, а найденное перепроверяется по живой доке.

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

## Воспроизводимость: адрес у объекта, шаги у сценария

Курс читают у экрана, ученик обязан повторить показанное сам. Поэтому:

- у каждого объекта («карточка X», «клик по …») рядом стоит блок **Как открыть**: путь по меню, что нажать, куда попадаешь, как вернуться;
- каждый сценарий с навигацией развёрнут в **нумерованные шаги** (где я → что делаю → что вижу → почему дальше);
- примеры берутся с живого тенанта (`easyTradeManager`), выдуманные имена вроде `payment-service` запрещены;
- адрес берётся из `ui_elements.json` / `study_plan.yaml`; чего там нет, описывается без URL.

Гейты (падают на сборке): `ROUTE_NO_ADDRESS`, `ROUTE_SCENARIO_NO_STEPS` в `quality_check.py` плюс `scripts/routes_check.py` (сверяет каждый адрес с ground truth). Формат и эталоны: `CONTENT_POLICY.md` §8.

**На демо-тенанте `guu84124` API-токен выпустить нельзя** (проверено 2026-07-30: «Your user does not have the necessary write permissions», кнопка Generate new token неактивна, personal access tokens отключены). Это не блокер: офлайн-сверка закрывает все адреса. Не отправлять владельца выпускать токен там повторно; `--confirm-live` пригодится на кластере, где права есть.

Подтверждение адресов по живому тенанту без браузера: `python scripts/routes_check.py --confirm-live` (Settings API v2, нужен `DT_API_TOKEN` с правами `settings.read` + `entities.read`; покрывает ~105 адресов из 149). Результат кэшируется в `state/routes_live.json` и с этого момента ужесточает офлайн-прогоны. Числа тенанта: `scripts/tenant_facts.py`. Оба шага уже вызываются суточной джобой `com.yerke.dt-freshness` и попадают в `output/freshness_report.md`.

## Обязательный workflow перед сборкой

```bash
# 1. Quality check (детекторы политики + ROUTE-детекторы)
python scripts/quality_check.py
# должно быть: ✅ 0 errors

# 1b. Сверка адресов с ground truth (без сети)
python scripts/routes_check.py --strict

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

## v2 Presenter Edition (сборка `--v2`)

Второй вариант курса живёт в ветке `v2-presenter`. `plan_html.py --v2` собирает `output/training_v2.html` (палитра Ctrl+K, окно докладчика по клавише P с карточками и таймером, синхронизация окон, масштаб). **Дефолтная `plan_html.py` без флага не меняется** — v2 трансформирует КОПИЮ шаблона, `HTML_TEMPLATE` не трогается.

Карточки лектора: `cards/<day>/<topic>.md`, 48/48, каждая цифра обязана присутствовать в explanation своей темы. Гейт: `python scripts/quality_check.py --cards` (CARD-детекторы, см. `CONTENT_POLICY.md` §7). Сборка `--v2` вызывает его автоматически, сборка v1 — без `--cards`.

Свежесть: `python scripts/drift_report.py --limit 3` (нужна сессия: `python auth.py` либо `python auth.py --manual`). Памятка запуска — в `README.md`, раздел «Свежесть».

**Готовность страницы в drift_report (правка 2026-07-30, не упрощать обратно).** Прежнее условие «в body больше 40 символов» выполняла одна навигационная оболочка, поэтому снимок делался до отрисовки контента: ~100 Settings-страниц уходили в отчёт как CHANGED с вырожденным заголовком «Settings - <окружение>», а на `/ui/user-sessions` «пропадали» все 12 заголовков панели фильтров. Тревога срабатывала всегда и потому ничего не значила. Теперь: `wait_render_stable()` ждёт стабилизации пары (заголовок, число h1-h4) — три одинаковых замера подряд и не раньше 4 с, плюс анти-флак-повтор `_has_missing_headings()` переснимает роут с запасом, если заголовки пропали относительно эталона (пропажа = почти всегда недорисовка; добавления не переснимаются). Проверено на живом тенанте: было 29 CHANGED из 173, из них 3 настоящих.

**Как читать CHANGED.** Живые данные демо-тенанта (счётчики Services/Databases, списки уязвимостей, число атак) и SaaS-баннеры («Try the new…», «Leverage…») это не дрейф курса: баннеры курс не цитирует по политике, счётчики привязаны к снимку. Смотреть в первую очередь на переименования страниц и на новые/пропавшие элементы управления.

Автообновление по докам: `scripts/docs_freshness.py` — launchd `com.yerke.dt-freshness` дважды в день сверяет 146 docs.dynatrace.com-страниц курса со снапшотом, при изменениях правит текст через `Codex -p` (валидатор + гейт + откат), пересобирает v1+v2, пишет `output/freshness_report.md`. Правки не коммитятся — дифф смотрит владелец. Подробности в README, раздел «Автообновление по официальной документации».

## Если что-то не находится

- Tech-факт не в dtkb и не в docs → **спроси пользователя**, не выдумывай.
- UI-элемент не в `ui_elements.json` → возможно, captured скрины устарели; не цитируй дословно, опиши обобщённо («в разделе Settings обычно есть поле X»).

## Репозиторий

dt-crawler, git-репозиторий: `https://github.com/Yerkebulan-Ardabayev/DynatraceLecture.git`; default branch `main`. Артефакт `training.html` собирается через `plan_html.py`. После значимых правок: проверить именованно staged diff, затем `git add <имена>` и `git commit -m "…"`. `git push` выполнять только после явного согласия пользователя в текущей сессии.

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

## Codex shared Dynatrace rules

- Для Dynatrace Managed не использовать DQL, Grail или Apps. Для метрик
  использовать Metrics Selector в Data Explorer Advanced mode, для сессий
  USQL, для логов search и UI-фильтры.
- Ссылки в учебном материале приоритизировать так: `/managed/`, затем
  `/docs/`. SaaS-only страницы допустимы только как явно помеченная
  иллюстрация, а не как инструкция для Managed.
- Токены Settings 2.0 имеют префикс `dt0s01.`, классические endpoint-токены
  `dt0c01.`. Никогда не публиковать их полностью.
- Шкала Apdex содержит пять диапазонов: 0.94-1.0, 0.85-0.94, 0.7-0.85,
  0.5-0.7, менее 0.5. Azure DevOps не является допустимой интеграцией
  Dynatrace Issue tracking.
- Любое утверждение о текущем продукте сверять с официальной документацией.
  Локальный dtkb ускоряет поиск, но не заменяет живой первоисточник.
