> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 4 из 9: «Мониторинг контейнеров»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:container.technology -->
>
> 🔖 **Редакция от 2026-04-27.** Все тех-факты сверены свежими WebFetch'ами на `docs.dynatrace.com/managed/` в текущей сессии. Ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed): корневая страница Managed Docs
> - [Setup on container platforms: Managed](https://docs.dynatrace.com/managed/ingest-from/setup-on-container-platforms): установка OneAgent в Docker / Kubernetes / Cloud Foundry / Heroku
> - [Container platform monitoring: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring): поддержка Kubernetes Classic / Cloud Foundry / Docker / Heroku, container monitoring rules
> - [Container monitoring rules: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/container-monitoring-rules): три Built-in правила (POD / pause-amd64 / openshift-sdn) + custom rules; работают только при установке OneAgent на хосты
> - [Cloud application and workload detection: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/cloud-app-and-workload-detection): K8s labels (`app.kubernetes.io/name|version|stage`), `DT_RELEASE_*` env vars, naming rules
> - [Infrastructure observability: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability): общий раздел Hosts / Process groups / Containers

## 📍 КАРТА: четыре страницы про контейнеры

Термины темы: `Container / контейнер`, `Container runtime / рантайм` (Docker, containerd, CRI-O, Podman), `Image / образ`, `cgroup / контрольная группа ядра`, `Pod / под`, `Workload / воркшлоад / Deployment/StatefulSet/DaemonSet`, `Cloud Application / CA / логическое приложение в облаке`, `OOMKilled / убит по превышению лимита памяти`.

| Что показать | Путь в меню | Прямая ссылка | Зачем |
|---|---|---|---|
| Container monitoring (глобально) | **Settings → Processes and containers → Container monitoring** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:container.technology` | Какие контейнерные runtime-ы мониторятся (Docker/containerd/CRI-O/Podman) |
| Built-in container monitoring rules | **Settings → Processes and containers → Built-in container monitoring rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:container.built-in-monitoring-rule` | Предустановленные правила мониторинга (инструментация + сбор метрик) для конкретных container-технологий |
| Container monitoring rules (кастом) | **Settings → Processes and containers → Container monitoring rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:container.monitoring-rule` | Пользовательские правила: включение/выключение мониторинга для конкретных контейнеров |
| Cloud application and workload detection | **Settings → Processes and containers → Cloud application and workload detection** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-group.cloud-application-workload-detection` | Распознавание Kubernetes workloads и cloud applications |

**Как Dynatrace видит контейнер:**

| Уровень | Что видит | Через что |
|---|---|---|
| **Хост** | Хост-OS с установленным OneAgent | `oneagentos`, обычный сбор ОС-метрик |
| **Container runtime** | Docker daemon, containerd, CRI-O как процессы | Process monitoring + специальные container sensors |
| **Container** | Сам контейнер как сущность: имя образа, labels, cgroup-ограничения | Запросы к API runtime (Docker socket, containerd gRPC) |
| **Application в контейнере** | Java/Node.js/.NET процесс внутри контейнера | OneAgent автоматически инструментирует процессы внутри контейнеров |
| **Kubernetes-слой** | Pod, Deployment, Service, Namespace | Kubernetes API через специальный ActiveGate/OneAgent Operator |

---

## 🎬 Работа с настройками контейнеров на четырёх экранах

### Шаг 1: Container monitoring (глобальный переключатель runtime-ов)

![Container monitoring: главная страница настройки мониторинга контейнеров](screenshots/day-2/containers/settings/builtincontainer.technology/Container-monitoring-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Container monitoring**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:container.technology`.

Страница: глобальное управление, **какие контейнерные технологии OneAgent мониторит**. Заголовков третьего уровня нет, страница состоит из тумблеров и списков.

**Поддерживаемые технологии:**

- **Docker.** OneAgent общается с Docker daemon через unix-socket (`/var/run/docker.sock` на Linux). Получает список контейнеров, образы, labels, статусы, метрики CPU / Memory в рамках cgroup.
- **containerd.** Runtime Kubernetes начиная с 1.24 (вместо Docker). OneAgent общается через containerd gRPC socket.
- **CRI-O.** Runtime для OpenShift и некоторых K8s-дистрибутивов. Общение через CRI-интерфейс.
- **Podman.** Daemonless-runtime от Red Hat, альтернатива Docker без постоянного root-процесса.
- **Linux cgroups v1 / v2.** Базовые ядерные контейнеры (systemd-unit, bare cgroups). Используются, когда runtime не распознан или нестандартный.

**Что настраивается:**

- **Главный тумблер сбора метрик контейнеров.** Если выключен: OneAgent не опрашивает runtime, метрик нет. По умолчанию включён.
- **Фильтры по технологиям**: можно выключить конкретный runtime, если он не используется.

На самой странице только эти тумблеры рантаймов (плюс поле фильтра списка). Исключение конкретных контейнеров из мониторинга настраивается не здесь, а правилами на соседней странице Container monitoring rules (Шаг 2).

*Типовая настройка.* Все runtime (Docker / containerd / CRI-O) включены: в большой инфраструктуре часто сосуществуют старые Docker-хосты и новые K8s-кластеры с containerd. Правила исключения добавляются по мере обнаружения шума: pause-контейнеры K8s, контейнеры самого ActiveGate, внутренние build-системы.

### Шаг 2: Built-in container monitoring rules

![Built-in container monitoring rules: предустановленные правила для популярных container runtime-ов](screenshots/day-2/containers/settings/builtincontainer.built-in-monitoring-rule/Built-in-container-monitoring-rules-Environment-Settings-Demo-live-Demo-Live-Dyn.png)

Путь в меню: **Settings → Processes and containers → Built-in container monitoring rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:container.built-in-monitoring-rule`.

Аналог `Built-in process monitoring rules` из Дня 1, только для контейнеров. Страница хранит **предустановленные правила, исключающие из мониторинга служебные контейнеры**, чтобы они не загромождали интерфейс.

**Три встроенных правила** (дословно из Managed-документации):

1. «Do not monitor containers where Kubernetes container name equals `POD`» (pause-контейнер пода).
2. «Do not monitor containers where Docker stripped image name contains `pause-amd64`».
3. «Do not monitor containers where Kubernetes namespaces equals `openshift-sdn`» (служебная сеть OpenShift).

Все три включены по умолчанию. Администратор может только выключать или включать их обратно: `you can't edit them`. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/container-monitoring-rules -->

Распознавание прикладных технологий внутри контейнеров (nginx, postgres, redis, kafka и т. п.) идёт **не здесь, а на странице Built-in process monitoring rules** из Дня 1: те правила работают на уровне процессов и применяются как к baremetal-процессам, так и к процессам в контейнерах. Эта страница: только про сами контейнеры как сущность.

*Типовая настройка.* Все три правила оставляют включёнными. Для специфичных случаев (исключить свои pause-контейнеры, sidecar service mesh, build-runners): кастомное правило на следующей странице.

### Шаг 3: Container monitoring rules (кастомные)

![Container monitoring rules: правила для управления мониторингом конкретных контейнеров](screenshots/day-2/containers/settings/builtincontainer.monitoring-rule/Container-monitoring-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Processes and containers → Container monitoring rules**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:container.monitoring-rule`.

> **Сначала проверьте, применима ли вам эта страница.**
> ЕСЛИ OneAgent установлен прямо на хосты (classic host monitoring) → ТО правила с этой страницы работают, читайте дальше.
> ЕСЛИ мониторинг идёт через webhook-инъекцию Kubernetes (`cloudNativeFullStack` или `applicationMonitoring` через Dynatrace Operator) → ТО эти правила игнорируются, сбор контролируется через DynaKube CR (подробности в конце шага). Настраивать тут нечего.

Кастомные правила для мониторинга контейнеров. Аналог `Custom process monitoring rules`: переопределяют дефолт для конкретных образов или лейблов.

**Типовые случаи:**

- **Исключение CI/CD-контейнеров.** Одноразовые build-контейнеры Jenkins / GitLab-Runner живут по 5 минут, но забивают списки. Правило: `image matches jenkins-agent:*` → disable monitoring.
- **Отключение экспериментальных сервисов.** Команда не хочет мониторить свои эксперименты на dev-кластере. Правило: `label environment=experimental` → disable.
- **Включение для lightweight-контейнера.** Маленький утилитарный контейнер по дефолту не инструментируется (размер образа, короткое время жизни). Правило: `label app=critical-utility` → force enable deep monitoring.

**Структура правила:**

- **Rule name.**
- **Matcher**: свойство контейнера (например, имя образа) с оператором сравнения (`begins with` и аналогичные).
- **Action**: Enable monitoring / Disable monitoring для совпавших контейнеров.

Правила применяются по порядку (drag-and-drop в UI), первое сматчившееся побеждает.

**Важное ограничение.** Дословно из Managed-документации: «Container monitoring rules are effective only when you install OneAgent on your hosts». В режимах Kubernetes-инъекции через webhook (`cloudNativeFullStack` или `applicationMonitoring` через Dynatrace Operator) механизм сбора другой и контролируется через DynaKube CR. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/container-monitoring-rules -->

### Шаг 4: Cloud application and workload detection

![Cloud application and workload detection: распознавание Kubernetes workloads](screenshots/day-2/containers/settings/builtinprocess-group.cloud-application-workload-detection/Cloud-application-and-workload-detection-Environment-Settings-Demo-live-Demo-Liv.png)

Путь в меню: **Settings → Processes and containers → Cloud application and workload detection**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:process-group.cloud-application-workload-detection`.

Страница специфична для **Kubernetes и cloud native**. Настраивает, как Dynatrace определяет Cloud Application и Workload: логические единицы, соответствующие Deployments / StatefulSets / DaemonSets / Jobs / Services в K8s.

**Терминология Dynatrace:**

- **Cloud Application / CA**: приложение в облаке или K8s. Например, весь deployment `payment-service` с 5 репликами.
- **Workload**: технический уровень: конкретный Deployment / StatefulSet / DaemonSet.
- **Pod**: один экземпляр (одна реплика).

**Где живут в интерфейсе:**

- Cloud Applications: `/ui/entity/list/CLOUD_APPLICATION`
- Kubernetes Workloads: `/ui/entity/list/CLOUD_APPLICATION` (часто то же представление)
- Kubernetes Cluster: `/ui/entity/list/KUBERNETES_CLUSTER`

**Что настраивается:**

- **Набор labels для детекции.** Managed-документация рекомендует пробрасывать стандартные K8s-labels в env-переменные: `app.kubernetes.io/version → DT_RELEASE_VERSION`, `app.kubernetes.io/name → DT_RELEASE_PRODUCT`, `app.kubernetes.io/stage → DT_RELEASE_STAGE`. Дополнительно поддерживаются `DT_RELEASE_BUILD_VERSION`. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/cloud-app-and-workload-detection -->
- **Правила группировки CA.** Например, deployments с префиксом `retail-` в одну CA `Retail Banking`. Удобно для дашбордов руководства.
- **Workload naming rules.** Шаблон формирования имени Process Group: `<tech_prefix> <product> <STAGE> <base_pod_name>`, где product/stage/base_pod_name появляются, только когда они определены применённым правилом. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/cloud-app-and-workload-detection -->
- **Специальные случаи.** Knative / OpenFaaS (serverless), StatefulSet с PersistentVolume, Jobs / CronJobs: для каждого своя логика.

*Типовая работа со страницей:*

- **При первичном внедрении.** Настраивают labels под схему команды DevOps. Если используются стандартные K8s labels: дефолт работает.
- **Через полгода-год.** Добавляют правила группировки CA по продуктам, чтобы дашборды руководства показывали бизнес-сущности, а не технические deployments.

---

## ⚙️ COOKBOOK: настройка мониторинга контейнеров

### Первое развёртывание OneAgent на Kubernetes-кластере

*Задача.* Мониторинг нового кластера из 30 нод.

*Шаги:*

1. Установить OneAgent через Dynatrace Operator (Helm chart). Operator ставит агент на каждую ноду как DaemonSet.
2. В настройках Operator включить `applicationMonitoring` для автоматической инструментации подов (CodeModules через mutating webhook).
3. В Container monitoring проверить, что все используемые runtime включены (containerd для нового кластера).
4. В Cloud application and workload detection проверить дефолтные labels. Если своя схема: добавить.
5. Через несколько минут Workloads появляются в интерфейсе с метриками, трейсами и проблемами.

### Исключить pause-контейнеры из интерфейса

*Задача.* Pause-контейнеры K8s (один на под, без приложенческого кода) создают шум.

*Решение.* В Container monitoring rules кастомное правило: условие по имени образа (`registry.k8s.io/pause:*` либо `k8s.gcr.io/pause:*`), действие «не мониторить». Исчезают из интерфейса.

### Выделить команду продуктов в одну Cloud Application

*Задача.* 25 микросервисов retail-команды, все в namespace `retail-*`. На дашборде руководства нужно видеть их как единую сущность, а не 25 отдельных.

*Решение.* В Cloud application and workload detection правило: `namespace starts with retail-` → Cloud Application `Retail Banking`. На следующий день сервисы появляются как одна CA с агрегированными метриками.

### Форсировать deep monitoring для конкретного контейнера

*Задача.* На dev-кластере запущен сервис, OneAgent его не инструментирует (dev-среда, ограничения).

*Решение.* В Container monitoring rules правило: `label monitoring.priority=critical` → Force enable. В манифесте пода добавляется соответствующий label. OneAgent включает полную инструментацию.

---

## 🎓 ТЕОРИЯ: как Dynatrace работает с контейнерами

### Архитектура Kubernetes-мониторинга

**Dynatrace Operator.** Рекомендуемый способ установки на K8s. Ставится как Helm chart в namespace `dynatrace`. Создаёт:

- DaemonSet для OneAgent на каждой ноде.
- ActiveGate как Deployment.
- Webhook-и для автоматической инъекции инструментации в приложения.

**OneAgent на ноде.** В режиме K8s работает немного иначе, чем на обычном хосте. Видит cgroup'ы всех контейнеров ноды, опрашивает kubelet API, получает список подов, собирает метрики. Всё локально, без обращения к control plane.

**ActiveGate с ролью Kubernetes.** Дополнительно опрашивает API server (через ServiceAccount). Собирает информацию о Deployments, Services, Ingresses, Namespaces, Events. Данные привязываются к контейнерам через метаданные.

**Автоматическая инструментация через CodeModules.** При старте нового пода mutating webhook добавляет init-контейнер с CodeModules (Java agent, Node.js agent и др.). Init-контейнер копирует агента в volume, основной контейнер при старте загружает агент автоматически. Изменений в приложении или Dockerfile не требуется.

### Что видно по Cloud Application и Workload

В карточке Workload:
- **Overview**: сводка метрик контейнеров: CPU, Memory, Network, количество реплик.
- **Pods**: список всех pods, их статусы (Running/Pending/Failed), возраст.
- **Events**: Kubernetes-события: scaling, scheduling failures, OOMKilled, restart loops.
- **Services**: какие K8s-сервисы (и endpoints) представляют этот workload.
- **Ingress**: какие ingress-правила ведут трафик в этот workload.
- **Related process groups**: какие Process Groups соответствуют контейнерам workload (связь с темой hosts-processes).

### Специфика сбора метрик контейнеров

**Лимиты и реальное использование.** Для каждого контейнера отдельно показываются:

- **Limit**: сколько разрешено (из K8s-манифеста `.resources.limits.cpu` / `.resources.limits.memory`).
- **Request**: сколько резервировано (из `.resources.requests`).
- **Actual usage**: сколько реально использовано.

Важная метрика: **CPU throttling**: сколько процессорного времени контейнер попросил, но получил не сразу из-за упирания в лимит. Высокий throttling = контейнер голодает.

**OOMKilled tracking.** Если контейнер упал из-за превышения memory limit (Out Of Memory Killed): отдельное событие в Dynatrace. Указывается: сколько памяти использовал в момент смерти, какой был лимит, какой процесс инициировал выделение. Ключевая метрика при анализе memory leak.

**Network между контейнерами.** Dynatrace через eBPF видит трафик между подами. Строит Service Flow внутри кластера, ловит проблемы связности.

### Сравнение с классическим мониторингом K8s

**Prometheus + Grafana + Alertmanager.** Open-source стек. Prometheus scrape'ит kubelet metrics и app-exposed metrics через annotations. Grafana строит дашборды. Alertmanager шлёт алерты. Требует отдельной инфраструктуры и настройки. Нет автоматической инструментации приложений: Prometheus-clients вшиваются явно.

**Datadog Agent / New Relic Infrastructure.** Коммерческие альтернативы с похожей моделью развёртывания (DaemonSet + автоинструментация). Их работу здесь не разбираем: каждая платформа имеет свои особенности конфигурации.

### Air-gapped в контексте контейнеров

**Всё работает локально.** OneAgent, ActiveGate, webhooks, CodeModules: всё в кластере. Ничего не ходит в интернет.

**Требование к образам.** Образы Dynatrace Operator и CodeModules должны быть в internal container registry. Админ скачивает их на машине с интернетом и загружает в свой Harbor / Artifactory. Helm chart Operator'а настраивается с `image.repository=registry.internal/dynatrace/...`. После этого установка идёт без интернета.

**Обновление агентов в K8s.** Новая версия OneAgent → админ скачивает новый образ CodeModules → пушит в свой registry → обновляет Helm values в Operator'e. Operator при следующей перевыкатке подов переходит на новую версию. Управляемый процесс, без автоматического pulling из интернета.
