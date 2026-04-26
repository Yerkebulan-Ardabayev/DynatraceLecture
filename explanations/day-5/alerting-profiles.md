> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 7 из 10: «Настройка правил оповещения и Alerting Profiles»

## 📍 КАРТА — три страницы про алерт-правила

Термины темы: `Alerting profile / профиль алертинга`, `Event filter / фильтр события`, `Severity / серьёзность`, `Maintenance window / окно обслуживания`, `Metric event / кастомный алерт по метрике`, `Static threshold / фиксированный порог`, `Auto-adaptive / адаптивный порог`, `Alert fatigue / усталость от избытка уведомлений`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Problem alerting profiles | **Settings → Alerting → Alerting profiles** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.profile` |
| Maintenance windows | **Settings → Alerting → Maintenance windows** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.maintenance-window` |
| Metric events (кастомные алерты) | **Settings → Anomaly detection → Metric events** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.metric-events` |

---

## 🎬 Работа с алерт-настройками на трёх экранах

### Шаг 1 — Problem alerting profiles

![Problem alerting profiles — правила маршрутизации проблем](screenshots/day-5/alerting-profiles/settings/builtinalerting.profile/Problem-alerting-profiles-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.profile`.

*Что видно.* Страница настройки alerting profiles. В air-gapped Managed новая Workflows-платформа не активна — работаем с классическими alerting profiles.

*Что такое alerting profile.* Именованный набор правил — «какие проблемы в какие интеграции отправлять».

**Поля правила:**

- **Event filter** — тип события (Davis problem, metric event, availability incident и др.).
- **Severity** — Critical / Warning / Info.
- **Entity filter** — какие сущности затронуты (hosts, services, applications) через management zone или tag.
- **Delay** — минут ждать перед отправкой. Отсекает случайные всплески.
- **Send event repeatedly** — дублировать уведомления при продолжении проблемы.

**Типовой набор профилей:**

| Profile name | Условия | Интеграции |
|---|---|---|
| `prod-critical-24x7` | severity=Critical + MZ=prod | PagerDuty (on-call), мессенджер дежурных, ITSM |
| `prod-warning-hours` | severity=Warning + MZ=prod + 08:00-22:00 | Канал warnings, email prod-team |
| `dev-all-quiet` | MZ=dev | Канал dev, без email |
| `db-specific` | Entity=database_service + severity ≥ Warning | Email DBA, ITSM (DBA queue) |
| `security-appsec` | Event=vulnerability-detected + severity=Critical | Email SOC, ITSM (Security queue) |

*Порядок правил.* Если проблема подпадает под несколько профилей — отправится во все, не только в первый. Critical на prod-сервисе БД уйдёт и в `prod-critical-24x7` (дежурному через PagerDuty), и в `db-specific` (DBA через email) — разные команды по своим каналам.

### Шаг 2 — Maintenance windows

