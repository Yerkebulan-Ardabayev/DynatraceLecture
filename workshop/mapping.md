# Карта соответствия: воркшоп «Ключ-Астром» → курс dt-crawler → тенант guu84124

Этап 2. Источники: `ОБЗОР.md` (темы и порядок КА), хронометражи этапа 1 (таймкоды, формат [день/часть ММ:СС] от начала части), `study_plan.yaml` (темы курса), `ui_elements.json` (снапшот тенанта, 166 маршрутов), `empty_screens_todo.md` (известные дыры). Поверх снапшота: живая досверка тенанта guu84124 от 2026-07-28 (версия 1.343.92): статусы с пометкой «сверено вживую» опираются на неё. Главное ограничение досверки: аккаунт демо-тенанта read-only («Your user does not have the necessary write permissions»), любые демо создания ведутся формой без сохранения или на существующих объектах.

Обозначения статуса:
- **показуемо** = маршрут есть в снапшоте тенанта, экран с данными;
- **показуемо\*** = экран есть, но поверх SaaS-баннер («Try the new…», «Analyze sessions in the new…»); в Managed баннера не будет, на демо его не читаем вслух (CONTENT_POLICY §4.5);
- **нет данных** = экран есть, данных в снапшоте нет; чем засеять, написано в колонке «Замена РГС/демо»;
- **нет в Managed** = SaaS-only, в материал не попадает (объясняем словами «в Managed это …»);
- **не сверено** = в снапшоте отсутствует, требуется проверка живым тенантом (кандидат в пре-флайт).

Демо-данные тенанта (замена боевых данных РГС): веб-приложение `www.angular.easytravel.com`, мобильное `easyTravel Mobile`, ~244 сервиса, хосты easytravel*, живые Problems. Удачное совпадение: сам курс КА дни 1-3 тоже вёлся на демо easyTravel/TravelUp, так что «боевые» примеры нужны только для переноса жанра дней 4-5.

---

## День 1 КА (часть 1): архитектура, шлюзы, агент, обзор интерфейса

| Тема КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Варианты инсталляции: SaaS / Managed / офлайн [Д1ч1 06:25] | day-1 / architecture | теория по доке + `/ui/hub` | не требуется (теория) | показуемо |
| Кластер: ноды, Cassandra/Elasticsearch/ФС [Д1ч1 09:38] | day-1 / architecture | слайд/дока; UI-опоры нет | не требуется (теория) | показуемо (как слайд) |
| Активные шлюзы: кластерный и среды [Д1ч1 18:31] | day-1 / components | `/ui/settings/builtin:deployment.activegate.updates`, `/ui/settings/builtin:activegate-token` | не требуется | показуемо |
| Расширения (аналогия iPhone) [Д1ч1 30:13] | day-1 / architecture + components | `/ui/hub` (Extensions) | расширения из Hub тенанта | показуемо (SaaS-баннер Hub не читаем) |
| Единый агент: автовнедрение, оверхед-демо [Д1ч1 36:21, демо 45:05] | day-1 / oneagent-principles | `/ui/settings/builtin:oneagent.features`, `/ui/settings/builtin:process.process-monitoring`; демо оверхеда: страница хоста | процессы OneAgent на хосте easytravel* | показуемо (страница хоста: не сверено, см. дыру №2) |
| Обзор интерфейса: тур «по часовой стрелке», таймфрейм, поиск [Д1ч1 49:53] | day-1 / ui-overview | `/ui/dashboards`, `/ui/services`, `/ui/applications`, `/ui/problems` | демо-окружение Demo Live | показуемо |
| Топология по уровням: ДЦ → хост → … → приложение [Д1ч1 1:08:47] | day-1 / smartscape + key-objects | Smartscape: `/#smartscape` (сверено вживую 07-28: заголовок «Smartscape topology», слои живые: Applications 124, Services 5232, Processes 111821, Hosts 2378, Data centers 17) | хост easytravel вместо «Казань / Easy Travel CPU» | показуемо (запасной показ на случай сбоя: карточка сервиса → «View service flow») |

## День 1 КА (часть 2): страницы сущностей, установка агента, метрики, базовые линии

