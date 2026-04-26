> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 7 из 9: «Типы сервисов / стандартная инфографика»
>
> 🔖 **Редакция от 2026-04-26.** Тех-факты сверены с `docs.dynatrace.com/managed/` и общими страницами Service detection / Service types (общие для Managed и SaaS). Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-26 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Managed-специфика (приоритетный источник):**
> - [Applications and microservices — Dynatrace Managed](https://docs.dynatrace.com/managed/observe/applications-and-microservices) — раздел про сервисы в Managed-документации
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed) — корневая страница раздела Managed Docs
>
> **Общая (одинаково для Managed и SaaS):**
> - [Services — overview](https://docs.dynatrace.com/docs/observe/applications-and-microservices/services) — корневая страница темы Services
> - [Service-related concepts](https://docs.dynatrace.com/docs/observe/application-observability/services/services-concepts) — концепции (типы, обнаружение, наименование)
> - [Service types](https://docs.dynatrace.com/docs/observe/applications-and-microservices/services/service-detection-and-naming/service-types) — Web request / Web / Database / Messaging / Remoting / Background — что считается каким
> - [Service detection — overview](https://docs.dynatrace.com/docs/observe/application-observability/services/service-detection) — как Dynatrace определяет тип сервиса по сенсорам
> - [Service detection v1](https://docs.dynatrace.com/docs/observe/applications-and-microservices/services/service-detection-v1) — классическая модель детекции (доступна в Managed)
> - [Service detection rules — settings schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-service-detection-rules) — формальная схема страницы Service detection rules
> - [Service detection v2 for OneAgent — settings schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-service-detection-v2-for-oneagent) — формальная схема Service detection v2
> - [Services — параметрический shortlink](https://docs.dynatrace.com/docs/shortlink/services) — каноническая точка входа для темы Services

## 📍 КАРТА — три страницы про типы сервисов и правила их детекции

Термины темы: `Service / сервис / логическая backend-единица`, `Service type / тип сервиса`, `Service detection / детекция сервиса`, `Endpoint / конечная точка / URL-путь`, `PurePath / сквозной трейс одного запроса`, `Custom service / кастомный сервис`.

| Что показать | Путь в меню | Прямая ссылка | Назначение |
|---|---|---|---|
| Список сервисов | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` | Все обнаруженные сервисы с типами, технологиями, метриками |
| Service detection | **Settings → Service Detection → Service detection rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection-rules` | Правила разбиения процессов на сервисы |
| Service Detection v2 for OneAgent | **Settings → Server-side service monitoring → Service Detection v2 for OneAgent** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection-v2-for-oneagent` | Новая версия механизма детекции (больше возможностей разбиения) |

**Типы сервисов в Dynatrace:**

| Тип | Что собой представляет | Как распознаётся |
|---|---|---|
| **Web service** | Сервер, отвечающий на входящие HTTP-запросы | OneAgent инструментирует Servlet/Filter/Controller/Express/etc. |
| **Web request service** | То же что Web service — входящие HTTP; часто используется как default | По той же инструментации, другое внутреннее имя |
| **Custom service** | Любой код, описанный вручную через правило | Через Custom Service rules в Settings |
| **Messaging service** | Producer или consumer сообщений (Kafka, RabbitMQ, ActiveMQ) | Инструментация клиентов Kafka/JMS |
| **Database service** | Клиент базы данных (JDBC/ODBC/Redis/MongoDB driver) | Инструментация драйверов |
| **External service** | Вызов внешнего API (не инструментированного) | Перехват исходящих HTTP клиентов |
| **Background activity** | Code без явного HTTP-вызова (batch, async workers) | Инструментация по правилам |
| **Queue listener** | Подписчик на очередь | Специализация Messaging service |

---

## 🎬 Работа с типами сервисов на трёх экранах

### Шаг 1 — Services (список всех сервисов с типами)

![Services — список 239 сервисов с фильтрами по типу, технологии и статусу проблем](screenshots/day-2/services-overview/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Application Observability → Services**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/services`.

На captured тенанте в момент сбора видно **239 Services** (h2 `239Services`). Это количество слегка меняется во времени (на день раньше было 244), что нормально: сервисы появляются при новых деплойментах и исчезают при удалениях.

Страница и её структура разбирались в Дне 1, Тема 5 и Тема 7. В контексте «типов сервисов» фокус смещается на **левую панель фильтров**, точнее на фильтр **Service type**.

**Service type как практический фильтр.** Когда нужно быстро найти, скажем, «все Kafka-consumer-сервисы в окружении» — применяем фильтр Service type = Messaging service → получаем список. Когда нужно «все backend HTTP-endpoints» — Service type = Web request service.

**Примеры реальных сервисов на captured тенанте** (из body_preview выше): `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 nginx ingress-nginx-controller-*` — это nginx-ingress-контроллеры Kubernetes. Автоматически распознаны как Web service, потому что отвечают на HTTP. Имена формируются по схеме «порт + технология + Kubernetes-имя».

**Зачем разные имена у одного сервиса.** Если в кластере запущено два nginx-ingress-controller deployment'а на разных портах (9024 и 80,443), Dynatrace создаёт два Service, по одному на каждый port-сочетание. Это позволяет отдельно видеть метрики каждого endpoint.

**Открываем конкретный сервис.** В карточке одного сервиса (клик по имени):
- **Service properties** — Service type, Technology, Detection rule (которая его породила), Instances (связанные Process Groups).
- **Service flow** — граф вызовов: кто ходит в этот сервис, куда он сам ходит.
- **Top endpoints** — самые частые HTTP-эндпоинты.
- **Top requests** — самые частые и самые медленные запросы.
- **Response time** / **Throughput** / **Failure rate** — ключевые метрики за период.
- **Instances** — список процессов, обслуживающих этот сервис, со связью с хостами.

### Шаг 2 — Service detection rules

![Service detection — правила классического механизма разбиения процессов на сервисы](screenshots/day-2/services-overview/settings/builtinservice-detection-rules/Service-detection-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Service Detection → Service detection rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection-rules`.

*Что такое Service detection.* Когда OneAgent инструментирует процесс (скажем, Tomcat), возможны варианты: создать один Service на весь процесс (`Tomcat @ host:port`) или разбить на несколько Service — по контекстам, URL-паттернам, entry points. Управляется правилами Service detection.

*Пример правила.* Web Request Service detection based on request path:

- Матч всех входящих HTTP-запросов на Tomcat.
- Group by URL prefix:
  - `/api/payments/*` → Service `Payment API`
  - `/api/accounts/*` → Service `Account API`
  - `/admin/*` → Service `Admin Interface`

Результат — три логических сервиса в интерфейсе, хотя физически они живут в одном Tomcat. Метрики, PurePath, проблемы разделяются по этим логическим сервисам.

**Типы правил:**

- **Web request service detection** — разбиение входящих HTTP по URL / Host / Port.
- **Full web service detection** — SOAP / REST / gRPC — разбиение по operation name или method.
- **Web request naming** — как именовать автоматически обнаруженный сервис.
- **Custom service** — явное добавление сервиса из non-HTTP кода (cron-задача, batch).

*Когда это нужно.* Почти всегда. Дефолт создаёт один Service на процесс — неудобно: внутри одного Tomcat могут жить 10-20 бизнес-endpoint'ов, их метрики без разбиения смешиваются. Правила пишут под архитектуру команды — если monolith разделён на `/api/retail/*`, `/api/corporate/*`, `/api/sme/*`, создаются три правила.

*Нюанс.* Страница относится к классическому механизму. Для новых версий OneAgent — Service Detection v2 (следующий шаг).

### Шаг 3 — Service Detection v2 for OneAgent

![Service Detection v2 — новая версия механизма разбиения процессов на сервисы](screenshots/day-2/services-overview/settings/builtinservice-detection-v2-for-oneagent/Service-Detection-v2-for-OneAgent-Environment-Settings-Demo-live-Demo-Live-Dynat.png)

Путь в меню: **Settings → Server-side service monitoring → Service Detection v2 for OneAgent**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection-v2-for-oneagent`.

**Что нового в v2.** Новая версия механизма детекции, поставляется с новыми сборками OneAgent. Улучшения:

- **Гибкие правила матчинга.** В v1 правила писались против технологических хинтов (Servlet-pattern, JVM-arg). В v2 — против произвольных свойств процесса: labels контейнера, annotations пода, переменных окружения.
- **Поддержка gRPC и GraphQL.** В v1 эти протоколы распознавались с ограничениями. В v2 — видно конкретные RPC-методы, GraphQL-queries.
- **Auto-split по метаданным.** Например, в Kubernetes автоматически разделять сервисы по namespace без явных правил.
- **Более детальные PurePath.** Trace-контекст распространяется через больше видов вызовов, включая background jobs.

*Переходный период.* Обычно часть OneAgent старые (v1), часть новые (v2). На этой странице включается глобальное предпочтение использовать v2 там, где доступно. Правила v1 продолжают работать для процессов со старым агентом.

**Что на странице:**

- Глобальный тумблер активации v2-правил.
- Список v2-правил (синтаксис как в Шаге 2, с расширенными возможностями).
- Статус применения v2 по парку OneAgent — сколько агентов уже на поддерживающей версии.

*Как делают переключение.* Плановое изменение, обсуждается с командой разработки — названия Service могут поменяться, это повлияет на Alerting profiles и Dashboards. Порядок: сначала обновляются агенты на не-prod хостах, проверяется корректность разбиения, потом массово на prod.

---

## ⚙️ COOKBOOK — типы сервисов в банковской практике

### Типичная архитектура одного сервиса

- **Frontend** (веб-приложение в браузере) — это **Application** в Dynatrace (разбиралось в DEM). Не Service.
- **API Gateway / Ingress** (nginx, Kong, AWS API Gateway) — Web request service.
- **Backend microservices** (Java / Node / .NET) — каждый отдельный Service. Обычно Web request service для синхронных и Messaging service для async.
- **Database clients** — Database service, появляются автоматически при инструментации.
- **Kafka / RabbitMQ clients** — Messaging service. Producer и Consumer могут быть разными Service.
- **Background jobs** (ночные batch, cron) — по умолчанию не Service. Нужно правило Custom service, чтобы попали в мониторинг.
- **Интеграции с legacy** (SOAP, IBM MQ, FTP) — External service или специальные сенсоры.

### Разбить monolith на логические сервисы

*Задача.* Legacy-monolith (Java, WebLogic) обслуживает 15 бизнес-направлений через разные URL-паттерны. Дефолтная детекция даёт один Service `WebLogic @ host:port`. Нужно разделить.

*Решение.* 15 Web request service detection rules. Каждое матчит URL-префикс: `/api/retail/*` → `Retail API`, `/api/corporate/*` → `Corporate API` и т.д. После деплоя — 15 отдельных Services, каждый со своими метриками. Alerting profiles настраиваются на каждый.

### Custom service для batch-job

*Задача.* Ночной ETL-процесс на Python. В Dynatrace виден только как процесс, не как Service. Нужны метрики выполнения.

*Решение.* Custom service rule: распознать процесс по command line `python /etl/daily_extract.py`, создать Custom service `Daily ETL`, включить instrumentation — чтобы каждый запуск был транзакцией. После настройки появится в Services с метриками количества запусков, длительности и ошибок.

### Включить v2 на части парка

*Задача.* Команда просит улучшенную поддержку gRPC (только в v2). Нужно включить на dev-кластере.

*Шаги:*

1. Обновить OneAgent на dev-хостах до версии с поддержкой v2 (через Update windows).
2. В Service Detection v2 включить `Enable v2 detection for OneAgent 1.XXX+`.
3. Проверить, что правила v1 продолжают работать на prod (ещё не обновлён).
4. После 1-2 недель стабильной работы — обновить prod-агенты постепенно.

---

## 🎓 ТЕОРИЯ — типы сервисов и их определяющие свойства

### Почему «тип сервиса» важен

- **Алерты по типу.** Типичный Alerting profile: «только Web request service в prod-namespace с Impact Application». Без типов все сервисы перемешаны, фильтр бесполезен.
- **Дашборды по типу.** DBA-команде — «все Database service со временем отклика > 100 мс». Kafka-команде — «все Messaging service с отставанием consumer group». Типы позволяют такие срезы.
- **Разные метрики для разных типов.** Web service: Response time, Failure rate, Throughput. Messaging service + Queue lag, Message count, Consumer group lag. Database service + Slow count, Top statements. Тип определяет, какие метрики применимы.

### Как Dynatrace определяет тип

При инструментации OneAgent смотрит:

- **Java** — какие классы вызываются: Servlet → Web service, JMS → Messaging, JDBC → Database client.
- **.NET** — аналогично: ASP.NET Controllers → Web, MSMQ → Messaging, ADO.NET → Database client.
- **Node.js** — Express / Koa / Fastify → Web, amqplib → Messaging, pg / mysql → Database client.

*Fallback — Generic service.* Если ни один из сенсоров не сработал, процесс попадает в Generic service с минимальным набором метрик. Обычно означает, что технология не поддерживается или нужно правило Custom service.

### Web service vs Web request service

*Исторически.* В старых версиях все HTTP-обслуживающие процессы считались Web service. С развитием появились тонкости: один Java-процесс мог обслуживать прямые HTTP-запросы (Web request) и быть вызванным из другого Java-процесса через RMI или EJB (Full web service). Появились два подтипа.

*Сейчас.* Большинство современных сервисов — Web request service (прямой HTTP). Web service остался для SOAP-WS-*, RMI и аналогичных enterprise-технологий. Команды разработки обычно встречают только Web request service при работе с современными микросервисами.

### Специфика в air-gapped

- **Правила Service detection** хранятся в кластере и применяются всем агентам. Ничего внешнего не требуется.
- **Обновление правил при апгрейде OneAgent.** Если новая версия агента поддерживает v2 и новые типы — правила обновляет администратор вручную через Settings. Автоматически в air-gapped правила не скачиваются.
- **Отличие от SaaS.** В SaaS доступна Service Detection v2 (для OpenTelemetry — GA, для OneAgent Java в Kubernetes — Public Preview). В Managed используется классическая Service Detection (v1) — она полностью функциональна, кастомизация идёт через страницы Simple / Advanced detection rules вручную.
