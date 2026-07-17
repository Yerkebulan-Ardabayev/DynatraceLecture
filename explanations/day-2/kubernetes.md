> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 5 из 9: «Мониторинг Kubernetes: кластеры, ноды, поды, ворклоады»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:cloud.kubernetes.monitoring -->
>
> 🔖 **Редакция от 2026-04-27.** Все тех-факты сверены свежими WebFetch'ами на `docs.dynatrace.com/managed/` в текущей сессии. Ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed): корневая страница Managed Docs
> - [Set up Dynatrace on Kubernetes: Managed (shortlink)](https://docs.dynatrace.com/managed/shortlink/kubernetes): Quickstart, Deployment, How it works, Reference, Operator release notes
> - [Setup on Kubernetes: Managed](https://docs.dynatrace.com/managed/ingest-from/setup-on-k8s): установка Operator/CodeModules в кластер (air-gapped registry, токены)
> - [Container platform monitoring: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring): Kubernetes Classic / Cloud Foundry / Docker / Heroku
> - [Kubernetes monitoring: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring): концептуальная страница Kubernetes-мониторинга в Managed
> - [Cloud application and workload detection: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/cloud-app-and-workload-detection): связка процессов внутри контейнеров с Workloads и Cloud Applications
> - [Infrastructure observability: Managed](https://docs.dynatrace.com/managed/observe/infrastructure-observability): общий раздел Hosts / Process groups / Containers / Message queues

## 📍 КАРТА: девять страниц для настройки Kubernetes-мониторинга

Термины темы: `Cluster / кластер`, `Node / нода / узел`, `Namespace / неймспейс`, `Pod / под`, `Workload / воркшлоад / Deployment/StatefulSet/DaemonSet`, `PVC / Persistent Volume Claim / заявка на постоянный том`, `ServiceAccount / SA / сервисный аккаунт`, `CIS Benchmark / набор правил безопасности от Center for Internet Security`.

| Что показать | Путь в меню | Прямая ссылка | Назначение |
|---|---|---|---|
| Основные настройки Kubernetes-мониторинга | **Settings → Cloud and virtualization → Kubernetes → Monitoring settings** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:cloud.kubernetes.monitoring` | Глобальные параметры сбора K8s-данных: опрос API, частота обновлений, включённые возможности |
| Kubernetes Telemetry Enrichment | **Settings → Cloud and virtualization → Kubernetes → Telemetry enrichment** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:kubernetes.generic.metadata.enrichment` | Добавление K8s-метаданных (labels, annotations) к трейсам и метрикам приложений |
| Security Posture Management: Kubernetes | **Settings → Application Security → Security Posture Management: Kubernetes** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:kubernetes.security-posture-management` | Оценка конфигурации кластера на соответствие best-practices безопасности (CIS Kubernetes benchmark) |
| Anomaly detection для кластеров | **Settings → Anomaly detection → Kubernetes cluster** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.cluster` | Пороги для обнаружения проблем на уровне всего кластера |
| Anomaly detection для namespaces | **Settings → Anomaly detection → Kubernetes namespace** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.namespace` | Пороги для отдельного namespace (CPU/Memory quotas, pod counts) |
| Anomaly detection для нод | **Settings → Anomaly detection → Kubernetes node** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.node` | Пороги для нод кластера (ready state, resource pressure, condition changes) |
| Anomaly detection для workloads | **Settings → Anomaly detection → Kubernetes workload** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.workload` | Пороги для Deployment/StatefulSet (pod availability, container restarts, OOMKilled) |
| Anomaly detection для PVC | **Settings → Anomaly detection → Kubernetes persistent volume claim** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.pvc` | Пороги для PVC (использование storage, пропускная способность, ошибки монтирования) |
| Kubernetes app (переход на новый UI) | **Settings → Kubernetes app** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:app-transition.kubernetes` | Переключатель на новое Kubernetes-приложение. В air-gapped Managed оно недоступно (требует Apps-платформу), экран остаётся информационным, работаем в Classic UI <!-- qc:ignore=SAAS строка тенанта существует, новый Kubernetes app требует Apps-платформу, в изолированном Managed остаёмся на Classic --> |

---

## 🎬 Работа с настройками Kubernetes на девяти экранах

### Шаг 1: Monitoring settings (главная страница сбора K8s-данных)

![Monitoring settings: глобальные параметры Kubernetes-мониторинга](screenshots/day-2/kubernetes/settings/builtincloud.kubernetes.monitoring/Monitoring-settings-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Cloud and virtualization → Kubernetes → Monitoring settings**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:cloud.kubernetes.monitoring`.

Центральная страница K8s-мониторинга. Здесь задаётся, **как Dynatrace общается с API Kubernetes, что собирает, с какой частотой**. Страница построена не из заголовков-разделов, а из тумблеров, полей и списков.

**Что настраивается:**

- **Подключение к кластеру.** Настраивается в отдельном флоу подключений (не на этой странице тумблеров): URL API server, токен ServiceAccount с правами чтения ресурсов, CA-сертификат. Эти данные использует ActiveGate для опроса API.
- **Интервалы опроса.** ActiveGate с ролью Kubernetes monitoring периодически опрашивает API server. Конкретные значения по умолчанию для разных типов ресурсов в публичной документации Dynatrace не зафиксированы: управление интервалом находится на стороне ActiveGate и подстраивается под нагрузку.
- **Типы собираемых ресурсов.** Можно отключить конкретные (например, Jobs / CronJobs, если их много и они создают шум).
- **Ограничения по namespaces.** Список, который НЕ мониторить: `kube-system`, `kube-public` и другие системные, если не нужны.
- **Обработка событий K8s.** Какие `Event`-объекты учитывать как события в Dynatrace: Pulled / Created / Started / Failed.

*Типовая работа.* Страница трогается при подключении нового кластера (вносят параметры) и при ревью (правят, что мониторить, а что нет).

**ЕСЛИ → ТО на этом экране.** Каждый exclude-список и отключённый сбор это прямое следствие для того, что появится в данных:

- ЕСЛИ namespace внесён в exclude-список (например, `kube-system`) → его поды, ворклоады и события перестают собираться, и по нему не будет ни метрик в Data Explorer, ни anomaly-detection-проблем. Шум уходит, но и слепая зона появляется осознанно.
- ЕСЛИ отключить сбор событий K8s → объекты `Event` кластера (Pulled, Created, Started, Failed, а также BackOff и Evicted) не попадают в Dynatrace, и алерты, которые считаются по событиям (pod backoff, pod eviction), срабатывать не будут.
- ЕСЛИ отключить сбор K8s-сущностей (namespaces, workloads, pods) → остаётся только нода как хост (через OneAgent), а K8s-топология (ворклоады, поды, сервисы) в Smartscape не строится.
<!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring/alert-on-kubernetes-issues -->

### Шаг 2: Kubernetes Telemetry Enrichment

![Kubernetes Telemetry Enrichment: добавление K8s-метаданных к трейсам и метрикам](screenshots/day-2/kubernetes/settings/builtinkubernetes.generic.metadata.enrichment/Kubernetes-Telemetry-Enrichment-Environment-Settings-Demo-live-Demo-Live-Dynatra.png)

Путь в меню: **Settings → Cloud and virtualization → Kubernetes → Telemetry enrichment**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:kubernetes.generic.metadata.enrichment`.

*Что такое Telemetry Enrichment.* Когда приложение в контейнере отправляет метрики (OneAgent или OpenTelemetry), эти метрики сами по себе не знают, в каком поде они родились, в каком namespace, под каким deployment. Enrichment: **автоматическое добавление меток K8s к метрикам**, чтобы их можно было фильтровать и группировать.

**Что обогащается.** Каждая метрика, трейс, лог от приложения в контейнере получает поля `k8s.pod.name`, `k8s.namespace.name`, `k8s.deployment.name`, `k8s.node.name`, `k8s.cluster.name`. Дальше в Data Explorer и Alerting profiles можно фильтровать по ним. Стандартные K8s-labels пробрасываются в env-переменные процессов: `app.kubernetes.io/version → DT_RELEASE_VERSION`, `app.kubernetes.io/name → DT_RELEASE_PRODUCT`, `app.kubernetes.io/stage → DT_RELEASE_STAGE`. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/cloud-app-and-workload-detection -->

**Что настраивается:**

- Какие стандартные поля добавлять (обычно все включены).
- Какие дополнительные labels и annotations включать (например, кастомные `company/product`, `company/team`).
- Формат имён: как ключ называется в метриках Dynatrace, чтобы совпадать с соглашениями команды.

*Практическая польза.* После настройки enrichment в Data Explorer можно отфильтровать метрику по namespace: `builtin:service.response.time:filter(eq(k8s.namespace.name,"retail-prod"))` (синтаксис Metrics API v2: условия задаются функциями eq/ne/in, оператор `==` селектор не принимает) и получить метрики только ретейл-продакшна. Без enrichment такой запрос невозможен.

### Шаг 3: Security Posture Management: Kubernetes

![Security Posture Management: оценка безопасности конфигурации кластера](screenshots/day-2/kubernetes/settings/builtinkubernetes.security-posture-management/Security-Posture-Management-Kubernetes-Environment-Settings-Demo-live-Demo-Live.png)

Путь в меню: **Settings → Application Security → Security Posture Management: Kubernetes**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:kubernetes.security-posture-management`.

Страница в UI включает оценку K8s-кластеров на соответствие best-practices безопасности (Kubernetes Security Posture Management, KSPM).

> ⚠️ **В air-gapped Managed эта оценка в боевом режиме не работает.** По документации Dynatrace KSPM собирает конфигурацию кластера через отдельный Kubernetes Node Configuration Collector (DaemonSet, ставится Dynatrace Operator) и складывает результат в платформенный слой (Grail, новый Kubernetes app, лицензия DPS). В изолированном Managed без Grail и DPS findings некуда складывать, поэтому страница в Settings есть, а рабочего compliance-результата по ней нет. <!-- source: docs.dynatrace.com/managed/ingest-from/setup-on-k8s/deployment/security-posture-management --> <!-- qc:ignore=SAAS Grail и DPS названы как причина недоступности KSPM в air-gapped, не как рекомендация -->

*Что показать на этом экране.* Страница оценивает конфигурацию кластера на соответствие best-practices безопасности. Типовые проверки: поды под root, слишком широкие права ServiceAccount, отсутствие Network Policies, открытый API server. Сам по себе KSPM это общеотраслевая практика, а не Dynatrace-специфичная: инструмент сканирует конфигурацию и превращает каждое отклонение в finding с severity.

*Как закрывают нишу в банке.* Раз compliance-pipeline в air-gapped Managed не работает, проверку конфигурации кластера делают сторонними инструментами: kube-bench (CIS Benchmark), Trivy Operator, Falco. Их отчёты при необходимости заводят в Dynatrace как логи или события и алертят уже стандартными средствами.

> 🧭 **Рамка для лектора: Шаги 4-8 это одна логика на пяти экранах.** Пять страниц anomaly detection (cluster, namespace, node, workload, PVC) устроены одинаково, поэтому логику проговариваем один раз, а на каждом экране показываем только специфичные правила.
>
> 1. **Уровень настройки не меняет поведение.** Один и тот же набор алертов настраивается на трёх уровнях (per tenant, per cluster, per namespace). По документации Dynatrace это только для удобства массовой настройки и не меняет поведения алерта: алерт всё равно оценивается и поднимает Problem по каждой сущности отдельно. Настройка на уровне кластера это просто способ применить правило ко всем его нодам и ворклоадам сразу. <!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring/alert-on-kubernetes-issues -->
> 2. **Каждый алерт это порог плюс окно наблюдения.** У правила есть тумблер вкл/выкл, числовой порог (где применимо) и пара sample period / observation period в минутах. Часть дефолтов зафиксирована (Container restarts: порог 1, sample 3 мин, observation 5 мин; Pending pods: порог 1, sample 10 мин, observation 15 мин), а событийные алерты (OOM kills, pod backoff, pod eviction) по умолчанию включены в режиме «alert always», то есть реагируют на сам факт события. Единого числового порога «чувствительности» для всех K8s-алертов в документации Managed нет, поэтому общий порог не называем. <!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring/alert-on-kubernetes-issues -->
> 3. **Куда уходит сработка.** Любой из этих алертов поднимает Problem, а кому он придёт, решает Alerting profile (по severity и по scope, например только prod-namespace). Это общий механизм для всех пяти экранов.
>
> **ЕСЛИ → ТО про порог и окно (без выдуманных чисел):**
>
> - ЕСЛИ задать порог жёстче или укоротить observation period → Problem поднимается при меньшем отклонении и быстрее, алертов больше, но растёт доля ложных на краткие всплески.
> - ЕСЛИ задать порог мягче или удлинить observation period → система молчит на мелких и кратких отклонениях, ложных меньше, но реальную деградацию видно позже.
>
> Дальше по каждому экрану только его специфика.

### Шаг 4: Kubernetes cluster anomaly detection

![Kubernetes cluster anomaly detection: пороги для проблем на уровне всего кластера](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.cluster/Kubernetes-cluster-anomaly-detection-Environment-Settings-Demo-live-Demo-Live-Dy.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes cluster**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.cluster`.

Пороги на уровне кластера. Типовые правила:

- **Cluster CPU pressure**: суммарная загрузка CPU всех нод выше порога.
- **Cluster memory pressure**: суммарное использование памяти выше порога.
- **Pod scheduling failures**: Pending pods из-за невозможности найти ноду более N минут.
- **API server latency**: задержки API Server выше нормы, влияют на все операции.
- **Pod count anomaly**: неожиданное падение или рост общего числа подов.

Срабатывание создаёт Problem на уровне кластера (а не отдельного workload). Сразу видно, что проблема системная.

### Шаг 5: Kubernetes namespace anomaly detection

![Kubernetes namespace anomaly detection: пороги для отдельного namespace](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.namespace/Kubernetes-namespace-anomaly-detection-Environment-Settings-Demo-live-Demo-Live.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes namespace**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.namespace`.

Пороги на уровне namespace. Типовые правила:

- **Resource quota exceeded**: namespace превысил свой CPU / Memory quota.
- **Pod count exceeded**: в namespace больше подов, чем в его quota.
- **Object count anomalies**: неожиданный рост ConfigMaps / Secrets / ServiceAccounts.

Полезно в shared-кластерах: когда одна команда начинает «переедать» свой лимит.

### Шаг 6: Kubernetes node anomaly detection

![Kubernetes node anomaly detection: пороги для нод кластера](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.node/Kubernetes-node-anomaly-detection-Environment-Settings-Demo-live-Demo-Live-Dynat.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes node**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.node`.

Пороги на уровне отдельной ноды. Типовые:

- **Node NotReady**: нода в состоянии NotReady более N минут.
- **Node conditions**: DiskPressure, MemoryPressure, PIDPressure, NetworkUnavailable.
- **Pod eviction rate**: ноду «эвакуируют» из-за ресурсных проблем, kubelet начинает убивать поды.
- **Kubelet unreachable**: kubelet не отвечает на запросы API server.

Ноду можно мониторить и обычными Host-правилами (Темы 1 и 3 Дня 2). Но K8s-специфичные правила ловят K8s-события, недоступные через ОС-мониторинг.

### Шаг 7: Kubernetes workload anomaly detection

![Kubernetes workload anomaly detection: пороги для Deployment/StatefulSet](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.workload/Kubernetes-workload-anomaly-detection-Environment-Settings-Demo-live-Demo-Live-D.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes workload**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.workload`.

Самый востребованный уровень в повседневной работе. Правила:

- **Pods not running**: Ready pods меньше, чем объявлено в `.spec.replicas`. Deployment не собрал реплики.
- **Container restarts**: один или несколько контейнеров часто перезапускаются (CrashLoopBackOff).
- **OOMKilled**: контейнер убит за превышение memory limit.
- **ImagePullBackOff**: не может скачать образ (проблема с registry или credentials).
- **CPU throttling**: контейнер упирается в CPU limit.

Ежедневная работа DevOps. Эти правила ловят большинство проблем конкретного приложения в K8s.

**ЕСЛИ → ТО на уровне workload.** Здесь хорошо видно разницу между порогом и режимом «alert always»:

- ЕСЛИ контейнер перезапускается чаще порога Container restarts (по умолчанию порог 1 на sample 3 мин / observation 5 мин) → поднимается Problem «Container restarts» по этому ворклоаду; ужесточение порога ловит даже единичные CrashLoopBackOff, смягчение оставляет только устойчивую болтанку.
- ЕСЛИ под убит по памяти → срабатывает «Out-of-memory kills»: этот алерт по умолчанию работает в режиме «alert always», то есть реагирует на сам факт OOM-kill, а не на превышение числового порога.
- ЕСЛИ в Alerting profile задать scope только на критичные namespace (`retail-prod`, `corporate-prod`) → эти Problem'ы доходят до дежурного канала только по проду, а dev и staging не будят команду ночью.
<!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring/alert-on-kubernetes-issues -->

### Шаг 8: Kubernetes persistent volume claim anomaly detection

![Kubernetes PVC anomaly detection: пороги для постоянных томов](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.pvc/Kubernetes-persistent-volume-claim-anomaly-detection-Environment-Settings-Demo-l.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes persistent volume claim**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.pvc`.

Для приложений с постоянным хранилищем (StatefulSet с БД, файловые хранилища). Правила:

- **PVC storage usage**: PVC заполнен более X%.
- **PVC Bound state**: PVC долго в Pending, не может найти подходящий PV.
- **PVC I/O errors**: ошибки доступа к хранилищу (backend: NFS, Ceph, AWS EBS).

Критично для PVC под СУБД: переполнение ведёт к инциденту.

### Шаг 9: Kubernetes app (переход на новый UI)

![Kubernetes app: настройки перехода к новому UI Kubernetes-приложения](screenshots/day-2/kubernetes/settings/builtinapp-transition.kubernetes/Kubernetes-app-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Kubernetes app**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:app-transition.kubernetes`.

Страница управляет **переключением на новое Kubernetes-приложение**. В обычном Dynatrace старая страница K8s-мониторинга постепенно заменяется отдельным Kubernetes-приложением с расширенной визуализацией (топология кластера, drill-down до подов с корреляцией метрик и логов). <!-- qc:ignore=SAAS новый Kubernetes app назван как контекст; ниже явно сказано, что в air-gapped Managed его нет -->

**Что на странице.** Тумблер или редирект: когда открывать классический UI (`/ui/kubernetes`), когда новое приложение.

*В air-gapped Managed остаёмся на Classic UI.* Новое Kubernetes-приложение это часть Apps-платформы (тот же стек, на котором работают Grail и KSPM-findings), а её в изолированном контуре нет. Поэтому экран здесь по сути информационный: вся работа с кластерами идёт через классические страницы Kubernetes-мониторинга и пять экранов anomaly detection из Шагов 4-8, которые в Classic полностью функциональны (в документации помечены «Supported in: Kubernetes Classic, Kubernetes app»). <!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring/alert-on-kubernetes-issues -->

---

## ⚙️ COOKBOOK: настройка K8s-мониторинга в банке

### Подключение нового K8s-кластера

*Задача.* Подключить новый кластер к Dynatrace.

*Шаги:*

1. На кластере создать ServiceAccount `dynatrace-monitoring` с правами чтения на все ресурсы.
2. Получить токен ServiceAccount.
3. В Settings → Cloud and virtualization → Kubernetes → Connections добавить кластер: URL API, токен, CA-сертификат.
4. Проверить, что ActiveGate с ролью `kubernetes_monitoring` имеет сетевой доступ к API server.
5. Установить Dynatrace Operator через Helm с указанием тенанта и API token.
6. Через 10-15 минут кластер появляется в интерфейсе со всеми ресурсами.

### Контроль namespace-квот

*Задача.* Команда retail имеет namespace `retail-prod` с CPU quota 40 cores, Memory quota 160 GB. Нужен алерт при приближении к лимиту.

*Решение.* Kubernetes namespace anomaly detection → правило `Resource quota usage exceeded 80%`. Alerting profile `retail-ops` шлёт команде. При приближении к лимиту приходит алерт: команда успевает запросить увеличение или почистить ненужные поды.

### Алерт на CrashLoopBackOff критичного сервиса

*Задача.* `payment-service` в production начал CrashLoopBackOff. Нужно узнать мгновенно.

*Решение.* Kubernetes workload anomaly detection → правило `Container restarts count above threshold`, scope: критичные namespace'ы (`retail-prod`, `corporate-prod`). Alerting profile `prod-high-priority` отправляет в ServiceNow + дежурный канал мессенджера. При первых 3-5 рестартах приходит алерт.

### Compliance audit кластера

*Задача.* Раз в квартал предоставить отчёт о соответствии production-кластеров best practices.

*Решение.* Security Posture Management сканирует кластеры автоматически. Перед отчётом: в SPM dashboard выгружается текущее состояние findings, передаётся в compliance. DevOps работает над устранением findings между квартальными ревью.

---

## 🎓 ТЕОРИЯ: Kubernetes в Dynatrace как первоклассная сущность

### Иерархия Kubernetes-сущностей

```
Kubernetes Cluster (кластер целиком)
├─ Node (отдельная нода)
│   └─ Pod
│       └─ Container
├─ Namespace
│   └─ Deployment / StatefulSet / DaemonSet (Workload)
│       └─ Pod
│           └─ Container
├─ Service (сетевая абстракция)
└─ PersistentVolumeClaim (хранилище)
```

Dynatrace поддерживает все эти уровни как отдельные сущности в Smartscape. Каждая имеет свой URL, карточку, метрики, аномалии, связи.

### Три источника данных о Kubernetes

**OneAgent на каждой ноде.** Работает как обычный агент на хосте, но дополнительно видит cgroup'ы контейнеров, опрашивает kubelet API, получает список локальных подов. Даёт метрики каждого контейнера: CPU, Memory, Network per-container.

**Dynatrace Operator через Kubernetes API.** Ставится как Deployment в кластер, опрашивает API server с правами ServiceAccount. Получает структурную информацию: Deployments, Services, Ingresses, Namespaces, Events. Связывается с метриками от OneAgent через enrichment.

**Автоматическая инъекция CodeModules.** Mutating webhook Operator при создании каждого пода добавляет init-контейнер с language-specific agent (Java, Node.js, .NET). Основной контейнер при старте загружает этот agent, он автоматически инструментирует приложение. Изменений в Docker-образе не требуется. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/kubernetes -->

### Автоматическая корреляция трейсов

**Trace headers.** OneAgent в контейнере добавляет заголовок `x-dynatrace` в каждый исходящий HTTP-запрос. Когда запрос попадает в другой инструментированный контейнер, тот понимает это и связывает свой span с родительским. Так строится PurePath через несколько сервисов, даже в разных namespaces или разных кластерах (если оба подключены к Dynatrace).

**Service Mesh (Istio / Linkerd).** Работает с Dynatrace из коробки. OneAgent обнаруживает sidecar-прокси, понимает их роль, корректно обрабатывает трейсы. Если в кластере mTLS между сервисами: Dynatrace показывает это в Smartscape и помогает диагностировать проблемы с сертификатами.

### Разная глубина настроек

- **Production-кластеры.** Все 9 страниц настроек оттюнены: своя схема labels, свои alerting profiles, включён SPM для compliance, тонко настроены workload anomaly detection thresholds.
- **Dev и staging.** Минимальные настройки, стандартные пороги. Часть anomaly detection отключается: чтобы не засорять дежурных ложными алертами на эксперименты.
- **Shared multi-tenant кластеры.** Фокус на namespace-level изоляции: namespace quotas, network policies, telemetry enrichment с team-labels, чтобы каждая команда видела только свои данные.

### Air-gapped Kubernetes

**Полная поддержка в изолированном контуре.** Все три источника данных (OneAgent, Operator, CodeModules) работают локально, без выхода в интернет.

**Требования:**

- Registry внутри контура для образов Dynatrace (Operator, OneAgent, CodeModules). Harbor, Artifactory или другой. Админ регулярно скачивает новые версии образов на машине с интернетом и загружает в свой registry.
- ActiveGate с ролью `kubernetes_monitoring`: в отдельном namespace с сетевым доступом к API server мониторимых кластеров.
- Токены ServiceAccount кластеров хранятся в Dynatrace Credential Vault с ограниченной областью действия.
- Сертификаты API server: внутренние CA, доверенные и в кластере, и в ActiveGate.

При соблюдении: мониторинг K8s работает одинаково с облачным Dynatrace, без потери функциональности.