| Тема КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Страница хоста сверху вниз [Д1ч2 04:46] | day-1 / key-objects; day-2 / hosts-processes | список хостов: пункт Hosts → `/#newhosts` (сверено вживую 07-28: заголовок «Hosts», «48 Hosts»; НЕ /ui/entity/list/HOST) | хост `easytravel` (Linux, VMware) | показуемо (список); внутренности карточки хоста всё ещё **не сверено** |
| Режимы агента: full stack vs инфраструктура [Д1ч2 05:37] | day-1 / components | `/ui/settings/builtin:deployment.oneagent.default-mode` | не требуется | показуемо |
| Проповедь тегов (мантра курса) [Д1ч2 11:30] | дыра курса (тем нет) | `/ui/settings/builtin:tags.auto-tagging` (сверено вживую 07-28: экран «Automatically applied tags» жив) | существующие теги easytravel, easytravel-app, ET Angular | блок добавлен (Д3ч2 автотеги); показуемо, но read-only: демо на существующих тегах |
| Страница процесса [Д1ч2 24:12] | day-2 / hosts-processes | со страницы хоста → процесс | Apache/Tomcat easytravel | не сверено (entity-страницы в снапшот не входили) |
| Страница сервиса: 3+1 базовые метрики [Д1ч2 27:15] | day-2 / service-cards | `/ui/services` → карточка сервиса (URL вида `/#services/serviceOverview;id=SERVICE-...`) | easyTravel Customer Frontend | показуемо (список и карточка; карточка сверена вживую 07-28: плитки Dynamic web requests, секция «Understand dependencies» с кнопками View service flow / View backtrace / View distributed traces / View web requests / View related logs) |
| Мониторинг веба: авто-инжект vs ручная вставка JS [Д1ч2 34:01] | day-3-4 / instrumentation | `/ui/settings/builtin:rum.web.enablement` и соседние | www.angular.easytravel.com | показуемо |
| Мобильные: мастер инструментирования [Д1ч2 43:44] | day-3-4 / instrumentation | `/ui/settings/builtin:rum.mobile.enablement` | easyTravel Mobile | показуемо |
| Установка агента: токен, «две команды», статус развертывания [Д1ч2 47:00] | ближайшая: day-1 / components | Deploy Dynatrace → `/#deploy` (сверено вживую 07-28: заголовок «Deploy Dynatrace», кнопка «Start installation», блок «Install ActiveGate to extend your monitoring») | демо мастера без реальной установки (как в оригинале) | блок в сценарии дня 1 есть; показуемо (вход); экран мастера после «Start installation» **не сверено** |
| Метрики: браузер метрик, конструктор-«мейковер» [Д1ч2 51:36] | day-1 / data-explorer | `/ui/metrics`, `/ui/data-explorer` | метрики easyTravel, трюк (CPU+RAM)/2 | показуемо |
| Базовые линии и аномалии «на пальцах» [Д1ч2 1:15:17] | day-1 / baselines | `/ui/settings/builtin:anomaly-detection.services` и соседние; бейзлайн на графике Data Explorer | график CPU easytravel | показуемо |

## День 2 КА (часть 1): проблема и root cause, сервисы, БД, агрегации

| Тема КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Раздел «Проблемы»: таймлайн, фильтры, 5 типов через иконки [Д2ч1 05:22] | day-1 / problems-feature | `/ui/problems` | живые проблемы Demo Live | показуемо\* |
| ГЛАВНОЕ ДЕМО: карточка проблемы + спуск до метода [Д2ч1 16:35] | day-2 / problems-navigation; day-3-4 / incident-lifecycle | `/ui/problems` → карточка → сервис → анализ через плитки Dynamic web requests → hotspots → stack trace | живая проблема тенанта вместо Authentication Service | показуемо\* (блоки карточки сверены вживую 07-28: Business impact analysis, Root cause, Visual resolution path, Comments; эталонный сюжет «Response time degradation» с корнем в базе наблюдался; наличие «богатой» проблемы на день лекции проверяется пре-флайтом) |
| Что такое сервис, типы сервисов, очереди [Д2ч1 36:57] | day-2 / services-overview | `/ui/services`, `/ui/settings/builtin:service-detection-rules` | 244 сервиса тенанта | показуемо |
| Три подхода к мониторингу БД [Д2ч1 45:05] | day-2 / databases | `/ui/databases` | БД easyTravel | показуемо |
| Метрики сервиса, медиана vs среднее, перцентили [Д2ч1 55:52] | day-2 / service-cards | карточка сервиса → метрики | сервис easyTravel | показуемо |

## День 2 КА (часть 2): инструменты анализа сервиса, аномалии, SLO

