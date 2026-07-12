---
topic_id: kubernetes
day_id: day-2
timing_min: 28
verified: 2026-07-12
---
## ГДЕ
Тема живёт на девяти экранах Settings.
Главный экран сбора данных: Settings → Cloud and virtualization → Kubernetes → Monitoring settings, route `/ui/settings/builtin:cloud.kubernetes.monitoring`.
Telemetry enrichment: `/ui/settings/builtin:kubernetes.generic.metadata.enrichment`. Security Posture Management: Kubernetes: `/ui/settings/builtin:kubernetes.security-posture-management`.
Пять экранов порогов: Settings → Anomaly detection → Kubernetes cluster / namespace / node / workload / persistent volume claim, routes `builtin:anomaly-detection.kubernetes.cluster` (и по аналогии namespace, node, workload, pvc).
Переход на новый UI: Settings → Kubernetes app, route `/ui/settings/builtin:app-transition.kubernetes`.

## ЗАЧЕМ
Kubernetes в Dynatrace это первоклассная сущность: кластер, нода, namespace, под, workload, PVC живут в Smartscape как отдельные сущности, у каждой свои метрики, аномалии и связи.
Экран Monitoring settings задаёт, как Dynatrace общается с API кластера и что собирает; пять экранов anomaly detection задают пороги на каждом уровне; enrichment цепляет K8s-метки к метрикам приложений.
Данные приходят из трёх источников: OneAgent на ноде, Dynatrace Operator через API кластера, автоинъекция CodeModules.

## ЦИФРЫ
- Девять экранов настройки: Monitoring settings, Telemetry enrichment, SPM, пять уровней anomaly detection (cluster, namespace, node, workload, PVC), Kubernetes app.
- Container restarts, дефолт по документации Managed: порог 1, sample 3 мин, observation 5 мин.
- Pending pods, дефолт: порог 1, sample 10 мин, observation 15 мин.
- Событийные алерты (OOM kills, pod backoff, pod eviction) по умолчанию в режиме «alert always»: реагируют на сам факт события, без числового порога.
- После установки Operator кластер появляется в интерфейсе со всеми ресурсами через 10-15 минут.
- Пример namespace-квоты в банке: CPU 40 cores, Memory 160 GB, алерт при 80% лимита (у вашего тенанта цифры могут быть другими).

## ЕСЛИ→ТО
- ЕСЛИ namespace внесён в exclude-список (например `kube-system`) → его поды, ворклоады и события перестают собираться, по нему не будет ни метрик в Data Explorer, ни anomaly-проблем: шум уходит, но слепая зона появляется осознанно.
- ЕСЛИ контейнер перезапускается чаще порога Container restarts (дефолт 1 на sample 3 мин / observation 5 мин) → поднимается Problem по этому ворклоаду; жёстче порог ловит даже единичные CrashLoopBackOff, мягче оставляет только устойчивую болтанку.
- ЕСЛИ под убит по памяти → срабатывает Out-of-memory kills: этот алерт по умолчанию в режиме «alert always», реагирует на сам факт OOM-kill, а не на превышение числового порога.
- ЕСЛИ в Alerting profile задать scope только на прод-namespace (`retail-prod`, `corporate-prod`) → Problem'ы доходят до дежурного канала только по проду, dev и staging ночью команду не будят.

## ЗАПАСНОЙ ПЛАН
Если открываю страницу Kubernetes app: проговариваю, что в изолированном Managed новое приложение недоступно (нужна Apps-платформа), вся работа идёт в Classic UI и на пяти экранах anomaly detection, которые в Classic полностью функциональны.
Если показываю Security Posture Management: говорю честно, что в air-gapped Managed рабочего compliance-результата по этой странице нет (findings некуда складывать без платформенного слоя), страница в Settings остаётся, а проверку конфигурации кластера закрываю сторонними инструментами (kube-bench по CIS, Trivy, Falco) и при необходимости завожу их отчёты в Dynatrace как логи или события.
Если страница дефолтов anomaly detection пуста или серая (нет write-прав на демо): не называю пороги по памяти сверх задокументированных, отсылаю к значениям на самой странице тенанта.

## ВОПРОСЫ АУДИТОРИИ
- «Откуда Dynatrace берёт данные о Kubernetes?» Ответ: из трёх источников: OneAgent на ноде (метрики контейнеров через cgroup и kubelet), Dynatrace Operator через API кластера (Deployments, Services, Namespaces, Events), автоинъекция CodeModules mutating-webhook'ом без правки Docker-образа.
- «Работает ли K8s-мониторинг в закрытом контуре?» Ответ: да, все три источника работают локально при наличии внутреннего registry для образов Dynatrace, ActiveGate с ролью `kubernetes_monitoring` и доступом к API server, токенов ServiceAccount в Credential Vault и доверенных внутренних CA.
- «Чем workload-пороги лучше обычного мониторинга ноды?» Ответ: K8s-специфичные правила ловят события уровня Kubernetes (Pods not running, CrashLoopBackOff, OOMKilled, ImagePullBackOff, CPU throttling), которые не видны через ОС-мониторинг хоста.
