> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 9 из 10: «USQL / DQL: запросы, возможности, ограничения»

## 📍 КАРТА — одна страница, два языка

Термины темы: `USQL / User Session Query Language` (SQL-подобный для сессий и actions в Managed), `DQL / Dynatrace Query Language` (pipeline-язык SaaS для Grail, **в Managed недоступен**), `Grail / облачное хранилище SaaS`, `usersession / виртуальная таблица сессий`, `useraction / виртуальная таблица действий`, `Funnel function / встроенная функция построения воронки`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User session query (USQL) | **Application Observability → Frontend → User sessions query** | `https://guu84124.live.dynatrace.com/ui/user-sessions/query` |

---

## 🎬 Работа с USQL на одном экране

### Шаг 1 — User Session Query editor

![User Session Query — редактор USQL](screenshots/day-5/usql/user-sessions/query/User-Session-Query-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/query`.

**Что здесь видно.** Страница с заголовком `Run a query to view results` и двумя действиями: `Run query`, `Copy`. Центральная часть страницы — текстовый редактор для написания USQL.

**Как показать клиенту.** Вводим простой запрос, нажимаем Run query, получаем результат в табличном виде.

Пример первой демонстрации:
```sql
SELECT
  userExperienceScore,
  count(*) AS sessions
FROM usersession
GROUP BY userExperienceScore;
```

Результат:
| userExperienceScore | sessions |
|---|---|
| SATISFIED | 203 |
| TOLERATING | 52 |
| FRUSTRATED | 23 |

Apdex получается: (203 + 0.5 × 52) / 278 = 0.824. То же самое, что платформа показывает в карточке приложения. Теперь мы сами получили его SQL-запросом — можем комбинировать как хотим.

**Разбивка по странам:**
```sql
SELECT
  country,
  count(*) AS sessions,
  avg(totalErrorCount) AS avg_errors
FROM usersession
WHERE startTime > now() - 7d
GROUP BY country
ORDER BY sessions DESC
LIMIT 20;
```

Топ-20 стран по количеству сессий со средним числом ошибок. Полезно для поиска региональных проблем — из определённого региона больше ошибок → возможно проблема с локальным провайдером.

**Поиск конкретных сессий с ошибками:**
```sql
SELECT
  userId,
  startTime,
  userActionCount,
  totalErrorCount,
  duration
FROM usersession
WHERE totalErrorCount > 5
  AND applicationId = 'APPLICATION-ABCDEF123456'
  AND startTime > now() - 1h
ORDER BY totalErrorCount DESC
LIMIT 50;
```

Список самых проблемных сессий за час — каждую можно открыть в Session Replay (если запись доступна) и посмотреть, что шло не так.

---

## 🎓 ТЕОРИЯ — USQL, DQL и связь с другими языками

### USQL — User Session Query Language

USQL — SQL-подобный язык для запросов по пользовательским сессиям и user actions. Создан Dynatrace в 2016 году, когда формировалась RUM-функциональность.

**Синтаксис близок к SQL**, но ориентирован на одну большую виртуальную таблицу `usersession` (и `useraction` для детального уровня):

```sql
SELECT <columns>
FROM {usersession | useraction}
WHERE <conditions>
GROUP BY <columns>
ORDER BY <columns>
LIMIT <n>;
```

**Особенности USQL:**

- **FROM только `usersession` или `useraction`.** Нет join-ов, нет других таблиц. Всё в одной виртуальной «таблице» сессий или действий.
- **Нет JOIN, UNION, subquery** — язык намеренно упрощён.
- **Специальные функции:**
  - `matchesUserActionName(useraction, 'Click on ...')` — проверка имени действия.
  - `IF(condition, value_if_true, value_if_false)` — условный оператор.
  - `funnel(step1, ..., stepN)` — построение воронки встроенной функцией.
  - `topValues(column, N)` — топ-N значений.
- **Ограничения ресурсов.** Квота по времени (обычно 30 сек) и по объёму (обычно 10 000 сессий).

**Доступ к USQL:**

- Через UI (разобрано в Шаге 1).
- Через Dynatrace API endpoint `/api/v1/userSessionQueryLanguage/table` — вызов из скриптов, дашбордов, BI-инструментов.
- Через Data Explorer — часть USQL-запросов встраивается как tile в dashboard.

### DQL — Dynatrace Query Language

DQL — новый язык, появившийся в 2022 году для работы с **Grail**, облачным хранилищем Dynatrace. Синтаксис совершенно другой — pipeline-based, как в Splunk SPL или Kusto.

Пример DQL:
```
fetch logs
| filter status == "ERROR"
| filter dt.entity.service == "payment-service"
| summarize count=count() by bin(timestamp, 1h)
| sort timestamp asc
```

**Ключевые отличия от USQL:**

- **Pipeline-синтаксис** — `|` разделяет шаги обработки.
- **Работает не только с сессиями** — со всей телеметрией: logs, metrics, spans, events, problems.
- **Нативная поддержка временных рядов** — binning, rolling windows.
- **Богатые аналитические функции** — percentiles, distinct counts, complex aggregations.
- **Требует Grail storage** — облачное хранилище с parquet-форматом. В Managed **его нет**.

### ⚠️ DQL и Grail в air-gapped Managed

**Важно.** Grail — архитектурное решение SaaS-платформы Dynatrace. В текущих релизах Managed он **не доступен**, соответственно **DQL тоже не работает** в air-gapped Managed-контуре.

Типовой вопрос слушателей: «почему у нас нет Grail / DQL, когда в документации они везде?». Ответ: документация Dynatrace ориентирована прежде всего на SaaS-платформу, а Managed — отдельный продукт с собственным циклом релизов. Сроки появления Grail и DQL в Managed в публичных roadmap Dynatrace не зафиксированы, поэтому закладываться на них в проектировании нельзя.

*В учебном плане* мы не показываем DQL напрямую, но упоминаем как «новая модель запросов, используемая в SaaS». Для текущего Managed-контура инструменты анализа — Metrics Selector, USQL и UI-фильтры логов.

### Синтаксис USQL детально

**SELECT columns:**
- `*` — все колонки (не рекомендуется, 50+ колонок).
- Конкретные поля: `userId`, `startTime`, `duration`, `applicationId`, `applicationType`, `country`, `city`, `browserFamily`, `browserMajorVersion`, `osFamily`, `osVersion`, `userActionCount`, `totalErrorCount`, `userExperienceScore`, `useragent`, `ip`, …

**Агрегации:**
- `count(*)`, `count(distinct userId)`.
- `avg(column)`, `sum(column)`, `min/max(column)`.
- `percentile(column, 95)` — 95-й перцентиль.

**WHERE filters:**
- Сравнения: `>`, `<`, `=`, `!=`, `IN (...)`, `LIKE '%pattern%'`.
- Дата/время: `now() - 1d`, `now() - 1h`, фиксированные timestamp'ы.
- Boolean: `AND`, `OR`, `NOT`.

**Funnel-функция:**
```sql
SELECT funnel(
  useraction.name = "Load of /",
  useraction.name = "Click on Login",
  useraction.name = "Load of /dashboard",
  useraction.name = "Click on New Transfer",
  useraction.name = "Load of /transfer/confirm"
) AS transfer_funnel
FROM usersession;
```

Возвращает массив с количеством сессий на каждом шаге.

### Когда USQL полезен

**Операционная аналитика.** Сложные вопросы, на которые UI-дашборды не отвечают:

- «Сколько сессий VIP-клиентов закончились rage click в прошлом месяце?»
- «Какая разбивка по версиям мобильного приложения среди проблемных сессий?»
- «В каких локациях больше 5% сессий с network error?»

**Ad-hoc расследования.** После инцидента — какие пользователи затронуты, какие сценарии ломались, откуда они подключались.

**Custom-метрики для дашбордов.** USQL-запрос встраивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversion rate по конкретному региону).

**Интеграция с внешним BI.** Скрипт, еженедельно запускающий USQL через API и складывающий результаты в корпоративный data warehouse (Vertica, ClickHouse), далее стратегические дашборды в Power BI / Tableau.

### Когда USQL не подходит

- **Логи приложений.** USQL про сессии и actions, не про логи. Для логов — Logs UI в Dynatrace (или DQL в SaaS).
- **Метрики сервисов.** USQL не работает с `builtin:service.*` метриками. Для них — Data Explorer / Metrics API.
- **Трейсы.** USQL не видит PurePath-данные на уровне backend. Для трейсов — dedicated API или Distributed Tracing.
- **Долгосрочные тренды.** По умолчанию USQL держит данные 35 дней. Старше — нет. Для долгосрочного хранения — экспорт в Elasticsearch / S3.

### Альтернативы — куда смотреть для других типов данных

- **Метрики инфраструктуры и сервисов** — Data Explorer (разбирался в Дне 1, Тема 8) или Metrics API.
- **Логи** — Log Management в Dynatrace, тоже через отдельный UI. В air-gapped Managed это отдельный модуль лицензии.
- **PurePath / Traces** — Distributed Tracing UI или API.
- **Конфигурация / Settings** — Configuration API.

USQL — специализированный инструмент для одного домена (RUM-сессии), не универсальный.

### Типичные ошибки новичков

- **Забыть `WHERE startTime > now() - N`.** По умолчанию USQL смотрит «всё, что есть» — занимает минуты или даёт timeout. Всегда ограничивать время.
- **Использовать `SELECT *`.** Получает 50+ колонок, ломает UI-таблицу, тратит квоту объёма.
- **Забыть `LIMIT`.** USQL отдаст столько, сколько сможет (до квоты), UI может повиснуть на рендеринге.
- **Путать FROM.** `FROM usersession` — одна строка на сессию. `FROM useraction` — одна строка на действие (много строк на сессию). Разные структуры, разные колонки.
- **Путать синтаксис `country = 'KZ'` vs `usersession.country = 'KZ'`.** В usersession — без префикса. В useraction — иногда нужен префикс `usersession.country`.

### API-экспорт USQL

Для интеграции с внешними системами — API:
```
POST /api/v1/userSessionQueryLanguage/table
Content-Type: application/json
Authorization: Api-Token dt0c01.ABC...

{
  "query": "SELECT userId, count(*) FROM usersession WHERE country = 'KZ' GROUP BY userId",
  "startTimestamp": 1700000000000,
  "endTimestamp": 1700086400000
}
```

Ответ:
```json
{
  "extrapolationLevel": 1,
  "columnNames": ["userId", "count"],
  "values": [
    ["user-id-123", 45],
    ["user-id-456", 32],
    ...
  ]
}
```

Это тот же USQL, но доступный из любого скрипта. Можно запускать из cron, складывать в корпоративный data lake, генерировать отчёты.

### Ключевые термины

- **USQL** — User Session Query Language, SQL-подобный, для сессий и actions.
- **DQL** — Dynatrace Query Language, новый pipeline-язык для Grail.
- **Grail** — облачное хранилище всей телеметрии, пока только в SaaS.
- **Funnel function** — встроенная функция USQL для построения funnel.
- **usersession** — виртуальная таблица сессий.
- **useraction** — виртуальная таблица действий.
- **Extrapolation level** — Dynatrace иногда экстраполирует результаты, если лимит квоты — смотрим этот флаг в API-ответе.