| Тема КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Анализ времени отклика, hotspots, гистограмма [Д2ч2 00:00] | day-3-4 / response-analysis | карточка сервиса → Analyze response time | сервис easyTravel | показуемо |
| Частота отказов, разбор 500-х [Д2ч2 04:00] | day-3-4 / response-analysis | карточка сервиса → Analyze failure rate | ошибки easyTravel | показуемо |
| Трассировки: дерево, таймлайн, цвета [Д2ч2 05:40] | day-3-4 / mlt-concepts | `/ui/diagnostictools/purepaths` | трейсы easyTravel | показуемо\* |
| Бэктрейс и поток обслуживания [Д2ч2 11:43] | day-3-4 / service-flow | карточка сервиса → Backtrace / Service flow | цепочка easyTravel | показуемо |
| Раздел «Анализ»: multidimensional, «Сохранить вид» [Д2ч2 15:31] | day-3-4 / mlt-concepts | `/ui/diagnostictools` | запросы easyTravel | показуемо\* (баннер про Notebooks не читаем) |
| Преобразование анализа в метрику (демо упало о лимит) [Д2ч2 21:38] | day-3-4 / mlt-concepts | `/ui/diagnostictools` → Create metric | метрика по запросам easyTravel | показуемо (лимит расчётных метрик проверить пре-флайтом, у КА демо упало) |
| Ключевые запросы [Д2ч2 31:17] | day-2 / service-cards | карточка сервиса → Key requests | пометить запрос easyTravel | показуемо (пункт меню сверить вживую) |
| Правила именования сервисов, обнаружение сбоев [Д2ч2 35:56] | day-3-4 / service-object + response-analysis | `/ui/settings/builtin:service-splitting-rules`, `failure-detection.*` | не требуется | показуемо |
| Тонкая настройка аномалий сервиса [Д2ч2 44:58] | day-1 / baselines; day-3-4 / response-analysis | `/ui/settings/builtin:anomaly-detection.services` | не требуется | показуемо |
| SLO и бюджет ошибок [Д2ч2 1:06:19] | day-3-4 / sli-slo-sla | `/ui/slo`, `/ui/settings/builtin:monitoring.slo` | живые SLO тенанта («Hourly SLO for easytravel.com homepage», «hourly SLO www.easytravel.com») | показуемо (сверено вживую 07-28: «55 SLOs», колонки Name / Status / Actions / Details; строки с ошибкой «At least one operand in the given metric expression provides no data» = живая иллюстрация привязки по идентификатору/тегу; создание SLO read-only) |

## День 3 КА (часть 1): RUM, сессии, USQL

| Тема КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Заведение приложений, правила обнаружения [Д3ч1 03:25] | day-3-4 / app-detection; day-5 / app-segments | `/ui/settings/builtin:rum.web.app-detection` | правило для www.angular.easytravel.com (вместо кинопоиск/yandex) | показуемо |
| Инфографика приложения: производительность [Д3ч1 12:46] | day-3-4 / app-cards; day-5 / ux-metrics | `/ui/applications` → карточка приложения | www.angular.easytravel.com (вместо TravelUp) | показуемо (карточка приложения: сверить вживую) |
| Ошибки как фактор Apdex [внутри блока Д3ч1 12:46-37:35] | day-5 / ux-metrics | карточка приложения → ошибки | JS/HTTP-ошибки easyTravel | показуемо (наличие ошибок проверяется пре-флайтом) |
| Поведение пользователей: новые/вернувшиеся, конверсии [Д3ч1 37:36] | day-5 / ux-metrics + journeys | карточка приложения → поведение | демо-конверсии easyTravel | показуемо |
| Сессии: фильтры, водопад, переход «в один клик» в бэкенд [Д3ч1 44:01, кульминация 55:09] | day-3-4 / sessions; day-5 / rum | `/ui/user-sessions` | сессии easyTravel | показуемо\* |
| USQL: лайфхак с фильтрами, метрика, воронка [Д3ч1 1:00:44] | day-5 / usql + journeys | `/ui/user-sessions/query` | воронка по действиям easyTravel («норвежских ребят» заменить на локальный юмор) | показуемо |
| Мобильные крэши [Д3ч1 1:13:03] | day-3-4 / thresholds (crash rate) | приложение easyTravel Mobile | крэши мобильного демо | **не сверено** (есть ли крэш-данные, проверить вживую) |

## День 3 КА (часть 2): настройки RUM, дашборды, автотеги, оповещения, синтетика, AppSec

