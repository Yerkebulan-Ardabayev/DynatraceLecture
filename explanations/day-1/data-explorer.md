> 📅 **День 1: Введение в систему Dynatrace** → Тема 8 из 11: «Встроенные метрики, Data Explorer»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/data-explorer?gf=all -->
>
> 🔖 **Редакция от 2026-04-27.** Тех-факты сверены с docs.dynatrace.com. **Важно для Managed:** Data Explorer Advanced mode использует **Metrics Selector** (синтаксис Dynatrace), DQL — это SaaS-only для Grail и в air-gapped Managed недоступен. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Общая (Managed + SaaS — UI Data Explorer + Metrics API единые):**
> - [Data Explorer](https://docs.dynatrace.com/docs/analyze-explore-automate/explorer) — корневая страница про Data Explorer
> - [Data Explorer quick start](https://docs.dynatrace.com/docs/observe-and-explore/explorer/explorer-quick-start) — пошаговый пример построения первого графика
> - [Data Explorer Advanced mode query editor](https://docs.dynatrace.com/docs/analyze-explore-automate/explorer/explorer-advanced-query-editor) — Metrics Selector синтаксис в Code-вкладке
> - [Metrics API — Metric selector](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/metric-v2/metric-selector) — полный референс Metrics Selector (`:filter(...)`, `:top(5)`, `:splitBy(...)`)
> - [Metrics browser (Classic)](https://docs.dynatrace.com/docs/analyze-explore-automate/dashboards-classic/metrics-browser) — каталог метрик окружения, поиск по описанию
> - [Metrics API — POST ingest data points](https://docs.dynatrace.com/docs/dynatrace-api/environment-api/metric-v2/post-ingest-metrics) — `POST /api/v2/metrics/ingest`, лимит 1 MB на запрос
> - [Metric ingestion protocol](https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics/reference/metric-ingestion-protocol) — Line-protocol формат `metric.key,dim=value gauge,min=X,max=Y,sum=Z,count=N`
> - [OneAgent metric API](https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics/ingestion-methods/oneagent-metric-api) — локальный эндпоинт `http://localhost:<port>/metrics/ingest` для приложений на хосте с OneAgent
> - [Extend metric observability](https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics) — обзорная страница способов отправки кастомных метрик
> - [Davis Data Units (DDU)](https://docs.dynatrace.com/docs/shortlink/davis-data-units) — лицензирование кастомных метрик и cardinality

## 📍 КАРТА — где работать с метриками

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Построение графиков | **Observe and explore → Data Explorer** | `https://guu84124.live.dynatrace.com/ui/data-explorer?gf=all` |
| Каталог метрик | **Observe and explore → Metrics** | `https://guu84124.live.dynatrace.com/ui/metrics` |
| Настройка кастомных метрик | **Settings → Monitoring → Metrics** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:metric.metadata` |
| API загрузки метрик | API-эндпоинт | `POST /api/v2/metrics/ingest` |

**Термины темы.**

- **Metric / метрика** — числовой показатель во времени.
- **Dimension / измерение / срез** — атрибут, по которому можно резать метрику (host, service, technology).
- **Key / ключ метрики** — уникальный идентификатор вида `builtin:host.cpu.usage`.
- **Metrics Selector / селектор метрик** — синтаксис запросов в Advanced mode (`builtin:*:avg:splitBy(...)`). В Managed используется именно он, а не DQL (DQL — язык SaaS-платформы для Grail, в Managed пока недоступен).
- **Space aggregation / пространственная агрегация** — как свести много значений в одно (average, max, sum, count).
- **Split by / разбивка** — по какому измерению разделить график на отдельные линии.

**Семейства встроенных метрик.**

| Семейство | Примеры | Префикс |
|---|---|---|
| Хосты | CPU, память, диск, сеть | `builtin:host.*` |
| Процессы и технологии | CPU процесса, JVM heap, .NET CLR | `builtin:tech.*` |
| Сервисы | Время отклика, ошибки, throughput | `builtin:service.*` |
| Приложения (RUM) | Время загрузки, JS-ошибки, Apdex | `builtin:apps.web.*`, `builtin:apps.mobile.*` |
| Synthetic | Доступность, время шага | `builtin:synthetic.*` |
| Сеть | Потеря пакетов, retransmissions, RTT | `builtin:host.net.*` |
| Kubernetes | Поды, узлы, контейнеры | `builtin:kubernetes.*` |
| Облака | AWS CloudWatch, Azure Monitor, GCP | `cloud.aws.*`, `cloud.azure.*` |
| Биллинг | Host Units, DDU, usage | `builtin:billing.*` |

---

## 🎬 Работа с метриками на двух экранах

### Шаг 1 — Data Explorer / построение графиков

![Data Explorer — построение графиков и шаблоны](screenshots/day-1/data-explorer/data-explorer/Data-explorer-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Data Explorer** → `https://guu84124.live.dynatrace.com/ui/data-explorer?gf=all`.

**Что на экране.** Три зоны:
- **Слева** — выбор визуализации и параметры запроса.
- **Центр** — область графика и шаблоны быстрого старта.
- **Справа** — настройка отображения.

**Выбор визуализации** (верх левой зоны). На скриншоте выбран **Graph / линейный график**. Другие варианты:
- **Bar / столбчатая диаграмма**.
- **Area / область с заливкой**.
- **Single Value / одно число** — удобно для KPI.
- **Table / таблица**.
- **Heatmap / тепловая карта** — распределение значений во времени.
- **Honeycomb / сотовая диаграмма** — состояние сущностей ячейками.
- **Pie / круговая диаграмма**.
- **Top list / топ-N самых больших или маленьких**.

**Select metric** — ввод имени или семейства. Поиск по всем словам в описании: набрали `cpu` — получили все метрики с CPU в имени или описании.

**Advanced mode** — тумблер справа. Включает редактор **Metrics Selector** для сложных выражений: деление метрик, соотношения, агрегации по нескольким метрикам одновременно. Это не DQL — DQL живёт на SaaS-платформе поверх Grail, в Managed пока недоступен.

**Start with a template** — готовые шаблоны визуализаций. На этом демо-тенанте представлены: Container restarts over time, Server-side response time, Web request/service failure rate, Kubernetes-дашборды, Disk space used %, Crash-free user rate, Core web vitals (LCP / CLS / FID), Application satisfaction SLO. Клик по шаблону моментально строит график на данных текущего окружения — удобно как стартовая точка или как референс синтаксиса.

**Settings** в правой панели:
- Тип линии.
- Цветовая палитра.
- Заголовок и подписи осей.
- **Resolution / разрешение по времени** — Auto / 1 минута / 5 минут / 1 час.

**Типовой маршрут построения графика.**

1. **Выбор метрики.** В поле Select metric ввести имя, например `builtin:host.cpu.usage`.
2. **Space aggregation / пространственная агрегация** — как свести много значений в одно. Для CPU по хостам это Average (усреднить), Max (максимум), Sum (сумма — для процентов не имеет смысла), Count (число значений). По умолчанию Auto — Dynatrace выбирает подходящую для природы метрики.
3. **Split by / разбивка** — разделить график по измерению. `dt.entity.host` → отдельная линия на каждый хост. `dt.entity.host_group` → линии по хост-группам.
4. **Filter / фильтр** — по тегам, Management zones, конкретным сущностям, значениям dimension.
5. **Выбор визуализации** — Graph / Bar / Single Value и т.д.

**Закрепление на дашборд.** Кнопка **Pin to dashboard** в правом верхнем углу добавляет график виджетом на выбранный дашборд. Ключевой приём построения дашбордов — не собирать виджеты внутри дашборда, а отточить их в Data Explorer и закрепить готовыми.

**Разрешение по времени и диапазон.** Временной диапазон задаётся в верхней панели (Last 2 hours / Last 24 hours / Last 7 days / Custom). Разрешение в дефолтном режиме **Auto** Dynatrace выбирает сам — короткому окну ставит более частые точки, длинному окну — более редкие, чтобы запрос не тянулся минутами и UI оставался отзывчивым. Точное соответствие «диапазон → шаг» одной авторитетной таблицы в публичной документации Advanced query editor [Dynatrace не даёт](https://docs.dynatrace.com/docs/analyze-explore-automate/explorer/explorer-advanced-query-editor) — фактический шаг видно по самому графику в момент построения. При желании конкретное разрешение задаётся вручную в правой панели Settings (поле Resolution) — независимо от диапазона.

Это компромисс между детальностью и объёмом. За долгие периоды Dynatrace подгружает свёрнутые агрегаты — иначе запрос тянулся бы минутами. Лестница прореживания метрик (1 мин → 5 мин → 1 час → 1 день) — отдельный механизм retention, описан на странице [Data retention periods](https://docs.dynatrace.com/docs/shortlink/data-retention-periods); это про хранение, не про показ в Data Explorer.

<!-- last-verified: 2026-04-27 source: docs.dynatrace.com/docs/analyze-explore-automate/explorer/explorer-advanced-query-editor -->

### Шаг 2 — Metrics / каталог всех метрик

![Metrics — каталог метрик окружения](screenshots/day-1/data-explorer/metrics/Metrics-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Metrics** → `https://guu84124.live.dynatrace.com/ui/metrics`.

**Что на экране.** Каталог всех метрик, доступных в окружении. Индикатор на этом демо-тенанте — **3.1k Metrics, showing 500** — примерно 3000 метрик, в отображаемой странице первые 500. На боевой инсталляции может быть больше в зависимости от использования: Extensions добавляют метрики SNMP с сетевого оборудования (каждое устройство даёт десятки метрик), кастомные метрики от приложений, метрики Kubernetes с учётом всех namespaces.

**Тумблер Only show metrics reported after the start of the selected timeframe** — фильтрует «мёртвые» метрики, которые когда-то регистрировались, но больше не приходят. Полезно для уборки.

**Левая панель — фильтры.**
- **Favorites** — Any / Yes / No. Метрики со звёздочкой в избранном.
- **Supported in Grail** — Any / Yes / No. Для классического Managed без Grail фильтр неактуален.

**Таблица.** Колонки:
- **Favorite** — звёздочка.
- **Name** — человекочитаемое описание (`(DPS) Available included metric data points for Full-Stack hosts`).
- **Key** — ключ метрики (`builtin:billing.full_stack_monitoring.metric_data_points.included`). Именно его вводят в Data Explorer и API.
- **Details** — раскрывающаяся карточка с полным описанием.

На демо-тенанте хорошо представлено семейство **billing**: `builtin:billing.full_stack_monitoring.metric_data_points.included`, `builtin:billing.infrastructure_monitoring.metric_data_points.included`, `builtin:billing.custom_metrics_classic.usage.other_by_entity`, `builtin:billing.synthetic.actions.usage_by_browser_monitor`. Эти метрики учитывают расход лицензии по типам мониторинга: Full Stack, Infrastructure, кастомные метрики, Synthetic, Log Monitoring.

**Раскрытие строки** (клик по стрелке справа) показывает:
- Полное описание.
- Единица измерения — проценты, байты, миллисекунды, запросы в минуту.
- Доступные measurements — min, max, avg для time-series.
- Dimensions, к которым метрика привязана.
- Примеры использования в Data Explorer.

**Типовой маршрут работы.**

1. Открываем Metrics.
2. Ищем метрику по описанию. Пример: «посмотреть потребление JVM heap». Вводим `jvm heap`, получаем список всех метрик с таким текстом.
3. Копируем Key нужной метрики.
4. Переходим в Data Explorer, вставляем Key, настраиваем split by и фильтры, строим график.

**Аудит расхода лицензии.** Семейство `builtin:billing.*` — прямой способ видеть текущее потребление. В air-gapped Managed это особенно важно: связи с внешним customer portal нет, единственный источник биллинговой информации — эти метрики в собственном окружении. Типичный дашборд менеджера Dynatrace в банке собирается именно из них: сколько Host Units сейчас активно, сколько DDU потрачено за месяц, сколько User Sessions для RUM.

---

## 🎓 ТЕОРИЯ — метрики как первый столп observability

### Три источника метрик в Dynatrace

Полный обзор способов подачи метрик описан в разделе [Extend metric observability](https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics).

**Встроенные.** OneAgent собирает автоматически, без настройки — хосты, процессы, сервисы, RUM. Никаких конфигов.

**Extensions.** Плагины на ActiveGate, опрашивающие внешние системы через SNMP, JMX, JDBC, Prometheus, REST. Данные приходят в кластер как обычные метрики с префиксом `ext:`. Разбирали в Дне 1, Тема 1.

**Custom ingest.** Метрики из приложений или внешних систем, отправленные через:
- **OneAgent SDK** — приложение само шлёт метрики через API агента.
- **API** `POST /api/v2/metrics/ingest` — приём метрик в формате [Metric ingestion protocol](https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics/reference/metric-ingestion-protocol) (Line Protocol, похож на InfluxDB).

Во всех трёх случаях данные остаются внутри контура — в интернет ничего не уходит.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics -->

### Metrics Selector в Advanced mode

В простом режиме — выбор метрики и измерения. В [Advanced mode](https://docs.dynatrace.com/docs/analyze-explore-automate/explorer/explorer-advanced-query-editor) пишутся сложные выражения на **Metrics Selector** (синтаксис Dynatrace для работы с метриками):

- `(builtin:service.response.time:avg) / 1000` — перевод из микросекунд в миллисекунды.
- `builtin:host.cpu.usage / builtin:host.mem.usage` — соотношение CPU к памяти.
- `:filter(...)` — фильтр по условию.
- `:top(5)` — топ-5 значений.
- `:splitBy("dt.entity.host")` — разбивка по хостам.

Нужно для вопросов вида:

- «Какой процент времени процесс был в iowait».
- «Какое соотношение между числом запросов и числом ошибок».
- «Топ-5 самых медленных сервисов по 95-му перцентилю отклика».

*Нюанс терминологии.* Metrics Selector часто путают с DQL. DQL — новый язык для Grail (облачное хранилище Dynatrace), доступен только на SaaS. В Managed работает Metrics Selector — язык старше и ограничен метриками (не покрывает логи и трейсы так, как DQL). Полный референс операторов Metrics Selector: [Metrics API — Metric selector](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/metric-v2/metric-selector).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/docs/analyze-explore-automate/explorer/explorer-advanced-query-editor -->

### Кастомные метрики в air-gapped

В air-gapped Managed любые кастомные метрики работают без особенностей. Ограничения только такие:

- **Квота DDU (Davis Data Units)**. Каждая кастомная метрика со своими dimensions потребляет DDU. Подробнее — [Davis Data Units (DDU)](https://docs.dynatrace.com/docs/shortlink/davis-data-units). На боевой инсталляции следить за потреблением через метрики `builtin:billing.custom_metrics_classic.*`.
- **Ограничение числа dimensions**. Слишком много dimensions на одной метрике приводят к cardinality explosion — десятки тысяч отдельных временных рядов, замедление UI, перерасход DDU.

### Связка двух экранов в ежедневной работе

1. **Metrics** — найти нужную метрику, скопировать Key. Пример быстрого старта — [Data Explorer quick start](https://docs.dynatrace.com/docs/observe-and-explore/explorer/explorer-quick-start).
2. **Data Explorer** — построить график, настроить split by, применить фильтры.
3. **Pin to dashboard** — закрепить на общем дашборде, если график полезен команде.

Если график нужен разово — остался в Data Explorer, не сохранён. Если постоянный показатель — попадает на дашборд и обновляется в реальном времени.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/docs/shortlink/davis-data-units -->
