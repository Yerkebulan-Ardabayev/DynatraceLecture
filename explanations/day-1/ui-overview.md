> 📅 **День 1: Введение в систему Dynatrace** → Тема 5 из 11: «Обзор интерфейса и навигации»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/dashboards -->
>
> 🔖 **Редакция от 2026-04-27.** Блок Источников переведён в строгий Managed-режим: ссылки на /docs/, /platform/, /apps/ удалены, оставлены только страницы из раздела `/managed/`. В air-gapped Managed Apps-интерфейс / Notebooks / Workflows / Davis Problems app не активированы. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (Dynatrace Managed: air-gapped):**
>
> - [Welcome to Dynatrace Managed Documentation](https://docs.dynatrace.com/managed): корень раздела для air-gapped инсталляций
> - [Smartscape](https://docs.dynatrace.com/managed/shortlink/smartscape): топология, которая лежит в основе экранов Hosts/Services/Problems
> - [Observe](https://docs.dynatrace.com/managed/observe): корень раздела для всех Classic-экранов (Dashboards, Services, Applications, Databases, Problems, Releases)
> - [Davis AI](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai): engine, который наполняет экран Problems инцидентами (RCA, anomaly detection, multidimensional baselining)
> - [Release Monitoring](https://docs.dynatrace.com/managed/deliver/release-monitoring): раздел Releases, version detection, привязка изменений к change-tickets
> - [Management zones](https://docs.dynatrace.com/managed/shortlink/management-zones): фильтр верхней панели, до 5 000 MZ на окружение
> - [Manage your Dynatrace Managed](https://docs.dynatrace.com/managed/manage): администрирование, Hub, Settings 2.0, network zones, system notifications

## 📍 КАРТА: основные разделы интерфейса

| Раздел | Путь в меню | Прямая ссылка |
|---|---|---|
| Dashboards / панели | **Observe and explore → Dashboards** | `https://guu84124.live.dynatrace.com/ui/dashboards` |
| Services / сервисы | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` |
| Applications / приложения | **Application Observability → Frontend** | `https://guu84124.live.dynatrace.com/ui/applications` |
| Databases / базы | **Application Observability → Database Services** | `https://guu84124.live.dynatrace.com/ui/databases` |
| Problems / инциденты | **Observe and explore → Problems** | `https://guu84124.live.dynatrace.com/ui/problems` |
| Releases / релизы | **Automations → Releases** | `https://guu84124.live.dynatrace.com/ui/releases` |

**Структура главного меню слева.**

| Секция | Что внутри |
|---|---|
| **Favorites** | Закреплённые пользователем разделы (по умолчанию Dashboards, Deploy Dynatrace, Problems) |
| **Observe and explore** | Ежедневная работа: Dashboards, Data Explorer, Metrics, Logs, Problems, Smartscape Topology, Reports |
| **Infrastructure Observability** | Hosts, Technologies & Processes, Kubernetes, Containers, Cloud Foundry, AWS / Azure / GCP / VMware, Host Networking, Extensions |
| **Automations** | Releases, SLO |
| **Application Observability** | Frontend, Services, Distributed Traces, Database Services, Synthetic |
| **Application Security** | Уязвимости и атаки на приложения |
| **Digital Experience** | RUM и Synthetic: пользовательский опыт |
| **Business Analytics** | Бизнес-события и Session segmentation |
| **Manage** | Hub, Deploy Dynatrace, Settings |

**Верхняя панель.** Глобальный поиск (Ctrl+Shift+F: по именам хостов, сервисов, метрик, настроек). Фильтр **Management zones** (сегментация окружения по командам или бизнес-зонам). Выбор временного диапазона (по умолчанию Last 2 hours). Индикатор активных проблем и уведомлений.

---

## 🎬 Шесть главных экранов

### Шаг 1: Dashboards / панели

![Dashboards: список дашбордов с фильтрами](screenshots/day-1/ui-overview/dashboards/Dashboards-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Dashboards** → `https://guu84124.live.dynatrace.com/ui/dashboards`.

**Что на экране.** Все дашборды окружения. На этом демо-тенанте счётчик: **618 Dashboards**. Пресеты плюс пользовательские, накопленные за время жизни окружения.

В правом верхнем углу две кнопки:
- **Import dashboard**: загрузить шаблон из JSON. Полезно при переносе дашбордов между окружениями (например, с тестового на продуктивный кластер).
- **Create dashboard**: создать пустой дашборд.

**Фильтры слева.**
- **Ownership**: Any / Mine / Shared with me.
- **Favorite**: Any / Yes / No.
- **Owner**: фильтр по автору.
- **Tag**: по тегу, присвоенному при создании.
- **Preset**: только встроенные или только пользовательские.

**Таблица.** Колонки: **Favorite** (звёздочка для закрепления), **Name** (имя), **Popularity** (полоска частоты использования: видно, что реально применяется), **Modified at** (дата последнего изменения), **Owner** (автор). На этом демо видны реальные имена: Monitoring Overview, Hyper-V Overview, Agency Overview Dashboard, APDEX, Neoload Testing.

**Зачем дашборды.** Набор виджетов (график, таблица, SLO-индикатор, карта Smartscape) собирается на одной странице и сохраняется. Управление панелями: создание, редактирование, импорт JSON: описано в разделе [Dashboards Classic](https://docs.dynatrace.com/managed/analyze-explore-automate/dashboards-classic). Типичный банк делит дашборды на три слоя:
- **Оперативные**: для дежурной смены. Инфраструктура в реальном времени, активные инциденты, ключевые SLI.
- **Бизнесовые**: для руководства. Доступность ключевых систем, конверсия, объёмы транзакций.
- **Инженерные**: для отдельных команд. Метрики конкретного сервиса, логи, ошибки.

Дашборды поддерживают Management zones. Выбранная в верхнем фильтре зона автоматически сужает все виджеты на дашборде: один дашборд может обслуживать несколько команд без дублирования.

Подробнее дашборды разбираются в Теме 11.

### Шаг 2: Services / сервисы

![Services: список сервисов с фильтрами](screenshots/day-1/ui-overview/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Services** → `https://guu84124.live.dynatrace.com/ui/services`.

**Что на экране.** Все сервисы, которые OneAgent распознал на хостах окружения. На этом демо-тенанте: **244 Services**.

**Что такое сервис.** Логическая единица backend, обслуживающая запросы одного типа: REST, SOAP, gRPC, очередь сообщений, вызов базы данных. Определение задают правила Service Detection, OneAgent применяет их автоматически. Один Java-процесс может содержать несколько сервисов (три REST-эндпоинта в одном Tomcat). Несколько процессов могут быть одним сервисом (инстансы одной логической единицы). Подробнее о концепции и типах: в разделе [Application Observability → Services](https://docs.dynatrace.com/managed/observe/application-observability/services).

**Фильтры слева.**
- **Service type**: Web service, Web request service, Custom service, Messaging service, Background activity и ещё 6 опций (Queue listener, Database service и другие).
- **Problem impact**: Any / Impacted / Not impacted.
- **Technology**: .NET, .NET Remoting, Kafka, ActiveMQ Artemis, ActiveMQ Client и ещё 53 опции.

**Таблица.** Колонки: **Name** (автоматически формируемое имя из класса, URL-паттерна или технологии), **Response time median**, **Slowest 10%**, **Failure rate**, **Requests** (в минуту), **Actions**. Над таблицей индикатор `11 Services that match your query are associated with Davis-detected problems`: кнопка **Apply filter** сужает список до сервисов с активными проблемами.

**Карточка сервиса.** Клик по имени. В ней: всё для расследования: графики отклика и пропускной способности, топ-10 медленных запросов, список экземпляров процессов, связанные базы, топология входящих и исходящих вызовов, активные проблемы.

**Типичный сценарий.** Жалоба «что-то тормозит на странице платежей». Инженер ищет сервис `payment-service` в списке, открывает карточку, смотрит Response time, проваливается в медленные запросы, оттуда в трейс (PurePath). Видит, где именно в цепочке происходит задержка.

### Шаг 3: Applications / приложения

![Applications: на демо центр пустой](screenshots/day-1/ui-overview/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Frontend** → `https://guu84124.live.dynatrace.com/ui/applications`.

**Что на экране.** Frontend-сторона платформы. На этом демо-тенанте центральная область пустая, RUM-приложения не настроены.

**Что бывает на боевой инсталляции.** Список веб- и мобильных приложений с RUM-данными. На каждой карточке: число активных пользователей, медианное время загрузки страницы, процент сессий с ошибками, распределение по браузерам и географии.

**Место в общей картине.**
- **Services**: как работает бэкенд.
- **Applications**: как видят приложение пользователи в своих браузерах.

При расследовании инженер обычно начинает с Problems, переходит на Services (если инцидент backend) или Applications (если проблема в браузере или мобильном клиенте), дальше проваливается в детали.

**Что нужно, чтобы приложения попали сюда.**
- На веб-сервере установлен OneAgent.
- В `https://guu84124.live.dynatrace.com/ui/settings/applications-web` создано приложение.
- RUM-сниппет внедряется в HTML-страницы.

**ЕСЛИ → ТО: почему центр пустой или заполнен.**
- ЕСЛИ все три условия выше выполнены → приложения появляются в списке.
- ЕСЛИ OneAgent на веб-сервере не установлен → RUM-сниппет не внедряется, список пустой (как на этом демо).
- ЕСЛИ OneAgent есть, но приложение в `https://guu84124.live.dynatrace.com/ui/settings/applications-web` не создано → данные не привязываются к карточке.

Полная механика: Тема 4 (Digital Experience Monitoring).

### Шаг 4: Databases / базы данных

![Databases: список баз с фильтрами](screenshots/day-1/ui-overview/databases/Databases-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Database Services** → `https://guu84124.live.dynatrace.com/ui/databases`.

**Что на экране.** Базы данных, к которым обращаются сервисы под мониторингом. На этом демо-тенанте: **30 Databases**.

**Важный момент.** Это не «все базы в инфраструктуре клиента» и не «все базы, куда OneAgent имеет доступ». Только те базы, к которым хоть раз за период обратился сервис под мониторингом.

**ЕСЛИ → ТО: почему база видна или нет.** Список это прямое следствие трафика инструментированных сервисов:
- ЕСЛИ инструментированный сервис хоть раз за период обратился к базе → база появляется в списке.
- ЕСЛИ инстанс (например, PostgreSQL) существует в сети, но ни одно приложение под OneAgent его не использует → в списке его не будет, даже если он работает.

**Фильтры слева.**
- **Cloud provider**: AWS RDS, Azure.
- **Database technology**: H2, Derby Client, AWS DB2, IBM и ещё 6 опций.
- **Problem impact**: Any / Impacted / Not impacted.

**Таблица.** Колонки: **Name**, **Response time median**, **Slowest 10%**, **Failure rate**, **Requests**, **Actions**. На этом демо видны реальные имена: `[eks-live][easytrade-live-debugger] TradeManagement`, `[eks-live][unguard] likeDb`, `BB2-apache-tomcatjms-iis`. Имя формируется из контекста окружения и обращения.

**Ключевое свойство.** Данные снимаются **со стороны клиента базы**, не с самой базы. OneAgent инструментирует драйвер JDBC / ODBC и видит каждый запрос: какой SQL отправлен, сколько база на него отвечала, был ли ответ успешным. На самой базе OneAgent ставить не обязательно: работает и для unmanaged-хостов (облачная Managed-база типа AWS RDS). Проблемы «база отвечает медленно» видны всё равно. Механика инструментации JDBC/ODBC описана в разделе [Database Services Classic](https://docs.dynatrace.com/managed/observe/infrastructure-observability/databases/database-services-classic).

### Шаг 5: Problems / инциденты

![Problems: таблица активных проблем](screenshots/day-1/ui-overview/problems/Problems-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Problems** → `https://guu84124.live.dynatrace.com/ui/problems`.

**Что на экране.** Один из самых важных экранов платформы. Проблемы, которые Davis AI обнаружил автоматически на основе аномалий в метриках, событиях и трейсах.

**Временной график сверху.** Красные столбцы: распределение проблем по времени. На этом демо график плотный: следствие синтетических аномалий демо-окружения. На боевой инсталляции график обычно разреженный, новый красный столбец сразу привлекает внимание.

**Фильтры слева.**
- **Status**: Any / Open / Closed.
- **Severity**: Monitoring unavailable, Availability, Error, Slowdown, Resource, Custom.
- **Impact level**: Infrastructure / Services / Application / Environment.
- **Maintenance**: Any / Under maintenance / Not under maintenance.

**Таблица.** Колонки: **Problem** (заголовок и идентификатор `P-NNNNNNNN`), **Impacted** (число сущностей), **Affected** (главная сущность), **Root cause** (корневая причина), **Start date**, **Duration**, **Alerting profiles** (какие профили сработали: сразу видно, в какие интеграции ушла проблема).

**Особенность Problems в Dynatrace.** Это не отдельные метрики, а целостные инциденты.

**ЕСЛИ → ТО: как Davis сворачивает симптомы в один инцидент.**
- ЕСЛИ одновременно деградировали web-сервер, база и зависящие от неё сервисы → Davis AI не создаст шесть проблем, а создаст одну с корневой причиной «медленная база» и привяжет к ней остальные симптомы.
- ЕСЛИ разбор начинать с этой одной проблемы → видна корневая причина сразу, не нужно сопоставлять десяток разрозненных алертов.

Такой подход резко снижает шум оповещений и даёт начинать разбор с корня.

**Карточка проблемы.** Клик по строке. В ней: полная хронология событий, какие объекты в какой момент были затронуты, вывод Davis о корневой причине. Прямые переходы к графикам метрик, трейсам, логам, затронутым сервисам.

Подробнее Problems разбираются в Теме 10.

### Шаг 6: Releases / релизы

![Releases: инвентарь версий приложений](screenshots/day-1/ui-overview/releases/Releases-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Automations → Releases** → `https://guu84124.live.dynatrace.com/ui/releases`.

**Что на экране.** Инвентарь всех версий приложений, которые когда-либо работали в этом окружении. Важен для банка при работе с change management и регуляторными требованиями: какая версия сервиса была в такой-то момент, что в ней было, были ли проблемы.

**Фильтры слева.**
- **Monitor state**: Any / Active / Inactive.
- **Problem impact**: Any / Impacted / Not impacted.
- **Security vulnerability**: Any / Detected / Not detected (интеграция с Application Security).

**Таблица Release inventory.** На этом демо: **77 релизов**. Колонки:
- **Name**: имя исполняемого компонента (`accounting.dll`, `aggregator-service-*`, `Apache Web Server`).
- **Release version**: версия (`1.1.1`, `1.3.17`, `2.0.0`).
- **Build version**: номер сборки с датой (`2.0.0.3650 (2024-05-09)`). Заполняется, только если команда разработки передаёт его в Dynatrace.
- **Stage**: `production` или пусто.
- **Product**: логическая группа (`easytrade`, `easytrade-live-debugger`, `astroshop`, `hipstershop`, `easytravel`).
- **Details**: раскрывающаяся карточка.

**Правая панель.**
- **Release events**: графики событий релизов по времени. Зелёный столбик = новая версия выкатилась. Быстро видно, когда был последний деплой.
- **Tracked issues**: привязанные issues из внешних трекеров (Jira, GitHub), если настроена интеграция. Колонки Time, Issue tracker, Issue count.

**Откуда берётся версия.** Полный перечень стратегий описан в разделе [Release Monitoring](https://docs.dynatrace.com/managed/deliver/release-monitoring) документации Managed. Поддерживаются:

- **Переменные окружения**: `DT_RELEASE_VERSION` (версия), `DT_RELEASE_STAGE` (этап: production / staging / dev), `DT_RELEASE_PRODUCT` (продукт), `DT_RELEASE_BUILD_VERSION` (номер сборки). Самый простой и универсальный способ.
- **Метки Kubernetes pods**: рекомендованные `app.kubernetes.io/version` и кастомная `dynatrace-release-stage`. Удобно для контейнеризованных деплоев.
- **События Dynatrace Events API**: pipeline CI/CD отправляет в Dynatrace deployment-event с метаданными версии и ссылкой на change-ticket.
- **OpenTelemetry resource attributes**: переменная `OTEL_RESOURCE_ATTRIBUTES` с deployment-метаданными, обогащает трейсы и логи.

Команда разработки выбирает любой из этих способов; в банке часто комбинируют переменные окружения для сред без Kubernetes и события Events API для централизованного pipeline.

**Типичный сценарий в банке.** Разбор инцидента после релиза. Смотрим Problems → фиксируем время начала → Releases → что выкатывалось в этот промежуток → по change-ticket узнаём, какие изменения были. Если новое приложение вызвало проблему, откат на предыдущую версию делается с того же change-ticket.

Отдельно: отчётность для регулятора и аудита. По любому моменту времени можно получить справку о том, какие версии приложений работали в production, когда они были задеплоены и были ли с ними проблемы.

---

## 📝 Практика обзора

После этой темы ученик должен уметь без подсказки пройти по тенанту за 10 минут:

1. Открыть Dashboards → увидеть список панелей окружения.
2. Открыть Services → найти любой сервис по имени.
3. Открыть Databases → увидеть список всех баз, к которым ходят сервисы.
4. Открыть Problems → увидеть активные проблемы и их приоритеты.
5. Открыть Releases → увидеть, что выкатывалось за последние сутки.
6. Использовать глобальный поиск (Ctrl+Shift+F) для перехода к любому объекту.
7. Переключить временной диапазон с Last 2 hours на Last 24 hours и посмотреть, как меняется картина.
8. Применить Management zone-фильтр и увидеть, как сужается весь интерфейс до выбранной зоны.