| Тема КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Настройки веб-приложения: Session Replay, маскирование, тег пользователя, SPA [Д3ч2 00:00] | day-3-4 / sessions + key-actions; day-5 / session-replay | `/ui/user-sessions/replay-landing`, `/ui/settings/builtin:sessionreplay.*`, настройки приложения | реплеи easyTravel | показуемо\* (наличие записей проверить вживую) |
| Дашборды: плитки, JSON-перенос, анонимный доступ (кейс ТВ) [Д3ч2 15:00] | day-1 / dashboards | `/ui/dashboards`, `/ui/settings/builtin:dashboards.*` | готовые дашборды Demo Live + сборка с нуля | показуемо |
| Автотеги (тег NorwayTeam по IP «192.») [Д3ч2 28:40] | дыра курса (темы нет) | `/ui/settings/builtin:tags.auto-tagging` (сверено вживую 07-28: экран «Automatically applied tags» жив) | разбор правил существующих тегов (easytravel, ET Angular); форма создания без сохранения | блок в сценарии есть; показуемо, но **read-only**: полный цикл создания только на стенде клиента |
| Кастомное оповещение в 3 шага [Д3ч2 33:45] | day-5 / alerting-profiles + alerting-logic | `/ui/settings/builtin:anomaly-detection.metric-events`, `alerting.profile`, `problem.notifications` | формы трёх шагов без сохранения (read-only) либо разбор существующей конфигурации | показуемо\* (сверено вживую 07-28: классический экран «Metric events» жив под SaaS-баннером, колонки Enabled / Summary / Query type / Model type / Management zone, Overview of limits: по 100 конфигураций каждого типа; но **read-only**: сохранение только на стенде клиента) |
| Синтетика: браузерный и HTTP-монитор [Д3ч2 50:15] | day-5 / synthetic | `/ui/synthetic` = 403 на тенанте; настройки `synthetic.*` живы | показ настроек + рассказ по офиц. Managed-доке | **нет данных** (известная дыра курса; фолбэк уже в explanation) |
| Модуль безопасности приложений [Д3ч2 52:35] | day-3-4 / appsec | `/ui/security/overview` + настройки appsec.* | уязвимости демо-тенанта | показуемо (обзор); списки уязвимостей под SaaS-баннером |
| Атрибуты запросов (Journey ID / Client IP) [Д3ч2 55:45] | дыра курса (темы нет) | Settings → Server-side service monitoring → Request attributes, классический маршрут `/#settings/server/requestattributes` (сверено вживую 07-28: заголовок «Request attributes», кнопка «Define a new request attribute») | показ экрана настройки; результат демонстрируется MDA-видом «Easy Trave User Request Attribute View1» | блок в сценарии есть; экран жив, но список пуст («No request attributes defined!») и **read-only** («Missing permissions to create or edit request attributes») |

## День 4 КА (РГС): жанр «разбор на живой системе»

Переносится как ЖАНР на наш прикладной день (4-й день воркшопа по дефолт-параметрам). Данные РГС заменяем демо-данными easyTravel, а у клиента: его боевой инсталляцией.

| Элемент дня 4 КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Сжатый повтор архитектуры «от данных» за 17 мин [Д4 00:03] | day-1 / architecture + components | те же, что день 1 | те же | показуемо |
| JS-агент вживую через DevTools Network [Д4 00:20] | day-3-4 / instrumentation | браузер поверх www.angular.easytravel.com + DevTools | ruxitagentjs/dtagent на easyTravel | **не сверено** (доступность страницы приложения из класса; фолбэк: скриншоты) |
| Веб-визор: реконструкция дефекта [Д4 00:46] | day-5 / session-replay | `/ui/user-sessions/replay-landing` | реплей сессии easyTravel с ошибкой | показуемо\* (наличие реплеев проверить) |
| Кейс «заявка агента»: поиск сессии, часовой пояс, 254 ошибки [Д4 01:13] | day-5 / rum + journeys | `/ui/user-sessions` + фильтры | сессия easyTravel с JS-ошибками; часовой пояс аудитории (KZ, UTC+5) | показуемо |
| Сквозная трассировка фронт → бэк [Д4 01:23] | day-3-4 / mlt-concepts + service-flow | сессия → действие → PurePath | цепочка easyTravel (вместо Nginx→Netty→Node→Postgres) | показуемо |
| Разбор реального инцидента: все блоки карточки, обратная трассировка [Д4 01:30, развязка 02:03] | day-3-4 / incident-lifecycle | `/ui/problems` → карточка | живая проблема тенанта | показуемо\* |
| Корреляция с внешними логами (Splunk, correlation ID) [Д4 01:26, 02:07] | day-3-4 / mlt-concepts (логи) | `/ui/logs-events` | лог-вьювер тенанта, внешние SIEM словами | показуемо (без Splunk-специфики) |

