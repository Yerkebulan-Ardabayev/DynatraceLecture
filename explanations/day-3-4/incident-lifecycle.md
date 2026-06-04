> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 13 из 14: «Incident Lifecycle: от детекции до Root Cause Analysis»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/problems -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [Problem alerting profiles: Managed](https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/alerting-profiles)
- [Maintenance windows: Managed](https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/maintenance-windows)
- [Problem notifications: Managed](https://docs.dynatrace.com/managed/analyze-explore-automate/notifications-and-alerting/problem-notifications)
- [Jira integration for problem notifications](https://docs.dynatrace.com/managed/analyze-explore-automate/notifications-and-alerting/problem-notifications/jira-integration)
- [Issue-tracking integration for releases](https://docs.dynatrace.com/managed/deliver/release-monitoring/issue-tracking-integration)

## 📍 КАРТА: пять страниц полного цикла инцидента

Термины темы: `Problem / проблема / инцидент`, `Alerting profile / профиль алертинга`, `Maintenance window / окно обслуживания`, `Problem notification / уведомление о проблеме`, `ITSM / IT Service Management` (Jira, ServiceNow), `Post-mortem / разбор инцидента после закрытия`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Problems (точка детекции) | **Observe and explore → Problems** | `https://guu84124.live.dynatrace.com/ui/problems` |
| Alerting profiles | **Settings → Alerting → Alerting profiles** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.profile` |
| Maintenance windows | **Settings → Alerting → Maintenance windows** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.maintenance-window` |
| Problem notifications | **Settings → Integration → Problem notifications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications` |
| Issue tracking integration | **Settings → Releases → Issue-tracking for releases** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:issue-tracking.integration` |

---

## 🎬 Работа с жизненным циклом инцидента на пяти экранах

### Шаг 1: Problems (детекция)

![Problems: все активные и прошлые проблемы](screenshots/day-3-4/incident-lifecycle/problems/Problems-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/problems`. **Первый этап lifecycle**: детекция Davis AI и появление Problem.

На captured-экране демо-тенанта счётчик в заголовке читается как **71 Problems showing 50**: всего 71 проблема под текущим фильтром, в списке показаны первые 50. Пустой список означает, что активных проблем нет, а не что мониторинг выключен.

**Фаза 1: Детекция.** ЕСЛИ Davis обнаружил аномалию по anomaly detection rules (правила обнаружения аномалий, пороговые или авто-адаптивные baseline) → ТО на этом экране появляется новая Problem с автоматически рассчитанным Severity (Critical/Warning/Info), полем Affected entity (затронутая сущность) и Root cause (корневая причина, если определима). ЕСЛИ аномалии нет → ТО Davis молчит, новой строки не появляется.

### Шаг 2: Alerting profiles

![Alerting profiles: правила маршрутизации проблем](screenshots/day-3-4/incident-lifecycle/settings/builtinalerting.profile/Problem-alerting-profiles-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:alerting.profile`.

*Второй этап lifecycle.* После создания Problem Davis проверяет, под какие alerting profiles она попадает. Profile: правило «какие проблемы в какие интеграции».

**Структура профиля по документации Managed.** Scope складывается из трёх блоков, объединённых по AND:

- **Management zone**: ограничивает профиль конкретной зоной видимости.
- **Severity rules**: фильтр по уровню severity, длительности проблемы и тегам entity. До **100 правил** в профиле, между ними OR.
- **Event filters**: фильтр по типу события (predefined или custom). До **20 правил** в профиле; среди них negated combine с AND, non-negated с OR, два набора потом объединяются по AND.

В каждом окружении есть **default-профиль**, его нельзя удалить. Свои профили создают для команд и интеграций.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/alerting-profiles -->

**Типовой набор профилей:**

- `prod-critical`: Critical на prod-сервисах → email + ServiceNow + мессенджер дежурных.
- `prod-warning`: Warnings на prod → канал тимлидов.
- `dev-any`: все проблемы на dev → dev-канал.
- `db-specific`: проблемы БД → DBA-команда отдельно.

### Шаг 3: Maintenance windows

![Maintenance windows: окна технического обслуживания](screenshots/day-3-4/incident-lifecycle/settings/builtinalerting.maintenance-window/Maintenance-windows-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:alerting.maintenance-window`.

*Что это.* Периоды, когда Dynatrace **не создаёт проблемы** или **не отправляет уведомления** (две независимые опции: `Suppress problem detection` и `Suppress alerting`). Используется для:

- Плановых работ (релиз, бэкап, миграция).
- Праздничных периодов (в эти дни изменён baseline из-за пониженной активности).
- Известных проблемных периодов (ночные ETL, которые тормозят БД).

**Типы maintenance window по документации Managed:**

- **Planned**: задаётся заранее, поддерживает recurrence (one-time, daily, weekly, monthly) c указанием таймзоны.
- **Unplanned**: создаётся пост-фактум для уже произошедшего сбоя, чтобы он не уходил в baseline.
- **Scope**: какие сущности затрагивает (всё окружение / management zone / конкретные entity).

Лимит: до **2000 окон** на окружение. Maintenance-периоды дополнительно исключаются из расчёта baseline, чтобы load testing или плановый рестарт не «учили» Davis ложным паттернам.

*Типовая практика.* Перед каждым плановым релизом создают maintenance window, чтобы не будить дежурных на «проблемы» во время деплоя.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/maintenance-windows -->

### Шаг 4: Problem notifications

![Problem notifications: интеграции для отправки уведомлений](screenshots/day-3-4/incident-lifecycle/settings/builtinproblem.notifications/Problem-notifications-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:problem.notifications`. Разбирался в Дне 1, Тема 10.

*Четвёртый этап lifecycle.* Problem попадает под alerting profile и отправляется в настроенные интеграции. По документации Managed доступны:

- **Incident management:** Opsgenie, PagerDuty, VictorOps, xMatters, Jira.
- **ChatOps:** Slack, Microsoft Teams.
- **Enterprise Service Management:** ServiceNow.
- **Custom:** Email и Webhook для всего остального.

Проблема покидает Dynatrace и попадает в рабочий процесс команды. Уведомления уходят только в момент **создания** и **закрытия** проблемы, это намеренно, чтобы не флудить промежуточными апдейтами.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/analyze-explore-automate/notifications-and-alerting/problem-notifications -->

### Шаг 5: Issue tracking integration

![Issue tracking for releases: интеграция с трекерами задач](screenshots/day-3-4/incident-lifecycle/settings/builtinissue-tracking.integration/Issue-tracking-for-releases-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:issue-tracking.integration`.

*Что это.* **Issue-tracking integration for releases**: это **не** канал автотикетинга. Это привязка трекера задач к Release inventory: каждый монитоируемый сервис связывается со статистикой багов в Jira / GitHub / GitLab / ServiceNow по динамическому запросу (например, JQL `project = RETAIL AND fixVersion = {VERSION}`). Цель: увидеть прямо в Release inventory число открытых/закрытых тикетов на конкретный релиз продукта. Лимит: до **20 issue-tracking конфигураций** на окружение.

Автоматическое создание тикета на Problem, это другая интеграция, **Problem notifications → Jira** (Шаг 4). При этом Dynatrace **не закрывает Jira-тикеты** автоматически после resolve проблемы: закрывать тикет нужно вручную в Jira или через свой workflow.

Пятый этап lifecycle: перевод инцидента в управляемую задачу разработки или эксплуатации; Release-привязка отдельно показывает, какой релиз скорее всего инициировал проблему.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/deliver/release-monitoring/issue-tracking-integration -->
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/analyze-explore-automate/notifications-and-alerting/problem-notifications/jira-integration -->

---

## 🎓 ТЕОРИЯ: полный жизненный цикл инцидента

### Шесть фаз lifecycle

1. **Detection.** Davis AI обнаруживает аномалию по anomaly detection rules. Создаётся Problem.
2. **Aggregation.** Davis объединяет связанные симптомы в одну Problem (вместо 20 отдельных алертов).
3. **Root cause identification.** Davis пытается определить первопричину. Если не может: оставляет пустым, решает инженер.
4. **Routing.** Problem matches Alerting profile. Попадает в нужные интеграции. Исключения: maintenance windows.
5. **Response.** Дежурный получает уведомление, начинает разбор. Ссылки в уведомлении ведут прямо в карточку Problem, Affected entity, Root cause, PurePath.
6. **Resolution and post-mortem.** Проблема решена, статус Closed в Dynatrace, тикет закрывается в ITSM. Опционально: post-mortem с данными Dynatrace (какие метрики изменились, какие релизы были, какая команда вовлечена).

### Практики для зрелой эксплуатации

- **Каждый сервис: в alerting profile.** Не должно быть сервиса, не mapped ни в один профиль. Иначе это «забытый» сервис, проблемы на нём не увидят.
- **Профили по командам и severity.** Отдельный профиль для каждой команды + severity. Позволяет маршрутизировать точно: проблема на retail → retail-team, а не всем.
- **Maintenance windows перед деплоями.** Регламент: за час до плановой выкатки создаётся maintenance window. Экономит ночные часы дежурных.
- **ITSM-интеграция с автосозданием.** Каждая Critical Problem → авто-тикет в ITSM через Problem notifications. Закрытие тикета остаётся ручным процессом или автоматизируется через ITSM-workflow со стороны заказчика.
- **Разделение профилей по типу сигнала.** Availability drop → немедленное уведомление. Slowdown → задержка 5 минут, чтобы отделить шум.

### Air-gapped specifics

Всё работает локально. Интеграции: только с внутренними системами (внутренний Jira / ServiceNow, корпоративный мессенджер, внутренний SMTP). Внешние cloud-сервисы не задействованы.
