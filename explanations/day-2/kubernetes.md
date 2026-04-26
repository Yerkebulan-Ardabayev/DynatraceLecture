> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 5 из 9: «Мониторинг Kubernetes: кластеры, ноды, поды, ворклоады»
>
> 🔖 **Редакция от 2026-04-26.** Тех-факты сверены с `docs.dynatrace.com/managed/` и общими страницами Kubernetes monitoring / SPM / anomaly detection (общие для Managed и SaaS). Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-26 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Managed-специфика (приоритетный источник):**
> - [Setup on Kubernetes — Dynatrace Managed](https://docs.dynatrace.com/managed/ingest-from/setup-on-k8s) — установка Operator/CodeModules в кластер на Managed-документации (air-gapped registry, токены)
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed) — корневая страница раздела Managed Docs
>
> **Общая (одинаково для Managed и SaaS):**
> - [Setup on Kubernetes — overview](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s) — установка OneAgent Operator, CodeModules, helm chart
> - [Kubernetes installation](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/installation) — варианты deployment (helm, manifests, OLM)
> - [Kubernetes deployment patterns](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/deployment) — типовые сценарии deployment
> - [Kubernetes monitoring](https://docs.dynatrace.com/docs/observe/infrastructure-observability/container-platform-monitoring/kubernetes-monitoring) — концепция и структура Kubernetes-мониторинга в Dynatrace
> - [Cloud Kubernetes monitoring — settings schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-cloud-kubernetes-monitoring) — формальная схема страницы Kubernetes monitoring
> - [Kubernetes Security Posture Management — settings schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-kubernetes-security-posture-management) — SPM (compliance чек-листы)
> - [Anomaly detection — Kubernetes cluster — schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-anomaly-detection-kubernetes-cluster) — пороги аномалий на уровне кластера
> - [Anomaly detection — Kubernetes workload — schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-anomaly-detection-kubernetes-workload) — пороги аномалий на уровне workload
> - [Kubernetes — параметрический shortlink](https://docs.dynatrace.com/docs/shortlink/kubernetes) — каноническая точка входа для темы Kubernetes

## 📍 КАРТА — девять страниц для настройки Kubernetes-мониторинга

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
| Kubernetes app (переходы в Latest Dynatrace) | **Settings → Kubernetes app** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:app-transition.kubernetes` | Настройки перехода к новому Kubernetes-приложению в Latest Dynatrace (для нового UI) |

---

## 🎬 Работа с настройками Kubernetes на девяти экранах

### Шаг 1 — Monitoring settings (главная страница сбора K8s-данных)

![Monitoring settings — глобальные параметры Kubernetes-мониторинга](screenshots/day-2/kubernetes/settings/builtincloud.kubernetes.monitoring/Monitoring-settings-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Cloud and virtualization → Kubernetes → Monitoring settings**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:cloud.kubernetes.monitoring`.

Центральная страница K8s-мониторинга. Здесь задаётся, **как Dynatrace общается с API Kubernetes, что собирает, с какой частотой**. Заголовков в captured нет, страница — тумблеры, поля, списки.

**Что настраивается:**

- **Подключение к кластеру.** URL API server, токен ServiceAccount с правами чтения ресурсов, CA-сертификат. Эти данные использует ActiveGate для опроса API.
- **Интервалы опроса.** ActiveGate с ролью Kubernetes monitoring периодически опрашивает API server. Конкретные значения по умолчанию для разных типов ресурсов в публичной документации Dynatrace не зафиксированы — управление интервалом находится на стороне ActiveGate и подстраивается под нагрузку.
- **Типы собираемых ресурсов.** Можно отключить конкретные (например, Jobs / CronJobs, если их много и они создают шум).
- **Ограничения по namespaces.** Список, который НЕ мониторить — `kube-system`, `kube-public` и другие системные, если не нужны.
- **Обработка событий K8s.** Какие `Event`-объекты учитывать как события в Dynatrace: Pulled / Created / Started / Failed.

*Типовая работа.* Страница трогается при подключении нового кластера (вносят параметры) и при ревью (добавляют exclude-списки namespaces).

### Шаг 2 — Kubernetes Telemetry Enrichment

![Kubernetes Telemetry Enrichment — добавление K8s-метаданных к трейсам и метрикам](screenshots/day-2/kubernetes/settings/builtinkubernetes.generic.metadata.enrichment/Kubernetes-Telemetry-Enrichment-Environment-Settings-Demo-live-Demo-Live-Dynatra.png)

Путь в меню: **Settings → Cloud and virtualization → Kubernetes → Telemetry enrichment**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:kubernetes.generic.metadata.enrichment`.

*Что такое Telemetry Enrichment.* Когда приложение в контейнере отправляет метрики (OneAgent или OpenTelemetry), эти метрики сами по себе не знают, в каком поде они родились, в каком namespace, под каким deployment. Enrichment — **автоматическое добавление меток K8s к метрикам**, чтобы их можно было фильтровать и группировать.

**Что обогащается.** Каждая метрика, трейс, лог от приложения в контейнере получает поля `k8s.pod.name`, `k8s.namespace.name`, `k8s.deployment.name`, `k8s.node.name`, `k8s.cluster.name`. Дальше в Data Explorer и Alerting profiles можно фильтровать по ним.

**Что настраивается:**

- Какие стандартные поля добавлять (обычно все включены).
- Какие дополнительные labels и annotations включать (например, кастомные `company/product`, `company/team`).
- Формат имён — как ключ называется в метриках Dynatrace, чтобы совпадать с соглашениями команды.

*Практическая польза.* После настройки enrichment в Data Explorer можно написать `builtin:service.response.time:filter(dt.entity.cloud_application.k8s.namespace.name=="retail-prod")` и получить метрики только ретейл-продакшна. Без enrichment такой запрос невозможен.

### Шаг 3 — Security Posture Management: Kubernetes

![Security Posture Management — оценка безопасности конфигурации кластера](screenshots/day-2/kubernetes/settings/builtinkubernetes.security-posture-management/Security-Posture-Management-Kubernetes-Environment-Settings-Demo-live-Demo-Live.png)

Путь в меню: **Settings → Application Security → Security Posture Management: Kubernetes**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:kubernetes.security-posture-management`.

Страница включает оценку K8s-кластеров на соответствие **CIS Kubernetes Benchmark** и другим стандартам безопасности. Часть функциональности Application Security.

*Что делает SPM.* Сканирует конфигурацию кластера: RBAC-правила, SecurityContext подов, Network Policies, PodSecurityPolicies (или PodSecurityStandards в новых K8s), сертификаты, конфигурацию API server. Каждое несоответствие benchmark превращается в **finding** с уровнем серьёзности (Critical / High / Medium / Low) и рекомендациями.

**Типовые findings в свежем кластере:**

- Поды запущены как root (должны быть с не-root SecurityContext).
- Контейнеры без `readOnlyRootFilesystem: true`.
- ServiceAccounts со слишком широкими правами.
- API server доступен с untrusted networks.
- Audit logging не включён.
- Network Policies отсутствуют в критичных namespaces.

*Роль SPM.* Часть compliance. Регуляторы требуют регулярного аудита K8s на соответствие best practices. SPM-репорты — вход для compliance-отчётности.

### Шаг 4 — Kubernetes cluster anomaly detection

![Kubernetes cluster anomaly detection — пороги для проблем на уровне всего кластера](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.cluster/Kubernetes-cluster-anomaly-detection-Environment-Settings-Demo-live-Demo-Live-Dy.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes cluster**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.cluster`.

Пороги на уровне кластера. Типовые правила:

- **Cluster CPU pressure** — суммарная загрузка CPU всех нод выше порога.
- **Cluster memory pressure** — суммарное использование памяти выше порога.
- **Pod scheduling failures** — Pending pods из-за невозможности найти ноду более N минут.
- **API server latency** — задержки API Server выше нормы, влияют на все операции.
- **Pod count anomaly** — неожиданное падение или рост общего числа подов.

Срабатывание создаёт Problem на уровне кластера (а не отдельного workload). Сразу видно, что проблема системная.

### Шаг 5 — Kubernetes namespace anomaly detection

![Kubernetes namespace anomaly detection — пороги для отдельного namespace](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.namespace/Kubernetes-namespace-anomaly-detection-Environment-Settings-Demo-live-Demo-Live.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes namespace**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.namespace`.

Пороги на уровне namespace. Типовые правила:

- **Resource quota exceeded** — namespace превысил свой CPU / Memory quota.
- **Pod count exceeded** — в namespace больше подов, чем в его quota.
- **Object count anomalies** — неожиданный рост ConfigMaps / Secrets / ServiceAccounts.

Полезно в shared-кластерах — когда одна команда начинает «переедать» свой лимит.

### Шаг 6 — Kubernetes node anomaly detection

![Kubernetes node anomaly detection — пороги для нод кластера](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.node/Kubernetes-node-anomaly-detection-Environment-Settings-Demo-live-Demo-Live-Dynat.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes node**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.node`.

Пороги на уровне отдельной ноды. Типовые:

- **Node NotReady** — нода в состоянии NotReady более N минут.
- **Node conditions** — DiskPressure, MemoryPressure, PIDPressure, NetworkUnavailable.
- **Pod eviction rate** — ноду «эвакуируют» из-за ресурсных проблем, kubelet начинает убивать поды.
- **Kubelet unreachable** — kubelet не отвечает на запросы API server.

Ноду можно мониторить и обычными Host-правилами (Темы 1 и 3 Дня 2). Но K8s-специфичные правила ловят K8s-события, недоступные через ОС-мониторинг.

### Шаг 7 — Kubernetes workload anomaly detection

![Kubernetes workload anomaly detection — пороги для Deployment/StatefulSet](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.workload/Kubernetes-workload-anomaly-detection-Environment-Settings-Demo-live-Demo-Live-D.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes workload**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.workload`.

Самый востребованный уровень в повседневной работе. Правила:

- **Pods not running** — Ready pods меньше, чем объявлено в `.spec.replicas`. Deployment не собрал реплики.
- **Container restarts** — один или несколько контейнеров часто перезапускаются (CrashLoopBackOff).
- **OOMKilled** — контейнер убит за превышение memory limit.
- **ImagePullBackOff** — не может скачать образ (проблема с registry или credentials).
- **CPU throttling** — контейнер упирается в CPU limit.

Ежедневная работа DevOps. Эти правила ловят большинство проблем конкретного приложения в K8s.

### Шаг 8 — Kubernetes persistent volume claim anomaly detection

![Kubernetes PVC anomaly detection — пороги для постоянных томов](screenshots/day-2/kubernetes/settings/builtinanomaly-detection.kubernetes.pvc/Kubernetes-persistent-volume-claim-anomaly-detection-Environment-Settings-Demo-l.png)

Путь в меню: **Settings → Anomaly detection → Kubernetes persistent volume claim**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.kubernetes.pvc`.

Для приложений с постоянным хранилищем (StatefulSet с БД, файловые хранилища). Правила:

- **PVC storage usage** — PVC заполнен более X%.
- **PVC Bound state** — PVC долго в Pending, не может найти подходящий PV.
- **PVC I/O errors** — ошибки доступа к хранилищу (backend — NFS, Ceph, AWS EBS).

Критично для PVC под СУБД — переполнение ведёт к инциденту.

### Шаг 9 — Kubernetes app (переход в Latest Dynatrace)

![Kubernetes app — настройки перехода к новому UI Kubernetes-приложения](screenshots/day-2/kubernetes/settings/builtinapp-transition.kubernetes/Kubernetes-app-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Settings → Kubernetes app**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:app-transition.kubernetes`.

Страница настраивает **переход к новому K8s-приложению в Latest Dynatrace**. В классическом Managed-интерфейсе старая страница K8s-мониторинга постепенно заменяется новым отдельным Kubernetes-приложением с расширенными возможностями визуализации — топология кластера, drill-down до подов с корреляцией метрик и логов.

**Что на странице.** Тумблер или URL-редирект: когда использовать старый UI (`/ui/kubernetes`), когда новый.

*В air-gapped Managed.* Обычно остаются на классическом UI по умолчанию — новый требует Apps-платформу, которая в изолированном контуре недоступна.

---

## ⚙️ COOKBOOK — настройка K8s-мониторинга в банке

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

*Решение.* Kubernetes namespace anomaly detection → правило `Resource quota usage exceeded 80%`. Alerting profile `retail-ops` шлёт команде. При приближении к лимиту приходит алерт — команда успевает запросить увеличение или почистить ненужные поды.

### Алерт на CrashLoopBackOff критичного сервиса

*Задача.* `payment-service` в production начал CrashLoopBackOff. Нужно узнать мгновенно.

*Решение.* Kubernetes workload anomaly detection → правило `Container restarts count above threshold`, scope — критичные namespace'ы (`retail-prod`, `corporate-prod`). Alerting profile `prod-high-priority` отправляет в ServiceNow + дежурный канал мессенджера. При первых 3-5 рестартах приходит алерт.

### Compliance audit кластера

*Задача.* Раз в квартал предоставить отчёт о соответствии production-кластеров best practices.

*Решение.* Security Posture Management сканирует кластеры автоматически. Перед отчётом — в SPM dashboard выгружается текущее состояние findings, передаётся в compliance. DevOps работает над устранением findings между квартальными ревью.

---

## 🎓 ТЕОРИЯ — Kubernetes в Dynatrace как первоклассная сущность

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

**Автоматическая инъекция CodeModules.** Mutating webhook Operator при создании каждого пода добавляет init-контейнер с language-specific agent (Java, Node.js, .NET). Основной контейнер при старте загружает этот agent, он автоматически инструментирует приложение. Изменений в Docker-образе не требуется.

### Автоматическая корреляция трейсов

**Trace headers.** OneAgent в контейнере добавляет заголовок `x-dynatrace` в каждый исходящий HTTP-запрос. Когда запрос попадает в другой инструментированный контейнер, тот понимает это и связывает свой span с родительским. Так строится PurePath через несколько сервисов, даже в разных namespaces или разных кластерах (если оба подключены к Dynatrace).

**Service Mesh (Istio / Linkerd).** Работает с Dynatrace из коробки. OneAgent обнаруживает sidecar-прокси, понимает их роль, корректно обрабатывает трейсы. Если в кластере mTLS между сервисами — Dynatrace показывает это в Smartscape и помогает диагностировать проблемы с сертификатами.

### Разная глубина настроек

- **Production-кластеры.** Все 9 страниц настроек оттюнены: своя схема labels, свои alerting profiles, включён SPM для compliance, тонко настроены workload anomaly detection thresholds.
- **Dev и staging.** Минимальные настройки, стандартные пороги. Часть anomaly detection отключается — чтобы не засорять дежурных ложными алертами на эксперименты.
- **Shared multi-tenant кластеры.** Фокус на namespace-level изоляции: namespace quotas, network policies, telemetry enrichment с team-labels, чтобы каждая команда видела только свои данные.

### Air-gapped Kubernetes

**Полная поддержка в изолированном контуре.** Все три источника данных (OneAgent, Operator, CodeModules) работают локально, без выхода в интернет.

**Требования:**

- Registry внутри контура для образов Dynatrace (Operator, OneAgent, CodeModules). Harbor, Artifactory или другой. Админ регулярно скачивает новые версии с customer portal и загружает в свой registry.
- ActiveGate с ролью `kubernetes_monitoring` — в отдельном namespace с сетевым доступом к API server мониторимых кластеров.
- Токены ServiceAccount кластеров хранятся в Dynatrace Credential Vault с ограниченной областью действия.
- Сертификаты API server — внутренние CA, доверенные и в кластере, и в ActiveGate.

При соблюдении — мониторинг K8s работает одинаково с облачным Dynatrace, без потери функциональности.