## День 5 КА (РГС): интерактив «клиент за рулём»

| Элемент дня 5 КА (таймкод) | Тема курса | Маршрут | Замена РГС/демо | Статус |
|---|---|---|---|---|
| Производительность vs поведение, разбивки, геокарта [Д5 00:16] | day-5 / ux-metrics + app-cards | карточка приложения | www.angular.easytravel.com | показуемо |
| Живая находка: гео-аномалия (VPN) [Д5 00:24] | day-5 / ux-metrics | геокарта приложения | аномалии демо-трафика (IP синтетические, честно оговаривать, как оригинал в Д3ч1) | показуемо с оговоркой |
| Глубокий Apdex: периоды, вычистка мусорных ошибок [Д5 00:26] | day-5 / ux-metrics | карточка приложения → Apdex; настройки Apdex | ошибки easyTravel (вместо 0.83→0.9 РГС) | показуемо |
| Топ ошибок, drill-in до stacktrace и сессий [Д5 00:36] | day-5 / ux-metrics + rum | карточка приложения → ошибки | JS/HTTP ошибки демо | показуемо |
| Метрики здоровья (vitals) [Д5 00:44] | day-5 / ux-metrics | карточка приложения | демо-данные | показуемо (состав vitals сверить с Managed-докой, не с SaaS) |
| Анализ снижения времени отклика, method hotspots [Д5 00:50] | day-3-4 / response-analysis | сервис → Analyze response time → hotspots | сервис easyTravel | показуемо |
| Дашборд с нуля: плитка проблем, CPU/RAM/диск со светофором, авто-добавление по тегу [Д5 00:59], health-плитки [Д5 01:23] | day-1 / dashboards | `/ui/dashboards` → новый дашборд | хосты easytravel, пороги 0/40/80 | показуемо |
| Тегирование + зоны управления, фильтр интерфейса по зоне [Д5 01:25] | дыра курса (тем нет) | `/ui/settings/builtin:tags.auto-tagging` («Automatically applied tags»), `/ui/settings/builtin:management-zones` («Management zones settings»); оба сверены вживую 07-28 | существующая зона «EasyTravel Angular» вместо OFR; теги easytravel / ET Angular | блоки в сценариях есть; показуемо, но **read-only**: демо фильтра на существующей зоне, создание только на стенде клиента |
| Ключевые действия, дробление из-за ID в URL, правила именования [Д5 01:41] | day-3-4 / key-actions | настройки приложения → naming rules | действия easyTravel (вместо «расчёт тарифа ОСАГО») | показуемо (экран naming rules сверить вживую) |
| Поведение: роботы, отказы [Д5 01:59] | day-5 / ux-metrics | карточка приложения → поведение | демо-данные | показуемо |
| Цели конверсии + воронка USQL + метрика с оповещением [Д5 02:13] | day-5 / journeys + usql | `/ui/user-sessions/query` | воронка бронирования easyTravel | показуемо |

---

## Темы курса БЕЗ образца в КА (сценарий строим без референса подачи)

| Тема курса | Комментарий |
|---|---|
| day-2 / containers, kubernetes | В КА-курсе контейнеры/K8s не разбирались (только упоминание оверхеда на OpenShift). Сценарий: своя подача по паттерну «настройки + рассказ», ритм заимствуем. |
| day-2 / os-monitoring, oneagent-infra | КА покрывает вскользь (страница хоста). Расширяем самостоятельно. |
| day-3-4 / mlt-concepts (логи отдельно) | У КА логи только в связке с трассировкой и Splunk-разговоре дня 4. Лог-вьювер покажем отдельно. |
| day-3-4 / reliability-config | Health Experience: «In development» в Managed (см. empty_screens_todo). Уже переписано в курсе через SLO/anomaly/alerting: сценарий так и ведём. |
| day-3-4 / thresholds (RUM-аномалии) | У КА только упомянуто в настройках приложения. Своя подача. |
| day-5 / api | КА не показывал API (только Swagger мельком в туре интерфейса, Д1ч1). Покажем `/ui/access-tokens` + пример запроса. |
| day-1 / dem | Обзорная тема нашего курса, у КА размазана по дням 1 и 3. Собираем из Д1ч1 (обзор) + Д3ч1 (мотивация RUM). |

## Сводка дыр (не маскируем)

