> 📅 **День 1: Введение в систему Dynatrace** → Тема 4 из 11: «Цифровой опыт (Digital Experience Monitoring): основные принципы»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/applications -->
>
> 🔖 **Редакция от 2026-04-27.** Блок Источников переведён в строгий Managed-режим: все ссылки на /docs/, /platform/ удалены, оставлены только страницы из раздела `/managed/`. В air-gapped Managed Apps-интерфейс «Users & Sessions» не активирован — используется Classic UI. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (Dynatrace Managed — air-gapped):**
>
> - [Welcome to Dynatrace Managed Documentation](https://docs.dynatrace.com/managed) — корень раздела для air-gapped инсталляций
> - [Digital Experience](https://docs.dynatrace.com/managed/observe/digital-experience) — корневой раздел DEM в Managed: RUM-концепции, Web/Mobile/Custom apps, Session segmentation, Session Replay, Synthetic
> - [Apdex ratings](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings) — 5-уровневая Apdex-шкала (Excellent 0.94-1.0 / Good 0.85-0.94 / Fair 0.7-0.85 / Poor 0.5-0.7 / Unacceptable <0.5) и 3-state user-action ratings (Satisfied / Tolerating / Frustrated)
> - [Session Replay](https://docs.dynatrace.com/managed/shortlink/session-replay) — захват и воспроизведение сессий пользователя; поддержка Web, Android, iOS (за исключением Cordova / React Native / Flutter / Xamarin / .NET MAUI)
> - [Synthetic Monitoring](https://docs.dynatrace.com/managed/shortlink/synthetic-monitoring) — 4 типа: single-URL browser monitor, browser clickpath, HTTP monitor, NAM monitor
> - [Data retention periods](https://docs.dynatrace.com/managed/shortlink/data-retention-periods) — RUM 35 дней, Session Replay configurable max 35 дней, Synthetic max 35 дней (Classic)

## 📍 КАРТА — где живут данные цифрового опыта

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Список веб-приложений | **Observe and explore → Applications** | `https://guu84124.live.dynatrace.com/ui/applications` |
| Пользовательские сессии | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| Настройки RUM для приложения | **Settings → Web and mobile monitoring → Application settings** | `https://guu84124.live.dynatrace.com/ui/settings/applications-web` |
| Synthetic Monitoring | **Application Observability → Digital Experience → Synthetic** | `https://guu84124.live.dynatrace.com/ui/synthetic` |

**Термины темы.**

- **DEM / Digital Experience Monitoring / мониторинг цифрового опыта** — общий зонтик для всего, что связано с наблюдением за пользователем на стороне клиента.
- **RUM / Real User Monitoring / мониторинг реальных пользователей** — сбор данных с реальных пользователей через JavaScript-сниппет в браузере или SDK в мобильном приложении.
- **Synthetic Monitoring / синтетический мониторинг** — проверки роботами по расписанию, без реальных пользователей.
- **Session Replay / воспроизведение сессии** — видеозапись того, что видел и делал конкретный пользователь на экране.
- **Application / приложение** — frontend-сущность: веб- или мобильное приложение.
- **Apdex / индекс удовлетворённости** — число от 0 до 1, отражающее, насколько пользователям комфортно по скорости.

**Три источника данных DEM.**

| Источник | Как работает | Что показывает |
|---|---|---|
| RUM | JavaScript-сниппет OneAgent внедряется в HTML-страницы; данные собираются в браузере и шлются через ActiveGate в кластер | Реальная скорость страниц, JS-ошибки, клики, переходы, геопозиция, браузер, версия приложения |
| Mobile RUM | SDK OneAgent встраивается в iOS/Android-приложение при сборке | Crash reports, сетевые запросы, жесты, версии ОС |
| Synthetic | HTTP- или Browser-мониторы запускаются с ActiveGate по расписанию | Доступность, базовая скорость без реального трафика, проверка критичных путей 24×7 |

---

## 🎬 Работа с DEM на двух экранах

### Шаг 1 — Applications / список приложений

![Applications — на демо страница пустая, баннер Connection issues](screenshots/day-1/dem/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Applications** → `https://guu84124.live.dynatrace.com/ui/applications`.

**Что на экране.** На этом демо-тенанте центральная область заполнена баннером `Connection issues / Too many requests` — демо-окружение в момент захвата упёрлось в лимит запросов. Это не нормальное состояние страницы.

**Что здесь на боевой инсталляции.** Таблица карточек приложений. На каждой карточке:
- **Apdex / индекс удовлетворённости** — число от 0 до 1.
- **Число активных пользователей** — в реальном времени и за период.
- **Медианное и 90-й перцентиль времени загрузки**.
- **Процент сессий с ошибками**.
- **Распределение по браузерам, устройствам, странам**.

Клик по карточке открывает подробный дашборд приложения с динамикой всех этих показателей.

**Как приложение попадает сюда.** Нужно три условия:
1. OneAgent установлен на веб-сервере или reverse-proxy, через который идут пользовательские запросы (Nginx / Apache на DMZ-серверах).
2. В **Settings → Web and mobile monitoring → Application settings** создано приложение — указан домен, под которым оно доступно. Правила сопоставления URL настраиваются через Application detection rules (URL starts with / contains / equals) — раздел Web and mobile monitoring в документации Dynatrace для вашей версии.
3. RUM (Real User Monitoring) включён. OneAgent автоматически добавляет в HTML-ответы ссылку на JavaScript-сниппет. Сниппет загружается в браузере пользователя, собирает данные и шлёт их через ActiveGate в кластер.

**Разница между приложением и сервисом.**

- **Сервис / Service** — backend-сущность. Живёт на хосте под OneAgent, обрабатывает HTTP или другие вызовы, обычно соответствует одному процессу.
- **Приложение / Application** — frontend-сущность. Живёт в браузере или в мобильном устройстве, идентифицируется доменом и конфигурацией RUM.

Связь между ними через `x-dynatrace`-заголовок: OneAgent автоматически добавляет его в каждый XHR-запрос браузера, и серверная обработка привязывается к клиентскому user action.

**Типичные причины, когда приложения нет в списке.**

- OneAgent не установлен на web-tier — RUM-сниппет не внедряется.
- В `Settings → Web and mobile monitoring → Application settings` приложение не создано, сниппет работает «в никуда».
- Content-Security-Policy на странице блокирует отправку beacon в ActiveGate.
- Домен ActiveGate недоступен из сети, откуда заходят пользователи.

### Шаг 2 — User sessions / список сессий

![User sessions — список сессий с фильтрами и таблицей](screenshots/day-1/dem/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Frontend → User sessions** → `https://guu84124.live.dynatrace.com/ui/user-sessions`.

**Что на экране.** Список пользовательских сессий — отдельных визитов реальных людей в приложения с включённым RUM. Каждая строка — одна сессия.

В air-gapped Managed работаем с классическим списком сессий — новый Apps-интерфейс (Users & Sessions app) в Managed не активен.

Заголовок **User sessions**, счётчик **First 100 sessions** — по умолчанию выводятся первые сто сессий. Временной период — селектор в правом верхнем углу (на скрине Last 2 hours).

**Слева — панель фильтров.** Применяются кликом, сразу сужают таблицу.

- **Analysis over time** — переключиться с таблицы на график числа сессий по времени.
- **Application type** — веб, мобильное.
- **Application versions** — конкретная версия приложения. Полезно при разборе проблем в новом релизе.
- **Applications** — конкретное приложение, если их несколько.
- **User experience score** — Satisfied / Tolerating / Frustrated по Apdex (3-state user-action ratings; общая шкала Apdex от 0 до 1 имеет 5 уровней: Excellent / Good / Fair / Poor / Unacceptable). <!-- last-verified: 2026-04-27 source: docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings -->
- **Errors and annoyances** — только сессии с ошибками или поведенческими раздражителями (rage clicks, навязчивые перезагрузки).
- **Conversions and bounces** — сессии с бизнес-конверсией (успешный платёж) или отказом (ушёл с первой страницы).
- **Users** — фильтр по User ID (если в RUM настроен).
- **Browsers** — браузер и версия.
- **Internet service provider** — провайдер связи по IP.
- **Operating systems** — ОС устройства.
- **Locations** — страна и город.

**Пример расследования.** Жалоба: «пользователи с Safari на iPhone не могут войти в интернет-банк». Фильтры: **Browser = Safari** + **Operating system = iOS** + **Errors and annoyances = Yes**. В таблице остаются только такие сессии — открываем карточку, смотрим, что именно ломалось. Для воспроизведения конкретного визита используется Session Replay — запись DOM-состояния экрана, доступная по кнопке **Play** в карточке сессии (требует включённого Session Replay в настройках приложения).

**Таблица справа.** Колонки:

- **Session start** — время начала визита.
- **Browser** — браузер и версия.
- **Application** — какое приложение.
- **User** — анонимный ID по cookie или реальный ID после авторизации.
- **Duration** — длительность от первой до последней активности.
- **Events** — сколько действий совершил пользователь.
- **Errors** — сколько ошибок.
- **Exits** — на скольких страницах заканчивалась сессия.
- **Conversions** — сколько бизнес-целей пройдено.

**Карточка сессии.** Клик на строку открывает подробную карточку. В ней:
- Полная хронология действий пользователя.
- Все страницы, которые он посетил.
- Все JavaScript-ошибки со стеком.
- Все XHR/fetch-запросы с временами и статусами.
- Все бизнес-события (если настроены).
- Кнопка **Play** для Session Replay, если включено для приложения.

**Связь с бэкендом.** На каждом XHR-запросе к backend-сервису Dynatrace связывает клиентский запрос с серверным PurePath. В карточке сессии клик на запрос открывает trace с полной цепочкой: браузер → web-tier → backend-сервис → база, с временами на каждом шаге. Видно, где именно медленно: на клиенте, в сети или на backend.

**Air-gapped контекст.** RUM-сниппет в браузере пользователя отправляет данные в ActiveGate. Если ActiveGate стоит в закрытом контуре, а пользователи — снаружи (клиенты, заходящие из интернета), то домен ActiveGate должен быть опубликован. Типичная схема банка — ActiveGate в DMZ с публичным доменом, либо reverse-proxy, принимающий RUM-трафик снаружи и проксирующий во внутренний ActiveGate. Для мобильных приложений аналогично — URL ActiveGate должен быть доступен с мобильных сетей.

**Synthetic как дополнение.** User sessions показывают только реальных пользователей. Если реального трафика мало (ночь, выходные) или нужна проверка критичного пути независимо от пользователей, используется Synthetic Monitoring — `https://guu84124.live.dynatrace.com/ui/synthetic`. Роботы ходят по приложению по скрипту раз в несколько минут. Synthetic-данные видны отдельно и не смешиваются с RUM — статистика не засоряется искусственным трафиком.
