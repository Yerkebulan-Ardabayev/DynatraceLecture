---
topic_id: alerting-profiles
day_id: day-5
timing_min: 26
verified: 2026-07-12
---
## ГДЕ
Три страницы в Settings, разделы Alerting и Anomaly detection.
Problem alerting profiles: Settings → Alerting → Alerting profiles, route `/ui/settings/builtin:alerting.profile`.
Maintenance windows: Settings → Alerting → Maintenance windows, route `/ui/settings/builtin:alerting.maintenance-window`.
Metric events (кастомные алерты): Settings → Anomaly detection → Metric events, route `/ui/settings/builtin:anomaly-detection.metric-events`.

## ЗАЧЕМ
Alerting profile это именованный набор фильтров: какие проблемы попадают в профиль и дальше в привязанные интеграции. Отвечает на вопрос КОМУ уходит уведомление.
Maintenance window отвечает на вопрос КОГДА молчать: период, когда Dynatrace либо не создаёт проблемы, либо создаёт без отправки нотификаций.
Metric event это кастомный алерт на произвольную метрику (когда метрика X переходит порог Y, создать Davis Problem), для бизнес-метрик, которых Davis сам не знает.

## ЦИФРЫ
- Severity rules: до 100 правил на профиль, между собой объединяются по OR.
- Event filters: до 20 правил на профиль; с блоком severity объединяются по AND.
- Maintenance windows: до 2000 на environment, типы Planned и Unplanned.
- Metric event configurations: до 10 000 на environment.
- Три стратегии порога metric event: static, auto-adaptive, seasonal (последние две только для metric selector events).
- Davis строит baseline автоматически за 7 дней и ловит аномалии по 3σ; delay 3-5 минут перед первым уведомлением гасит проблему, мигнувшую за 90 секунд.

## ЕСЛИ→ТО
- ЕСЛИ проблема попала хотя бы в одно severity rule → блок severity сработал (внутри по OR), но уведомление уйдёт, только если проблема прошла ещё и event filters (блоки между собой по AND).
- ЕСЛИ одна проблема подошла под несколько профилей → уйдёт во все сразу, не только в первый: Critical на prod-БД идёт и дежурному через PagerDuty, и в очередь DBA по email.
- ЕСЛИ в maintenance window включить только Suppress alerting → detection работает, гаснут лишь нотификации; ЕСЛИ включить Suppress problems → гасится и само обнаружение проблем.
- ЕСЛИ metric event типа metric key → доступен только static threshold; ЕСЛИ metric selector → доступны все три стратегии (static, auto-adaptive, seasonal).

## ЗАПАСНОЙ ПЛАН
Если на демо нет write-прав и профиль не сохранить: показываю снимок alerting profiles из курса и проговариваю структуру (management zone, severity rules, event filters) и логику OR внутри severity, AND между блоками.
В air-gapped Managed новая Workflows-платформа и новый Apps-интерфейс для custom alerts не активны: говорю честно, что работаем в классических alerting profiles и классическом конфиге metric events, SaaS-версии этих экранов рабочими не показываю.
Если Metric events открывает только заголовок Overview of limits: разбираю лимит 10 000 конфигураций на environment и типовой кейс бизнес-метрики (меньше 10 заявок на кредит за минуту в рабочие часы), конкретные пороги тенанта по памяти не называю.

## ВОПРОСЫ АУДИТОРИИ
- «Проблема подошла под несколько профилей, уведомление задвоится или уйдёт в один?» Ответ: уйдёт во все подходящие профили сразу, не только в первый, это штатно, разные команды получают свой канал (дежурный через PagerDuty, DBA через email).
- «Чем metric event отличается от Davis baseline?» Ответ: Davis автоматический по встроенным метрикам hosts/services/apps, metric event ручной на любую метрику включая бизнесовую; Davis для техники, metric events для бизнеса, дублировать Davis metric-ивентом не нужно.
- «Как не будить дежурного на плановые работы?» Ответ: оформить maintenance window, Suppress alerting гасит только нотификации, Suppress problems гасит и обнаружение, оба типа окна вырезают период из расчёта baseline.
