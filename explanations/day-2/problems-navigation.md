> 📅 **День 2: Инфраструктура, контейнеры, базы данных, сети** → Тема 9 из 9: «Переход к сервисам и хостам из карточки Problems»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/problems -->
>
> 🔖 **Редакция от 2026-04-27.** Все тех-факты сверены свежими WebFetch'ами на `docs.dynatrace.com/managed/` в текущей сессии. Ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Welcome to Dynatrace Managed](https://docs.dynatrace.com/managed) — корневая страница Managed Docs
> - [Davis AI — Managed](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai) — Davis AI causation engine: anomaly detection / root cause analysis / problem retracing
> - [Anomaly detection — Managed](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai/anomaly-detection) — auto-adaptive / static thresholds / sensitivity, contextual baselining
> - [Root cause analysis — Managed](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai/root-cause-analysis) — RCA автоматически выделяет entities в causal topology
> - [Root cause analysis — concepts — Managed](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts) — Affected vs Root cause, causal topology, vertical/horizontal зависимости
> - [Event analysis and correlation — Managed](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts/events) — ingestion / normalization / topology / dedup (by source / over time / by causal relationship)
> - [Problem alerting profiles — Managed](https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/alerting-profiles) — Default profile нельзя удалить; AND-логика трёх scope: Management zones + Severity rules (≤100, OR) + Event filters (≤20)
> - [Alerting rules evaluation — Managed](https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/alerting-profiles/alerting-rules-evaluation) — AND-логика scope, OR между severity rules

## 📍 КАРТА — откуда стартует расследование инцидента

Термины темы: `Problem / проблема / инцидент`, `Affected entity / затронутая сущность / где болит`, `Root cause / корневая причина / где чинить`, `Davis AI / Davis / движок автоматического анализа`, `Alerting profile / профиль алертинга`.

Тема не о самой странице Problems (разобрана в Дне 1, Тема 10), а о том, **как из карточки проблемы быстро провалиться в затронутые сущности** — сервис, хост, процесс, БД, приложение. Это основной путь работы дежурного инженера.

| Точка входа | Путь в меню | Прямая ссылка |
|---|---|---|
| Список всех проблем | **Observe and explore → Problems** | `https://guu84124.live.dynatrace.com/ui/problems` |
| Карточка одной проблемы | Клик по строке в списке | `https://guu84124.live.dynatrace.com/ui/problems/<P-NNNNNNNN>` |

**Два ключевых направления навигации из Problems:**

| Направление | Куда ведёт | Когда используем |
|---|---|---|
| **Affected entity** (затронутая сущность) | В карточку сервиса / хоста / приложения / базы, где зафиксирована деградация | Сразу при старте расследования, чтобы увидеть метрики самой больной сущности |
| **Root cause** (корневая причина) | В карточку сущности, которую Davis AI считает первопричиной | Когда нужно понять «где чинить», а не «где болит» |

---

## 🎬 Работа с навигацией из Problems на одном экране тенанта

### Шаг 1 — Список Problems и переходы в затронутые сущности

