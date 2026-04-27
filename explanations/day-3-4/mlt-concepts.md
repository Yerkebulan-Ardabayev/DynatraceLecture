> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 1 из 14: «Метрики, логи, трейсы: концепции и реализация»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/data-explorer -->
<!-- revision: 2026-04-27 -->

🔖 Редакция от 2026-04-27.

Путь в UI: **Observe and explore → Data Explorer / Metrics / Logs**, **Application Observability → Distributed Traces / Multidimensional Analysis**.

## 📚 Источники

- [Distributed traces (Managed)](https://docs.dynatrace.com/managed/observe-and-explore/distributed-traces)
- [Log Monitoring (Managed)](https://docs.dynatrace.com/managed/observe-and-explore/log-monitoring)
- [Metrics (Managed)](https://docs.dynatrace.com/managed/observe-and-explore/metrics)
- [Data Explorer (Managed)](https://docs.dynatrace.com/managed/observe-and-explore/explorer)
- [Data retention periods (Managed)](https://docs.dynatrace.com/managed/shortlink/data-retention-periods)
- [Span and trace context propagation (Managed)](https://docs.dynatrace.com/managed/observe/application-observability/distributed-traces/context-propagation)

## 📍 КАРТА — три основы observability и их экраны в Dynatrace

Термины темы: `Metric / метрика` (численный временной ряд), `Log / лог` (текстовая запись), `Trace / трейс / PurePath` (сквозная трассировка запроса), `Span / спан` (шаг трейса), `Metrics Selector / селектор метрик` (синтаксис запросов в Managed Data Explorer), `DQL / Dynatrace Query Language` (язык SaaS Grail — в Managed недоступен), `Dimension / измерение / срез`, `OpenTelemetry / OTel` (открытый стандарт телеметрии).

| Тип данных | Экран в Dynatrace | Прямая ссылка |
|---|---|---|
| **Metrics — построение графиков** | Observe and explore → Data Explorer | `https://guu84124.live.dynatrace.com/ui/data-explorer` |
| **Metrics — каталог** | Observe and explore → Metrics | `https://guu84124.live.dynatrace.com/ui/metrics` |
| **Logs — просмотр и поиск** | Observe and explore → Logs | `https://guu84124.live.dynatrace.com/ui/logs-events` |
| **Traces — PurePath** | Application Observability → Distributed Traces | `https://guu84124.live.dynatrace.com/ui/diagnostictools/purepaths` |
| **Multidimensional Analysis** | Application Observability → Multidimensional Analysis | `https://guu84124.live.dynatrace.com/ui/diagnostictools` |

---

## 🎬 Работа с тремя столпами observability на пяти экранах

### Шаг 1 — Data Explorer (метрики как графики)

![Data Explorer — ad-hoc построение графиков по метрикам](screenshots/day-3-4/mlt-concepts/data-explorer/Dynatrace.png)

Путь в меню: **Observe and explore → Data Explorer**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/data-explorer`.

Data Explorer разбирался в Дне 1 (Тема 8). В теме observability его роль — инструмент **анализа метрик**, одного из трёх столпов. Инженер работает с численными временными рядами: CPU, Response time, Failure rate, Throughput.

*Контекстно-богатые метрики.* В Dynatrace метрика не существует сама по себе. У каждого значения есть контекст — к какой сущности (хост / сервис / приложение) привязана, какие dimensions (host name, service technology, container image). Отличие от «плоских» систем (Prometheus), где метрика — просто число с метками.

### Шаг 2 — Metrics (каталог всех метрик)

![Metrics — каталог всех метрик окружения](screenshots/day-3-4/mlt-concepts/metrics/Metrics-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Observe and explore → Metrics**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/metrics`.

Каталог всех метрик. Разбирался в Дне 1. В контексте observability служит **справочником**: когда инженер не помнит точное имя нужной метрики, он идёт сюда, ищет по описанию, копирует ключ.

### Шаг 3 — Logs (второй столп — логи)

![Logs and events — поисковый интерфейс по логам окружения](screenshots/day-3-4/mlt-concepts/logs-events/Logs-and-events-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Observe and explore → Logs**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/logs-events`.

**Второй столп observability — логи.** В Dynatrace логи собирает OneAgent с хостов (системные + приложенческие) или они передаются через API (внешние системы, Kubernetes stdout). `/ui/logs-events` — поисковый UI по всем логам.

**Что делает Dynatrace с логами:**

- **Собирает.** OneAgent читает конфигурированные пути (`/var/log/*.log`, Kubernetes container logs через kubelet), ActiveGate принимает REST-ingest.
- **Парсит.** Автоматически распознаёт формат (syslog, Apache access log, JSON, Java stacktrace), извлекает поля (severity, timestamp, message).
- **Индексирует.** Строит обратный индекс для быстрого полнотекстового поиска.
- **Связывает с сущностями.** Каждая запись привязывается к хосту / процессу / контейнеру. Из карточки сервиса клик «посмотреть логи» открывает только логи этого сервиса.

**Формат запроса в Managed** — простой поиск по словам + фильтры в UI: `ERROR AND service.name=payment-service`, `severity=FATAL AND host.name=prod-app-01`. Полноценный DQL (Dynatrace Query Language) — язык нового SaaS-стэка поверх Grail. В air-gapped Managed он **не работает**, используются классический Logs UI и USQL для сессий.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/log-monitoring -->

*Типовое включение.* Log Monitoring — Opt-In фича (разбиралась в Дне 2, Тема 2). Полный сбор логов всей инфраструктуры дорог по DDU-лицензиям. Обычно ограничивают prod-приложениями и критичной инфраструктурой.

### Шаг 4 — Distributed Traces (третий столп — трейсы)

![Distributed traces — PurePath, сквозной трейсинг запроса через все сервисы](screenshots/day-3-4/mlt-concepts/diagnostictools/purepaths/Distributed-traces-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Application Observability → Distributed Traces**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/diagnostictools/purepaths`.

**Третий столп — трейсы.** В Dynatrace трейсинг реализован через **PurePath** — сквозную трассировку запроса через все инструментированные сервисы. Исторически отличительная технология Dynatrace.

**Как работает PurePath:**

1. Входящий HTTP-запрос попадает в инструментированный сервис. OneAgent перехватывает вход, генерирует `trace ID` и `span ID`.
2. Сервис делает исходящие вызовы — другие сервисы по HTTP, БД по SQL, очереди по Kafka / JMS. OneAgent автоматически добавляет trace-заголовки в каждый исходящий запрос. Используются три механизма: **`x-dynatrace`** (проприетарный), **`traceparent` / `tracestate`** (стандарт W3C Trace Context, общий для OneAgent и OpenTelemetry), **`dtdTraceTagInfo`** (для очередей и messaging).
3. Принимающий сервис видит заголовок, связывает свою работу с контекстом родителя, создаёт child span.
4. Ветки развиваются рекурсивно. Получается **дерево спанов** — все работы, выполненные для обслуживания одного изначального запроса.
5. Все спаны уходят в кластер и связываются в единый PurePath.

На экране Distributed Traces — список PurePath-ов с фильтрами по времени, сервису, длительности, статусу. Клик открывает **waterfall-диаграмму**: временная развёртка всех спанов с длительностью каждого.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/application-observability/distributed-traces/context-propagation -->

*Пример использования.* Жалоба «оформление платежа занимает 5 секунд». Без трейсов инженер видит только «клиент ждал 5 сек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (ожидание LDAP), 1300 мс payment-service. Корень — медленный LDAP. Без ручного поиска логов.

### Шаг 5 — Multidimensional Analysis

![Multidimensional Analysis — углублённый анализ метрик по нескольким измерениям](screenshots/day-3-4/mlt-concepts/diagnostictools/Multidimensional-analysis-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Application Observability → Multidimensional Analysis**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/diagnostictools`.

Инструмент **многомерного анализа трейсов**. Data Explorer показывает агрегаты (одна линия на сервис). Multidimensional Analysis разбивает данные по произвольным dimensions: endpoint, client IP, user agent, версия приложения, любая user-defined метка.

*Пример.* У сервиса `payment-api` response time растёт. В Data Explorer — одна общая линия до 500 мс. Вопрос: равномерно по всем клиентам или только у одной группы? В Multidimensional Analysis указываем метрику Response time и разбивку по client geo. Видно: медленно у клиентов одного региона, остальные в норме. Корневая причина быстро локализуется — проблема с конкретной зоной или CDN.

---

## 🎓 ТЕОРИЯ — связь MLT (metrics/logs/traces) в Dynatrace

### Три столпа как единая модель

В классическом подходе observability метрики / логи / трейсы живут в отдельных системах: Prometheus + ELK + Jaeger. Каждая со своим языком запросов, интерфейсом, хранилищем. Корреляция между ними — ручная работа инженера.

В Dynatrace это **единая модель**. Каждая метрика, лог, трейс привязаны к Smartscape-сущности (сервис / процесс / хост / приложение). Из карточки сервиса одним кликом:

- В **метрики** этого сервиса — Data Explorer с заполненным фильтром.
- В **логи** — Logs с фильтром по host / process.
- В **трейсы** — PurePath с фильтром service=X.

Ручная корреляция не нужна.

### Трейсинг без ручной инструментации

PurePath работает **автоматически** для всех технологий, которые поддерживает OneAgent. Не нужно вшивать `tracer.startSpan(...)` в код приложения (как требуют OpenTelemetry или Jaeger). OneAgent при старте инструментирует:

- Servlet / Filter в Java.
- Middleware в Express / Koa.
- Controller в ASP.NET.
- 64-bit Go-исполняемые файлы — автоматическая инъекция инструментации в бинарь (поддержка x86 c OneAgent 1.323+, ARM64 на отдельных версиях).

Каждая точка входа и выхода автоматически становится спаном в PurePath.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/distributed-traces -->

**Совместимость с OpenTelemetry.** Dynatrace принимает OTLP-поток от приложений, инструментированных OTel, и объединяет его спаны с автоматическими PurePath-спанами в единое дерево. В одной системе видно и автоматически, и вручную инструментированные части.

### Хранение и прореживание MLT-данных

- **Metrics Classic.** Cassandra и metrics-store. Горизонт хранения — **5 лет** с прогрессивным прореживанием:
  - 0–14 дней → гранулярность 1 минута
  - 14–28 дней → 5 минут
  - 28–400 дней → 1 час
  - 400 дней – 5 лет → 1 день
- **Log Monitoring Classic.** Elasticsearch с replication factor 2. Срок хранения — **35 дней** (фиксировано).
- **Distributed Traces Classic.** Cassandra с индексами для быстрого поиска. Полные транзакционные детали — **до 365 дней (настраивается)**. Code-Level Insights (детальный код-профиль) — **10 дней** в исходном виде, дальше данные оптимизируются под агрегированный анализ.
- **Davis problems & events.** 14 месяцев (фиксировано).

Долгосрочные агрегаты сервисов (Throughput, percentiles) хранятся как метрики с retention из лестницы выше, не как PurePath.

Цифры из retention для SaaS / Grail (10 лет, 15 месяцев и т.п.) к Managed Classic не относятся.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/data-retention-periods -->

### Air-gapped контекст

Все три типа данных хранятся локально в кластере. OneAgent собирает, ActiveGate пересылает, Cassandra / Elasticsearch хранят. Внешних вызовов нет.

*Экспорт данных.* В Managed доступны API для экспорта в другие системы (SIEM, долгосрочное архивное хранилище). Если compliance требует хранить логи 7 лет — настраивается экспорт во внутренний Hadoop или S3-compatible архив.
