# Dynatrace Managed — обучающий курс (РК)

Курс «Dynatrace Managed для Казахстана» (5 учебных дней, 48 тем) на основе скрейпа реального тенанта. Главный артефакт — `output/training.html`, собирается через `plan_html.py` из `explanations/*.md`.

**Стек:** Python 3.10+, Playwright (Chromium) для краулера + статический HTML-генератор для курса.
**Тенант:** см. `.env`
**Репозиторий:** `https://github.com/Yerkebulan-Ardabayev/DynatraceLecture.git` (default branch `main`)

---

## Состав курса

| День | Папка | Тема (по PDF) | Файлов |
|---|---|---|---|
| 1 | `explanations/day-1/` | Введение в систему Dynatrace | 11 |
| 2 | `explanations/day-2/` | Инфраструктура, контейнеры, базы данных, сети | 9 |
| 3 + 4 | `explanations/day-3-4/` | Архитектура сквозного мониторинга и Observability | 17 |
| 5 | `explanations/day-5/` | Мониторинг фронтенда и пользовательского опыта | 10 |

Программа курса зафиксирована в `Обучение Dynatrace.pdf` (соседний проект `dynatrace-platform/`). Внутри каждого дня порядок строго по `study_plan.yaml`.

---

## Политика контента — `/managed/`-only

Это технический обучающий курс для Dynatrace Managed Classic в air-gapped среде. **Любая выдумка = дефект.**

### Единственный авторитет для tech-фактов

`docs.dynatrace.com/managed/...` через WebFetch. Никаких fallback'ов на `/docs/`, `/platform/`, `/grail/`, `/dql/`, `/apps/`, `blog.dynatrace.com`, dt-university, ChatGPT.

Каждый файл в `explanations/*.md` имеет:
- блок `📚 Источники` — только `/managed/...` ссылки (минимум 2, типично 4-6);
- метки `<!-- last-verified: <date> source: <managed-URL> -->` после блоков с конкретикой;
- `<!-- revision: <date> -->` после первой строки темы;
- `<!-- live-ui: https://guu84124.live.dynatrace.com/ui/<путь> -->` для прямой ссылки на UI.

### Запрещено

| Категория | Примеры |
|---|---|
| RU-регулятор | ФСТЭК, Astra Linux как обязательный (курс для РК) |
| Roadmap-даты | «Grail в 2027», «DQL следом» |
| Marketing | сравнения с конкурентами, «лучше чем X» |
| Support-instruction | «обратитесь в поддержку Dynatrace» |
| Fake success | «клиент X сократил MTTR с 60 до 15 мин» |
| Unsourced numbers | «1-2% CPU», «800 RPS» без `/managed/`-источника |
| DQL/Grail/Apps/Workflows как функция Managed | DQL только SaaS; в Managed — Metrics Selector / USQL / UI-фильтры |
| SaaS-баннеры | «Try the new…», «Leverage…», «Discover…» |

Подробнее — `CONTENT_POLICY.md`.

---

## Сборка курса

```bash
# 1. Quality gate (7 детекторов)
python scripts/quality_check.py
# ожидание: ✅ 0 errors

# 2. Link check (все ссылки /managed/ → 200 OK)
python scripts/link_check.py
# ожидание: ✅ N URL — все 200 OK

# 3. Build
python plan_html.py
# pre_build_quality_check() вызывается автоматически
# escape (не использовать без явной просьбы): SKIP_QC=1 python plan_html.py
```

Артефакт: `output/training.html` (~1.1 MB, 235 скриншотов inline, build-id в `<meta>` + cache-bust по sha).

---

## v2 — Presenter Edition (ветка `v2-presenter`)

Второй вариант курса для ведения на онлайн-звонке. Собирается ОТДЕЛЬНО флагом `--v2` в отдельный файл. Дефолтная сборка v1 (`output/training.html`) при этом не меняется ни на байт.

```bash
.venv/bin/python plan_html.py --v2
# -> output/training_v2.html (48 карточек лектора, ~1.5 MB, офлайн: 0 сетевых запросов)
```

**Что добавляет v2:**
- **Палитра Ctrl+K** — нечёткий поиск по 48 темам плюс полнотекст по контенту с подсветкой и прыжком к совпадению; Esc возвращает к теме плана.
- **Окно докладчика (клавиша P)** — открывается тем же файлом с `#presenter` через `window.open`. Показывает карточку лектора, план дня, следующую тему, таймер темы с ориентиром из `timing_min`. Синхронизация окон: основной канал `postMessage` по ссылке окна, запасные BroadcastChannel и storage-событие (надёжно на `file://`). Стрелки листают оба окна синхронно.
- **Масштаб** — клавиши `+` / `-` / `0` (zoom области чтения, персист в localStorage).
- Офлайн: без Google Fonts, ноль внешних запросов при открытии.

