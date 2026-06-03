> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 1 из 10: «Real User Monitoring (RUM): реальные пользовательские сессии»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/user-sessions -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Real User Monitoring (RUM)](https://docs.dynatrace.com/managed/shortlink/rum)
> - [RUM JavaScript injection](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/initial-setup/rum-injection)
> - [Firewall constraints for RUM](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/initial-setup/firewall-constraints-for-rum)
> - [User actions](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-actions)
> - [Apdex ratings](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings)
> - [Scores and ratings](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings)
> - [User session (shortlink)](https://docs.dynatrace.com/managed/shortlink/user-session)
> - [Dynatrace Android Gradle plugin](https://docs.dynatrace.com/managed/observe/digital-experience/mobile-applications/instrument-android-app/instrumentation-via-plugin)
> - [Instrument iOS apps](https://docs.dynatrace.com/managed/observe/digital-experience/mobile-applications/instrument-ios-app)

## 📍 КАРТА: четыре страницы Real User Monitoring

Термины темы: `RUM / Real User Monitoring / мониторинг реальных пользователей`, `User session / сессия пользователя`, `User action / действие пользователя`, `Beacon / HTTP-пакет с телеметрией`, `USQL / User Session Query Language`, `Apdex / индекс удовлетворённости`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions (список) | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| User session query | **Application Observability → Frontend → User sessions query** | `https://guu84124.live.dynatrace.com/ui/user-sessions/query` |
| RUM Web enablement | **Settings → Web and mobile monitoring → Web enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement` |
| RUM Mobile enablement | **Settings → Web and mobile monitoring → Mobile enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.mobile.enablement` |

---

## 🎬 Работа с RUM на четырёх экранах

### Шаг 1: User sessions (список всех пользовательских сессий)

![User sessions: список пользовательских сессий](screenshots/day-5/rum/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions`.

**Что здесь видно.** Список всех сессий за выбранный период. Сессия: полный визит одного пользователя от открытия первой страницы до ухода. В air-gapped Managed работаем с классическим list-view, показанным на скриншоте: новый Apps-интерфейс (Users & Sessions app) в Managed не активен.

**Левая колонка: фильтры:**

- **Analysis over time**: переключает представление между списком сессий и временным графиком.
- **Application type**: Web / Mobile.
- **Application versions**: версии приложения, если используется `dtrum.enterAction`.
- **Applications**: конкретное RUM-приложение (на captured-тенанте видно 5 приложений, созданных через application detection rules).
- **User experience score**: Apdex: Satisfied / Tolerating / Frustrated.
- **Errors and annoyances**: сессии с JS-ошибками, падениями сети, долгими загрузками.
- **Conversions and bounces**: сессии с конверсионным action, либо с уходом после первой страницы.

**Правая часть: таблица сессий.** Для каждой сессии: время старта, продолжительность, количество user actions, Apdex, тип (Web / Mobile), платформа, геолокация. Клик по строке открывает карточку сессии с полным списком user actions в хронологическом порядке.

### Шаг 2: User session query (произвольные запросы по сессиям)

![User session query: экран запросов по сессиям](screenshots/day-5/rum/user-sessions/query/User-Session-Query-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/query`.

**Что здесь видно.** Страница с единственным заголовком `Run a query to view results` и редактором USQL-запроса в центре. Кнопки `Run query` и `Copy`. По умолчанию открывается пустая сессия: пользователь пишет запрос сам.

*USQL: User Session Query Language.* SQL-подобный язык выборки по сессиям и user actions. Пример:

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

*Ограничение.* USQL объявлен устаревшим в SaaS-платформе Dynatrace: там его заменяет DQL (Dynatrace Query Language) через Notebooks поверх Grail. **В air-gapped Managed ни DQL, ни Grail не работают**: доступен только USQL в классическом UI, и он останется рабочим, пока существует классический интерфейс. Подробнее в Теме 9.

### Шаг 3: RUM Web enablement (включение мониторинга веб-приложений)

![RUM Web enablement: включение мониторинга веб-приложений](screenshots/day-5/rum/settings/builtinrum.web.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement`.

*Что на странице.* `Enablement and cost control` для web-приложений. Администратор включает / выключает сбор RUM-данных, задаёт лимиты на количество сессий и user actions за период.

*Что значит «включение RUM».* Инжекция JavaScript-агента (тег `<script>` со ссылкой на `ruxit.js`) в каждую HTML-страницу, отдаваемую сервером.

**Два способа инжекции:**

- **Автоматическая через OneAgent.** Если на бэкенде установлен OneAgent, он перехватывает ответы веб-сервера (NGINX, Apache, IIS, Java app-server) и добавляет тег автоматически. Менять код не нужно.
- **Ручная.** Администратор вставляет тег в шаблон страницы сам.

**Cost control: лимиты:**

- **Monthly limit**: сколько user actions примем за месяц (например, 50 млн).
- **Sampling**: если предел достигнут, какую долю сессий записывать (например, 10%).

*Зачем нужны лимиты.* Managed-лицензия фиксирует максимум user actions в месяц. Лимит защищает от всплесков трафика (маркетинговая рассылка, черная пятница), когда квота может быть «съедена» за сутки.

### Шаг 4: RUM Mobile enablement (включение мониторинга мобильных приложений)

![RUM Mobile enablement: включение мониторинга мобильных приложений](screenshots/day-5/rum/settings/builtinrum.mobile.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.mobile.enablement`.

*Что на странице.* Та же `Enablement and cost control`, но для мобильных приложений iOS и Android.

*Разница с Web.* Автоматической инжекции нет: в мобильных приложениях нет HTML-страниц. Разработчик встраивает **OneAgent for mobile** в код приложения при сборке.

- **Android.** Подключается **Dynatrace Android Gradle plugin** (опубликован в Maven Central) на уровне top-level `build.gradle` / `build.gradle.kts`. Plugin использует bytecode instrumentation (Java / Kotlin / другие JVM-языки), обрабатывает source-файлы основного модуля и сторонних библиотек до R8-обфускации. Native-код, web-компоненты и resource-файлы (XML layouts) автоматически не инструментируются.
- **iOS.** Рекомендуемый способ интеграции: **Swift Package Manager** (`https://github.com/Dynatrace/swift-mobile-sdk.git` через `File → Swift Packages → Add Package Dependency` в Xcode). CocoaPods исторически поддерживался, но новые версии OneAgent SDK там больше не публикуются: для получения хотфиксов рекомендуется миграция на SPM. Static builds и Carthage для OneAgent for iOS перестали поддерживаться, начиная с версии 8.323.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/mobile-applications/instrument-android-app/instrumentation-via-plugin -->

**OneAgent for mobile собирает:**

- **Crash reports**: native crashes, Java / Kotlin exceptions, Swift / Objective-C exceptions.
- **HTTP-запросы и тайминги**: через автоматическую инструментацию URLSession / OkHttp.
- **User actions**: запуски, тапы по экранам, переходы между активностями.
- **Lifecycle events**: cold start, warm start, suspend, resume.

*Типовое применение.* Отслеживание падений на реальных устройствах, анализ каких моделей телефонов или версий Android / iOS проблемнее всего, реальное время входа в приложение на разных устройствах и в разных регионах.

---

## 🎓 ТЕОРИЯ: как RUM устроен изнутри

### Принцип: агент на стороне клиента

OneAgent на сервере живёт внутри JVM или process tree и собирает телеметрию изнутри. RUM работает **иначе**: агент на стороне пользователя, в браузере или мобильном приложении.

Это фундаментально меняет наблюдаемость. Серверный агент видит: «запрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, потому что:

- 200 мс запрос шёл до дата-центра (мобильный интернет, плохой Wi-Fi).
- 35 мс обрабатывал сервер.
- 250 мс ответ шёл обратно.
- 245 мс браузер парсил HTML, исполнял JavaScript, рендерил DOM.

Без RUM видно только 35 мс. С RUM: все 730 с разбивкой на каждый этап.

### Что собирает Web-агент (ruxit.js)

При загрузке страницы `ruxit.js` подключается первым делом. Он использует Browser Performance API (`window.performance`, `PerformanceObserver`, `Navigation Timing API`, `Resource Timing API`) и собирает:

- **Core Web Vitals**: LCP (Largest Contentful Paint, измеряется в Chromium-браузерах через Google-предоставленный API), CLS (Cumulative Layout Shift) и метрика отзывчивости на ввод (FID: First Input Delay в более старых версиях, INP: Interaction to Next Paint в актуальных). LCP для Chromium доступен напрямую; для прочих браузеров используется собственная Visually complete-метрика Dynatrace.
- **Resource timings**: сколько времени качался каждый CSS, JS, картинка, AJAX-запрос.
- **Navigation timings**: сколько длились DNS lookup, TCP connect, TLS handshake, ответ сервера, парсинг HTML.
- **User actions**: три типа: **Load actions** (загрузка страницы по URL), **XHR actions** (XmlHttpRequest или `fetch()`-вызовы и связанные DOM-изменения) и **Custom actions** (определяет разработчик через JS API). RUM-агент «оборачивает» их и связывает с backend-запросами, которые пошли в результате действия.
- **JavaScript errors**: необработанные исключения, ошибки в Promise.
- **Network errors**: неудачные AJAX (HTTP 5xx, таймауты, CORS-отказы).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-actions -->

Поддержка Internet Explorer 11 прекращена начиная с RUM JavaScript 1.293: для legacy-приложений на IE остаются только OneAgent serverside-данные.

Все эти данные отправляются **beacon'ом**: небольшим HTTP-запросом к Dynatrace cluster (конкретно на ActiveGate или напрямую в cluster node). В Managed тенанте beacon идёт к ActiveGate, который пересылает его в Cluster Management Console.

### User session vs User action

**User action**: атомарное действие пользователя: клик, переход по ссылке, отправка формы. RUM-агент связывает каждый user action с **цепочкой backend-запросов**, которые он вызвал. Получается сквозная трассировка: клик в браузере → HTTP-запрос → сервис → база → ответ.

**User session**: последовательность user actions одного пользователя, сгруппированных по одному client-id cookie и временному окну. По умолчанию session завершается:
- **Web**: после 30 минут бездействия (inactivity timeout).
- **Mobile / Custom**: после 10 минут бездействия.

Новая session с тем же пользователем считается отдельной: у неё свой session-id. Только что закрывшаяся сессия может оставаться в UI ещё какое-то время до полной финализации.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/user-session -->

**Один user: много сессий.** Если пользователь заходит каждое утро на неделе, это 5 сессий. Если на одном устройстве дважды в день: 14 сессий. Это важно для биллинга (цена в лицензии за user actions, не за пользователей) и для аналитики (retention: какой процент пользователей возвращается на следующий день).

### Apdex: User experience score

Apdex (Application Performance Index): единая метрика, которая показывает производительность приложения и влияние ошибок на пользовательский опыт. Dynatrace для каждого user action классифицирует его как **Satisfied**, **Tolerating** или **Frustrated** на основании настроенного на приложение порога; user actions с JavaScript-ошибками автоматически попадают в **Frustrated**.

Итоговый Apdex score лежит в диапазоне 0.0–1.0 и в Dynatrace разбит на пять уровней:

- **Excellent**: 0.94–1.0
- **Good**: 0.85–0.94
- **Fair**: 0.7–0.85
- **Poor**: 0.5–0.7
- **Unacceptable**: < 0.5

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings -->

Пороги действий настраиваются на странице **User experience score** (увидим в Теме 2). Помимо action-уровня Apdex, в Dynatrace есть session-level **User Experience Score**, который классифицирует сессию целиком (Satisfying / Tolerating / Frustrating).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings -->


### Классический UI vs Apps-интерфейс

**В air-gapped Managed новый Apps-интерфейс (Users & Sessions app) пока не активирован**, и мы работаем с классическим list-view. Это не устаревшая функциональность, это параллельные интерфейсы с разным UI: классический (stable в Managed) и новый (SaaS-first). В 2026 году Managed ещё полностью не мигрировал на Apps-модель, поэтому в учебнике опираемся на классический UI.

### Счётчик `278` в навигационной панели

На всех страницах тенанта в верхней панели виден значок `278` рядом с кнопкой пользователя. Это количество активных проблем, зарегистрированных Davis AI в текущий момент. Счётчик живой, обновляется в реальном времени. Клик открывает список Problems. Это не RUM-специфично: счётчик виден на любой странице.

### Как ingest RUM-данных связан с air-gapped контекстом

В SaaS Dynatrace RUM-beacon пользовательского браузера идёт напрямую в `<tenant>.live.dynatrace.com`. В Managed такая схема требовала бы, чтобы каждый компьютер клиента из интернета мог достучаться до вашей Managed-инсталляции, это нарушает air-gapped принцип.

**Что делает beacon:**

- При **auto-injection** (OneAgent встроил `ruxit.js` сам) beacon идёт обратно на тот же web/app сервер на root-relative путь с префиксом `rb_` (например, `/rb_xxxxxxxxxx`); OneAgent на этом сервере перехватывает beacon и пересылает данные в кластер.
- При **agentless monitoring** (тег вставлен в шаблон вручную) beacon по умолчанию отправляется на endpoint Cluster ActiveGate (URL вида `/bf` или `/bf/<id>`).

**Решение в Managed:**
- Для внутренних приложений (корпоративный портал, ДБО для сотрудников): beacon идёт через ActiveGate внутри сети либо через web-сервер с OneAgent.
- Для интернет-приложений (публичный сайт банка, мобильное приложение для клиентов): ставят ActiveGate в DMZ: он смотрит наружу, принимает beacon'ы, пересылает внутрь на Cluster через защищённый канал.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/initial-setup/firewall-constraints-for-rum -->

Схема ActiveGate в DMZ обсуждалась в Дне 1, Тема 2 «Компоненты Dynatrace». В настройках Web enablement задаётся endpoint, на который браузер шлёт beacon: критично, чтобы он был достижим с устройств пользователей.

### Cost control: почему это важно в Managed

В SaaS Dynatrace лимиты биллятся помесячно, превышение: автоматический overage charge. В Managed лицензия фиксирует максимум User Actions в месяц. При превышении Dynatrace **не прекращает запись**, но начинает сэмплировать: случайно отбрасывает часть сессий.

*Типовой сценарий.* Обычный день: 500 тыс. user actions. Пиковый день (выплаты, распродажа): 2 млн. При лицензии 30 млн/месяц один пиковый день «съедает» ~7% квоты. Важно либо закладывать буфер при покупке лицензии, либо включать adaptive sampling: Dynatrace автоматически режет cap при приближении к лимиту.

### Ключевые термины

- **RUM (Real User Monitoring)**: сбор данных о реальных пользователях с клиентской стороны.
- **Synthetic Monitoring**: противоположность: роботы-эмуляторы ходят по сайту по расписанию. Разберём в Теме 6.
- **User Action**: одно действие пользователя: клик, переход, отправка формы.
- **User Session**: последовательность user actions одного пользователя.
- **Beacon**: HTTP-запрос от браузера/мобильного приложения к Dynatrace с телеметрией.
- **Apdex (User Experience Score)**: индекс удовлетворённости пользователей.
- **LCP / FID / CLS (Core Web Vitals)**: индустриальные метрики скорости веб-страницы.