![Problems — список проблем с колонками Impacted, Affected, Root cause, Alerting profiles](screenshots/day-2/problems-navigation/problems/Problems-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Observe and explore → Problems**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/problems`.

На captured-экране **71 активная проблема, в списке показано 50**. Это реальные продолжающиеся инциденты демо-тенанта, на них удобно проходить путь «проблема → корневая причина → сущность → метрика».

Примеры из списка. Первая строка — `Http monitor local outage P-26049005: Availability`. Affected: `easytravel storebooking`. Root cause: `EasytravelService`. Началась 21 апреля в 11:11, длится 10 минут. Вторая — `Postgres Availability P-26049003`, Affected — AWS RDS-инстанс `pg-16-dynatrace-demo.ckhuiwsqmnv8.us-east-1.rds.amazonaws.com:5432`, длится 16 минут. Каждая запись — потенциальная точка входа в расследование.

**Колонки для навигации:**

- **Problem** — заголовок и идентификатор `P-NNNNNNNN`.
- **Impacted** — количество затронутых сущностей.
- **Affected** — главная затронутая сущность. Кликабельна, ведёт в карточку сущности в обход карточки проблемы.
- **Root cause** — первопричина по Davis AI. Кликабельна, ведёт в карточку первопричины.
- **Alerting profiles** — сработавшие профили. Видно, в какие интеграции проблема уже ушла. На скриншоте: `ServiceNow Default Problem Notification Profile`, `ServiceNow Default Problem Notification - ven07742 Profile`, `Default`.

**Два сценария перехода из списка:**

- **Клик по строке** (любая область, кроме ссылок Affected / Root cause). Открывает карточку проблемы: хронология событий, граф сущностей, рассуждение Davis AI о корневой причине, связанные логи и трейсы. Путь для вдумчивого разбора.

- **Клик на имени в Affected или Root cause**. Открывает карточку сущности (сервис / хост / приложение / БД), минуя карточку проблемы. Путь «быстро посмотреть метрики этой сущности» без погружения в аналитику Davis.

### Шаг 2 — Карточка проблемы и прыжок в затронутые объекты

Карточка проблемы открывается по клику на строку. Это не отдельная страница, а часть механики Problems, но именно отсюда идут все целевые прыжки.

**Структура карточки по зонам:**

- **Верх** — имя, идентификатор, статус (Open / Closed), длительность, кнопка Acknowledge.
- **Центр** — граф затронутых сущностей. Узлы — сервисы, процессы, хосты, БД. Связи — вызовы между ними. Раскраска: красные — реально пострадавшие, жёлтые — затронутые, зелёные — соседние без нарушений.
- **Низ** — лента событий: когда и какая аномалия была добавлена, с ссылками на графики.

**Четыре типа прыжков:**

- **Клик по узлу в графе** → карточка сущности. Сервис: Service flow, Top requests, Top backend calls. Хост: CPU / Memory / Disk / Network, список процессов, связанные сервисы. Самый частый путь: инженер видит в графе виноватую БД, кликает, попадает в метрики подключений.

- **Прыжок в метрику из ленты**. Записи типа `Response time degraded on X` или `Error rate increased on Y` имеют ссылку `View in charts` или раскрывают миниатюру графика. Оттуда — в Data Explorer с заполненной метрикой и фильтром по сущности.

- **Прыжок в PurePath (трейс)**. Если замедление сервиса, блок `Distributed Traces` ведёт к конкретным медленным запросам. Открывается PurePath — трассировка одного запроса сквозь все участвующие сервисы, БД и внешние вызовы.

- **Прыжок в логи**. Если на затронутой сущности включен Log Monitoring и проблема связана с ошибками, блок `Logs` ведёт в `/ui/logs-events` с уже применённым фильтром по времени и сущности.

### Шаг 3 — Типичные маршруты расследования

Пять сценариев, которые стоит уметь проходить без подсказки.

**Жалобы на интернет-банк.** Точка входа: Problems, фильтр `Impact level = Application`. Все активные проблемы, влияющие на пользователей. Клик на Affected первой проблемы → карточка приложения. Смотрим Apdex, число активных пользователей, распределение ошибок. Если проблема в backend — возврат в карточку, граф сущностей, красный узел сервиса, клик. В карточке сервиса смотрим Response time, drilldown в медленный endpoint, оттуда в PurePath.

**Алерт о БД.** Точка входа: письмо или Slack с номером Problem ID. Копируем идентификатор, вставляем в поиск Problems. Открывается карточка → клик на Affected → карточка БД. Видно, что происходит: растёт время ответа, кончаются соединения, появились ошибки. Если картина не ясна — назад в карточку, смотрим Root cause. Davis может указать на хост БД (проблема на уровне ОС) или на клиентский сервис (виноват запрос приложения, не БД).

**Multiple infrastructure problems.** Агрегированная проблема — Davis заметил несколько связанных инфраструктурных проблем одновременно. В графе — несколько затронутых хостов и связи между ними. По цепочке host → process → service определяем: это один сервис (локализуем) или несколько (ищем общую причину — сеть, гипервизор, storage).

**Проблемы после релиза.** Точка входа: Problems + фильтр по времени (последние два часа после выкатки). Хронология появления. Клик в каждую → затронутый сервис → блок Release events, проверка — обновлялся ли сервис в это время. По цепочке можно сказать предметно: «проблема из-за релиза сервиса X, версия такая-то».

**Ревью open problems в конце смены.** Проход по списку в статусе Open, клик в каждую, проверка Affected / Root cause / длительности. Устаревшие или ложные закрываются (Acknowledge → комментарий → вручную). Остальные — эскалация следующей смене с резюме.

---

## 🎓 ТЕОРИЯ — почему навигация из Problems построена именно так

**Проблема как контекст.** Проблема в Dynatrace — это не уведомление, а структурированный объект. В нём ссылки на все затронутые сущности, их связи и история. Карточка — контекстный хаб. Все инструменты (метрики, трейсы, логи) привязаны к нему. Переход между ними идёт через проблему, не через глобальный поиск. Инженер не ищет «какие сервисы пострадали» — видит их список в карточке.

**Отличие от классического мониторинга.** В классической схеме каждая метрика даёт свой алерт, оператор склеивает их руками. При серьёзном инциденте приходят десятки писем, большая часть времени уходит на «склейку». Davis AI делает это автоматически в момент обнаружения. Оператор получает один объект с полной картиной.

**Affected vs Root cause.** Не путать.

- **Affected** — «где болит». Сущность, на которой наблюдается деградация. Пользователь видит её симптомы.
- **Root cause** — «где чинить». Сущность, породившая деградацию. Её восстановление вернёт всех зависимых.

В простых случаях совпадают (проблема локальна). В сложных различаются: Affected — сервис платежей, Root cause — хост, на котором живёт БД, используемая этим сервисом. Причину ищут в Root cause, эффект — в Affected.

Davis для определения Root cause использует **context-aware** подход (а не простую корреляцию по времени): применяет всю доступную топологию, distributed traces и code-level информацию, чтобы связать события одного и того же корня в одну Problem. Анализируются и **вертикальные** (application → service → process → host), и **горизонтальные** (service ↔ service) зависимости; влияние ранжируется по силе. Дословно из Managed-документации: «detects interdependent Davis events across time, processes, hosts, services, applications, and both vertical and horizontal topological monitoring perspectives». <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai/root-cause-analysis/concepts -->

**Когда Davis не смог определить Root cause.** Колонка остаётся пустой. Это не ошибка, а честное «недостаточно данных». В таких случаях инженер опирается на граф сущностей и определяет причину экспертно. Обычно это проблемы на инфраструктуре без OneAgent (чистое сетевое железо, внешние SaaS) или новые технологии без накопленного baseline.

**Alerting profiles в списке.** Колонка функциональная, не декоративная. Видно, в какие интеграции (Email / Jira / ServiceNow / Slack / Opsgenie / PagerDuty / Teams) ушла проблема. Профиль фильтрует problems по трём scope-компонентам, объединённым AND: Management zones + Severity rules (до 100, между ними OR) + Event filters (до 20). Каждое окружение содержит неудаляемый профиль `Default`. Если проблема критичная, а Alerting profiles пусто — она не попала ни в одну интеграцию, дежурный о ней не знает. Ревью: фильтр «высокий Impact level + пустые Alerting profiles» → разобраться, почему не рассылается. <!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe-and-explore/notifications-and-alerting/alerting-profiles -->

**Air-gapped контекст.** Workflow одинаков в облачном Dynatrace и в изолированном Managed. Данные переходов полностью локальные, наружу ничего не уходит. Если интеграция уведомлений настроена на внутренний Jira или Slack — Alerting profiles шлют туда, переход из письма/чата в интерфейс Dynatrace идёт по внутренней ссылке.
