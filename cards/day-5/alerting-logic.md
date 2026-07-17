---
topic_id: alerting-logic
day_id: day-5
timing_min: 25
verified: 2026-07-12
---
## ГДЕ
Тема живёт на трёх экранах доставки уведомлений.
System notifications (внутренние сообщения платформы): Manage → System Notifications (левая навигация), route `/ui/system-notifications`.
Problem notifications (интеграции с внешними системами): Settings → Integration → Problem notifications, route `/ui/settings/builtin:problem.notifications`.
Issue-tracking: Settings → Cloud Automation → Issue-tracking for releases, route `/ui/settings/builtin:issue-tracking.integration`.

## ЗАЧЕМ
Три экрана делят логику оповещений: System notifications это алерты самой платформы (лицензия кончается, интеграция упала, extension сломался), Problem notifications это алерты приложений во внешние системы (сервис упал, БД тормозит), Issue-tracking это статистика тикетов, привязанных к релизу.
Ключевой момент доставки: push во внешнюю систему уходит только на detect и на resolve проблемы, не на каждое обновление статуса, это гасит alert fatigue.
В air-gapped Managed движок Workflows / AutomationEngine не активен (это часть Apps-платформы SaaS): работаем на классических Problem notifications плюс кастомные webhook-receiver'ы.

## ЦИФРЫ
- Issue-tracking: до 20 конфигураций на environment.
- Issue-tracking читает статистику из 5 систем: Jira on-premises, Jira Cloud, GitHub, GitLab, ServiceNow.
- System notifications на демо-тенанте: заголовок 0 Notifications, список пуст.
- Integration failure виден в System notifications; точный порог повторов отправки в доке не зафиксирован.
- Pull-model для закрытого контура: внутренний poller спрашивает Dynatrace API о новых проблемах каждые 30 секунд, исходящее соединение инициируется изнутри сети.

## ЕСЛИ→ТО
- ЕСЛИ проблема «мерцает» (появилась → исчезла → появилась) → каждое появление это новая Problem со своей парой detect / resolve, в канал прилетает серия пар уведомлений на один реальный сбой.
- ЕСЛИ firewall блокирует исходящий HTTPS к hooks.slack.com → Slack-webhook молчит; решение: ActiveGate как outbound proxy, либо internal webhook receiver, либо только внутренний SMTP.
- ЕСЛИ нужна эскалация «за 10 минут никто не взял → уровень выше» → её делает внешняя on-call система (PagerDuty, OpsGenie), Dynatrace шлёт только начальное уведомление.
- ЕСЛИ уведомление не ушло (integration unhealthy) → сбой виден в System notifications; политика повторов в публичной доке не описана.

## ЗАПАСНОЙ ПЛАН
System notifications на демо пуст (0 Notifications): показываю пустой inbox и проговариваю, что сюда платформа пишет license warnings, tenant configuration changes, extension issues, integration failures; в закрытом контуре это единственный ранний сигнал, Mission Control недоступен.
Problem notifications: если форма пуста, открываю тип интеграции (Email или Webhook), показываю поля Name, URL / credentials, Alerting profile filter, Custom payload и закрываю без сохранения.
Issue-tracking: по снимку показываю, что это чтение статистики open / closed тикетов по релизу, а не создание тикетов; само создание тикета настраивается в Problem notifications.

## ВОПРОСЫ АУДИТОРИИ
- «Чем System notifications отличается от Problem notifications?» Ответ: System это алерты самой платформы (лицензия, упавшая интеграция, extension), Problem это алерты приложений (сервис упал, БД тормозит) во внешние системы.
- «Как слать уведомления наружу в закрытом контуре?» Ответ: через ActiveGate как outbound proxy, либо внутренний webhook-receiver с пересылкой разрешёнными каналами, либо ограничиться внутренним SMTP.
- «Issue-tracking создаёт тикеты по проблеме?» Ответ: нет, он только читает статистику тикетов по релизу; создание тикета настраивается в Problem notifications с трекером (Jira, ServiceNow).
