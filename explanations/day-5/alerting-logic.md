> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 8 из 10: «Работа с оповещениями и их логика в Dynatrace»

## 📍 КАРТА — три страницы про доставку уведомлений

Термины темы: `Problem notification / уведомление о проблеме`, `System notification / внутреннее сообщение платформы`, `Webhook / HTTP POST от Dynatrace`, `Issue tracking / привязка проблем к тикетам и релизам`, `Custom payload / кастомный формат webhook`, `Escalation policy / правила повышения приоритета`, `ActiveGate as outbound proxy / ActiveGate как промежуточное звено для исходящих HTTP`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| System notifications (UI-уведомления) | **User menu → System notifications** | `https://guu84124.live.dynatrace.com/ui/system-notifications` |
| Problem notifications (интеграции) | **Settings → Integration → Problem notifications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications` |
| Issue-tracking integration | **Settings → Releases → Issue-tracking for releases** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:issue-tracking.integration` |

---

## 🎬 Работа с уведомлениями на трёх экранах

### Шаг 1 — System notifications (уведомления в самом Dynatrace)

![System notifications — внутренние уведомления Dynatrace](screenshots/day-5/alerting-logic/system-notifications/Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/system-notifications`.

*Что видно.* Заголовок `0 Notifications`. Колонки — Received, Severity. Список пустой, на captured-тенанте нет внутренних системных сообщений.

*Что это.* Встроенная inbox Dynatrace для сообщений, которые сама платформа генерирует администратору:

- **License warnings** — «квота User Actions за месяц израсходована на 80%».
- **Tenant configuration changes** — «изменён alerting profile `prod-critical`».
- **Extension issues** — «custom extension `db-monitor` упала с ошибкой».
- **Integration failures** — «не удалось отправить уведомление в интеграцию 3 раза подряд».

*Отличие от Problem notifications.* Problem notifications — об АЛЕРТАХ ПРИЛОЖЕНИЙ (сервис упал, БД тормозит). System notifications — об АЛЕРТАХ САМОЙ ПЛАТФОРМЫ (лицензия кончается, интеграция не работает).

*Практика.* Админ тенанта должен заходить сюда раз в неделю — много информации о здоровье Managed-инсталляции. В air-gapped контексте это особенно важно: нет Mission Control, который бы предупредил сам, все такие сигналы копятся здесь.

### Шаг 2 — Problem notifications (интеграции с внешними системами)

![Problem notifications — настройка интеграций](screenshots/day-5/alerting-logic/settings/builtinproblem.notifications/Problem-notifications-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications`.

Разбирался в Дне 1, Тема 10 (problems-feature). Здесь дополнительно, с упором на alerting. В air-gapped Managed движок AutomationEngine / Workflows не активен — работаем с классическими Problem notifications.

**Типы интеграций:**

- **Email** — SMTP-уведомление на заданные адреса. Требует настройки SMTP-сервера на уровне Cluster Management Console. Обычно корпоративный Exchange или Postfix.
- **Slack / Microsoft Teams** — через incoming webhook URL. Настройка на стороне мессенджера: создать webhook в admin-панели, получить URL, вставить в Dynatrace.
- **Jira / ServiceNow / Other ITSM** — через REST API и token. Dynatrace создаёт тикет при появлении проблемы, обновляет при изменении статуса, закрывает при resolution.
- **PagerDuty / OpsGenie** — специализированные on-call системы. Триггерят дежурного по телефону или SMS согласно rotation schedule.
- **Webhook (generic)** — простой HTTP POST с JSON-payload проблемы на любой кастомный endpoint. Можно написать собственный receiver: webhook → парсинг → запись в SIEM или внутренний мессенджер.

**Для каждой интеграции настраивается:**

- **Name** — имя для идентификации.
- **URL / credentials** — куда слать.
- **Alerting profile filter** — какие проблемы покрывает (связка с Темой 7).
- **Custom payload** — опционально: кастомизировать формат сообщения (для webhook и некоторых других).

*Исходящие соединения в air-gapped контуре.* Dynatrace Cluster не может напрямую достучаться до внешних сервисов (Slack API, PagerDuty API) — firewall между внутренней сетью и интернетом их блокирует.

**Решения в air-gapped:**

- **ActiveGate как proxy.** Настроить исходящие HTTP-запросы через ActiveGate, который имеет доступ наружу.
- **Internal webhook receiver.** Собственный сервис внутри сети принимает webhook от Dynatrace и пересылает наружу через разрешённые каналы.
- **Ограничиться email.** SMTP внутренний, всегда работает.

### Шаг 3 — Issue-tracking for releases

![Issue-tracking for releases — интеграция с трекерами задач](screenshots/day-5/alerting-logic/settings/builtinissue-tracking.integration/Issue-tracking-for-releases-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:issue-tracking.integration`.

*Что настраивает.* Специальная интеграция, связывающая Dynatrace с системами трекинга задач на уровне **releases**. В отличие от Problem notifications, здесь речь не об алертах, а о **привязке багрепортов к релизам кода**.

**Как работает.** Dynatrace знает о релизах через Release API или метаданные build-сервера. Каждый сервис имеет версию. При возникновении проблемы Dynatrace может:

1. Определить, с какого релиза проблема появилась.
2. Автоматически создать тикет в Jira / ServiceNow с описанием.
3. Связать тикет с релизом в своём UI. Из карточки релиза видно все проблемы, которые он вызвал.
4. При resolution проблемы обновить статус тикета.

**Поддерживаемые системы:**

- **Jira** (Cloud, Server, Data Center) — через Jira REST API.
- **GitHub Issues** — через GitHub API.
- **Azure DevOps / Azure Boards** — через Azure DevOps REST API.
- **ServiceNow Incidents** — через ServiceNow REST API.

**Поля настройки:**

- **Integration name.**
- **Base URL** (например `https://jira.example.com`).
- **Username + API token** (для Jira Cloud — API token, не пароль).
- **Project key / target queue** — куда создавать тикеты.
- **Default issue type** — Bug, Incident, Story.

*Типовой use case.* Пост-mortem после инцидента:

1. Команда разбирает, что произошло.
2. Заводят action items: «починить retry logic», «добавить cache», «увеличить timeout».
3. Каждый action item — тикет в Jira, привязанный к исходному Dynatrace-инциденту.
4. Менеджер отслеживает на следующий sprint planning: все action items разобраны, на следующий review — все закрыты.

Issue-tracking integration автоматизирует шаг «создать тикет», сокращает ручную работу после инцидента.

---

## 🎓 ТЕОРИЯ — логика оповещений

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Metric events — условия алертов](https://docs.dynatrace.com/docs/shortlink/metric-events)

### Когда уведомление срабатывает

Уведомление отправляется по цепочке:

1. **Davis AI обнаружил Problem** (или metric event, или availability outage).
2. **Alerting profile matched** — проблема подпадает под условия фильтра.
3. **Maintenance window check** — нет активного maintenance window для этих сущностей.
4. **Problem notification configured** — есть интеграция, привязанная к профилю.
5. **Integration healthy** — Dynatrace может достучаться до внешней системы.

Если любой шаг не выполнен — уведомление НЕ уходит.

### Дубликаты и rate limiting

Каждая проблема создаёт уведомление **один раз** в самом начале. Нюансы:

- Если в alerting profile включено `Send event repeatedly` — дубликаты каждые N минут, пока проблема жива.
- Если проблема «мерцает» (появляется-исчезает-появляется) — создаются отдельные проблемы, каждая своё уведомление.
- Если уведомление не удалось отправить (integration fail) — Dynatrace делает retry до 3 раз.

Жалобы на дубликаты в каналах — обычно следствие `Send repeatedly` или плохо настроенных мерцающих проблем (нестабильный baseline).

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

Dynatrace сам не умеет делать escalation («если никто не взял в работу за 10 минут — эскалировать уровень выше»). Это делают специализированные on-call системы:

- **PagerDuty** — rotation schedules, L1→L2→L3 escalation, ACK от дежурного.
- **OpsGenie** — аналогично.
- **Собственная** — можно разработать свой escalation engine, который принимает webhook от Dynatrace и реализует корпоративные правила.

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
- **Test notification button.** В настройках интеграции есть кнопка `Send test notification` — шлёт фейковый alert. Использовать регулярно для проверки живости.
- **External uptime monitoring.** Мониторить сам Dynatrace через internal synthetic — если Dynatrace не дошёл до этого monitor-а, значит лежит либо сеть, либо кластер.

### Почему `Strict firewall policy?` важен

Типовая ошибка: настроить Slack webhook и удивляться, что уведомления не приходят. Причина — firewall блокирует исходящий HTTPS к `hooks.slack.com`.

**Варианты решения:**

- Запросить у сетевой команды **исключение** для целевых хостов (`hooks.slack.com` и др.).
- Настроить через **ActiveGate as outbound proxy** — все исходящие HTTP от Cluster идут через ActiveGate в DMZ с доступом к интернету.
- Перейти на **pull-model** — внутренний сервис-poller каждые 30 секунд спрашивает Dynatrace API «есть ли новые проблемы» и сам кидает в мессенджер. Исходящее соединение инициируется изнутри сети, а не кластером Dynatrace.

### Issue tracking vs Problem notification — разница

| Признак | Problem notification | Issue tracking |
|---|---|---|
| Когда срабатывает | На любую Problem | На Problem с указанием затрагиваемого release |
| Что делает | Шлёт уведомление в Slack/Teams/email | Создаёт тикет в Jira/ServiceNow, связывает с release |
| Зачем | Дежурный узнал | Тикет есть для работы, трекинг |
| Дубликаты | Возможны (alerting profile logic) | Нет (один Problem → один тикет) |
| Life cycle | Не отслеживает закрытие тикета | Синхронизирует статус с статусом Problem |

Обычно используют оба: notification-канал для оперативного реагирования (дежурный увидел в мессенджере → полез разбираться), issue tracking — для систематизации работы (пост-инцидентный тикет в Jira → tracked до закрытия).

### AutomationEngine / Workflows — новая модель

**Dynatrace Workflows** — low-code движок автоматизации поверх классического Problem notifications. Вместо простого «получить problem → отправить webhook» можно:

- Получить problem → обогатить данными из CMDB → проверить business impact → решить приоритет → если Critical — триггернуть PagerDuty + открыть тикет в Jira + записать в аудит-лог. Всё в одном workflow.

*В air-gapped Managed Workflows доступны НЕ ВЕЗДЕ* — это часть новой Apps-платформы. В курсе опираемся на классические Problem notifications.

### Ключевые термины

- **Problem notification** — интеграция для уведомления внешней системы.
- **System notification** — внутреннее сообщение платформы Dynatrace.
- **Webhook** — HTTP POST от Dynatrace в произвольный endpoint.
- **Issue tracking integration** — привязка проблем к тикетам и релизам.
- **Custom payload** — кастомный формат webhook-сообщения.
- **Escalation policy** — правила повышения приоритета.
- **ActiveGate as outbound proxy** — ActiveGate как промежуточное звено для исходящих HTTP.
- **Strict firewall policy** — air-gapped firewall, блокирующий исходящие соединения.
