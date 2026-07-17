---
topic_id: incident-lifecycle
day_id: day-3-4
timing_min: 26
verified: 2026-07-12
---
## ГДЕ
Тема идёт по пяти экранам полного цикла инцидента.
Детекция: Observe and explore → Problems, route `/ui/problems`.
Маршрутизация: Settings → Alerting → Alerting profiles, route `/ui/settings/builtin:alerting.profile`.
Подавление: Settings → Alerting → Maintenance windows, route `/ui/settings/builtin:alerting.maintenance-window`.
Отправка: Settings → Integration → Problem notifications, route `/ui/settings/builtin:problem.notifications`.
Связь с релизом: Settings → Releases → Issue-tracking for releases, route `/ui/settings/builtin:issue-tracking.integration`.

## ЗАЧЕМ
Problem это готовый инцидент от Davis AI, а тема показывает весь путь: детекция → агрегация симптомов → корневая причина → маршрутизация → реакция дежурного → закрытие и разбор.
Пять экранов Settings и есть управление этим путём: куда ушла проблема, кого будить, когда молчать, в какой трекер завести.

## ЦИФРЫ
- Счётчик на демо: 69 Problems, в списке первые 50 (у вашего тенанта цифры могут быть другими).
- Severity rules в alerting profile: до 100 правил, между ними OR.
- Event filters в alerting profile: до 20 правил.
- Maintenance windows: до 2000 окон на окружение.
- Issue-tracking конфигураций: до 20 на окружение.
- Slowdown: уведомление с задержкой 5 минут, чтобы отделить шум.

## ЕСЛИ→ТО
- ЕСЛИ Davis нашёл аномалию по anomaly detection rules → на экране Problems появляется новая Problem с Severity, Affected entity и Root cause; ЕСЛИ аномалии нет → Davis молчит, новой строки нет.
- ЕСЛИ сервис не привязан ни к одному alerting profile → проблемы по нему никуда не маршрутизируются, это «забытый» сервис.
- ЕСЛИ создать maintenance window перед плановым релизом → Dynatrace не создаёт проблемы либо не шлёт уведомления (режим подавления: только уведомления либо и само обнаружение), дежурных ночью не будят.
- ЕСЛИ нужно авто-создание тикета на Problem → это Problem notifications → Jira, а Issue-tracking integration только привязывает трекер к Release inventory, автотикетинга там нет.

## ЗАПАСНОЙ ПЛАН
Если список Problems пуст: проговариваю, что пустой список значит отсутствие активных проблем, а не выключенный мониторинг, показываю снимок со счётчиком из курса.
Если Alerting profiles, Problem notifications или Maintenance windows на демо пусты либо без write-прав: иду по снимкам из курса и провожу все пять экранов цикла по порядку (Problems → Alerting profiles → Maintenance windows → Problem notifications → Issue tracking), лимиты называю только задокументированные.
SaaS-плашку про новое приложение Problems проговариваю как неактуальную для Managed: работаем в Classic UI.

## ВОПРОСЫ АУДИТОРИИ
- «Придёт ли уведомление на каждое изменение проблемы?» Ответ: нет, уведомления уходят только при создании и закрытии Problem, промежуточные апдейты намеренно не шлются.
- «Закроет ли Dynatrace тикет в Jira сам после устранения?» Ответ: нет, Dynatrace не закрывает Jira-тикеты автоматически, закрытие вручную в Jira или через свой workflow.
- «Работает ли весь цикл в закрытом контуре?» Ответ: да, всё локально, интеграции только с внутренними системами (внутренний Jira/ServiceNow, корпоративный мессенджер, внутренний SMTP), внешние cloud-сервисы не задействованы.
