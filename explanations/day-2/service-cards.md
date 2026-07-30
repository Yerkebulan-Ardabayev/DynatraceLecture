> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 8 из 9: «Сравнение периодов, анализ времени отклика, ключевые запросы»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/services -->
>
> 🔖 **Редакция от 2026-04-27.** Все тех-факты сверены свежими WebFetch'ами на `docs.dynatrace.com/managed/` в текущей сессии. Ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed): корневая страница Managed Docs
> - [Applications and microservices: Managed](https://docs.dynatrace.com/managed/observe/applications-and-microservices): общий раздел про сервисы в Managed
> - [Services: Managed](https://docs.dynatrace.com/managed/observe/applications-and-microservices/services): services overview (response time / throughput / failure rate)
> - [Service analysis timings: Managed](https://docs.dynatrace.com/managed/observe/application-observability/services-classic/service-analysis-timing): типы timing'а: response time / processing time / execution time / suspension / wait / lock / network I/O / disk I/O / CPU / self time; в каких analysis-типах какие появляются
> - [Service flow: Managed](https://docs.dynatrace.com/managed/observe/application-observability/services-classic/service-flow): последовательность service calls для каждого запроса, dynamic aggregation минорных сервисов
> - [Adjust sensitivity of anomaly detection for services: Managed](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services): пороги response time / failure rate / throughput
> - [Data retention periods: Managed](https://docs.dynatrace.com/managed/shortlink/data-retention-periods): Distributed traces 365 (cfg) / Services 365 (cfg) / Metrics Classic 5 лет с лестницей

## 📍 КАРТА: три страницы про детальный анализ сервиса

Термины темы: `Response time / время отклика`, `Failure rate / частота ошибок`, `Throughput / пропускная способность`, `Endpoint / конечная точка / URL-путь`, `Percentile / перцентиль`, `PurePath / waterfall / сквозной трейс`, `Baseline / базовая линия`, `SLO / цель уровня обслуживания`.

| Что показать | Путь в меню | Прямая ссылка | Назначение |
|---|---|---|---|
| Список сервисов как точка входа | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` | Отсюда кликаем в конкретный сервис для анализа |
| Anomaly detection for services | **Settings → Anomaly detection → Services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services` | Пороги, от которых зависит, когда карточка сервиса загорается «красным» |
| Endpoint metrics | **Settings → Service Detection → Endpoint metrics** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:unified-services-endpoint-metrics` | Какие метрики собирать на уровне отдельных endpoint'ов сервиса |

---

## 🎬 Работа с карточкой сервиса на трёх экранах

### Шаг 1: Services (вход в карточку конкретного сервиса)

![Services: список 239 сервисов как точка входа в карточку](screenshots/day-2/service-cards/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Application Observability → Services**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/services`.

На снимке этой темы видно **239 Services** (число живое: на день раньше обход видел 244, у вашего тенанта будет своё). Эта страница, точка входа в детальный анализ.

**Как открыть карточку.** Что нажать: имя сервиса в колонке **Name**, либо кнопку **Open service drilldown** в той же строке. Куда попадаешь: карточка одного сервиса, адрес вида `https://guu84124.live.dynatrace.com/ui/nav/SERVICE-4B770D7846DE018B` (канонический вид `/#services/serviceOverview;id=SERVICE-…`, сверено 2026-07-28). Как вернуться: кнопка «назад» браузера либо снова **Application Observability → Services**. Вся работа, описанная дальше в этой теме, происходит внутри этой карточки.

**Структура карточки сервиса** (при открытии конкретного сервиса, например `EasytravelService`):

**Зона 1: Overview.** Метрики Response time / Failure rate / Throughput в динамике за выбранный период. Над каждым графиком: **текущее значение** (медиана), **сравнение с предыдущим периодом** (стрелка ↑/↓ с процентом изменения), активные Problem-маркеры.

**Зона 2: Service flow.** Граф вызовов: кто ходит в этот сервис (слева), куда он сам ходит (справа). Ширина рёбер пропорциональна частоте вызовов. Цвета: по состоянию (зелёный = норма, жёлтый = деградация, красный = проблема).

**Зона 3: Top requests (endpoints).** Список самых частых и самых медленных endpoint'ов сервиса. Для каждого: запрос (паттерн URL), число вызовов, медианное время, 90/95/99 перцентили, частота ошибок.

**Зона 4: Top backend calls.** Что вызывает сервис наружу: другие сервисы, базы данных, внешние API. Для каждого: число вызовов, общее время, частота ошибок.

**Зона 5: Top database statements.** Только для сервисов с database-клиентами. Топ самых частых и медленных SQL.

**Зона 6: Instances.** Список Process Groups и хостов, на которых работает сервис.

**Зона 7: Problems.** Активные и недавние проблемы, связанные с этим сервисом.

### Дословный состав живой карточки (сверено на живом тенанте 2026-07-28)

Канонический адрес карточки: `/#services/serviceOverview;id=SERVICE-...` (пример: карточка `easyTravel Customer Frontend`). Секции сверху вниз, названия дословно:

- **Properties and tags**: свойства и теги сервиса.
- Плитки блока **Dynamic web requests**: Response time, Failure rate, CPU, Throughput; под ними кнопка **View dynamic requests**.
- **Resource requests** с кнопкой **View resource requests**.
- Секция проблем (на досверке «2 Problems») и **Problematic requests**.
- **Multidimensional analysis views** с кнопкой **Create analysis view**.
- **Understand dependencies**: кнопки **View service flow**, **View backtrace**, **View distributed traces**, **View web requests**, **View related logs**. Это главный «пульт» переходов: поток обслуживания, обратная трассировка «кто меня вызвал», трейсы, запросы и связанные логи в один клик.
- **Events**: события сервиса (деплои, изменения конфигурации).

Концептуальные «зоны» выше и дословные секции: одно и то же с разной детализацией; на живом показе называйте элементы по дословным именам.

### Сравнение периодов: ключевая механика карточки

*Как работает.* В верхней панели селектор временного диапазона (Last 2 hours / Last 24 hours / Custom). Выбор применяется к дашборду. В карточке сервиса добавлена механика **сравнения с предыдущим периодом той же длительности**.

*Пример.* Выбран Last 24 hours: Dynatrace показывает метрики за последние 24 часа и параллельно сравнивает с предыдущими 24 часами (48-24 часа назад). Если Response time вырос, над графиком появляется стрелка `↑ 15%` с указанием, насколько хуже стало.

*Использование.* Жалоба «утром было быстро, сейчас медленно». В карточке сервиса выбираем Last 4 hours, видим сравнение с 4h → 8h назад. Видно: в каком endpoint произошло замедление, на сколько процентов. Сравнение с «тем же временем прошлой недели» через кастомный Timeframe помогает отделить долгосрочные тренды от разовых отклонений.

### PurePath waterfall

При выборе одного медленного запроса в карточке открывается **waterfall-диаграмма**. На ней все шаги обработки:

- Время на сервере (Server-side time).
- Время каждого backend-вызова (HTTP / gRPC к другим сервисам).
- Время каждого SQL-запроса.
- Время ожидания внешних API.

Инструмент для поиска bottleneck. *Пример вывода:* общее время 800 мс, из них 620 мс: один SQL-запрос в БД X. Дальше: SQL оптимизировать, индекс добавить, кэш поставить.

### Шаг 2: Anomaly detection for services (пороги для «красных» сервисов)

![Anomaly detection for services: пороги, определяющие когда сервис считается проблемным](screenshots/day-2/service-cards/settings/builtinanomaly-detection.services/Anomaly-detection-for-services-Environment-Settings-Demo-live-Demo-Live-Dynatrac.png)

Путь в меню: **Settings → Anomaly detection → Services**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services`.

Эта страница разбиралась в Дне 1, Тема 9 (baselines). В контексте «карточки сервиса» её значение такое: настройки этой страницы определяют, **когда карточка сервиса получает красный статус и создаётся Problem**.

**Ключевые блоки** (повтор для контекста):
- **Response time degradations**: детекция деградаций времени отклика (All requests + Slowest 10%).
- **Failure rate**: детекция роста ошибок.
- **Service load drops/spikes**: детекция резких падений или скачков нагрузки.
- **Reference period**: период эталона (по умолчанию Last 7 days).

**Что важно помнить в контексте анализа.** Если при разборе жалобы «сервис медленный» в карточке сервиса вы не видите активной Problem, но Response time действительно выше нормы: проверьте пороги этой страницы. Возможно, пороги слишком консервативные и Davis AI ждёт больше отклонения. Или, наоборот, пороги слишком чувствительные, и Problem создаётся по любой мелочи, и дежурный её игнорирует: тогда реальная проблема теряется в шуме.

**Тонкая настройка** per service делается через Settings в карточке самого сервиса: можно перекрыть глобальные пороги для одного критичного сервиса более жёсткими, или наоборот: ослабить для сервиса с нестабильной нормой.

### Шаг 3: Endpoint metrics (сбор метрик на уровне отдельных endpoint'ов)

![Endpoint metrics: настройка сбора метрик на уровне отдельных endpoint сервиса](screenshots/day-2/service-cards/settings/builtinunified-services-endpoint-metrics/Endpoint-metrics-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Service Detection → Endpoint metrics**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:unified-services-endpoint-metrics`.

*Что такое Endpoint metrics.* Сервис может иметь десятки-сотни endpoint'ов. По умолчанию Dynatrace агрегирует все запросы в общие метрики сервиса. Endpoint metrics позволяет **собирать отдельные метрики для каждого endpoint'а**: Response time, Throughput, Failure rate per endpoint.

Нужно, когда часть endpoint'ов значительно отличается от остальных. Пример: `/api/reports/heavy` медленный по дизайну, `/api/simple` быстрый. Общие метрики сервиса смешивают оба и не показывают реальную картину каждого.

*Что на странице.* Единственный тумблер включения Endpoint metrics; дополнительных правил, лимитов и naming-полей на этом экране нет. Включение даёт заметный объём дополнительных метрик, поэтому решение принимают осознанно.

*Типовое применение.* Включают для критичных public API (интернет-банк, мобильный фронт), где SLA считается на уровне конкретного endpoint. Для внутренних микросервисов обычно выключено: общая метрика сервиса достаточна, данных меньше.

*Связь с SLO.* Endpoint metrics: основа SLO на конкретный endpoint. Типовой SLO: «Availability `/api/auth/login` должна быть ≥ 99.9% за 30 дней». Для измерения нужна метрика именно этого endpoint'а, отдельно от других (у которых могут быть другие требования).

---

## ⚙️ COOKBOOK: типовые workflow анализа через карточку

### Жалобы «интернет-банк тормозит»

*Вход.* Жалоба → Problems → проблема на Application Retail Banking Frontend → Root cause указывает на backend-сервис `payment-api`.

*Работа в карточке payment-api:*

1. Overview → Response time вырос с 120 мс до 450 мс за последний час.
2. Сравнение с предыдущим периодом: `↑ 275%`. Значимое отклонение.
3. Top requests → какой endpoint замедлился больше всех. `/api/payment/process`: с 150 мс до 600 мс.
4. Открываем endpoint → PurePath waterfall → 500 мс, это один SQL-запрос к БД `account-db`.
5. Переход в `account-db` → Top Database Statements → конкретный SQL с резким ростом времени.
6. Передача DBA для оптимизации.

### Проверка после пика нагрузки

*Задача.* Прошла плановая рассылка SMS-уведомлений, нагрузка на `notification-service` выросла в 10 раз. Нужно убедиться, что сервис справился.

*Работа в карточке:*

1. Выбираем Last 4 hours (охватывает рассылку).
2. Overview → Throughput пик 10000 req/min вместо обычных 1000.
3. Response time: медиана выросла с 30 до 45 мс. Приемлемо.
4. Failure rate: 0.2% (вместо обычных 0.1%). Не критично.
5. Service flow → основной bottleneck: внешний SMS-gateway, замедлился, но остался работоспособным.
6. *Вывод.* Сервис справился, обновить capacity plan на следующую рассылку с запасом.

### Разбор Failure rate spike

*Задача.* В карточке `auth-service` внезапно вырос Failure rate до 5%. Нужно найти причину.

*Работа:*

1. График Failure rate за последний час: пик 5% в конкретные 10 минут.
2. Top requests → какой endpoint даёт больше всего ошибок. `/api/auth/login`: 80% ошибок.
3. Клик на endpoint → распределение ошибок по status code: 70% `401 Unauthorized`, 10% `500 Internal Server Error`.
4. `500` открываем в PurePath → исключение `ConnectionTimeout to LDAP server`.
5. `401` штатно: пользователи вводят неправильные пароли. Но 70% нехарактерно. Проверка RUM в Application → большинство `401` с одного IP → подозрение на brute-force.
6. Тикет в SOC на анализ.

---

## 🎓 ТЕОРИЯ: архитектура карточки сервиса в Dynatrace

### Какие данные агрегируются

**Response time.** Время от прихода запроса в сервис до отправки ответа. Включает все backend-вызовы рекурсивно. OneAgent измеряет на уровне инструментационных хуков в начале и конце обработки. Метрики «Services: Requests and request attributes» хранятся **до 365 дней** (configurable). Долгосрочно метрика идёт также в Metrics Classic с собственной лестницей прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/data-retention-periods -->

**Throughput.** Число запросов в минуту. Простой счётчик на стороне OneAgent.

**Failure rate.** Процент запросов с ошибкой от общего числа. Ошибка определяется по HTTP-статусу (≥500) и по exception в коде. Для каждого exception OneAgent фиксирует stack trace: потом можно группировать ошибки по типу.

**Percentiles (90 / 95 / 99).** Считаются приближённо, потоковой агрегацией без хранения полной истории запросов. Компромисс: точные перцентили требуют слишком много памяти, приближённые достаточны для практики.

### Service flow: как строится

*Основа: распределённые трейсы (PurePath).* Каждый запрос в инструментированном сервисе получает заголовок `x-dynatrace` с trace ID и span ID. Исходящий вызов: OneAgent добавляет этот заголовок в запрос. Принимающий сервис видит trace и связывает свои данные с контекстом вызова.

*Service flow*: агрегация всех таких трейсов за период. Для каждой пары сервисов: число вызовов, среднее время, частота ошибок. Граф строится из этих данных. Для читаемости при большом числе участников Dynatrace применяет dynamic aggregation: сервисы с малой долей в общем времени отклика автоматически сворачиваются в группы.

Service flow: самое крупнозернистое представление timing'а сервиса. Более детальные срезы: Response time (на уровне методов внутри сервиса) и Distributed Traces (на уровне отдельных нод трейса с разбивкой processing / suspension / wait / lock / I/O). <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/application-observability/services-classic/service-analysis-timing -->

*Ограничения.* Если сервис не инструментирован (не-OneAgent, legacy), он виден как External service без детализации. Если между сервисами нестандартный протокол (бинарный, кастомный), PurePath может не распространиться, связь в графе теряется.

### Сравнение периодов: техника

**Reference period.** При выборе Last X Dynatrace берёт X предыдущих единиц как reference. Пример: Last 2 hours → reference = часы 4-2 назад.

**Метрика изменения.** Процент изменения между current и reference: `(current - reference) / reference × 100`.

**Цветовой индикатор.** Красный: рост «плохих» метрик (Response time, Failure rate). Зелёный: рост «хороших» (Throughput) или снижение «плохих».

*Нюанс: сезонность.* Сравнение с «2 часа назад» может обманывать: если переход между пиком и затишьем, ночью vs днём, будни vs выходные. Кастомный Timeframe `same time last week` сравнивает ровно с 7 днями назад: часто даёт более осмысленную картину для сервисов с выраженной сезонностью.

### Air-gapped нюансы

**Вся механика локальна.** PurePath собирается в кластере, метрики агрегируются в Cassandra, карточка сервиса отрисовывается через API кластера.

**Долгосрочное хранение метрик.** Metrics Classic хранятся до **5 лет** с той же лестницей прореживания, что приведена выше в разделе про Response time. Distributed traces: конфигурируется, **до 365 дней** максимум; код-уровень insights детально 10 дней (фикс). Services: Requests and request attributes: конфигурируется, **до 365 дней** максимум. Точные параметры: в [Data retention periods: Managed](https://docs.dynatrace.com/managed/shortlink/data-retention-periods). Расширения retention в Managed настраиваются в лицензии через CMC, либо через экспорт в отдельную долгосрочную систему через API. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/data-retention-periods -->

**Метаданные облачных хостов.** Если хост в частном облаке (AWS / Azure / GCP): Dynatrace видит облачные метаданные только при наличии Cloud ActiveGate с соответствующей ролью. В полностью on-premises контуре ограничение не применяется.

---

## 📝 Практика (3 минуты, выполнимо на demo-тенанте)

1. Открыть **Application Observability → Services** → карточка `easyTravel Customer Frontend`.
2. Найти секцию **Understand dependencies** и прочитать вслух пять кнопок переходов.
3. Через **View distributed traces** открыть трассировки и найти любой трейс с ошибкой.

Что должно получиться: имя сервиса, на котором ошибка загорелась. Контрольный вопрос себе: медиана времени отклика невысокая, а 99-й перцентиль в разы выше; о ком из пользователей рассказывает перцентиль и почему среднему верить нельзя.
