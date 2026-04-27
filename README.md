# Dynatrace Managed — обучающий курс (РК)

Курс «Dynatrace Managed для Казахстана» (5 учебных дней, 44 темы) на основе скрейпа реального тенанта. Главный артефакт — `output/training.html`, собирается через `plan_html.py` из `explanations/*.md`.

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

Скриншоты НЕ кликают по destructive-кнопкам (Save / Delete / Apply / Send) — см. `config.yaml → safe_actions.click_deny_text`.

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
- Crawler не нажимает destructive UI. Новые опасные кнопки → добавить в `config.yaml → click_deny_text`.

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