![Maintenance windows — окна технического обслуживания](screenshots/day-5/alerting-profiles/settings/builtinalerting.maintenance-window/Maintenance-windows-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.maintenance-window`.

*Что настраивает.* Периоды, когда Dynatrace либо не создаёт проблемы, либо создаёт без отправки уведомлений. Разбирали в Дне 3-4, Тема 13 — здесь дополнительные детали.

**Три режима maintenance window:**

- **Detect and alert** — нормальный режим (не maintenance window, а дефолт).
- **Detect, no alerting** — проблемы фиксируются в истории, уведомления не идут. Полезно для ночных ETL: хочется видеть проблемы постфактум, но не будить дежурных.
- **Do not detect or alert** — ничего не происходит. Полезно для plan-release, когда в ходе деплоя 5-10 минут «хаоса» — норма.

**Параметры окна:**

- **Name and description** — для документации.
- **Type** — Planned (разовое) или Recurring (повторяющееся).
- **Schedule** — дата, время, часовой пояс.
- **Scope** — какие сущности попадают: All entities, Management zone (например, prod-retail), Specific entities (выбранные hosts / services / apps).
- **Alerting mode** — один из трёх режимов выше.

**Типовые окна:**

- `quarterly-release-saturday-2-6` — Recurring, первая суббота квартала 02:00-06:00, scope=all prod, mode=Do not detect.
- `daily-backup-3-5` — Recurring, ежедневно 03:00-05:00, scope=database-services, mode=Detect no alert.
- `new-year-window` — Planned, 31 декабря 23:00 — 1 января 06:00, scope=all, mode=Detect no alert (низкий трафик + возможные glitch-и).
- `holiday-window` — Planned, праздничный день, scope=all, mode=Detect no alert (праздничный трафик, baseline смещён).

### Шаг 3 — Metric events (кастомные алерты)

![Metric events — настройка кастомных алертов по метрикам](screenshots/day-5/alerting-profiles/settings/builtinanomaly-detection.metric-events/Metric-events-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.metric-events`.

*Что видно.* Страница с заголовком `Overview of limits`. В air-gapped Managed новый Apps-интерфейс для custom alerts не активен — работаем с классическим конфигом metric events.

*Metric events — кастомный алерт по произвольной метрике.* В отличие от Davis baselining (автоматическое определение аномалий по истории), metric events — «когда метрика X превышает значение Y, создать Davis Problem».

*Типовой кейс.* Автоматические Davis baselines не покрывают специфическую бизнес-метрику. Например, в Dynatrace через Extensions идёт метрика «количество заявок на кредит за минуту». Davis её не знает — для него это просто число. Бизнес знает: если меньше 10 за минуту в рабочие часы — что-то сломано на фронтенде. Создаём metric event.

**Поля metric event:**

- **Metric selector** — какая метрика следить (`builtin:custom.loan_applications_per_minute`).
- **Dimension filters** — по каким dimensions (`mz = retail-banking`, `branch_type = online`).
- **Threshold:**
  - **Static threshold** — `< 10` или `> 100`.
  - **Auto-adaptive** — больше 3σ отклонение от недельной нормы.
- **Condition duration** — сколько времени должно держаться условие (например, 3 минуты).
- **Severity** — Critical / Warning / Info.
- **Alerting profile** — сразу привязка, в какой профиль уйдёт.

*Лимиты.* Overview of limits — счётчик использованных / доступных metric events. У Managed-лицензии обычно лимит 1000 metric events на тенант. Следить за счётчиком, чтобы не упереться.

---

## 🎓 ТЕОРИЯ — архитектура алертинга в Dynatrace

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Metric events — alerting profile scope](https://docs.dynatrace.com/docs/shortlink/metric-events)

### Полный pipeline алерта

```
Источник данных (OneAgent / RUM / Synthetic / Extensions)
  ↓ метрика
Davis AI (baseline / anomaly detection / correlation)
  ↓ Problem объект
Alerting profile filter (match условий)
  ↓ matched problem
Maintenance window check (активно ли maintenance)
  ↓ passed check
Problem notifications (интеграция Slack/Teams/Email/Jira/…)
  ↓ делает HTTP-запрос
Внешняя система (Slack / PagerDuty / ServiceNow)
```

Каждый шаг настраивается отдельно. Нарушение в любом звене → алерт не уйдёт.

### Davis AI — автоматическая детекция

Davis — AI-engine Dynatrace:

1. Считывает метрики в реальном времени.
2. Строит baseline (референсное значение) для каждой метрики автоматически за 7 дней.
3. Детектит аномалии по 3σ (стандартное отклонение).
4. Коррелирует связанные сущности. Упал сервис + упал CPU на хосте = одна проблема, не две.
5. Создаёт Problem с root cause analysis.

Davis работает **без настройки** для hosts, services, applications (встроенные baseline-правила). Кастомные бизнес-метрики требуют metric events.

### Management zone как основа фильтрации

Типовые MZ:

- `prod-retail` — розничный backend.
- `prod-corporate` — корпоративный.
- `prod-treasury` — казначейство и трейдинг.
- `prod-core` — core system (карты, счета, проводки).
- `staging` — предпрод.
- `dev` — разработка.

Alerting profile фильтрует по MZ как основному измерению. Внутри MZ — более тонкие фильтры по severity, tags, entity types.

### Alert fatigue — главная проблема

*Alert fatigue* — дежурный получает столько алертов, что перестаёт реагировать, пропускает реальные инциденты.

**Проявления:**

- В канал шлёт 50 алертов в день — дежурный их просто не читает.
- PagerDuty триггерит в 3 часа ночи 4 раза за месяц — на пятый телефон выключен.
- Email-ящик с алертами переполнен — фильтры отправляют всё в архив.

**Лечение через настройку alerting profile:**

- **Строгие severity.** Critical только для настоящих катастроф (сервис упал, деньги не идут). Warning — «что-то странное, разбирайся утром». Info — в канал-историю, без push-ей.
- **Маленький scope.** Не `MZ=prod` (слишком широко), а `MZ=prod AND tag=customer-facing` (критичное для клиентов).
- **Delay.** 3-5 минут перед первым уведомлением. Проблема «мигнула и ушла» за 90 секунд — не тревожить дежурного.
- **Grouping.** Один инцидент = одно уведомление, а не 15 штук про один и тот же сервис.

### Metric events vs Davis baselines

| Критерий | Davis baselines | Metric events |
|---|---|---|
| Настройка | Автоматическая | Ручная |
| Источник метрик | Встроенные (hosts/services/apps) | Любые, включая custom |
| Динамика | Адаптируется к истории | Строгий threshold (static) или к истории (adaptive) |
| Use case | Общий мониторинг | Конкретные бизнес-метрики |

**Рекомендация**: не заменять Davis metric-ивентами. Davis для техники, metric events для бизнеса. Техническая метрика (CPU usage, error rate, response time) — Davis справится лучше. Бизнес-метрика (loans per hour, cart abandonment rate) — нужны metric events.

### Maintenance windows как compliance-инструмент

Maintenance windows — не только удобство, но и compliance-требование:

- Казначейские операции проводятся в определённые часы (работа с валютой).
- Регуляторная отчётность отправляется в конкретное время (иначе штраф).
- Ежемесячные закрытия периодов требуют полной остановки модулей.

Все «запланированные нестабильности» должны быть записаны как maintenance windows, иначе дежурный тревожится на них каждый месяц.

### Metric events лимит 1000 — как не упереться

Лимит 1000 metric events на тенант кажется большим, но быстро исчерпывается:

- Каждый микросервис × каждая важная метрика = быстрый рост.
- 100 микросервисов × 10 метрик = уже 1000.

**Стратегии экономии:**

- **Использовать dimensions, а не отдельные metric events.** Один metric event с фильтром `service:*` сам создаёт алерты для каждого сервиса.
- **Не дублировать Davis.** Если Davis смотрит метрику — не создавать свой metric event на то же самое.
- **Периодический аудит.** Раз в квартал смотреть список metric events, удалять неактуальные.

### Alerting profiles vs Anomaly Detection settings

Важное разделение:
- **Anomaly Detection** (в разделе Settings) — **КАК** обнаруживать аномалии. Пороги для hosts CPU, для service errors, для RUM Apdex.
- **Alerting profiles** — **КОМУ** отправлять уведомления о найденных аномалиях.

Настройка anomaly detection → вы меняете частоту обнаружения (более чувствительно / менее чувствительно). Настройка alerting profile → вы меняете маршрутизацию (кому приходит уведомление).

### Ключевые термины

- **Alerting profile** — правила фильтрации и маршрутизации проблем.
- **Event filter** — тип события для фильтрации.
- **Severity** — уровень серьёзности (Critical/Warning/Info).
- **Maintenance window** — окно технического обслуживания.
- **Metric event** — кастомный алерт по метрике.
- **Static threshold** — фиксированный порог.
- **Auto-adaptive threshold** — адаптивный порог по истории.
- **Alert fatigue** — усталость от избытка уведомлений.
- **Davis baseline** — автоматический baseline от AI.