Приёмка синхронизации окон: Chrome и Safari на `file://`.

### Карточки лектора — `cards/<day>/<topic>.md`

По одной на каждую из 48 тем. YAML-шапка (`topic_id`, `day_id`, `timing_min`, `verified`) плюс 6 блоков: `## ГДЕ` (route и путь) / `## ЗАЧЕМ` / `## ЦИФРЫ` / `## ЕСЛИ→ТО` / `## ЗАПАСНОЙ ПЛАН` / `## ВОПРОСЫ АУДИТОРИИ`.

**Контракт:** любая цифра в карточке обязана присутствовать в explanation своей темы. Карточка не вводит новых фактов, только сжимает проверенные. Проверяется автоматически:

```bash
python scripts/quality_check.py --cards
# CARD-детекторы (включаются флагом --cards; дефолт проверяет explanations как раньше):
#   CARD_MISSING          (warn)  — тема без карточки
#   CARD_EMDASH           (error) — длинное тире в карточке
#   CARD_BANNED_CATEGORY  (error) — запрещённая категория контент-политики
#   CARD_UNSOURCED_NUMBER (error) — число, которого нет в explanation темы
```
Сборка `--v2` вызывает `quality_check --cards` автоматически. Сборка v1 запускает его без `--cards`, поэтому гейт v1 не затронут.

### Свежесть — `scripts/drift_report.py` (памятка запуска)

Детектор дрейфа UI живого тенанта относительно эталона `ui_elements.json`.

```bash
python scripts/drift_report.py --limit 3      # смоук: первые 3 роута плана
python scripts/drift_report.py                # полный прогон по live-роутам
python scripts/drift_report.py --routes day-1 # фильтр по дню или подстроке роута
```

Выход: `drift_report.md`, 5 секций (сводка / изменённые экраны / битые роуты / транзиентные счётчики / затронутые темы). Транзиентные счётчики (`Services 241` на `Services 239`) нормализуются и дрейфом НЕ считаются. Exit 1, если есть CHANGED или BROKEN.

**Когда запускать:** перед каждым потоком обучения и после обновления кластера или тенанта. По изменённым темам из секции 5 перепроверить факты по dtkb и `/managed/`, обновить `tech_claims_verification.md`, затем пересобрать.

**Требует живую сессию:** `.env` (`DT_LOGIN` / `DT_PASSWORD`), затем `python auth.py` (или `python auth.py --manual` для ручного входа в окне без пароля в `.env`, поддерживает MFA), сессия сохраняется в `state/storage_state.json`.

### Автообновление по официальной документации — `scripts/docs_freshness.py`

Второй контур свежести: следит не за UI тенанта, а за **страницами docs.dynatrace.com**, на которые ссылается курс (146 URL). Работает полностью автоматически (launchd-агент `com.yerke.dt-freshness`, ежедневно 07:30 и 19:30, лог `~/Library/Logs/dt-freshness.log`).

Цикл: скачать страницы → извлечь основной текст → сравнить со снапшотом (`state/docs_snapshot.json`) → для изменившихся страниц определить темы курса, цитирующие URL → через `claude -p` (Sonnet, подписка) решить, устарело ли утверждение → применить минимальную правку (русский текст в месте старого утверждения, числа только из новой доки, без длинных тире) → гейт `quality_check --cards` (провал = откат правок запуска) → пересборка v1+v2 → отчёт `output/freshness_report.md` (архив в `logs/freshness/`) + уведомление в Notification Center.

Предохранители: детерминированный валидатор поверх LLM (правка только в `explanations/`/`cards/`, `old` встречается ровно один раз, каждая цифра нового текста существует в новой доке либо в старом фрагменте, em-dash запрещён); не больше 12 LLM-вызовов за запуск; после 2 неудачных попыток по диффу страница уходит в ручной разбор (`state/freshness_manual.json`); новые факты доки в текст НЕ вносятся, а попадают в отчёт как предложения. Правки остаются в рабочем дереве **незакоммиченными**: коммит и push за владельцем.

```bash
python scripts/docs_freshness.py --dry-run   # только дифф-отчёт, без LLM и правок
python scripts/docs_freshness.py --no-llm    # диффы в отчёт, файлы не трогать
python scripts/docs_freshness.py --url secure/faq   # смоук по одному URL
launchctl kickstart gui/$(id -u)/com.yerke.dt-freshness   # внеплановый запуск
```

