> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 2 из 9: «Как OneAgent собирает инфраструктурные метрики»
>
> 🔖 **Редакция от 2026-04-26.** Тех-факты сверены с `docs.dynatrace.com/managed/` и общими страницами OneAgent / Infrastructure monitoring modes (общие для Managed и SaaS). Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-26 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Managed-специфика (приоритетный источник):**
> - [Dynatrace OneAgent — Dynatrace Managed](https://docs.dynatrace.com/managed/ingest-from/dynatrace-oneagent) — раздел OneAgent в Managed-документации (точка входа для air-gapped инсталляций)
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed) — корневая страница раздела Managed Docs
>
> **Общая (одинаково для Managed и SaaS):**
> - [Dynatrace OneAgent — overview](https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent) — корневая страница про OneAgent (модули, режимы, поддержка платформ)
> - [OneAgent — параметрический shortlink](https://docs.dynatrace.com/docs/shortlink/oneagent) — каноническая точка входа для темы OneAgent
> - [OneAgent installation and operation](https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent/installation-and-operation) — установка, обновление, диагностика OneAgent на хосте
> - [Infrastructure and Discovery monitoring modes](https://docs.dynatrace.com/docs/observe/infrastructure-observability/hosts/monitoring-modes) — Full-Stack / Infrastructure / Discovery — что собирается в каждом режиме
> - [Process deep monitoring](https://docs.dynatrace.com/docs/observe/infrastructure-observability/process-groups/configuration/pg-monitoring) — глубокая инструментация процессов и правила её включения
> - [OneAgent platform and capability support matrix](https://docs.dynatrace.com/docs/ingest-from/technology-support/oneagent-platform-and-capability-support-matrix) — какие ОС, какие фичи, какие версии поддерживаются
> - [Technology support — overview](https://docs.dynatrace.com/docs/ingest-from/technology-support) — поддерживаемые технологии и сенсоры
> - [Extensions 2.0](https://docs.dynatrace.com/docs/extend-dynatrace/extensions20) — фреймворк расширений (SNMP, JMX, REST) для нестандартного железа
> - [Extend metrics](https://docs.dynatrace.com/docs/ingest-from/extend-dynatrace/extend-metrics) — способы добавить пользовательские метрики через OneAgent

## 📍 КАРТА — где управлять сбором инфраструктурных метрик

Термины темы: `OneAgent / агент`, `ActiveGate / AG / шлюз`, `Feature / фича / возможность`, `Sensor / сенсор`, `Edge sensor / Edge-сенсор / опрос с ActiveGate`, `eBPF / extended Berkeley Packet Filter` (механизм перехвата в ядре Linux), `Opt-In / по умолчанию выключено`.

| Что показать | Путь в меню | Прямая ссылка | Зачем |
|---|---|---|---|
| Список возможностей агента | **Settings → Preferences → OneAgent features** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:oneagent.features` | Включение / отключение сенсоров (eBPF, SNMP-edge и др.) |
| Disk Edge — аномалии | **Settings → Anomaly detection → Disk Edge** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:infrastructure.disk.edge.anomaly-detectors` | Правила для Edge-устройств и удалённых хостов |

**Три слоя сбора инфраструктурных метрик:**

| Слой | Что собирает | Как настраивается |
|---|---|---|
| **OS-слой** (базовый) | CPU / Memory / Disk / Network через системные API | Автоматически, настроек нет |
| **Process-слой** | Метрики каждого процесса + группировка | Settings → Processes and containers (День 1, Тема 3) |
| **Feature-слой** | Расширенные сенсоры (eBPF, SNMP, container runtimes) | Settings → Preferences → OneAgent features |

---

## 🎬 Работа с настройками инфраструктурного сбора на двух экранах

### Шаг 1 — OneAgent features (общие возможности, включая инфраструктурные)

![OneAgent features — таблица всех фич OneAgent с тумблерами включения и метаданными](screenshots/day-2/oneagent-infra/settings/builtinoneagent.features/OneAgent-features-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Preferences → OneAgent features**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:oneagent.features`.

Страница разбиралась в Дне 1, Тема 3 в контексте инструментации приложений. Здесь фокус — на **сборе низкоуровневых инфраструктурных данных**.

**Инфраструктурные фичи на этой странице:**

- **eBPF network tracing.** Механизм в ядре Linux, перехватывающий сетевые соединения процессов без модификации приложения. OneAgent видит каждое TCP/UDP-соединение: кто, к кому, на какой порт, с каким трафиком. Из этих данных строится сетевая карта Smartscape. Требуется OneAgent нужной версии и поддержка eBPF в ядре (Linux 4.9+).

- **OpenTelemetry ingest.** Приём OTLP-потоков от приложений, инструментированных OpenTelemetry. Альтернатива OneAgent-инструментации для языков, которые OneAgent не поддерживает напрямую. ActiveGate принимает OTLP на специальном endpoint, превращает в Dynatrace-спаны и метрики.

- **SNMP Edge / ICMP Edge / WMI Edge.** Edge-сенсоры, опрашивающие устройства напрямую от ActiveGate. Для оборудования без OneAgent: сетевые устройства, принтеры, UPS, промышленные контроллеры. Каждый сенсор — отдельная фича в списке.

- **Container monitoring** (варианты для Docker, containerd, CRI-O, Podman). Углублённый сбор данных по контейнерам. Базовые варианты включены по умолчанию, специфичные для новых рантаймов часто Opt-In. Подробности — в теме containers.

- **Log monitoring.** Сбор логов с хостов. По умолчанию выключен, включается вручную.

**Колонки таблицы:**

- **Enabled** — тумблер.
- **Summary** — описание фичи и технология.
- **Min. OneAgent version** — минимальная версия, с которой фича доступна.
- **Details** — раскрывающаяся карточка с параметрами.

Фильтрация через поле вверху. Набрал `eBPF` — получил все eBPF-сенсоры.

*Air-gapped нюанс.* Метка `Opt-In` — по умолчанию выключено, администратор включает явно. Сделано, чтобы не нагружать свежий OneAgent избыточными сенсорами. В изолированном контуре часть Opt-In фич — интеграции с облачными сервисами (AWS Lambda sensor, Azure Functions sensor). Включать их бессмысленно — соответствующих ресурсов в контуре нет. Администратор просматривает Opt-In список и включает только то, что реально используется.

### Шаг 2 — Anomaly detection for infrastructure: Disk Edge

![Disk Edge anomaly detection — правила для удалённых edge-мониторов дисков](screenshots/day-2/oneagent-infra/settings/builtininfrastructure.disk.edge.anomaly-detectors/Anomaly-detection-for-infrastructure-Disk-Edge-Environment-Settings-Demo-live-De.png)

Путь в меню: **Settings → Anomaly detection → Disk Edge**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:infrastructure.disk.edge.anomaly-detectors`.

Страница — настройки аномалий для **Disk Edge**, мониторинга дисков через Edge-сенсоры (не OneAgent, а опрос с ActiveGate с соответствующей ролью). Заголовков в captured нет, страница минималистичная.

*Что такое Disk Edge.* Способ сбора метрик с устройств без OneAgent — опрос от ActiveGate по специализированному протоколу. Для дисков обычно SNMP-опрос дисковой полки или SAN-контроллера (NetApp, EMC/Dell, HPE 3PAR). Получаются метрики состояния RAID, занятости LUN, скорости ввода-вывода на уровне массива.

*Отличие от обычного Disk monitoring.* Обычный Disk monitoring видит файловую систему на хосте с OneAgent: `/`, `/var`, `/backup`. Disk Edge видит **само хранилище**, уровнем ниже ФС: состояние RAID, пропускная способность контроллера, число ошибок дисков массива. Первое — перспектива клиента, второе — перспектива провайдера.

*Типовое применение.* Хосты с выделенными массивами под СУБД — нужно видеть состояние самого оборудования, а не только то, что показывает Linux. На ActiveGate ставится Extension (плагин SNMP / NetApp / EMC), данные идут в Dynatrace как отдельные метрики.

*Что на странице настраивается.* Правила аномалий для метрик Disk Edge. Примеры:

- RAID-массив в состоянии degraded более 5 минут → Problem.
- Очередь I/O дисковой полки > 200 → Problem.
- Число hot spare uninitialized выше порога → Problem.

Структура правил стандартная: scope (устройства), condition (условие), severity (уровень Problem).

На captured-тенанте правил нет. Для демо без реального оборудования это нормально. Страница используется, когда в контуре есть дисковые массивы с мониторингом через ActiveGate.

---

## 🎓 ТЕОРИЯ — детальный разбор механики сбора инфраструктурных метрик

### Как OneAgent интегрируется с ОС

**Модульная архитектура.** OneAgent — не один большой процесс, а набор взаимодействующих модулей. На Linux три основных:

- **Core** (`oneagentos`) — опрос ОС, сбор CPU / Memory / Disk / Network, отправка в кластер.
- **Process observer** (`oneagentwatchdog`) — наблюдение за процессами, группировка, старт инструментации для сервисов.
- **Code module (loader)** — загрузчик инструментации в адресное пространство приложений (`-javaagent` в JVM, CLR Profiling API в .NET).

**Периодичность сбора и отправки.** OneAgent агрегирует метрики ОС на агенте и публикует их в кластер с **минутной гранулярностью** — это базовая publication-частота для built-in метрик. Внутри агента дискретизация для целей anomaly detection может выполняться чаще (для отдельных метрик хоста — до 10 секунд), но в Data Explorer и в metric events точки с интервалом меньше минуты не видны.

**Адаптивный приоритет.** Если на хосте высокая нагрузка, OneAgent может **снижать** интенсивность собственного сбора, чтобы не добавлять overhead. Поведение саморегулирующееся: в момент стресса агент шлёт меньше деталей, но базовый минутный publication остаётся. По окончании стресса детализация возвращается к норме.

### Что отличает OneAgent от традиционных агентов

**Zero configuration.** После установки OneAgent начинает собирать всю базовую инфраструктурную информацию без настройки. Ни конфига, ни регистрации метрик, ни списка портов. В Zabbix каждая метрика описывается в template, в Prometheus каждый endpoint добавляется в scrape-config.

**Auto-discovery технологий.** OneAgent сам определяет запущенные технологии: Java, .NET, БД, веб-серверы, контейнеры. Для каждой применяется соответствующий сенсор из Feature-слоя. В Zabbix / Prometheus это делается вручную.

**Единый канал.** Все данные — метрики, трейсы, логи, события — идут через одно TLS-соединение с ActiveGate на один порт. В традиционных мониторингах это несколько отдельных систем и протоколов (SNMP / StatsD / Syslog / scraping API).

**Адаптивный сэмплинг трейсов.** OneAgent выбирает, какие трейсы сохранять полностью, а какие агрегировать. При высоком трафике это снижает объём данных без потери диагностической ценности.

### Типовые сценарии настройки

**Первое развёртывание на 100-200 хостов.** Администратор не трогает OneAgent features — принимает дефолты. Собираются все базовые инфраструктурные метрики, большинство Opt-In фич выключено. В первый месяц копится baseline, Davis учится нормальному поведению окружения. Во второй месяц — ревью: какие Opt-In фичи стоит включить (Log monitoring для ошибок серверов приложений, OpenTelemetry ingest для новых сервисов на Go), какие нет.

**Подключение нового типа оборудования** (пример — сетевые устройства через SNMP). Шаги:

1. В CMC на ActiveGate включается роль Extensions.
2. В Dynatrace Hub ищется нужный extension, `.zip` скачивается с customer portal на машине с интернетом и загружается в кластер через Hub → Upload extension.
3. В OneAgent features проверить, что SNMP-сенсоры включены.
4. В Extensions → настройка списка устройств (IP + community string).
5. Через несколько минут метрики появляются в Data Explorer по префиксу `ext:*`.

**Массовое включение фичи с исключением для dev.** Нужно Log monitoring на всех prod-хостах, но не на dev. Шаги:

1. На OneAgent features включить Log monitoring глобально.
2. Для dev-хост-группы в Host settings — override: выключить Log monitoring.

prod получает логи, dev нет.

**Отладка ложной инструментации.** Приложение даёт ошибки после OneAgent. Разработка просит отключить инструментацию конкретной библиотеки. Шаги:

1. На OneAgent features через Filter найти сенсор этой библиотеки.
2. Выключить глобально — после перезапуска приложения сенсор не применяется.
3. Если сенсор нужен на других приложениях — вернуть в глобальное On, для конкретного хоста override через Host settings.

### Хранение на стороне кластера

- **Distributed traces Classic** — полные детали каждой транзакции хранятся **10 дней** (после 10 дней детализация падает, остаются агрегированные code-level insights). Источник: [Data retention periods](https://docs.dynatrace.com/docs/shortlink/data-retention-periods).
- **Services Classic / Request attributes** — короткосрочное хранение метрик сервиса для multidimensional-анализа: **35 дней**. Гранулярность зависит от timeframe (от 10 секунд для < 20 минут до 1 минуты для > 1 часа).
- **RUM Classic** — user actions / user sessions / Session Replay / mobile crashes — все по **35 дней**.
- **Log Monitoring Classic** — логи хранятся в Elastic File System в зоне кластера. Размер дискового хранилища настраивается в лицензии, фиксированного дефолтного срока в публичной документации не указано.
- **Metrics Classic** — единый ряд с прореживанием, ретеншн до **5 лет**. Гранулярность по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней–5 лет → 1 день.
- **События и Problems** — хранятся в Cassandra, длительный срок. Проблемы остаются доступными для пост-фактум разбора на месяцы и годы (точный дефолт зависит от настроек кластера).

### Air-gapped нюансы инфраструктурного сбора

- **Полная изоляция.** Никаких исходящих вызовов в интернет. Локальные фичи (eBPF, SNMP на внутренние устройства, container monitoring) работают без проблем.
- **Что не работает.** Фичи, требующие облачных API (AWS Lambda sensor, Azure Functions sensor). Включать их бессмысленно — ресурсов в контуре нет.
- **Edge-сенсоры** (SNMP / ICMP / WMI от ActiveGate) работают во внутренней сети. ActiveGate должен иметь сетевой доступ к опрашиваемым устройствам (обычно VLAN управления), но не в интернет.
- **Extensions** ставятся через CMC или Hub → Upload. Цикл: скачать на машине с интернетом → перенести через шлюз → загрузить в кластер через UI. Автообновления нет, обновления — по плановому окну.
- **Docker / CRI-O / containerd мониторинг** работает локально, внешних API не вызывает. Совместим с air-gapped. Это важно для окружений с Kubernetes — метрика контейнеров собирается и хранится локально.
