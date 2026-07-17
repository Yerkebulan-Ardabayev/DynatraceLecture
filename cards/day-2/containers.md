---
topic_id: containers
day_id: day-2
timing_min: 25
verified: 2026-07-12
---
## ГДЕ
Четыре страницы в одном разделе: Settings → Processes and containers.
- Container monitoring, route `/ui/settings/builtin:container.technology` (глобальный переключатель рантаймов).
- Built-in container monitoring rules, route `/ui/settings/builtin:container.built-in-monitoring-rule` (предустановленные правила-исключения).
- Container monitoring rules, route `/ui/settings/builtin:container.monitoring-rule` (кастомные правила вкл/выкл).
- Cloud application and workload detection, route `/ui/settings/builtin:process-group.cloud-application-workload-detection` (распознавание Kubernetes-сущностей).

## ЗАЧЕМ
Настраиваем, как Dynatrace мониторит контейнеры и склеивает поды в логические сущности Kubernetes.
Отвечает на «какие рантаймы собирать», «какие служебные контейнеры прятать из интерфейса», «как из подов собрать Workload и Cloud Application».

## ЦИФРЫ
- Четыре страницы настроек контейнеров живут в разделе Settings → Processes and containers.
- containerd стал рантаймом Kubernetes с версии 1.24 (пришёл на смену Docker); OneAgent мониторит также Docker, CRI-O, Podman.
- Linux cgroups двух версий, v1 и v2: базовый уровень, когда рантайм не распознан или нестандартный.
- Три встроенных правила-исключения (включены по умолчанию, редактировать нельзя, только вкл/выкл): имя K8s-контейнера равно POD, Docker-образ содержит pause-amd64, namespace равен openshift-sdn.
- Три уровня Kubernetes-иерархии в терминах Dynatrace: Cloud Application (логическое приложение) · Workload (Deployment/StatefulSet/DaemonSet) · Pod (одна реплика).

## ЕСЛИ→ТО
- ЕСЛИ OneAgent установлен прямо на хосты (classic host monitoring) → правила Container monitoring rules работают; ЕСЛИ мониторинг идёт через webhook-инъекцию Kubernetes (cloudNativeFullStack или applicationMonitoring через Dynatrace Operator) → эти правила игнорируются, сбор задаётся через DynaKube CR, на странице настраивать нечего.
- ЕСЛИ главный тумблер сбора метрик контейнеров выключен → OneAgent не опрашивает рантайм и метрик контейнеров нет (по умолчанию тумблер включён).
- ЕСЛИ поды несут стандартные K8s-labels (app.kubernetes.io/name|version|stage) → детекция Workload работает на дефолте; ЕСЛИ схема лейблов своя → пробросить их в env-переменные DT_RELEASE_* и добавить правило.
- ЕСЛИ контейнер убит по превышению memory limit → Dynatrace пишет отдельное событие OOMKilled с использованной памятью и лимитом, это ключ к разбору memory leak.

## ЗАПАСНОЙ ПЛАН
Тумблеры и встроенные правила на демо серые (нет write-прав): это ожидаемо, показываю снимок из курса, проговариваю главный тумблер сбора метрик и три встроенных правила, ничего не переключаю.
Если список Cloud Applications / Workloads пуст (на демо нет живого Kubernetes): показываю снимок страницы Cloud application and workload detection из курса и на пальцах разбираю связку Cloud Application · Workload · Pod, сущности не выдумываю.
Навигацию по меню подстраховываю прямой ссылкой по route (например `/ui/settings/builtin:container.technology`), если пункты меню на тенанте расположены иначе.

## ВОПРОСЫ АУДИТОРИИ
- «Почему одноразовые build-контейнеры Jenkins/GitLab-Runner висят в списках и шумят?» Ответ: они живут недолго, но попадают в мониторинг; убираются кастомным правилом на Container monitoring rules (условие по image jenkins-agent:*, действие «не мониторить»).
- «Мониторим Kubernetes через Dynatrace Operator, а Container monitoring rules не срабатывают, почему?» Ответ: при webhook-инъекции (cloudNativeFullStack или applicationMonitoring) эти правила игнорируются, сбор задаётся через DynaKube CR, а не через страницу Settings.
- «Как контейнерный мониторинг работает в закрытом контуре без интернета?» Ответ: образы Dynatrace Operator и CodeModules заранее кладут во внутренний registry (Harbor/Artifactory), Helm настраивают на него, дальше установка и обновление агентов идут без выхода в интернет.
