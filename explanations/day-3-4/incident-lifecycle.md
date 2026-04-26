> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 13 из 14: «Incident Lifecycle: от детекции до Root Cause Analysis»

## 📍 КАРТА — пять страниц полного цикла инцидента

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

### Шаг 1 — Problems (детекция)

![Problems — все активные и прошлые проблемы](screenshots/day-3-4/incident-lifecycle/problems/Problems-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/problems`. Разбирался многократно. **Первый этап lifecycle** — детекция Davis AI и появление Problem.

**Фаза 1 — Детекция.** Davis обнаруживает аномалию на основе пороговых правил. Создаёт Problem с автоматически рассчитанным Severity (Critical/Warning/Info), Affected entity, Root cause (если определимо).

### Шаг 2 — Alerting profiles

![Alerting profiles — правила маршрутизации проблем](screenshots/day-3-4/incident-lifecycle/settings/builtinalerting.profile/Problem-alerting-profiles-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:alerting.profile`.

*Второй этап lifecycle.* После создания Problem Davis проверяет, под какие alerting profiles она попадает. Profile — правило «какие проблемы в какие интеграции».

**Структура профиля:**

- **Name** — `prod-high-priority`.
- **Conditions** — Severity ≥ Critical AND Management zone = prod AND Impact = Application.
- **Severity rules** — минимальный severity для срабатывания.
- **Event filters** — специфичные типы событий (slowdowns only, crashes only и др.).
- **Related integrations** — куда слать (ссылка на Problem notifications).

**Типовой набор профилей:**

- `prod-critical` — Critical на prod-сервисах → email + ServiceNow + мессенджер дежурных.
- `prod-warning` — Warnings на prod → канал тимлидов.
- `dev-any` — все проблемы на dev → dev-канал.
- `db-specific` — проблемы БД → DBA-команда отдельно.

### Шаг 3 — Maintenance windows

![Maintenance windows — окна технического обслуживания](screenshots/day-3-4/incident-lifecycle/settings/builtinalerting.maintenance-window/Maintenance-windows-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:alerting.maintenance-window`.

*Что это.* Периоды, когда Dynatrace **не создаёт проблемы** или **не отправляет уведомления**. Используется для:

- Плановых работ (релиз, бэкап, миграция).
- Праздничных периодов (в эти дни изменён baseline из-за пониженной активности).
- Известных проблемных периодов (ночные ETL, которые тормозят БД).

**Типы maintenance window:**

- **Planned** — единоразовое окно на конкретную дату и время.
- **Recurring** — периодическое (каждое воскресенье 02:00-06:00).
- **Scope** — какие сущности затрагивает (все / конкретные сервисы / хост-группы).

*Типовая практика.* Перед каждым плановым релизом создают maintenance window, чтобы не будить дежурных на «проблемы» во время деплоя.

### Шаг 4 — Problem notifications

![Problem notifications — интеграции для отправки уведомлений](screenshots/day-3-4/incident-lifecycle/settings/builtinproblem.notifications/Problem-notifications-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:problem.notifications`. Разбирался в Дне 1, Тема 10.

*Четвёртый этап lifecycle.* Problem попадает под alerting profile и отправляется в настроенные интеграции:

- Email.
- Slack / Microsoft Teams.
- Jira / ServiceNow / другие ITSM.
- PagerDuty / OpsGenie.
- Webhook для кастомной логики.

Проблема покидает Dynatrace и попадает в рабочий процесс команды.

### Шаг 5 — Issue tracking integration

![Issue tracking for releases — интеграция с трекерами задач](screenshots/day-3-4/incident-lifecycle/settings/builtinissue-tracking.integration/Issue-tracking-for-releases-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:issue-tracking.integration`.

*Что это.* Двусторонняя интеграция с трекерами задач (Jira, GitHub Issues, Azure DevOps, ServiceNow Incidents):

- При создании Problem автоматически открывается тикет в трекере (через Problem notifications).
- При изменении статуса Problem (Acknowledged / Resolved) обновляется статус тикета.
- В тикете видны обогащённые данные: affected entity, root cause, PurePath, логи.

Пятый этап lifecycle — перевод инцидента в управляемую задачу разработки или эксплуатации.

---

## 🎓 ТЕОРИЯ — полный жизненный цикл инцидента

### Шесть фаз lifecycle

1. **Detection.** Davis AI обнаруживает аномалию по anomaly detection rules. Создаётся Problem.
2. **Aggregation.** Davis объединяет связанные симптомы в одну Problem (вместо 20 отдельных алертов).
3. **Root cause identification.** Davis пытается определить первопричину. Если не может — оставляет пустым, решает инженер.
4. **Routing.** Problem matches Alerting profile. Попадает в нужные интеграции. Исключения — maintenance windows.
5. **Response.** Дежурный получает уведомление, начинает разбор. Ссылки в уведомлении ведут прямо в карточку Problem, Affected entity, Root cause, PurePath.
6. **Resolution and post-mortem.** Проблема решена, статус Closed в Dynatrace, тикет закрывается в ITSM. Опционально — post-mortem с данными Dynatrace (какие метрики изменились, какие релизы были, какая команда вовлечена).

### Практики для зрелой эксплуатации

- **Каждый сервис — в alerting profile.** Не должно быть сервиса, не mapped ни в один профиль. Иначе это «забытый» сервис, проблемы на нём не увидят.
- **Профили по командам и severity.** Отдельный профиль для каждой команды + severity. Позволяет маршрутизировать точно: проблема на retail → retail-team, а не всем.
- **Maintenance windows перед деплоями.** Регламент: за час до плановой выкатки создаётся maintenance window. Экономит ночные часы дежурных.
- **ITSM-интеграция с автосозданием.** Каждая Critical Problem → авто-тикет в ITSM. Гарантирует, что проблема не потеряется в письмах.
- **Разделение профилей по типу сигнала.** Availability drop → немедленное уведомление. Slowdown → задержка 5 минут, чтобы отделить шум.

### Air-gapped specifics

Всё работает локально. Интеграции — только с внутренними системами (внутренний Jira / ServiceNow, корпоративный мессенджер, внутренний SMTP). Внешние cloud-сервисы не задействованы.
