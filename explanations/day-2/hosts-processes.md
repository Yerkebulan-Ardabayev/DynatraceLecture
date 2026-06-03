> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 3 из 9: «Хосты и процессы: взаимосвязи, показатели, атрибуты»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/entity/list/HOST -->
>
> 🔖 **Редакция от 2026-04-27.** Все тех-факты сверены свежими WebFetch'ами на `docs.dynatrace.com/managed/` в текущей сессии. Ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed): корневая страница Managed Docs
> - [Infrastructure observability: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability): раздел Hosts / Processes / Containers / Message queues / VMware
> - [Hosts: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/hosts): раздел Hosts (точка входа)
> - [Host monitoring with Dynatrace: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/hosts/monitoring/host-monitoring): host metrics, process instance snapshots (20 минут окна, 60 мин/день, 100 процессов), trigger при ≥1% CPU/RAM/network
> - [Organize your environment using host groups: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/hosts/configuration/organize-your-environment-using-host-groups): host groups, `--set-host-group`, влияние на process group detection, лимит 100 символов
> - [Process groups: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups): концепция Process Group, авто-merge на основе технологических маркеров (`CATALINA_HOME`, `JBOSS_HOME` и т.п.)
> - [Process group detection: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/pg-detection): Simple (только split, Java system property / env variable) vs Advanced (split + merge, составные условия, delimiter-extraction)
> - [Declarative process grouping: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/declarative-process-grouping): Settings 2.0 формат, операторы `$prefix`/`$suffix`/`$eq`/`$contains`, OneAgent 1.259+ для Report process group option

## 📍 КАРТА: семь страниц про хосты, процессы и их группировку

Термины темы: `Host / хост`, `Process / процесс` (конкретный запущенный бинарник с PID), `Process Group / группа процессов / PG` (логическое объединение одинаковых процессов одного приложения), `Process Instance / инстанс процесса`, `Smartscape / карта связей`, `Service / сервис / логическая backend-единица`.

| Что показать | Путь в меню | Прямая ссылка | Зачем |
|---|---|---|---|
| Список хостов (как точка входа) | **Infrastructure Observability → Hosts** | `https://guu84124.live.dynatrace.com/ui/entity/list` | 404 на старом адресе: используется `/ui/entity/list/HOST` |
| Process grouping rules | **Settings → Processes and containers → Process grouping rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-grouping-rules` | Правила превращения процессов в группы для отображения |
| Simple detection rules | **Settings → Processes and containers → Process group detection → Simple detection rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-group.simple-detection-rule` | Простые правила распознавания: имя + один критерий |
| Advanced detection rules | **Settings → Processes and containers → Advanced detection rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-group.advanced-detection-rule` | Продвинутые правила с составными условиями |
| Custom process monitoring rules | **Settings → Processes and containers → Custom process monitoring rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:process.custom-process-monitoring-rule` | Правила включения/выключения мониторинга для конкретных процессов |
| Process availability | **Settings → Processes and containers → Process availability** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:processavailability` | Правила отслеживания доступности процессов (когда считать упавшим) |
| Process instance snapshots | **Settings → Processes and containers → Process instance snapshots** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-visibility` | Моментальные снимки деталей процесса для диагностики |

---

## 🎬 Работа с группировкой процессов на семи экранах

### Шаг 1: Entity list (404) → Hosts

