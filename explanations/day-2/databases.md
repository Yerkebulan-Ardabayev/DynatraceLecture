> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 6 из 9: «Мониторинг БД: Oracle, PostgreSQL, MS SQL, MongoDB»
>
> 🔖 **Редакция от 2026-04-26.** Тех-факты сверены с `docs.dynatrace.com/managed/` и общими страницами Database services classic / anomaly detection (общие для Managed и SaaS). Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-26 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Managed-специфика (приоритетный источник):**
> - [Applications and microservices — Dynatrace Managed](https://docs.dynatrace.com/managed/observe/applications-and-microservices) — раздел про сервисы (включая БД) в Managed-документации
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed) — корневая страница раздела Managed Docs
>
> **Общая (одинаково для Managed и SaaS):**
> - [Databases — overview](https://docs.dynatrace.com/docs/observe/applications-and-microservices/databases) — корневая страница темы Databases
> - [Database services classic](https://docs.dynatrace.com/docs/observe/applications-and-microservices/databases/database-services-classic) — классический интерфейс мониторинга БД (используется в Managed)
> - [How database activity is monitored](https://docs.dynatrace.com/docs/observe/applications-and-microservices/databases/database-services-classic/how-database-activity-is-monitored) — почему клиентская инструментация, как работает перехват SQL-запросов
> - [Analyze database services (classic page)](https://docs.dynatrace.com/docs/observe/applications-and-microservices/databases/database-services-classic/analyze-database-services) — карточка БД, hotspots, failed statements
> - [Top database statements](https://docs.dynatrace.com/docs/observe/applications-and-microservices/multidimensional-analysis/top-database-statements) — топ SQL по Total time / Average time
> - [Database insights](https://docs.dynatrace.com/docs/observe/applications-and-microservices/databases/database-services-classic/database-insights) — расширенная диагностика, включая Oracle insights
> - [Adjust sensitivity of anomaly detection for database services](https://docs.dynatrace.com/docs/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services-database) — пороги response time, failure rate, failed connects
> - [Anomaly detection — databases — settings schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-anomaly-detection-databases) — формальная схема страницы Database anomaly detection

## 📍 КАРТА — где смотреть и настраивать базы данных

Термины темы: `Database Service / сервис базы / клиентская сторона БД`, `Database Host / хост базы`, `Statement / оператор / SQL-запрос`, `Anomaly detection / обнаружение аномалий`, `Failed connect / ошибка подключения`.

| Что показать | Путь в меню | Прямая ссылка | Зачем |
|---|---|---|---|
| Список баз данных | **Application Observability → Database Services** | `https://guu84124.live.dynatrace.com/ui/databases` | Все БД, к которым обращаются инструментированные сервисы |
| Настройка аномалий БД | **Settings → Anomaly detection → Database services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.databases` | Пороги по времени отклика, ошибкам, проблемам подключения |

**Что Dynatrace видит в базе через клиентскую инструментацию:**

| Наблюдение | Откуда | Что даёт |
|---|---|---|
| Каждый SQL-запрос с параметрами | JDBC/ODBC-драйвер приложения | Top Database Statements — самые частые и медленные SQL |
| Время ответа на запрос клиента | Round-trip на стороне клиента | Response time median / Slowest 10% |
| Ошибки выполнения | Exceptions от драйвера | Failure rate и детали в карточке |
| Проблемы с соединением | Timeouts / Refused / Auth failures | Правило Anomaly detection → Failed connects |
| Пул соединений | HikariCP, Apache DBCP и аналоги | Активные / idle / утечки |

---

## 🎬 Работа с базами данных на двух экранах тенанта

### Шаг 1 — Список баз данных

![Databases — список 30 баз с фильтрами Cloud provider, Database technology, Problem impact](screenshots/day-2/databases/databases/Databases-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Application Observability → Database Services**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/databases`.

Экран показывает все БД, к которым обращаются сервисы под мониторингом. Сверху — заголовок **30 Databases**. Это количество баз на демо-тенанте за выбранный период. На боевой цифра зависит от числа инструментированных приложений и их трафика.

Нюанс: сюда попадают только те базы, с которыми работал хотя бы один инструментированный клиент. Неиспользуемая БД в списке не появится. Это клиентская перспектива, не инвентарь инфраструктуры.

Под заголовком подсказка от интерфейса: `See all databases that were active within the selected timeframe and match the filter settings`. Список зависит от двух вещей: timeframe сверху (по умолчанию Last 2 hours) и фильтров слева.

**Левая панель фильтров — три категории:**

- **Cloud provider** — чекбоксы AWS RDS и Azure. Видно, где живут managed-базы в облаке.
- **Database technology** — AWS DB2, Derby Client, H2, IBM и ещё шесть опций в выпадающем списке (`+6 options in the filter field`). Тип определяется по JDBC-драйверу клиента.
- **Problem impact** — Any / Impacted / Not impacted. На captured-экране индикатор: `1 Database that matches your query is associated with Davis-detected problems`. То есть одна база сейчас под активной проблемой от Davis.

**Колонки таблицы:**

- **Name** — имя БД. Dynatrace строит его из контекста запроса: технология + идентификатор хоста/инстанса.
- **Response time median** — медиана времени ответа.
- **Slowest 10%** — время отклика верхних 10% запросов. Показывает «тяжёлые» операции.
- **Failure rate** — процент запросов с ошибкой.
- **Requests** — запросов в минуту.
- **Actions** — контекстное меню, переход в карточку БД.

Логика имени в captured-данных: `[eks-live][easytrade-live-debugger] TradeManagement i-0f7a7ed4fe4218ffb`. Префикс — среда и приложение, имя — TradeManagement, суффикс — EC2-инстанс `i-0f7a7ed4fe4218ffb`. Для managed-БД в облаке в имени идентификатор инстанса. Для embedded-БД (H2/SQLite) префикс `[embedded]`.

Реальные показатели `TradeManagement` на демо: медиана `2.09 ms`, Slowest 10% `10.1 ms`, 0% ошибок, 248 запросов в минуту.

**Клик по имени БД** открывает карточку:

- **Overview** — Response time / Throughput / Failure rate за период с наложением активных Problems.
- **Top Database Statements** — топ частых и медленных SQL-операторов. Текст запроса, количество вызовов, время, вызывающий сервис.
- **Service flow** — граф сервисов, ходящих в эту БД, с долями трафика.
- **Consumers** — список процессов-клиентов.

**Кнопки сверху справа:** `Update` — ручной refresh. `Pin to dashboard` — закрепить на дашборд. `Top database statements` — общий отчёт по всем SQL-операторам окружения. `Multidimensional analysis` — разрез по нескольким измерениям.

### Шаг 2 — Anomaly detection for databases (пороги аномалий)

![Anomaly detection for databases — правила обнаружения деградаций по всем базам окружения](screenshots/day-2/databases/settings/builtinanomaly-detection.databases/Anomaly-detection-for-databases-Environment-Settings-Demo-live-Demo-Live-Dynatra.png)

Путь в меню: **Settings → Anomaly detection → Database services**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.databases`.

Страница — глобальные пороги обнаружения проблем для всех БД окружения. Устройство такое же, как `/ui/settings/builtin:anomaly-detection.services` (разобрана в Дне 1, Тема 9). Отличие — один блок, специфичный для баз.

В captured-хедингах виден только заголовок **Reference period**. Это окно истории для построения baseline / базовой линии. По умолчанию Last 7 days. Davis AI анализирует семь дней поведения БД с учётом времени суток и дня недели.

*Риск:* если за эти семь дней была миграция, новый индекс или резкая смена нагрузки — baseline будет ложно срабатывать несколько дней, пока модель пересчитается.

Остальные блоки — вложенные элементы формы, в headings не извлекаются. По смыслу:

**Response time.** Тумблер `Detect response time degradations`. Внутри два подблока — All requests (медиана всех запросов) и Slowest 10% (верхние 10% самых медленных). Для каждого абсолютный и относительный пороги, срабатывают одновременно. Пороги для БД обычно выше, чем для сервисов — сами базы медленнее.

**Failure rate.** Тумблер `Detect increases in failure rate`. Абсолютный и относительный пороги. Ловит любые SQL-ошибки, которые драйвер возвращает клиенту.

**Database failed connects.** Специфичное для БД правило. Ловит проблемы подключения: сетевые разрывы, исчерпание пула, истёкший пароль, отказ аутентификации, failover с прерыванием. Порог — процент неудачных подключений в минуту.

*Почему отдельное правило, а не часть Failure rate:* в приложениях с пулом соединений ошибки подключения возникают раньше пользовательских. Их нужно ловить быстрее.

**Load drops / spikes.** Резкое падение или скачок нагрузки. Падение — клиенты не могут достучаться до БД (сеть, DNS, балансировщик). Скачок — новая версия приложения делает больше запросов или выкатился медленный SQL с ретраями.

**Когда менять дефолты:**

- БД с высокой нагрузкой (например, центральная БД). Порог Slowest 10% имеет смысл поднять — время верхних 10% может быть десятки миллисекунд даже в норме. Дефолт 1000 мс будет срабатывать слишком часто.
- БД с редкой нагрузкой (отчётные, ночные). Параметр `Avoid over-alerting` поднять выше стандартного «10 запросов в минуту». Иначе каждый всплеск активности в окне обслуживания будет создавать аномалию.

Переопределение на уровне конкретной БД — в карточке этой БД → Settings. Глобальная страница задаёт дефолт, карточка — индивидуальное исключение.

---

## ⚙️ COOKBOOK — что настраивать для разных типов БД

Для каждого типа БД — где ставить OneAgent, какие пороги Anomaly detection скорректировать, на что смотреть в первую очередь.

### Oracle DB

*Типичное применение:* центральные OLTP-системы, ERP, учётные системы.

- **OneAgent.** Обязателен на всех серверах приложений, которые ходят в Oracle (Java/WebLogic, .NET). На самом сервере Oracle агент не обязателен — мониторинг клиентский. Но если хост БД на собственном железе и доступ есть — поставить и туда, получим метрики ОС (CPU / Memory / Disk I/O).
- **Anomaly detection.** Порог Slowest 10% часто нужно поднять выше дефолта 1000 мс. Oracle под нагрузкой может естественно давать десятки-сотни миллисекунд на верхних 10% даже в норме. Конкретное значение — по результатам наблюдения baseline первые 2-3 недели.
- **Maintenance windows.** На ночное техобслуживание. Иначе плановое окно будет постоянно триггерить алерты.
- **Alerting profile.** Выделенный профиль для prod-базы. Проблемы отправляются DBA-команде через ServiceNow или почту.

*Если пойдут ошибки:* Dynatrace создаст одну Problem с корневой причиной на БД и затронутыми клиентскими сервисами. В карточке будут конкретные SQL-операторы, начавшие падать. В ServiceNow уйдёт алерт с контекстом — какие приложения затронуты.

### PostgreSQL в Kubernetes

*Типичное применение:* новые микросервисы, проекты модернизации.

- **OneAgent.** На K8s-нодах через Operator. Клиентские поды инструментируются автоматически.
- **PostgreSQL в поде.** Включить container monitoring или поставить OneAgent sidecar.
- **Anomaly detection.** Дефолтные пороги обычно подходят — нагрузка на один инстанс небольшая.
- **Теги по namespace.** `k8s:namespace:payment-services` и аналогичные. Это даёт фильтрацию всех БД одного namespace вместе.

### Microsoft SQL Server

*Типичное применение:* CRM, шины данных, аналитика, .NET-приложения.

- **OneAgent.** На всех .NET-серверах приложений. Если MSSQL на отдельном Windows-сервере — поставить и туда, получим метрики ОС.
- **Anomaly detection.** Дефолтные пороги.
- **Slowest 10%.** В MSSQL долгие запросы часто указывают на блокировки. Рост этого показателя ловить быстрее обычного.

### Redis

*Типичное применение:* кэш, сессии, очереди. Латентность — микросекунды, обычные запросы укладываются в 1 мс.

- **OneAgent.** Инструментирует клиентов Redis автоматически — Jedis / Lettuce / StackExchange.Redis и другие популярные драйверы.
- **Slowest 10%.** Порог понизить. Redis всегда отвечает быстро, рост до миллисекунд — уже деградация.
- **Failed connects.** Оставить дефолт. Redis очень чувствителен к сетевым проблемам, обычно падает первым в цепочке инцидентов.

---

## 🎓 ТЕОРИЯ — ключевые концепции мониторинга БД в Dynatrace

**Database Service vs Database Host.** Два термина, которые путают. `Database Service / сервис БД` — это БД с точки зрения клиента. Её видит OneAgent через JDBC/ODBC-драйвер приложения. Метрики — время ответа на запрос клиента. `Database Host / хост БД` — физический или виртуальный хост, где живёт процесс БД. Метрики — CPU, Memory, Disk I/O операционной системы. Связаны через Smartscape (Service → Process → Host), но сущности разные. Список `/ui/databases` — это Database Services. На хосты смотреть — Infrastructure → Hosts или drilldown из карточки БД.

**Почему клиентская инструментация.** Dynatrace не подключается к административному интерфейсу БД, не делает `SELECT FROM pg_stat_statements`. Вместо этого — перехват каждого запроса в клиенте. Преимущества:

- Нет отдельных учётных записей для мониторинга в каждой БД. Никаких `GRANT SELECT`, `CREATE USER`.
- Работает с managed-БД в облаке, где административный доступ закрыт (AWS RDS, Azure Database).
- Видно именно то, что видит приложение — тот же SQL, то же время, те же ошибки.
- Нулевая нагрузка на саму БД. OneAgent работает на стороне клиента.

**Ограничение клиентской инструментации.** Видны только запросы инструментированных клиентов. Ночной cron со скриптом на чистом psql — не инструментирован, его запросы не видны. Решения: обернуть в Python/Java с OneAgent или использовать Extensions с прямым опросом БД (JMX, SQL-плагин).

**Top Database Statements — как работает.** В карточке БД список топ N частых и медленных SQL. «Самый медленный» = запрос с максимальным суммарным временем за период (число вызовов × среднее время).

*Пример.* Один запрос вызывается раз в час, занимает минуту — это 60 секунд в час. Сто запросов вызываются раз в секунду, занимают 100 мс — тоже 60 секунд в час. Оба одинаково нагружают БД, оба попадают в топ.

Dynatrace показывает обе метрики отдельно: **Total time** — для системной нагрузки, **Average time** — для медленных индивидуальных операций.

**Параметры SQL в статистике.** SQL нормализуется перед группировкой. `SELECT * FROM users WHERE id = 42` и `SELECT * FROM users WHERE id = 43` считаются одним запросом с параметром id. Иначе каждый запрос был бы уникальным, статистика не имела бы смысла. В карточке виден параметризованный SQL (`WHERE id = ?`) и примеры реальных значений. Это помогает диагностировать случаи «почему именно для этого пользователя запрос медленный».

**Failed connects — почему отдельный индикатор.** Когда клиент не может подключиться (`Connection refused`, `Authentication failed`, timeout), драйвер бросает исключение. OneAgent фиксирует это как Failed connect. Если процент за минуту превышает порог — Davis создаёт Problem.

*Особенность:* эта Problem появляется быстрее, чем проблема по времени отклика. Failed connects ловятся за минуту плохих попыток. Для response time нужно несколько минут устойчивого ухудшения. Поэтому Failed connects — самый чувствительный индикатор «БД недоступна» и первым попадает в ServiceNow при сетевых или конфигурационных инцидентах.

**Air-gapped контекст.** Мониторинг БД полностью локален. OneAgent на сервере приложения собирает метрики, отправляет через ActiveGate в кластер, данные живут в Cassandra. Никаких внешних вызовов — ни к облачным сервисам Dynatrace, ни к БД напрямую от кластера. Контур изолирован, мониторинг не создаёт новых каналов связи.

**Связь с другими темами.** Проблемы в БД часто идут рука об руку с проблемами хостов (Темы 1 и 3 Дня 2) и ошибками бизнес-сервисов (Темы 7-8 Дня 2). Маршрут расследования: жалоба на сервис → в карточке сервиса блок Database calls → карточка конкретной БД → Top Statements для поиска проблемного SQL → при необходимости хост БД для проверки ресурсов.