Тесты решающей логики: `pytest tests/test_docs_freshness.py`. Тенант-дрейф (`drift_report.py`) вызывается тем же циклом автоматически, если сессия `state/storage_state.json` свежее 20 часов, иначе помечается пропущенным.

---

## Журнал верификации

`tech_claims_verification.md` — журнал сессий аудита: какой блок, какой WebFetch'ом проверен, цитата из `/managed/`-страницы, решение (✅ оставить / ⚠️ переписать / ❌ удалить). За весь курс — 9 сессий, 161 решение по блокам.

`empty_screens_todo.md` — пустые / SaaS-only / `In development` скрины с captured-тенанта, которые НЕ описываются как часть Managed-курса (на 2026-04-27 — 3 скрина reliability-config + Шаг 1 synthetic).

---

## Часть 1 — Crawler (источник UI-данных)

Краулер уже отработал и собрал captured-тенант в `output/`. Перезапускать обычно не нужно — данные стабильны для текущей версии Dynatrace.

### Что делает

1. **`auth.py`** — логин один раз, сохраняет cookies/localStorage в `state/storage_state.json`.
2. **`crawler.py discovery`** — обходит top-level разделы, снимает скриншоты, сохраняет HTML.
3. **`crawler.py deep --section <X>`** — рекурсивно по разделу.
4. **`extract_ui_elements.py`** — извлекает headings/buttons/fields в `output/data/ui_elements.json`.

Краулер только переходит по URL и снимает страницу, он вообще не кликает по кнопкам. Поэтому destructive-действия (Save / Delete / Apply / Send) невозможны by construction.

### Структура output/

```
output/
├── screenshots/         # PNG по структуре URL
├── pages/               # rendered HTML каждой страницы
├── data/
│   ├── pages.jsonl      # одна строка JSON на страницу
│   └── ui_elements.json # headings/buttons/fields для цитирования в курсе
└── training.html        # итоговый курс (собирается plan_html.py)
```

### Перезапуск краулера

```bash
# 1. Логин (если сессия истекла)
python auth.py

# 2. Discovery
start-discovery.bat

# 3. Углубление по разделу
start-deep.bat settings
start-deep.bat settings/anomaly-detection

# 4. Извлечь UI-элементы
python extract_ui_elements.py
```

`checkpoints/visited.json` — список обойдённых URL. Чтобы переснять с нуля — удалить файл (и при желании `output/`).

---

## Безопасность

- `.env` содержит plain-text пароль. В `.gitignore`. Не коммитить.
- `state/storage_state.json` ≈ logged-in cookie. Не делиться.
- Crawler не нажимает destructive UI: он только открывает URL и снимает страницу, кликов по кнопкам нет.

---

## Связанные правила и контекст

- `CLAUDE.md` — инструкции для AI-ассистента в проекте
- `CONTENT_POLICY.md` — детальные категории запрещённого контента
- `study_plan.yaml` — программа курса (порядок тем по дням)
- `tech_claims_verification.md` — журнал верификации против `/managed/`
- `empty_screens_todo.md` — SaaS-only / пустые скрины

---

## Известные ограничения

1. **Mirror живого SPA = невозможен.** Сохранённый HTML — frozen snapshot. Графики остаются картинками.
2. **MFA** — только в headed-режиме (вводится руками в окне).
3. **Entity-страницы** (`/entity/HOST-...`) пропускаются специально (combinatorial explosion).
4. **Settings разделов в Dynatrace ~100+** — разбирать батчами через `deep --section`.
5. Если Dynatrace выкатит новый UI / роуты — обновить `seed_routes` в `config.yaml`.

---

## Troubleshooting

| Симптом | Что делать |
|---|---|
| `storage state missing` | `python auth.py` |
| `timeout waiting for navigation` | тенант долго грузится / SSO зависло — перезапустить `auth.py` |
| Пустые скриншоты | Playwright снял до загрузки SPA — увеличить `crawl.navigation_wait_ms` |
| Сессия истекла | Dynatrace Managed обычно держит ~24h — перезапустить `auth.py` |
| `quality_check` падает на NO_SOURCE | tech-spec без `/managed/`-источника — добавить ссылку или пометить `<!-- qc:ignore=NO_SOURCE -->` если это generic-иллюстрация |
| `link_check` падает | URL вернул не-200 — найти новый `/managed/`-URL через WebSearch site:docs.dynatrace.com/managed |