![Entity list: страница возвращает 404, для хостов используется `/ui/entity/list/HOST`](screenshots/day-2/hosts-processes/entity/list/404-We-cant-find-this-page-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Infrastructure Observability → Hosts**.
Прямая ссылка (устаревшая): `https://guu84124.live.dynatrace.com/ui/entity/list`.
Прямая ссылка (рабочая): `https://guu84124.live.dynatrace.com/ui/entity/list/HOST`.

Универсальный entity list на этом тенанте возвращает 404 (аналогично Теме 1 Дня 2). Для работы с хостами используется типизированный вариант с суффиксом `/HOST`.

**Ключевые поля карточки хоста, которые связывают его с процессами.**

**Running processes**: список всех процессов, запущенных на хосте, сгруппированных по Process Groups. Каждая Process Group: одна карточка со сводкой: сколько инстансов, общая CPU-нагрузка, общая потребляемая память, когда был последний рестарт любого инстанса, связанные сервисы.

**Technology overview**: сводка по автоматически обнаруженным технологиям: Java (с версиями JVM), .NET (с версиями CLR), Node.js, Python, PHP, PostgreSQL, Oracle, Redis и так далее. Каждая запись: кликабельный переход к процессам этой технологии на этом хосте.

**Smartscape**: мини-граф связей именно для этого хоста. Показывает, какие Process Groups работают на нём, какие Services ими представлены, с какими другими хостами они общаются.

### Шаг 2: Process grouping rules

![Process grouping rules: глобальные правила объединения процессов в группы](screenshots/day-2/hosts-processes/settings/builtinprocess-grouping-rules/Process-grouping-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Process grouping rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-grouping-rules`.

**Process grouping: фундаментальная концепция Dynatrace.** Задача: взять сотни одинаковых процессов (например, 200 копий `java -jar payment-service.jar` на 50 хостах) и свернуть в **одну Process Group**. В интерфейсе это один объект с метриками всего парка инстансов.

**Что настраивается на странице.** Правила, как отличать одну Process Group от другой при одинаковой технологии.

*Пример.* На хосте два Java-процесса с разными `-jar`:

- `java -jar authservice-1.4.jar`
- `java -jar paymentservice-2.1.jar`

По умолчанию Dynatrace идентифицирует по имени главного `.jar`-файла. Получается две Process Groups: `authservice` и `paymentservice`. Но имени недостаточно, если, например, есть две инсталляции одного приложения (prod и staging) с одинаковыми именами, но из разных директорий. Для этого и нужны правила grouping.

**Структура правила:**

- **Rule name**: человекочитаемое имя.
- **Property**: по какому свойству разделять или объединять. Варианты: command line fragment, environment variable, path prefix, JVM argument, Kubernetes pod label, Docker image name.
- **Action**: `Split by this property` (разделить по значениям свойства) или `Merge by this property` (объединить по совпадающему).
- **Scope**: глобально / на хост-группе / на конкретном хосте.

**Типовые правила:**

- Split по environment variable `APP_ENV` или `DT_CLUSTER_ID`: разделяет одноимённые приложения в dev / test / prod.
- Split по K8s label `app.kubernetes.io/version`: разные версии одного микросервиса в отдельные Process Groups. Нужно для чистых трейсов в canary-выкатке.
- Merge по имени deployment в Kubernetes: все поды одного deployment считаются единой Process Group, независимо от случайных имён подов.
- Split по пути установки: когда на хосте две копии одного продукта в разных директориях.

### Шаг 3: Simple detection rules

![Simple detection rules: упрощённый интерфейс распознавания процессов по одному критерию](screenshots/day-2/hosts-processes/settings/builtinprocess-group.simple-detection-rule/Simple-detection-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Process group detection → Simple detection rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-group.simple-detection-rule`.

Упрощённая форма правил, когда нужен один-два критерия. Альтернатива Advanced detection rules (следующий шаг) с полным редактором составных условий.

*Типовой случай.* Внутреннее приложение на нестандартной технологии (Perl-прослойка, shell-скрипт). OneAgent по умолчанию распознаёт его как generic process. Все инстансы попадают в огромную Process Group «другие процессы» вместе с системными демонами. Simple rule превращает это в осмысленное: «процессы с `my-corp-app` в командной строке → Process Group `MyCorpApp`».

**Поля правила:**

- Имя правила.
- **Match condition**: что ищем: значение environment variable либо Java system property (для JVM-процессов). Это два основных источника, поддерживаемых Simple-формой.
- **Match value**: конкретное значение.
- **Action**: выделить новую Process Group по совпадению (Simple умеет только split, это явно подтверждено в Managed-документации; merge: на странице Advanced detection rules). <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/pg-detection -->

**Simple vs Advanced.** Simple закрывает большинство случаев: распознать приложение по одному признаку. Advanced нужен для логических выражений `(path contains "myapp") AND (env DT_STAGE = prod) AND (port == 8080)`. Рекомендация: начинать с Simple, переходить на Advanced, когда Simple не хватает.

### Шаг 4: Advanced detection rules

![Advanced detection rules: полный редактор правил с логическими выражениями](screenshots/day-2/hosts-processes/settings/builtinprocess-group.advanced-detection-rule/Advanced-detection-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Advanced detection rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-group.advanced-detection-rule`.

Полный редактор правил распознавания. Те же возможности, что у Simple, плюс составные логические выражения, условные зависимости и приоритеты правил (если матчатся несколько: какое применяется первым).

**Возможности Advanced:**

- Составные условия `AND` / `OR` между проверками.
- Переменные окружения с regex.
- JVM-аргументы с конкретным значением (`-Dmy.cluster.id=prod`).
- Свойства контейнера: image name, image tag, labels.
- Условное связывание: «если процесс: `java`, AND содержит `-jar`, AND jar-файл в пути `/opt/bank/...`, THEN создать Process Group с именем из каталога jar».
- Приоритизация: правила применяются в заданном порядке, первое сматчившееся побеждает.

*Когда нужно.* Зрелые инсталляции с десятками кастомных Java-приложений, собранных по разным политикам. Пример: три продуктовые команды (retail, corporate, SME), каждая деплоит свой стек с собственными именами и JVM-параметрами. Advanced rules выделяют каждую команду в отдельную Process Group с префиксом, несмотря на общую технологию (Java).

*Риск.* Большое число сложных правил делает конфиг хрупким: новое приложение может перекрыть старое правило, метрики смешиваются.

*Рекомендация:* минимум правил, комментарии к каждому, периодическое ревью.

### Шаг 5: Custom process monitoring rules

![Custom process monitoring rules: правила включения/выключения мониторинга для конкретных процессов](screenshots/day-2/hosts-processes/settings/builtinprocess.custom-process-monitoring-rule/Custom-process-monitoring-rules-Environment-Settings-Demo-live-Demo-Live-Dynatra.png)

Путь в меню: **Settings → Processes and containers → Custom process monitoring rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:process.custom-process-monitoring-rule`.

Эта страница: не про распознавание или группировку, а про **включение или выключение глубокого мониторинга конкретного процесса**.

По умолчанию OneAgent мониторит все распознанные сервисные процессы (Java-серверы, .NET, Node.js). Custom rules переопределяют default:

- **Выключить** мониторинг конкретного процесса, даже если он распознан как Java. Нужно для приложений, несовместимых с инструментацией, или для legacy, которые нельзя перезапускать для применения `-javaagent`.
- **Включить** мониторинг процесса, который по умолчанию не попадает в мониторинг. Например, Python-скрипт, который не считается «сервером», но нужен для анализа времени выполнения.

**Структура правила:**

- **Scope**: по имени технологии, по имени процесса, по тегам хоста.
- **Condition**: match на командную строку / путь / environment.
- **Action**: включить / выключить / снимать только базовые метрики без глубокой инструментации.

**Типовые случаи:**

- **Отключение инструментации legacy-приложения.** Старое Java-приложение крашится при загрузке дополнительных JAR. Правило: процесс с `legacy-trading-app.jar` в command line → Disable monitoring.
- **Отключение мониторинга stress-тестировщика.** JMeter или loadgen на проде генерирует миллионы запросов и забивает лицензии ненужными метриками. Правило: отключить.
- **Включение для скрипта автоматизации.** Shell-скрипт ночного ETL по умолчанию не мониторится. Правило: включить с базовыми метриками времени работы.

### Шаг 6: Process availability

![Process availability: правила отслеживания доступности процессов](screenshots/day-2/hosts-processes/settings/builtinprocessavailability/Process-availability-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Process availability**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:processavailability`.

Страница: про **когда считать процесс упавшим и создавать Problem**.

По умолчанию Dynatrace наблюдает за процессами сервисов (Tomcat, WildFly, Node.js). Создаёт Problem, если процесс внезапно исчез: был минуту назад, сейчас нет. Для тонкой настройки: какой процесс критичный, какой нет, сколько ждать перед созданием Problem.

**Структура правила:**

- **Rule name**: имя.
- **Scope**: охват: по тегам хоста, по Process Group, по именам.
- **Condition**: что считать «упавшим»: процесс не обнаружен N секунд / CPU равен 0 более N секунд / memory не меняется более N секунд.
- **Action**: Severity Problem, Alerting Profile.

**Типовые случаи:**

- **Критичные сервисы с hot-standby.** На основной ноде: упал, сразу Problem. На standby: ожидаемо остановлен, Problem не создаётся.
- **Batch-процессы.** Ночной ETL работает только ночью, днём его нет. Правило: мониторить в определённые часы, в другие отсутствие: норма.
- **Плановый рестарт.** Приложение перезапускается каждый час для очистки кэшей. Правило: не создавать Problem, если отсутствие меньше 60 секунд.

### Шаг 7: Process instance snapshots

![Process instance snapshots: настройка моментальных снимков процессов для диагностики](screenshots/day-2/hosts-processes/settings/builtinprocess-visibility/Process-instance-snapshots-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Process instance snapshots**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-visibility`.

Страница: про **сбор детальных снимков состояния процесса** для углублённой диагностики.

Снимки делаются **по триггеру**, не по расписанию. OneAgent активирует сбор детальных метрик процесса автоматически, когда процесс превышает 1% потребления CPU, памяти или сети, а также при ручном запросе через меню «Request process snapshot now» (данные появляются после reload в течение 90 секунд). Один снимок содержит **20 минут данных: 10 минут до триггера и 10 минут после**. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/hosts/monitoring/host-monitoring -->

*Что попадает в снимок.* Для каждого процесса: счётчики CPU / памяти / сети, открытые файлы и сокеты, загруженные библиотеки. Для JVM-процессов дополнительно: thread dump главных потоков. Эти данные позволяют ответить на «почему процесс не отвечает», когда стандартных хостовых метрик недостаточно.

**Настройки:**

- **enabled**: главный тумблер активации фичи.
- **Maximum/default: 100 процессов** в одном снимке (можно понизить).

**Лимит на хост:** каждый хост шлёт суммарно **до 60 минут** таких метрик в сутки. Метрики собираются с минутным интервалом внутри окон вокруг триггеров. Когда суточный лимит исчерпан: новые снимки в этот день не пишутся. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/hosts/monitoring/host-monitoring -->

**Типовое применение.** Включают для production-хостов с критичными сервисами. Для dev и test выключают: экономия квоты 60 мин/день. Ревью списка процессов раз в квартал.

---

## ⚙️ COOKBOOK: типичные сценарии настройки группировки

### Разделить prod и dev одного приложения

*Проблема.* Одно Java-приложение на двух хост-группах: `prod-app-servers` и `dev-app-servers`. Дефолтная группировка объединяет все инстансы в одну Process Group. Метрики смешиваются.

*Решение.* В Process grouping rules split-правило по environment variable `APP_ENV` (или по тегу хост-группы). Получаем `MyApp [prod]` и `MyApp [dev]`.

### Выделить каждую команду в свой префикс

*Проблема.* Три команды с собственными микросервисами, имена подов в K8s одинаковые (`user-service` и `auth-service` у retail vs corporate).

*Решение.* Advanced detection rule с проверкой namespace `.metadata.namespace`: добавить префикс из namespace к имени Process Group. Получаем `retail/user-service`, `corporate/user-service`: непересекающиеся и понятные.

### Отключить мониторинг проблемного приложения

*Проблема.* Старое Java-приложение падает с `OutOfMemoryError` через час после старта. Инструментация увеличивает memory footprint слишком сильно.

*Решение.* Custom process monitoring rule с уникальным маркером в command line (`-Dapplication.id=legacy-trading`), action: Disable monitoring. После рестарта OneAgent не инструментирует процесс, но продолжает собирать метрики ОС хоста. Разработка получает стабильность, Dynatrace: частичную наблюдаемость.

### Не алертить на плановый ночной рестарт

*Проблема.* Процесс прогрева кэша стартует в 02:00, работает 15 минут, корректно завершается. Dynatrace каждую ночь создаёт Problem «процесс исчез».

*Решение.* Process availability rule со scope на этот процесс, action: не создавать Problem, если отсутствие меньше 20 минут. Ложный алерт исчезает.

---

## 🎓 ТЕОРИЯ: как Process Groups связывают всю пирамиду сущностей

### Место Process Groups в иерархии Smartscape

```
Application (фронтенд, RUM)
    ↓ вызывает через HTTP/gRPC
Service (логическая backend-единица)
    ↓ исполняется в одном или нескольких
Process Group (логическая группа процессов одного приложения)
    ↓ состоит из
Process Instance (конкретный процесс с PID)
    ↓ запущен на
Host (физический или виртуальный хост)
```

Process Group, это слой абстракции между «инстансом процесса на одном хосте» и «сервисом, который обрабатывает запросы».

**Один Service может быть представлен одной или несколькими Process Groups.** Например, один микросервис `payment-service`, это одна Process Group. Но сложный backend типа WebSphere с несколькими деплойментами: несколько Process Groups (одна на каждый деплоймент).

**Одна Process Group содержит N Process Instances.** Это и есть главная ценность: 200 копий `payment-service.jar` на 50 хостах превращаются в одну сущность в интерфейсе. Метрики агрегируются, но при необходимости можно провалиться в конкретный инстанс для детального анализа.

### Почему авто-группировка иногда ошибается

- **Одинаковые имена, разные приложения.** Два независимых приложения с одним именем executable по дефолту попадают в одну Process Group. Типовой случай: несколько инстансов JVM с разным кодом, но одним именем jar.

- **Контейнеры с динамическими именами.** Kubernetes генерирует имена подов вида `payment-service-6d8b9f7f85-xh9k2`. Каждая перевыкатка создаёт новые имена. Без правил каждая перевыкатка создаёт новую Process Group, метрики теряют непрерывность.

- **Multitenancy.** Один Spring Boot хостит API нескольких продуктов на разных endpoint'ах. Без правил: одна Process Group. С правилами: несколько, по разным JVM-аргументам.

### Последствия плохой группировки

- **Метрики не связываются.** Новая версия приложения попала в отдельную Process Group. Дашборды показывают метрики старой группы (пустой), реальные данные в новой. Дашборды ломаются.

- **Baseline не формируется.** Каждая новая Process Group: новая модель Davis AI. Ей нужно 7 дней истории для baseline. Если плохие правила создают новую группу раз в день: baseline не успевает сформироваться, аномалии не детектируются.

- **Alerting profiles не срабатывают.** Если профиль завязан на имя конкретной Process Group и оно изменилось из-за перегруппировки, алерты не доходят.

- **Smartscape захламляется.** Дублированные Process Groups засоряют граф, делают его нечитаемым.

### Air-gapped specifics

Вся механика группировки, распознавания и Process availability работает полностью локально. Никаких внешних сервисов. Встроенные правила (Built-in process monitoring rules, разбирались в Дне 1) поставляются в сборке OneAgent: новые технологии добавляются при обновлении агентов через CMC. Кастомные правила (эти семь страниц) хранятся в кластере и применяются всем агентам.

**Ограничение:** если в инфраструктуре появляется новая технология (скажем, банк впервые выкатывает приложение на Rust), встроенных правил для неё нет до момента, когда Dynatrace выпустит новую сборку OneAgent с поддержкой, и администратор загрузит эту сборку через CMC. До этого: единственный способ получить осмысленные Process Groups для новой технологии: написать Simple или Advanced detection rule вручную, опираясь на признаки технологии (имя executable, наличие конкретных библиотек в path).
