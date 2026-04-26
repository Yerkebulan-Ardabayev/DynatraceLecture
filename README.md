# Dynatrace Tenant Crawler

Автоматический обход Dynatrace SaaS тенанта: screenshots + rendered HTML + structured JSON + автодокументация.

**Тенант:** см. `.env`
**Стек:** Python 3.10+, Playwright (Chromium)

---

## Что делает

1. **`auth.py`** — логинится один раз, сохраняет cookies/localStorage в `state/storage_state.json`.
2. **`crawler.py discovery`** — обходит top-level разделы (Hosts, Services, Settings и т.д.), снимает скриншоты, сохраняет HTML, собирает структуру.
3. **`crawler.py deep --section <X>`** — углубляется в выбранный раздел (рекурсивно по depth из конфига).
4. **`crawler.py docs`** — генерирует `output/docs.md` — единый человекочитаемый документ со всеми скриншотами и описанием.

**Скриншоты НЕ кликаются по destructive-кнопкам** (Save / Delete / Apply / Send и т.д.) — см. `config.yaml → safe_actions.click_deny_text`.

---

## Структура выхода (человекочитаемая)

```
output/
├── screenshots/
│   ├── start/start.png
│   ├── hosts/Hosts.png
│   ├── settings/Settings-Preferences.png
│   ├── settings/preferences/notifications/Notifications.png
│   └── ...
├── pages/                 # rendered HTML каждой страницы
│   └── ...same tree...
├── data/
│   └── pages.jsonl        # одна строка JSON на страницу
└── docs.md                # сгенерированная документация
```

Папки получают имя из URL-пути (`/ui/settings/preferences` → `settings/preferences/`), файлы — из `<title>` страницы.

---

## Первый запуск

### 1. Один раз — логин

```bash
cd C:\Users\yerke\dt-crawler
python auth.py
```

- Откроется headed Chrome.
- Скрипт сам введёт email + пароль.
- **Если есть MFA** — введи код вручную в окне, у тебя 3 минуты.
- После того как откроется главная тенанта (`/ui/start`) — окно само закроется и сохранит сессию.

Если что-то пошло не так — окно остаётся, можешь долистать вручную и нажать Enter в консоли.

### 2. Discovery (карта сайта)

```bash
start-discovery.bat
```

Это запустит обход верхнего уровня (~20 разделов из `config.yaml → seed_routes`). Время — 5-15 мин. Окно cmd можно свернуть, закрывать нельзя.

Прогресс: `logs/discovery-stdout.log`.

### 3. Сгенерируй docs.md

```bash
python crawler.py docs
```

Откроется `output/docs.md` со всеми скриншотами и текстом.

### 4. Углубление по разделам

Когда увидишь карту — выбираешь раздел, который надо разобрать подробно:

```bash
start-deep.bat settings
start-deep.bat settings/preferences
start-deep.bat settings/anomaly-detection
```

Crawler пойдёт рекурсивно по всем найденным внутри ссылкам (depth=2 по умолчанию, max_pages=1000).

---

## Конфиг (`config.yaml`)

| Параметр | Что |
|---|---|
| `seed_routes` | Список top-level URL для discovery |
| `crawl.max_depth` | Глубина для deep mode |
| `crawl.max_pages` | Жёсткий лимит страниц за один прогон |
| `crawl.url_skip_patterns` | URL'ы которые НЕ обходить (entity-страницы — иначе бесконечно) |
| `safe_actions.click_deny_text` | Тексты кнопок, которые НИКОГДА не кликать |

---

## Resume / повторные запуски

`checkpoints/visited.json` — список обойдённых URL. При повторном запуске они **пропускаются**. Чтобы переснять всё с нуля — удали этот файл (и при желании `output/`).

---

## Безопасность

- `.env` содержит **plain-text пароль**. Файл в `.gitignore` — не коммить.
- Crawler не нажимает на destructive UI-элементы. Если в Dynatrace появятся новые опасные кнопки — добавь их текст в `config.yaml → click_deny_text`.
- Сессия в `state/storage_state.json` ≈ logged-in cookie. Не делись файлом.

---

## Известные ограничения

1. **Mirror живого SPA = невозможен.** Сохранённый HTML — frozen snapshot. Графики/чарты остаются картинками.
2. **MFA** — обрабатывается только в headed-режиме (вводишь руками в окне).
3. **Entity-страницы** (`/entity/HOST-...`) пропускаются специально — иначе combinatorial explosion (тысячи хостов × десятки табов).
4. **Settings разделов в Dynatrace ~100+** — разбирай батчами через `deep --section`.
5. Если Dynatrace выкатит новый UI / роуты — обнови `seed_routes` в config.yaml.

---

## Troubleshooting

**"storage state missing"** — запусти `python auth.py`.

**"timeout waiting for navigation"** — тенант долго грузится / SSO зависло. Перезапусти `auth.py`.

**Пустые скриншоты** — Playwright снял до загрузки SPA. Увеличь `crawl.navigation_wait_ms` в config.yaml.

**Сессия истекла** — Dynatrace SaaS обычно держит ~24h. Перезапусти `auth.py`.
