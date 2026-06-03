> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 8 из 10: «Работа с оповещениями и их логика в Dynatrace»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Problem notifications](https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/problem-notifications)
> - [Problem alerting profiles](https://docs.dynatrace.com/managed/analyze-explore-automate/notifications-and-alerting/alerting-profiles)
> - [Issue-tracking integration](https://docs.dynatrace.com/managed/deliver/release-monitoring/issue-tracking-integration)

## 📍 КАРТА: три страницы про доставку уведомлений

Термины темы: `Problem notification / уведомление о проблеме`, `System notification / внутреннее сообщение платформы`, `Webhook / HTTP POST от Dynatrace`, `Issue tracking / привязка проблем к тикетам и релизам`, `Custom payload / кастомный формат webhook`, `Escalation policy / правила повышения приоритета`, `ActiveGate as outbound proxy / ActiveGate как промежуточное звено для исходящих HTTP`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| System notifications (UI-уведомления) | **User menu → System notifications** | `https://guu84124.live.dynatrace.com/ui/system-notifications` |
| Problem notifications (интеграции) | **Settings → Integration → Problem notifications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications` |
| Issue-tracking integration | **Settings → Releases → Issue-tracking for releases** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:issue-tracking.integration` |

---

## 🎬 Работа с уведомлениями на трёх экранах

### Шаг 1: System notifications (уведомления в самом Dynatrace)

![System notifications: внутренние уведомления Dynatrace](screenshots/day-5/alerting-logic/system-notifications/Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/system-notifications`.

*Что видно.* Заголовок `0 Notifications`. Колонки: Received, Severity. Список пустой, на captured-тенанте нет внутренних системных сообщений.

*Что это.* Встроенная inbox Dynatrace для сообщений, которые сама платформа генерирует администратору:

- **License warnings**: «квота User Actions за месяц израсходована на 80%».
- **Tenant configuration changes**: «изменён alerting profile `prod-critical`».
- **Extension issues**: «custom extension `db-monitor` упала с ошибкой».
- **Integration failures**: «не удалось отправить уведомление в интеграцию 3 раза подряд».

*Отличие от Problem notifications.* Problem notifications: об АЛЕРТАХ ПРИЛОЖЕНИЙ (сервис упал, БД тормозит). System notifications: об АЛЕРТАХ САМОЙ ПЛАТФОРМЫ (лицензия кончается, интеграция не работает).

*Практика.* Админ тенанта должен заходить сюда раз в неделю: много информации о здоровье Managed-инсталляции. В air-gapped контексте это особенно важно: нет Mission Control, который бы предупредил сам, все такие сигналы копятся здесь.

### Шаг 2: Problem notifications (интеграции с внешними системами)

![Problem notifications: настройка интеграций](screenshots/day-5/alerting-logic/settings/builtinproblem.notifications/Problem-notifications-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications`.

Разбирался в Дне 1, Тема 10 (problems-feature). Здесь дополнительно, с упором на alerting. В air-gapped Managed движок AutomationEngine / Workflows не активен: работаем с классическими Problem notifications.

**Типы интеграций (по официальной /managed/ документации):**

- **Incident Management:** Opsgenie, VictorOps, PagerDuty, xMatters, Jira: эскалация, on-call rotation, тикеты.
- **ChatOps:** Slack, Microsoft Teams: через incoming webhook URL мессенджера.
- **Enterprise Service Management:** ServiceNow: для ITIL-процессов крупных enterprise.
- **Custom:** Email (SMTP) и Webhook (generic HTTP POST с настраиваемым JSON-payload).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/problem-notifications -->

**Когда уходят уведомления.** Push в третью сторону происходит **только при появлении (detected)** и **при разрешении (resolved)** проблемы: не на каждое обновление. Это сделано, чтобы снизить alert fatigue, но даёт сюрприз: если сервис «мерцает» без формального resolve, дополнительных нотификаций не будет.

**Для каждой интеграции настраивается:**

- **Name**: имя для идентификации.
- **URL / credentials**: куда слать.
- **Alerting profile filter**: какие проблемы покрывает (связка с Темой 7).
- **Custom payload**: опционально: кастомизировать формат сообщения (для webhook и некоторых других).

*Исходящие соединения в air-gapped контуре.* Dynatrace Cluster не может напрямую достучаться до внешних сервисов (Slack API, PagerDuty API): firewall между внутренней сетью и интернетом их блокирует.

**Решения в air-gapped:**

- **ActiveGate как proxy.** Настроить исходящие HTTP-запросы через ActiveGate, который имеет доступ наружу.
- **Internal webhook receiver.** Собственный сервис внутри сети принимает webhook от Dynatrace и пересылает наружу через разрешённые каналы.
- **Ограничиться email.** SMTP внутренний, всегда работает.

### Шаг 3: Issue-tracking for releases

![Issue-tracking for releases: интеграция с трекерами задач](screenshots/day-5/alerting-logic/settings/builtinissue-tracking.integration/Issue-tracking-for-releases-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:issue-tracking.integration`.

*Что настраивает.* Специальная интеграция, которая показывает **статистику багов и тикетов привязанных к релизу**: это не двусторонняя синхронизация Problem ↔ ticket, а получение из issue-tracker'а количества и сводки issue для конкретной версии.

**Как работает.** Dynatrace знает о релизах через метаданные сервиса (см. version detection в Дне 1, Тема 5). Для каждой версии задаётся query (с placeholder'ами `{PRODUCT}` и `{VERSION}`), который Dynatrace выполняет в issue-tracker'е и показывает результат в Release inventory: сколько open / closed багов привязано к релизу.

**Важно.** Issue-tracking integration **не создаёт тикеты сам** и **не закрывает их по resolution problem**. Автоматическое создание тикета на проблему: отдельная задача через **Problem notifications** (Шаг 2 этой темы).

**Поддерживаемые системы (5 интеграций):**

- **Jira on-premises** (Server / Data Center): через REST API + standard credentials.
- **Jira Cloud**: через REST API + OAuth/API token.
- **GitHub**: через GitHub API + token.
- **GitLab**: через GitLab API + API token.
- **ServiceNow**: фильтрация attribute-value (placeholder'ы `{PRODUCT}`/`{VERSION}` не используются).

**Лимит:** до **20 issue-tracking конфигураций**.

**Поля настройки:**

- **Issue label**, **Query** (с placeholder'ами).
- **Issue type / Target system / Target URL.**
- **Credentials** (зависит от системы: OAuth, API token или standard credentials).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/deliver/release-monitoring/issue-tracking-integration -->

*Типовой use case.* После релиза руководитель команды открывает Release inventory и видит: «версия 2.34.0: 3 open issues в Jira». Это даёт быструю обратную связь: что новый релиз ещё ловит баги, прежде чем переходить к следующему. Создание самих тикетов и автоматизация post-mortem-action items: задача Problem notifications + наружных автоматизаций (см. ниже).

---

## 🎓 ТЕОРИЯ: логика оповещений

### Когда уведомление срабатывает

Уведомление отправляется по цепочке:

1. **Davis AI обнаружил Problem** (или metric event, или availability outage).
2. **Alerting profile matched**: проблема подпадает под условия фильтра.
3. **Maintenance window check**: нет активного maintenance window для этих сущностей.
4. **Problem notification configured**: есть интеграция, привязанная к профилю.
5. **Integration healthy**: Dynatrace может достучаться до внешней системы.

Если любой шаг не выполнен: уведомление НЕ уходит.

### Дубликаты и rate limiting

По официальной документации, push в третью сторону происходит **только при detect и при resolve** проблемы: Dynatrace не дублирует нотификацию на каждое обновление статуса:

- Если проблема «мерцает» (появляется → исчезает → появляется): каждое появление это **новая Problem** с собственной парой detect / resolve, поэтому в каналах будет несколько пар уведомлений на один реальный сбой.
- Если уведомление не удалось отправить (integration unhealthy), Dynatrace делает retry: состояние интеграции отображается в System notifications (Шаг 1).

Жалобы на «дубликаты в каналах»: обычно следствие нестабильного baseline'а, из-за которого одна и та же ситуация распадается на серию мерцающих проблем.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/problem-notifications -->

### Custom payload для webhook

Для webhook-интеграций Dynatrace даёт возможность задать **кастомный JSON-payload** с подстановкой переменных:

```json
{
  "title": "{ImpactedEntity} в {State}",
  "severity": "{Severity}",
  "start_time": "{StartTime}",
  "description": "{ProblemDetailsText}",
  "link": "{ProblemURL}",
  "environment": "{Tags:environment}",
  "team": "{Tags:team}"
}
```

Доступные переменные: ImpactedEntity, State, Severity, ProblemURL, StartTime, Tags, RootCauseEntity, ImpactedEntities, ProblemDetailsText, и десятки других.

*Use case.* Организация использует корпоративный мессенджер (не Slack, не Teams). Пишется простой webhook-receiver на Python / Node: принимает Dynatrace payload, форматирует как нужно, отправляет во внутренний мессенджер.

### Escalation policies

Dynatrace сам не умеет делать escalation («если никто не взял в работу за 10 минут: эскалировать уровень выше»). Это делают специализированные on-call системы:

- **PagerDuty**: rotation schedules, L1→L2→L3 escalation, ACK от дежурного.
- **OpsGenie**: аналогично.
- **Собственная**: можно разработать свой escalation engine, который принимает webhook от Dynatrace и реализует корпоративные правила.

Dynatrace шлёт только начальное уведомление, дальше эскалация управляется внешней системой.

### Интеграция с Wiki / Confluence / Notion

Иногда команды хотят, чтобы при каждом инциденте автоматически создавалась страница в корпоративной wiki с шаблоном post-mortem. Через generic webhook:

1. Dynatrace → webhook → internal service.
2. Internal service → Wiki / Confluence / Notion API → создаёт страницу.
3. URL страницы возвращается в тикет Jira.

Логика пишется вручную, но webhook-механизм Dynatrace гибкий для любых таких цепочек.

### Integration health monitoring

Как узнать, что integration сломалась? Варианты:

- **System notifications** (первый экран темы). Dynatrace сам отметит там, что интеграция X упала.
- **Test notification button.** В настройках интеграции есть кнопка `Send test notification`: шлёт фейковый alert. Использовать регулярно для проверки живости.
- **External uptime monitoring.** Мониторить сам Dynatrace через internal synthetic: если Dynatrace не дошёл до этого monitor-а, значит лежит либо сеть, либо кластер.

### Почему `Strict firewall policy?` важен

Типовая ошибка: настроить Slack webhook и удивляться, что уведомления не приходят. Причина: firewall блокирует исходящий HTTPS к `hooks.slack.com`.

**Варианты решения:**

- Запросить у сетевой команды **исключение** для целевых хостов (`hooks.slack.com` и др.).
- Настроить через **ActiveGate as outbound proxy**: все исходящие HTTP от Cluster идут через ActiveGate в DMZ с доступом к интернету.
- Перейти на **pull-model**: внутренний сервис-poller каждые 30 секунд спрашивает Dynatrace API «есть ли новые проблемы» и сам кидает в мессенджер. Исходящее соединение инициируется изнутри сети, а не кластером Dynatrace.

### Issue tracking vs Problem notification: разница

| Признак | Problem notification | Issue tracking integration |
|---|---|---|
| Что делает | Push-уведомление в Slack/Teams/email/PagerDuty/Jira/ServiceNow/webhook | Подтягивает **статистику тикетов** из Jira/GitHub/GitLab/ServiceNow по query на конкретный релиз |
| Когда срабатывает | На detect и на resolve проблемы | По расписанию / при просмотре Release inventory |
| Создаёт тикеты? | Да, при наличии integration с trackerom (Jira / ServiceNow): но только при detect | Нет: только читает данные |
| Закрывает тикеты? | Нет | Нет |
| Лимит | По alerting profile | До 20 конфигураций на environment |

Обычно используют оба: Problem notifications: для оперативного реагирования (дежурный увидел в мессенджере → полез разбираться), issue tracking: для пост-релизной статистики (сколько багов привязано к версии 2.34.0). Двусторонняя синхронизация Problem ↔ ticket в публичной /managed/ документации не задокументирована: её нужно реализовывать вручную через webhook + внешний automation-сервис.

### AutomationEngine / Workflows, это SaaS

Dynatrace Workflows: low-code-движок автоматизации поверх Problem notifications, который позволяет цепочку «получить problem → обогатить данными → решить приоритет → триггернуть несколько действий» собирать как orchestration. **В air-gapped Managed эта функциональность не активна**: это часть Apps-платформы Dynatrace SaaS. В курсе опираемся на классические Problem notifications + кастомные webhook-receiver'ы для расширенной логики.

### Ключевые термины

- **Problem notification**: интеграция для уведомления внешней системы.
- **System notification**: внутреннее сообщение платформы Dynatrace.
- **Webhook**: HTTP POST от Dynatrace в произвольный endpoint.
- **Issue tracking integration**: привязка проблем к тикетам и релизам.
- **Custom payload**: кастомный формат webhook-сообщения.
- **Escalation policy**: правила повышения приоритета.
- **ActiveGate as outbound proxy**: ActiveGate как промежуточное звено для исходящих HTTP.
- **Strict firewall policy**: air-gapped firewall, блокирующий исходящие соединения.
