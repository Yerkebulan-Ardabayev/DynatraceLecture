> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 1 из 9: «Мониторинг ОС: CPU, RAM, IO, процессы в Dynatrace»
>
> 🔖 **Редакция от 2026-04-26.** Тех-факты сверены с `docs.dynatrace.com/managed/` и общими страницами Hosts / OS services monitoring (общие для Managed и SaaS). Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-26 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Managed-специфика (приоритетный источник):**
> - [Hosts — Dynatrace Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/hosts) — раздел Hosts в Managed-документации (точка входа)
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed) — корневая страница раздела Managed Docs
>
> **Общая (одинаково для Managed и SaaS):**
> - [Host monitoring with Dynatrace](https://docs.dynatrace.com/docs/observe/infrastructure-observability/hosts/monitoring/host-monitoring) — концепция инфраструктурного мониторинга, метрики хоста и интервалы сбора
> - [OS services monitoring](https://docs.dynatrace.com/docs/observe/infrastructure-observability/hosts/monitoring/os-services) — мониторинг Windows-служб и Linux systemd units, политики, требования systemd 230+
> - [Classic Windows services monitoring](https://docs.dynatrace.com/docs/observe/infrastructure-observability/hosts/monitoring/windows-services) — расширенная конфигурация мониторинга Windows-служб
> - [Host-level settings](https://docs.dynatrace.com/docs/observe/infrastructure-observability/hosts/configuration) — глобальные/per-host параметры, включая Disk options
> - [Host anomaly detection](https://docs.dynatrace.com/docs/observe/infrastructure-observability/hosts/configuration/anomaly-detection) — пороги CPU/Memory/Disk + Custom disk-detection rules
> - [Hosts — параметрический shortlink](https://docs.dynatrace.com/docs/shortlink/hosts) — каноническая точка входа для темы Hosts
> - [Host Units (HU) — формула лицензирования](https://docs.dynatrace.com/docs/shortlink/host-unit) — единица лицензирования и лестница 16 GiB
> - [Data retention periods](https://docs.dynatrace.com/docs/shortlink/data-retention-periods) — сроки хранения метрик и логов в Managed Classic

## 📍 КАРТА — где настраивается и где смотрится мониторинг ОС

Термины темы: `Host / хост`, `OS service / сервис ОС / служба` (Windows-служба или Linux systemd unit), `Process / процесс` (конкретный запущенный бинарник с PID), `Mount point / точка монтирования`, `Entity list / список сущностей`.

| Что показать | Путь в меню | Прямая ссылка | Статус на captured |
|---|---|---|---|
| Список хостов (entity list) | **Infrastructure Observability → Hosts** | `https://guu84124.live.dynatrace.com/ui/entity/list` | **404** — старый универсальный entity list отключён |
| OS services monitoring | **Settings → Monitoring → OS services monitoring** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:os-services-monitoring` | Мониторинг Windows-служб и Linux systemd units |
| Disk options | **Settings → Preferences → Disk options** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:disk.options` | Глобальные опции работы с дисками |
| Custom disk-detection rules | **Settings → Anomaly detection → Disk anomaly detection rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.disk-rules` | Пользовательские правила аномалий по дискам |

**Типизированные list-страницы, которые заменили старый `/ui/entity/list`:**

| Тип сущности | Прямая ссылка |
|---|---|
| Хосты | `https://guu84124.live.dynatrace.com/ui/entity/list/HOST` |
| Контейнеры (группы) | `https://guu84124.live.dynatrace.com/ui/entity/list/CONTAINER_GROUP` |
| Kubernetes workloads | `https://guu84124.live.dynatrace.com/ui/entity/list/CLOUD_APPLICATION` |
| Message queues | `https://guu84124.live.dynatrace.com/ui/entity/list/QUEUE` |
| Kubernetes clusters | `https://guu84124.live.dynatrace.com/ui/entity/list/KUBERNETES_CLUSTER` |

---

## 🎬 Работа с мониторингом ОС на четырёх экранах тенанта

### Шаг 1 — Entity list (404) и типизированные замены

![Entity list — страница возвращает 404, заменена типизированными списками по типам сущностей](screenshots/day-2/os-monitoring/entity/list/404-We-cant-find-this-page-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: ранее — универсальный список сущностей.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/entity/list`.

На этом тенанте страница возвращает 404: `We can't find this page. The page no longer exists or the link you clicked may be old and no longer available`. Версия платформы `1.336.55.20260417-205630`. Универсальный entity list заменён на типизированные списки по типу сущности.

Для работы с хостами используется `https://guu84124.live.dynatrace.com/ui/entity/list/HOST`. Список показывает все машины с установленным OneAgent.

**Колонки:** имя хоста, ОС, статус OneAgent (Active / Disabled), версия OneAgent, CPU, Memory, активные проблемы.

**Фильтры слева:** разрез по ОС (Linux / Windows / AIX), по хост-группам, по тегам, по облачному провайдеру (AWS / Azure / GCP).

**Клик на имя** открывает карточку хоста. Блоки:

- **Overview** — сводка CPU / Memory / Disk / Network в реальном времени.
- **Infrastructure** — графики каждой метрики: CPU per-core, Memory breakdown (Used/Cache/Buffers), Disk I/O, Network in/out.
- **Processes** — все процессы, сгруппированные по Process Groups.
- **Technology overview** — автоматически обнаруженные технологии (Java, .NET, PHP, Python и др.).
- **Events** — хронология событий: перезапуски OneAgent, проблемы, изменения конфигурации.
- **Logs** — если включен Log Monitoring, связанные системные и приложенческие логи.
- **Смонтированные файловые системы** — список дисков с параметрами и свободным местом.

### Шаг 2 — OS services monitoring

![OS services monitoring — конфигурация мониторинга Windows-сервисов и Linux-демонов](screenshots/day-2/os-monitoring/settings/builtinos-services-monitoring/OS-services-monitoring-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Monitoring → OS services monitoring**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:os-services-monitoring`.

Страница настраивает мониторинг **сервисов ОС** — Windows-служб и Linux systemd units. Это не то же, что мониторинг процессов (тема hosts-processes).

*Разница.* Процесс — запущенный бинарник с PID. Сервис ОС — логическая единица операционной системы, которую можно запустить / остановить / посмотреть в `systemctl status` или `services.msc`.

*Зачем отдельно.* Критичные компоненты часто регистрируются как службы: СУБД, службы очередей, антивирус, агенты интеграций, драйверы ключей. Если такая служба упала — её процесс не запущен, мониторинг процессов данных не имеет. А сам факт «служба была, сейчас не Running» — важный сигнал.

*Как работает.* OneAgent периодически опрашивает менеджер сервисов и фиксирует статус: Running / Stopped / Paused / Starting / Stopping. Статусы уходят в кластер как метрики.

На странице управление — какие службы мониторить, какие считать критичными (Problem при остановке), какие игнорировать (служебные Windows-сервисы, которые стартуют и падают штатно — `wuauserv`, `bits` и подобные).

**Типовые цели мониторинга:**

- Windows-серверы с MSSQL: `MSSQLSERVER`, `SQLSERVERAGENT`, `MSDTC`. Остановка — критичный алерт.
- Linux-серверы с PostgreSQL: `postgresql`, `pgbouncer`, `pgpool`. Переход в Stopped без планового окна — алерт.
- Серверы приложений: `tomcat`, `wildfly`, `weblogic`.
- Хосты с антивирусом: сервис антивирусного движка. Остановка может быть признаком компрометации, должна дойти до SOC.

Страница — это правила фильтрации «мониторить, если имя сервиса соответствует шаблону X». Правила глобальные, с возможностью переопределения на уровне хост-группы или конкретного хоста.

### Шаг 3 — Disk options (глобальные опции дисков)

![Disk options — глобальные параметры обработки дисков OneAgent](screenshots/day-2/os-monitoring/settings/builtindisk.options/Disk-options-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Preferences → Disk options**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:disk.options`.

Страница — глобальные параметры работы с дисками на всех хостах. Заголовков третьего уровня в captured нет, страница состоит из тумблеров и значений. Хлебная крошка: Settings → Preferences → Disk options.

*Где находится.* Preferences (Environment settings), не Monitoring или Anomaly detection. Эти настройки — не «как ловить аномалии», а «как обращаться с дисками при их обнаружении».

**Типовые параметры:**

- **Игнорирование типов файловых систем.** По умолчанию не собираются метрики с сетевых ФС (NFS, SMB/CIFS, Gluster), временных (tmpfs) и служебных (procfs, sysfs). Причина: tmpfs — это память, не диск; NFS может зависнуть при опросе и блокировать агент. Whitelist — если критичные данные лежат на специфичной ФС.

- **Игнорирование точек монтирования по пути.** Шаблоны `/proc/*`, `/sys/*`, `/var/lib/docker/*`. Скрывают технические монтирования из Smartscape и списков дисков.

- **Политика расчёта свободного места.** По умолчанию `available for non-root` — с учётом процента, зарезервированного root под ext3/ext4. Для СУБД на выделенных дисках иногда переключают на `total free`, чтобы точнее видеть запас.

- **Частота сбора и отправки метрик.** OneAgent отправляет агрегированные метрики хоста в кластер с минутной гранулярностью — это базовая (publication) частота. Внутри агента дискретизация для целей anomaly detection может идти чаще (до 10 секунд для отдельных метрик), но это не меняет интервал точек, видимых в Data Explorer.

Обычно страница трогается один раз при развёртывании: добавляется корпоративный шаблон монтирований для скрытия внутренних путей. Дальше — только при изменениях в инфраструктуре.

### Шаг 4 — Custom disk-detection rules

![Disk anomaly detection rules — кастомные правила детекции проблем с дисками](screenshots/day-2/os-monitoring/settings/builtinanomaly-detection.disk-rules/Disk-anomaly-detection-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Anomaly detection → Disk anomaly detection rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.disk-rules`.

Страница создаёт **пользовательские правила аномалий по дискам**. Это не замена глобальным правилам из Anomaly detection → Hosts, а дополнение для случаев, когда стандартные пороги не подходят конкретному диску.

*Типовой случай.* Диск под бэкапы СУБД, 10 ТБ. Бэкапы пишутся пачками и занимают 60-70% диска. Глобальное правило «меньше 30% свободного — проблема» срабатывает каждую ночь и генерирует шум. Кастомное правило «на диске `/backup` на хостах `db-*` считать проблемой только ниже 5%» — ночные всплески не триггерят алерты, реальные проблемы ловятся.

**Структура правила:**

- **Scope** — охват: по имени хоста, по хост-группе, по тегам, по точке монтирования (`/backup`, `/var/log`).
- **Condition** — условие: низкое свободное место (процент или абсолют), низкая скорость записи/чтения, высокое число ошибок I/O, высокая очередь к диску.
- **Action** — что делать: создать Problem с таким-то Severity, использовать такой-то alerting profile.

**Типовые правила в практике:**

- Исключение диска бэкапов из общего порога свободного места.
- Отдельный порог для `/var/log` на production-хостах — ловить переполнение логов раньше общего.
- Правило для файлового хранилища с контролем роста I/O-ошибок (признак старения дисков).
- Специфичный порог для Oracle Flash Recovery Area.
- Правило для SSD под индексы — при переполнении производительность падает быстрее, чем у HDD.

На captured демо-тенанте правил нет. Обычно пишутся в первый месяц после развёртывания, когда накопилась история нагрузки и понятно, какие диски требуют особой политики.

---

## 🎓 ТЕОРИЯ — как OneAgent собирает ОС-метрики и что с этим делает Dynatrace

### Механика сбора

**OneAgent на каждом хосте** запускает отдельный процесс мониторинга (`oneagentos` на Linux, `Dynatrace OneAgent Operating System Agent` на Windows), который постоянно опрашивает операционную систему по стандартным API.

**На Linux** это чтение файлов `/proc` (CPU, memory, processes, network connections), `/sys` (block devices, interfaces, hardware), вызов `stat()` на файловые системы, чтение `/var/log/messages` и аналогичных для системных событий, взаимодействие с `systemd` через D-Bus для статусов сервисов.

**На Windows** это вызовы Windows Performance Counters (CPU, memory, disk, network), Windows Management Instrumentation (WMI) для hardware и сервисов, чтение Event Log для системных событий, взаимодействие с Service Control Manager для статусов служб.

**На AIX** это чтение аналогов proc и sys через AIX API, взаимодействие с System Resource Controller для сервисов.

**Все эти данные** OneAgent агрегирует и отправляет в кластер через ActiveGate с минутной гранулярностью (это базовая частота publication для built-in метрик). В кластере данные попадают в Cassandra (недавние временные ряды) и в метрики-store для долговременного хранения с прореживанием. Гранулярность точек, видимых в Data Explorer, привязана к timeframe запроса (см. таблицу гранулярности в теме «Как OneAgent собирает инфраструктурные метрики»).

### Базовые метрики хоста, которые всегда доступны

**CPU.** Total usage (процент общей загрузки), Per-core usage (отдельно по каждому ядру — важно для анализа bottleneck в Java с привязкой к ядру), User / System / Iowait / Idle / Steal percentages (последнее важно в виртуализации — сколько процессорного времени крадёт гипервизор), Load average 1m/5m/15m (Linux specific).

**Memory.** Total / Used / Available / Free, Cache, Buffers, Swap used, Swap I/O (page in / page out — индикатор катастрофического swapping). На Windows также Committed bytes, Page file usage.

**Disk.** Per-filesystem: free space (absolute и percent), used space, total size, inode usage (на Linux), mount point и тип ФС. Per-block-device: read/write bytes per second, read/write operations per second, average queue length, busy time percent, read/write latency.

**Network.** Per-interface: bytes in/out, packets in/out, errors, retransmissions, current connections, listening sockets.

**Processes.** Per-process: CPU usage, Memory RSS/VSZ, open file descriptors, thread count, PID, command line, user, parent PID. Агрегация в Process Groups (тема hosts-processes) даёт группы процессов одного приложения.

**OS Services.** Per-service: name, status (Running/Stopped), start type (Auto/Manual/Disabled), executable path, description.

Все эти метрики доступны в Data Explorer по именам `builtin:host.cpu.*`, `builtin:host.mem.*`, `builtin:host.disk.*`, `builtin:host.net.*`, `builtin:tech.*`, `builtin:os-services.*`.

### Сравнение с классическими мониторингами

**Zabbix / Nagios.** В этих системах агент опрашивает ОС по своим скриптам, данные идут в центральный сервер. Админ вручную настраивает, какие метрики собирать и с каким интервалом. Алерты — через статические пороги в конфиге. В OneAgent всё происходит автоматически: метрики собираются полностью сразу после установки, пороги — адаптивные, baseline Davis AI сам понимает норму.

**Prometheus + node_exporter.** Pull-модель: Prometheus сам ходит к каждому node_exporter'у и забирает метрики. Нужен отдельный Prometheus-сервер с настроенным scrape-config, отдельный Alertmanager, отдельный Grafana для визуализации. В Dynatrace это одно целое: агент пушит в кластер, кластер хранит, строит графики, определяет аномалии.

**CloudWatch / Azure Monitor.** Облачный мониторинг только для ресурсов конкретного облака, нет видимости внутри гостевой ОС без дополнительного агента. OneAgent даёт одинаковый уровень видимости в on-premises и в облаке, объединяя инфраструктуру в один интерфейс.

### Специфика air-gapped

**Ничего не меняется в механике сбора.** OneAgent опрашивает свою ОС, ActiveGate пересылает в кластер, кластер хранит. Никаких внешних вызовов (к Dynatrace-облаку, в интернет, к внешним API) не происходит.

**Одно ограничение.** AWS/Azure/GCP метаданные хостов (теги EC2, идентификаторы VPC, AZ) требуют облачного API. В air-gapped контуре банковские облачные хосты внутри VPC без NAT в интернет — эти метаданные не прилетают. Если банк хочет видеть их в Dynatrace, нужно настроить ActiveGate с ролью Cloud (`--set-cloud-metadata=true`), стоящий в DMZ с ограниченным доступом к API облака, и он забирает метаданные и пересылает в кластер.

### Типовые сценарии работы

**Диагностика медленного приложения.** Жалоба пользователей → Problem → в карточке замедление в сервисе X → drilldown в хост → на хосте CPU 100% iowait → Top Processes → один из процессов съедает диск → звонок ответственной команде → pump останавливается. От жалобы до решения — минуты.

**Предупреждение о переполнении диска.** Alerting profile на low disk space. Алерт: на хосте `log-prod-03` 8% свободного места. В карточке хоста → Filesystems → забит `/var/log`. Top processes по write → приложение пишет чрезмерно много логов после включения debug. Debug выключается, старые логи удаляются.

**Плановая проверка хостов раз в месяц.** Список хостов → сортировка по Memory used — кандидаты на расширение RAM. По CPU — хосты с постоянной загрузкой 80-100%, план миграции на более мощные. По Disk — занятые >80%, план расширения.

**Подготовка к пиковому дню** (зарплаты, пенсии, праздники). Дашборд с top-20 критичных хостов, проверка запаса: CPU до 50% в норме, Memory до 60%, Disk до 70%. Где не хватает — добавить ресурсы или перераспределить нагрузку.

**Анализ причин перезагрузки хоста.** После инцидента — карточка хоста → Events → событие `Host restart` с временем. Метрики за минуту до события: резкий рост iowait и CPU, активный swap. Top processes этого периода — приложение съело память, начало swapping, каскадная деградация. Репорт команде разработки с прямой ссылкой на метрики.
