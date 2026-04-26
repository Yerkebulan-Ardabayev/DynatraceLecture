> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 1 из 10: «Real User Monitoring (RUM): реальные пользовательские сессии»

## 📍 КАРТА — четыре страницы Real User Monitoring

Термины темы: `RUM / Real User Monitoring / мониторинг реальных пользователей`, `User session / сессия пользователя`, `User action / действие пользователя`, `Beacon / HTTP-пакет с телеметрией`, `USQL / User Session Query Language`, `Apdex / индекс удовлетворённости`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions (список) | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| User session query | **Application Observability → Frontend → User sessions query** | `https://guu84124.live.dynatrace.com/ui/user-sessions/query` |
| RUM Web enablement | **Settings → Web and mobile monitoring → Web enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement` |
| RUM Mobile enablement | **Settings → Web and mobile monitoring → Mobile enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.mobile.enablement` |

---

## 🎬 Работа с RUM на четырёх экранах

### Шаг 1 — User sessions (список всех пользовательских сессий)

![User sessions — список пользовательских сессий](screenshots/day-5/rum/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions`.

**Что здесь видно.** Список всех сессий за выбранный период. Сессия — полный визит одного пользователя от открытия первой страницы до ухода. В air-gapped Managed работаем с классическим list-view, показанным на скриншоте, — новый Apps-интерфейс (Users & Sessions app) в Managed не активен.

**Левая колонка — фильтры:**

- **Analysis over time** — переключает представление между списком сессий и временным графиком.
- **Application type** — Web / Mobile.
- **Application versions** — версии приложения, если используется `dtrum.enterAction`.
- **Applications** — конкретное RUM-приложение (на captured-тенанте видно 5 приложений, созданных через application detection rules).
- **User experience score** — Apdex: Satisfied / Tolerating / Frustrated.
- **Errors and annoyances** — сессии с JS-ошибками, падениями сети, долгими загрузками.
- **Conversions and bounces** — сессии с конверсионным action, либо с уходом после первой страницы.

**Правая часть — таблица сессий.** Для каждой сессии: время старта, продолжительность, количество user actions, Apdex, тип (Web / Mobile), платформа, геолокация. Клик по строке открывает карточку сессии с полным списком user actions в хронологическом порядке.

### Шаг 2 — User session query (произвольные запросы по сессиям)

![User session query — экран запросов по сессиям](screenshots/day-5/rum/user-sessions/query/User-Session-Query-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/query`.

**Что здесь видно.** Страница с единственным заголовком `Run a query to view results` и редактором USQL-запроса в центре. Кнопки `Run query` и `Copy`. По умолчанию открывается пустая сессия — пользователь пишет запрос сам.

*USQL — User Session Query Language.* SQL-подобный язык выборки по сессиям и user actions. Пример:

```sql
SELECT userId, count(*) AS actions
FROM usersession
WHERE userExperienceScore = 'FRUSTRATED'
  AND country = 'Kazakhstan'
GROUP BY userId
ORDER BY actions DESC
LIMIT 100;
```

Результат: топ-100 пользователей с плохим Apdex и количеством их user actions.

*Типовое применение.* Операционная аналитика: «какие сценарии чаще всего ломаются у VIP-клиентов», «в каком городе больше jank-ов», «какие версии мобильного приложения стабильнее». USQL отдаёт сырые сессии напрямую, без промежуточных дашбордов.

*Ограничение.* USQL объявлен устаревшим в SaaS-платформе Dynatrace: там его заменяет DQL (Dynatrace Query Language) через Notebooks поверх Grail. **В air-gapped Managed ни DQL, ни Grail не работают** — доступен только USQL в классическом UI, и он останется рабочим, пока существует классический интерфейс. Подробнее в Теме 9.

### Шаг 3 — RUM Web enablement (включение мониторинга веб-приложений)

![RUM Web enablement — включение мониторинга веб-приложений](screenshots/day-5/rum/settings/builtinrum.web.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement`.

*Что на странице.* `Enablement and cost control` для web-приложений. Администратор включает / выключает сбор RUM-данных, задаёт лимиты на количество сессий и user actions за период.

*Что значит «включение RUM».* Инжекция JavaScript-агента (тег `<script>` со ссылкой на `ruxit.js`) в каждую HTML-страницу, отдаваемую сервером.

**Два способа инжекции:**

- **Автоматическая через OneAgent.** Если на бэкенде установлен OneAgent, он перехватывает ответы веб-сервера (NGINX, Apache, IIS, Java app-server) и добавляет тег автоматически. Менять код не нужно.
- **Ручная.** Администратор вставляет тег в шаблон страницы сам.

**Cost control — лимиты:**

- **Monthly limit** — сколько user actions примем за месяц (например, 50 млн).
- **Sampling** — если предел достигнут, какую долю сессий записывать (например, 10%).

*Зачем нужны лимиты.* Managed-лицензия фиксирует максимум user actions в месяц. Лимит защищает от всплесков трафика (маркетинговая рассылка, черная пятница), когда квота может быть «съедена» за сутки.

### Шаг 4 — RUM Mobile enablement (включение мониторинга мобильных приложений)

![RUM Mobile enablement — включение мониторинга мобильных приложений](screenshots/day-5/rum/settings/builtinrum.mobile.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.mobile.enablement`.

*Что на странице.* Та же `Enablement and cost control`, но для мобильных приложений iOS и Android.

*Разница с Web.* Автоматической инжекции нет — в мобильных приложениях нет HTML-страниц. Разработчик встраивает **Dynatrace Mobile Agent SDK** в код приложения при сборке. Android — gradle-зависимость, iOS — CocoaPods или Swift Package Manager.

**Mobile Agent собирает:**

- **Crash reports** — native crashes, Java / Kotlin exceptions, Swift / Objective-C exceptions.
- **HTTP-запросы и тайминги** — через автоматическую инструментацию URLSession / OkHttp.
- **User actions** — запуски, тапы по экранам, переходы между активностями.
- **Lifecycle events** — cold start, warm start, suspend, resume.

*Типовое применение.* Отслеживание падений на реальных устройствах, анализ каких моделей телефонов или версий Android / iOS проблемнее всего, реальное время входа в приложение на разных устройствах и в разных регионах.

---

## 🎓 ТЕОРИЯ — как RUM устроен изнутри

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Real User Monitoring (RUM)](https://docs.dynatrace.com/docs/shortlink/rum)

### Принцип: агент на стороне клиента

OneAgent на сервере живёт внутри JVM или process tree и собирает телеметрию изнутри. RUM работает **иначе** — агент на стороне пользователя, в браузере или мобильном приложении.

Это фундаментально меняет наблюдаемость. Серверный агент видит: «запрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, потому что:

- 200 мс запрос шёл до дата-центра (мобильный интернет, плохой Wi-Fi).
- 35 мс обрабатывал сервер.
- 250 мс ответ шёл обратно.
- 245 мс браузер парсил HTML, исполнял JavaScript, рендерил DOM.

Без RUM видно только 35 мс. С RUM — все 730 с разбивкой на каждый этап.

### Что собирает Web-агент (ruxit.js)

При загрузке страницы `ruxit.js` подключается первым делом. Он использует Browser Performance API (`window.performance`, `PerformanceObserver`, `Navigation Timing API`, `Resource Timing API`) и собирает:

- **Core Web Vitals** — LCP (Largest Contentful Paint), FID (First Input Delay), CLS (Cumulative Layout Shift). Это метрики Google, которые стали индустриальным стандартом «быстро ли грузится страница».
- **Resource timings** — сколько времени качался каждый CSS, JS, картинка, AJAX-запрос.
- **Navigation timings** — сколько длились DNS lookup, TCP connect, TLS handshake, ответ сервера, парсинг HTML.
- **User actions** — клики, ввод в формы, переходы по ссылкам. RUM-агент «оборачивает» их и связывает с backend-запросами, которые пошли в результате действия.
- **JavaScript errors** — необработанные исключения, ошибки в Promise.
- **Network errors** — неудачные AJAX (HTTP 5xx, таймауты, CORS-отказы).

Все эти данные отправляются **beacon'ом** — небольшим HTTP-запросом к Dynatrace cluster (конкретно на ActiveGate или напрямую в cluster node). В Managed тенанте beacon идёт к ActiveGate, который пересылает его в Cluster Management Console.

### User session vs User action

**User action** — атомарное действие пользователя: клик, переход по ссылке, отправка формы. RUM-агент связывает каждый user action с **цепочкой backend-запросов**, которые он вызвал. Получается сквозная трассировка: клик в браузере → HTTP-запрос → сервис → база → ответ.

**User session** — последовательность user actions одного пользователя, сгруппированных по одному client-id cookie и временному окну. По умолчанию session завершается, если пользователь 30 минут неактивен (inactivity timeout). Новая session с тем же пользователем считается разной — у неё свой session-id.

**Один user — много сессий.** Если пользователь заходит каждое утро на неделе, это 5 сессий. Если на одном устройстве дважды в день — 14 сессий. Это важно для биллинга (цена в лицензии за user actions, не за пользователей) и для аналитики (retention — какой процент пользователей возвращается на следующий день).

### Apdex — User experience score

Dynatrace для каждого user action считает **время отклика** и сравнивает с порогом:
- **Satisfied** — время < T (например, 3 секунды для веб-страницы).
- **Tolerating** — T ≤ время ≤ 4T.
- **Frustrated** — время > 4T.

**Apdex (Application Performance Index)** = (Satisfied + 0.5 × Tolerating) / Total. Диапазон 0.0–1.0. 1.0 — все пользователи довольны, 0.0 — все страдают.

Пороги настраиваются на странице User experience score (увидим в Теме 2).

### Классический UI vs Apps-интерфейс

**В air-gapped Managed новый Apps-интерфейс (Users & Sessions app) пока не активирован**, и мы работаем с классическим list-view. Это не устаревшая функциональность — это параллельные интерфейсы с разным UI: классический (stable в Managed) и новый (SaaS-first). В 2026 году Managed ещё полностью не мигрировал на Apps-модель, поэтому в учебнике опираемся на классический UI.

### Счётчик `278` в навигационной панели

На всех страницах тенанта в верхней панели виден значок `278` рядом с кнопкой пользователя. Это количество активных проблем, зарегистрированных Davis AI в текущий момент. Счётчик живой, обновляется в реальном времени. Клик открывает список Problems. Это не RUM-специфично — счётчик виден на любой странице.

### Как ingest RUM-данных связан с air-gapped контекстом

В SaaS Dynatrace RUM-beacon пользовательского браузера идёт напрямую в `<tenant>.live.dynatrace.com`. В Managed такая схема требовала бы, чтобы каждый компьютер клиента из интернета мог достучаться до вашей Managed-инсталляции — это нарушает air-gapped принцип.

**Решение в Managed:**
- Для внутренних приложений (корпоративный портал, ДБО для сотрудников) — beacon идёт напрямую к ActiveGate внутри сети.
- Для интернет-приложений (публичный сайт банка, мобильное приложение для клиентов) — ставят **Public ActiveGate** в DMZ: он смотрит наружу, принимает beacon'ы, пересылает внутрь на Cluster через защищённый канал.

Схема Public ActiveGate обсуждалась в Дне 1, Тема 2 «Компоненты Dynatrace». В настройках Web enablement есть параметр Beacon URL — он должен указывать на Public ActiveGate, а не на Cluster напрямую.

### Cost control — почему это важно в Managed

В SaaS Dynatrace лимиты биллятся помесячно, превышение — автоматический overage charge. В Managed лицензия фиксирует максимум User Actions в месяц. При превышении Dynatrace **не прекращает запись**, но начинает сэмплировать — случайно отбрасывает часть сессий.

*Типовой сценарий.* Обычный день — 500 тыс. user actions. Пиковый день (выплаты, распродажа) — 2 млн. При лицензии 30 млн/месяц один пиковый день «съедает» ~7% квоты. Важно либо закладывать буфер при покупке лицензии, либо включать adaptive sampling — Dynatrace автоматически режет cap при приближении к лимиту.

### Ключевые термины

- **RUM (Real User Monitoring)** — сбор данных о реальных пользователях с клиентской стороны.
- **Synthetic Monitoring** — противоположность: роботы-эмуляторы ходят по сайту по расписанию. Разберём в Теме 6.
- **User Action** — одно действие пользователя: клик, переход, отправка формы.
- **User Session** — последовательность user actions одного пользователя.
- **Beacon** — HTTP-запрос от браузера/мобильного приложения к Dynatrace с телеметрией.
- **Apdex (User Experience Score)** — индекс удовлетворённости пользователей.
- **LCP / FID / CLS (Core Web Vitals)** — индустриальные метрики скорости веб-страницы.
