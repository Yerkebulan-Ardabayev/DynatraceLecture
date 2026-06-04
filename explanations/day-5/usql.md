> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 9 из 10: «USQL / DQL: запросы, возможности, ограничения»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/user-sessions/query -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Custom queries, segmentation, and aggregation of session data (USQL)](https://docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/custom-queries-segmentation-and-aggregation-of-session-data)
> - [Leverage user action and user session properties for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/analyze-and-use/action-and-session-properties)
> - [User actions](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-actions)
> - [Real User Monitoring (RUM)](https://docs.dynatrace.com/managed/shortlink/rum)

## 📍 КАРТА: одна страница, два языка

Термины темы: `USQL / User Session Query Language` (SQL-подобный для сессий и actions в Managed), `DQL / Dynatrace Query Language` (pipeline-язык SaaS для Grail, **в Managed недоступен**), `Grail / облачное хранилище SaaS`, `usersession / виртуальная таблица сессий`, `useraction / виртуальная таблица действий`, `Funnel function / встроенная функция построения воронки`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User session query (USQL) | **Application Observability → Frontend → User sessions query** | `https://guu84124.live.dynatrace.com/ui/user-sessions/query` |

---

## 🎬 Работа с USQL на одном экране

### Шаг 1: User Session Query editor

![User Session Query: редактор USQL](screenshots/day-5/usql/user-sessions/query/User-Session-Query-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/query`.

**Что здесь видно.** Страница с заголовком `Run a query to view results` и двумя действиями: `Run query`, `Copy`. Центральная часть страницы: текстовый редактор для написания USQL.

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

Apdex получается: (203 + 0.5 × 52) / 278 = 0.824. То же самое, что платформа показывает в карточке приложения. Теперь мы сами получили его SQL-запросом: можем комбинировать как хотим.

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

Топ-20 стран по количеству сессий со средним числом ошибок. Полезно для поиска региональных проблем: из определённого региона больше ошибок → возможно проблема с локальным провайдером.

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

Список самых проблемных сессий за час: каждую можно открыть в Session Replay (если запись доступна) и посмотреть, что шло не так.

---

## 🎓 ТЕОРИЯ: USQL, DQL и связь с другими языками

### USQL: User Session Query Language

USQL: SQL-подобный язык для запросов по пользовательским сессиям и user actions.

**Синтаксис близок к SQL**, но ориентирован на четыре виртуальные таблицы:

- `usersession`: одна строка на сессию.
- `useraction`: одна строка на user action.
- `userevent`: события (например, page changes, rage events).
- `usererror`: ошибки и crashes.

```sql
SELECT <columns>
FROM <usersession | useraction | userevent | usererror>
WHERE <conditions>
GROUP BY <columns>
ORDER BY <columns>
LIMIT <n>;
```

Только `SELECT` и `FROM` обязательны.

**Поддерживаемые ключевые слова и функции (по официальной документации):**

- **Keywords:** `AND`, `OR`, `WHERE`, `GROUP BY`, `ORDER BY`, `DISTINCT`, `BETWEEN`, `IN`, `LIKE`, `FILTER`.
- **Aggregation:** `SUM`, `AVG`, `MIN`, `MAX`, `MEDIAN`, `COUNT`, `PERCENTILE`.
- **Date functions:** `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `DATETIME`.
- **Специализированные:** `FUNNEL`, `TOP`, `CONDITION`, `KEYS`.

**Ограничения USQL:**

- **Только закрытые сессии.** Live-сессии в выборке не участвуют.
- **Default LIMIT 50, max 5000**: увеличить можно через `LIMIT <n>` до 5000, выше: нельзя.
- **Single table per SELECT.** JOIN-ов между таблицами нет.
- **Нет field-to-field comparisons**: нельзя сравнить два поля строки между собой.
- **LIKE-ограничение**: запрос с 11+ LIKE-условиями, у которых wildcard стоит не в конце, отклоняется.

**Доступ к USQL:**

- Через UI (разобрано в Шаге 1).
- Через REST endpoints **`/table`** (плоский результат) и **`/tree`** (иерархический) с API-токеном.
- Через Data Explorer: часть USQL-запросов встраивается как tile в dashboard.

**Time filtering** в USQL: переменные `$TIME_FRAME_START`, `$TIME_FRAME_END`, `$NOW` (с конструкциями вида `$NOW - DURATION("2h")`).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/custom-queries-segmentation-and-aggregation-of-session-data -->

### DQL: Dynatrace Query Language

DQL: новый язык, появившийся в 2022 году для работы с **Grail**, облачным хранилищем Dynatrace. Синтаксис совершенно другой: pipeline-based, как в Splunk SPL или Kusto.

Пример DQL:
```
fetch logs
| filter status == "ERROR"
| filter dt.entity.service == "payment-service"
| summarize count=count() by bin(timestamp, 1h)
| sort timestamp asc
```

**Ключевые отличия от USQL:**

- **Pipeline-синтаксис**: `|` разделяет шаги обработки.
- **Работает не только с сессиями**: со всей телеметрией: logs, metrics, spans, events, problems.
- **Нативная поддержка временных рядов**: binning, rolling windows.
- **Богатые аналитические функции**: percentiles, distinct counts, complex aggregations.
- **Требует Grail storage**: облачное хранилище с parquet-форматом. В Managed **его нет**.

### ⚠️ DQL и Grail в air-gapped Managed

**Важно.** Grail: архитектурное решение SaaS-платформы Dynatrace. В текущих релизах Managed он **не доступен**, соответственно **DQL тоже не работает** в air-gapped Managed-контуре.

Типовой вопрос слушателей: «почему у нас нет Grail / DQL, когда в документации они везде?». Ответ: документация Dynatrace ориентирована прежде всего на SaaS-платформу, а Managed: отдельный продукт с собственным циклом релизов. Сроки появления Grail и DQL в Managed в публичных roadmap Dynatrace не зафиксированы, поэтому закладываться на них в проектировании нельзя.

*В учебном плане* мы не показываем DQL напрямую, но упоминаем как «новая модель запросов, используемая в SaaS». Для текущего Managed-контура инструменты анализа: Metrics Selector, USQL и UI-фильтры логов.

### Синтаксис USQL детально

**SELECT columns:**
- `*`: все колонки (не рекомендуется, 50+ колонок).
- Конкретные поля: `userId`, `startTime`, `duration`, `applicationId`, `applicationType`, `country`, `city`, `browserFamily`, `browserMajorVersion`, `osFamily`, `osVersion`, `userActionCount`, `totalErrorCount`, `userExperienceScore`, `useragent`, `ip`, …

**Агрегации:**
- `count(*)`, `count(distinct userId)`.
- `avg(column)`, `sum(column)`, `min/max(column)`.
- `percentile(column, 95)`: 95-й перцентиль.

**WHERE filters:**
- Сравнения: `>`, `<`, `=`, `!=`, `IN (...)`, `LIKE '%pattern%'`.
- Дата/время: `now() - 1d`, `now() - 1h`, фиксированные timestamp'ы.
- Boolean: `AND`, `OR`, `NOT`.

**FUNNEL-функция**: строит воронку по последовательности шагов:

```sql
SELECT FUNNEL(
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

**Ad-hoc расследования.** После инцидента: какие пользователи затронуты, какие сценарии ломались, откуда они подключались.

**Custom-метрики для дашбордов.** USQL-запрос встраивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversion rate по конкретному региону).

**Интеграция с внешним BI.** Скрипт, еженедельно запускающий USQL через API и складывающий результаты в корпоративный data warehouse (Vertica, ClickHouse), далее стратегические дашборды в Power BI / Tableau.

### Когда USQL не подходит

- **Логи приложений.** USQL про сессии и actions, не про логи. Для логов: Logs UI в Dynatrace (или DQL в SaaS).
- **Метрики сервисов.** USQL не работает с `builtin:service.*` метриками. Для них: Data Explorer / Metrics API.
- **Трейсы.** USQL не видит PurePath-данные на уровне backend. Для трейсов: dedicated API или Distributed Tracing.
- **Долгосрочные тренды.** Реальная глубина истории по сессиям ограничена retention RUM/Sessions Classic (35 дней). Для долгосрочного хранения: экспорт в Elasticsearch (User session export) или внешний BI (см. ниже).

### Альтернативы: куда смотреть для других типов данных

- **Метрики инфраструктуры и сервисов**: Data Explorer (разбирался в Дне 1, Тема 8) или Metrics API.
- **Логи**: Log Management в Dynatrace, тоже через отдельный UI. В air-gapped Managed это отдельный модуль лицензии.
- **PurePath / Traces**: Distributed Tracing UI или API.
- **Конфигурация / Settings**: Configuration API.

USQL: специализированный инструмент для одного домена (RUM-сессии), не универсальный.

### Типичные ошибки новичков

- **Забыть фильтр по времени** (`WHERE startTime > $NOW - DURATION("1d")` или диапазон через `BETWEEN`). USQL без явного окна работает по дольшему интервалу: времени уходит много, легко получить timeout.
- **Использовать `SELECT *`.** Получает 50+ колонок, ломает UI-таблицу, тратит квоту объёма.
- **Забыть `LIMIT`.** Default: 50 строк, max: 5000. UI может повиснуть на рендеринге, если ожидать тысячи строк.
- **Путать FROM.** Четыре таблицы: `usersession` (одна строка на сессию), `useraction` (одна строка на действие), `userevent` (события), `usererror` (ошибки/crashes). Разные структуры, разные колонки.
- **Поле-к-полю сравнения нельзя.** USQL не поддерживает сравнение двух полей одной строки между собой: для такого сценария нужно вычислять оба поля и сравнивать в скрипте.

### API-экспорт USQL

Для интеграции с внешними системами: API:
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

- **USQL**: User Session Query Language, SQL-подобный, для сессий и actions.
- **DQL**: Dynatrace Query Language, новый pipeline-язык для Grail.
- **Grail**: облачное хранилище всей телеметрии, пока только в SaaS.
- **Funnel function**: встроенная функция USQL для построения funnel.
- **usersession**: виртуальная таблица сессий.
- **useraction**: виртуальная таблица действий.
- **Extrapolation level**: Dynatrace иногда экстраполирует результаты, если лимит квоты: смотрим этот флаг в API-ответе.