1. **Smartscape**: ЗАКРЫТО живой досверкой 07-28: экран работает по `/#smartscape` (заголовок «Smartscape topology», слои с числами живые). Service Flow остаётся запасным показом на случай сбоя.
2. **Список хостов / страница хоста**: список ЗАКРЫТ досверкой 07-28: пункт Hosts → `/#newhosts` (НЕ /ui/entity/list/HOST), заголовок «Hosts», «48 Hosts», живой хост `easytravel` (Linux, VMware). ОСТАЁТСЯ: внутренности карточки хоста (блоки, список процессов) не сверены: проверить на пре-флайте.
3. **SLO**: ЗАКРЫТО досверкой 07-28: `/ui/slo` не пуст, «55 SLOs», easytravel-SLO живые. Засев не нужен; пре-флайт лишь проверяет, что easytravel-SLO живы и показывают значения. Строки с ошибкой метрики оставлены как живая иллюстрация привязки по идентификатору/тегу.
4. **Synthetic**: `/ui/synthetic` 403 на тенанте (известная дыра курса). Фолбэк: настроечные экраны + рассказ по Managed-доке; либо запросить право/модуль (вопрос пользователю).
5. **Session Replay записи, мобильные крэши, «богатая» проблема с root cause, лимит расчётных метрик**: наличие живых данных проверяется пре-флайтом (этап 4). По «богатой» проблеме досверка 07-28 подтвердила блоки карточки и эталонный сюжет («Response time degradation», корень в базе), но проблемы демо-тенанта сменяются: свежую выбирает пре-флайт.
6. **Дыры плана курса относительно КА**: установка агента (Deploy Dynatrace), автотеги, зоны управления, Request Attributes: блоки в сценарии добавлены, экраны сверены живьём 07-28. Ограничения: мастер после «Start installation» не сверен; автотеги/зоны/Request attributes read-only (демо на существующих объектах); список Request attributes пуст.
7. **Metric events (кастомные оповещения)**: ЧАСТИЧНО ЗАКРЫТО досверкой 07-28: классический экран «Metric events» жив под SaaS-баннером (колонки и Overview of limits сверены). ОСТАЁТСЯ: аккаунт read-only, сценарий «3 шага» ведём формами без сохранения; полный цикл только на стенде клиента.
8. **Названия пунктов меню для блоков «Как найти»**: ЗАКРЫТО досверкой 07-28: группы и спорные пункты сверены (Automations, Releases, Service-Level Objectives в хвосте Infrastructure Observability между Extensions и Application Observability; Frontend в Application Observability; Web, Mobile, Session Segmentation, Query User Sessions, Session Replay, Synthetic, Custom Applications в Digital Experience; Manage: Dynatrace Hub, Deploy Dynatrace, Deployment Status, OneAgent Health, System Notifications, Access Tokens, Credential Vault, Settings). Запасная навигация: глобальный поиск (поле «Search <имя окружения>...» в верхней панели) и поле «Filter menu...» в левом меню.
9. **Права demo-аккаунта (НОВОЕ, досверка 07-28)**: аккаунт read-only («Your user does not have the necessary write permissions»; у Request attributes «Missing permissions to create or edit request attributes»). Все демо создания (теги, зоны, metric events, alerting, дашборды, request attributes) на демо-тенанте ведутся формой без сохранения либо разбором существующих объектов; полный цикл создания возможен только на стенде клиента (режим А дня 4).

## Замены примеров РГС → демо (сводно)

| РГС-пример из дней 4-5 | Наш эквивалент |
|---|---|
| ЛК РГС (портал агентов) | `www.angular.easytravel.com` |
| Расчёт тарифа ОСАГО (ключевое действие) | Действие бронирования easyTravel (Booking) |
| Сессия агента с 254 ошибками | Сессия easyTravel с JS/HTTP-ошибками (найти пре-флайтом) |
| Инцидент ЛК РГС (карточка проблемы) | Живая проблема Demo Live с root cause |
| Зона управления OFR | Существующая зона «EasyTravel Angular» (создание на демо-тенанте read-only; своя зона только на стенде клиента) |
| Дашборд руководства РГС / «перфмон» Антона | Дашборд с нуля на хостах easytravel (пороги 0/40/80) |
| Часовой пояс Благовещенска | Часовой пояс аудитории (Казахстан, UTC+5): учитывать при поиске инцидентов |
| Splunk-корреляция, correlation ID | Лог-вьювер тенанта + рассказ про внешние SIEM словами |
| «Норвежские ребята» (USQL-метрика count_norway) | Аналогичная гео-метрика по демо-трафику easyTravel |
