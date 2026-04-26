> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 10 из 10: «Dynatrace API: обзор сценариев интеграции»

## 📍 КАРТА — две страницы про API

Термины темы: `API token / токен доступа`, `Scope / права токена`, `Rate limit / лимит запросов`, `Monaco / CLI для управления тенантом как кодом`, `Configuration API / endpoint настроек`, `Metrics API / получение метрик`, `Events API / создание custom events`, `Webhook vs Pull / push-pull модели алертов`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Access tokens (список токенов) | **User menu → Access tokens** | `https://guu84124.live.dynatrace.com/ui/access-tokens` |
| Token settings (общие настройки) | **Settings → Security → Access token settings** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:tokens.token-settings` |

---

## 🎬 Работа с API на двух экранах

### Шаг 1 — Access tokens (управление токенами)

![Access tokens — список токенов](screenshots/day-5/api/access-tokens/Access-tokens-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/access-tokens`.

*Что видно.* Список всех API-токенов текущего пользователя. Колонки: `Token name`, `Last used`. Кнопки: `Generate new token`, `Show more actions`.

*Что такое API-токен.* Строка вида `dt0c01.ABC123...XYZ789` длиной ~100 символов. Заменяет пароль при вызове API: вместо логин/пароль в заголовке идёт `Authorization: Api-Token dt0c01.ABC...`.

**Зачем несколько токенов.** Каждая интеграция — свой токен с минимально необходимыми правами:

- `jira-integration` — создаёт тикеты в Jira при проблеме. Scope: `ReadConfig`, `ReadProblems`.
- `grafana-export` — тянет метрики для стороннего дашборда. Scope: `ReadMetrics`.
- `ansible-deploy` — при выкатке добавляет tag к сервисам. Scope: `WriteConfig`.
- `monitoring-bot` — читает проблемы, постит в мессенджер. Scope: `ReadProblems`, `WriteProblemsComments`.

Если токен утёк — отзываем только его, остальные интеграции продолжают работать. С одним общим токеном пришлось бы перегенерировать и переписывать всё одновременно.

**Создание токена (Generate new token):**

1. Имя (для идентификации в логах).
2. Срок действия — 1 день / 30 дней / 1 год / unlimited. Для production обычно 1 год с напоминанием.
3. Scopes — **строго минимум** для этой интеграции.
4. IP-ограничения (опционально) — токен принимается только с определённых IP.

**Группы scopes:**

- **Read** (Read problems, Read metrics, Read configuration, Read audit logs…) — данные.
- **Write** (Write configuration, Write tags, Write problem comments…) — изменения.
- **Admin** (Access token administrator, User management…) — управление платформой.

Admin-категория очень ограничительна, только для реально админских скриптов.

*Last used.* Dynatrace фиксирует время последнего использования. Если токен не использовался 6+ месяцев — можно удалить (интеграция уехала на другой токен или прекратила работу).

### Шаг 2 — Token settings (общая политика токенов)

![Token settings — политика токенов](screenshots/day-5/api/settings/builtintokens.token-settings/Access-tokens-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:tokens.token-settings`.

*Что настраивает.* Общая политика работы с API-токенами тенанта. Применяется ко всем пользователям и всем токенам.

**Ключевые параметры:**

- **Maximum token expiration** — максимальный срок действия. Если политика = 90 дней, пользователь не может создать токен «на 1 год». Реализация требования «регулярная ротация секретов».
- **Require expiration date** — запретить токены без expiration. Для compliance-среды обычно Да.
- **Allowed scopes per user role** — какие scope-ы пользователь может выдать в зависимости от своей роли. Обычный пользователь не должен выдавать Admin-токены.
- **Minimum token prefix length** — длина видимого префикса. В логах показывается только префикс, не полный токен.
- **Token audit logging** — логирование всех операций с токенами. Обязательно для compliance-аудитов.

*Audit log.* Можно включить запись всех использований токенов: кто, когда, какой endpoint вызывал, с какого IP. Критично для расследований после инцидентов безопасности.

---

## 🎓 ТЕОРИЯ — Dynatrace API и сценарии интеграции

### Структура API

Dynatrace API — REST API, JSON-ответы. Базовый URL: `https://guu84124.live.dynatrace.com/api/`.

Основные версии:

- **API v1** — классический набор endpoint'ов (ретро, поддерживается, не развивается). Используется большинством старых интеграций.
- **API v2** — современный, с улучшенной пагинацией, фильтрацией, идемпотентностью. Новый код писать на v2.
- **Configuration API** — отдельный для настроек (v1), частично переезжает в **Settings API** (v2).
- **Problem Feed API v1/v2** — для проблем.
- **Smartscape API** — для иерархии сущностей.

**Документация** — встроенный Swagger/OpenAPI в самом Dynatrace: `/rest/*/openapi` — можно тыкать API прямо из браузера без написания кода.

### Основные группы endpoint'ов

1. **Metrics API v2** (`/api/v2/metrics`) — получение метрик по селектору.
2. **Problems API v2** (`/api/v2/problems`) — список проблем с фильтрами.
3. **Entities API v2** (`/api/v2/entities`) — все сущности (hosts, services, apps) с атрибутами.
4. **Logs API v2** (`/api/v2/logs`) — запросы к логам.
5. **Events API v2** (`/api/v2/events`) — события и создание custom-событий (deployment events, info events).
6. **Tags API v2** (`/api/v2/tags`) — управление тегами сущностей.
7. **User Sessions Query** (`/api/v1/userSessionQueryLanguage/table`) — USQL, который обсуждали в Теме 9.
8. **Configuration API v1** (`/api/config/v1/*`) — настройки (alerting profiles, monitor configurations, и т.д.).

### Типичные сценарии интеграции

**Export для BI.** Скрипт ежедневно тянет метрики через Metrics API, складывает в Vertica / ClickHouse. BI-команда строит отчёты. Dynatrace остаётся source of truth для операционки, стратегические данные в корпоративном DWH.

**Custom events для CI/CD.** При выкатке релиза пайплайн шлёт event в Dynatrace:
```bash
curl -X POST "$DT_ENV/api/v2/events/ingest" \
  -H "Authorization: Api-Token $DT_TOKEN" \
  -d '{
    "eventType": "CUSTOM_DEPLOYMENT",
    "title": "payment-service deployed v2.3.1",
    "properties": {
      "source": "GitLab",
      "author": "i.ivanov",
      "commit": "abc123"
    },
    "entitySelector": "type(SERVICE),entityName(payment-service)"
  }'
```

Dynatrace показывает event в карточке сервиса. Когда Davis найдёт проблему, в root cause увидит «в 14:23 был деплой, в 14:27 началась проблема».

**Automation через tags.** Скрипт ansible / terraform при создании новой VM ставит tag в Dynatrace:
```bash
curl -X POST "$DT_ENV/api/v2/tags" \
  -H "Authorization: Api-Token $DT_TOKEN" \
  -d '{
    "entitySelector": "type(HOST),entityId($HOST_ID)",
    "tags": [
      {"key": "team", "value": "retail-banking"},
      {"key": "environment", "value": "prod"},
      {"key": "criticality", "value": "high"}
    ]
  }'
```

Далее management zones автоматически группируют сервисы по тегам, alerting profiles разруливают маршрутизацию.

**Pull-модель для алертов.** Скрипт каждые 30 сек: `GET /api/v2/problems?from=now-1m&status=OPEN`, парсит новые проблемы, шлёт в корпоративный мессенджер. Используется вместо webhook в air-gapped контекстах, когда исходящие соединения от Dynatrace невозможны.

**Auto-remediation.** Скрипт слушает webhook с проблемами. Для известных шаблонов — автоматические действия:

- Проблема «disk full on `/var/log`» → запуск cleanup через Ansible.
- Проблема «pod CrashLoopBackOff» → `kubectl delete pod` для перезапуска.
- Проблема «OOM on app-server» → увеличить лимит через terraform apply.

Уровень зрелости SRE. Требует дисциплины, но даёт большую экономию ручной работы.

**Dashboard-as-code.** Вместо ручной настройки в UI — хранить JSON-описание дашборда в Git и применять через Configuration API:
```bash
curl -X POST "$DT_ENV/api/config/v1/dashboards" \
  -H "Authorization: Api-Token $DT_TOKEN" \
  -d @dashboards/prod-retail-overview.json
```

При изменении dashboard — через PR, с code review. Это GitOps для observability.

### Security best practices для токенов

- **Отдельный токен на интеграцию.** Не переиспользовать.
- **Минимальные scope.** Спрашивать себя: «нужен ли мне Admin scope, или хватит Read?».
- **Expiration date.** Всегда. Ротировать каждые 90 дней по политике безопасности.
- **Не в коде.** Токены в environment variables, secret vault (HashiCorp Vault, Kubernetes Secrets), не в Git.
- **IP-ограничение.** Если токен используется с конкретного IP (CI/CD pipeline) — настроить allowlist.
- **Audit log.** Отслеживать использование, реагировать на подозрительные паттерны.
- **Revocation plan.** Подозрение на утечку — немедленный revoke, не ждать.

### Rate limits

Dynatrace API имеет ограничения на частоту запросов. Для Managed обычно **1000 запросов в минуту на токен**. Превышение — HTTP 429 с заголовком `Retry-After`.

**Правила работы:**

- **Батчинг.** Если можно получить 1000 метрик в одном запросе — не слать 1000 отдельных.
- **Caching.** Кэшировать редко меняющиеся результаты (список сущностей — раз в 5 минут, не на каждый запрос).
- **Backoff.** При 429 ждать `Retry-After` и повторять.

### Air-gapped и API

В air-gapped Managed API работает **внутри сети** — не проблема. Cluster доступен клиентам внутри контура.

Проблема возникает, когда **внешняя** интеграция хочет тянуть данные из Dynatrace (например, SaaS-BI типа Tableau Online). Варианты:

- Пробить канал через firewall для BI-сервиса.
- Хранить данные в корпоративном DWH, к которому BI подключается отдельно.

### SDK и библиотеки

Официальные SDK от Dynatrace:

- **Python** — `dynatrace-python-api` (pip install).
- **JavaScript / TypeScript** — `@dynatrace/api`.
- **Go** — `github.com/dtcookie/dynatrace-go-api`.

Оборачивают HTTP-вызовы в типизированные методы. Для сложных интеграций удобнее SDK, для простых скриптов — обычный `curl`.

### Monaco (Monitoring as Code)

Отдельный инструмент Dynatrace — **Monaco**. CLI для управления конфигурацией тенанта как код (yaml-файлы). Позволяет:

- Держать все alerting profiles, dashboards, monitor settings в Git.
- Применять изменения через `monaco deploy` с diff-проверкой.
- Синхронизировать несколько тенантов (staging / prod / DR).

*Типовой use case.* Поддержка нескольких Dynatrace-тенантов в идентичной конфигурации — основной ЦОД и резервный.

### Завершение курса

Последняя тема курса. Пройденный путь:

- **День 1** — архитектура, компоненты, первые взгляды на UI.
- **День 2** — инфраструктура и backend-мониторинг.
- **День 3-4** — observability, приложения, надёжность, безопасность.
- **День 5** — фронтенд, пользовательский опыт, алертинг, интеграции.

Слушатель понимает, как устроена платформа Dynatrace Managed в air-gapped контуре — от OneAgent на хосте до API-токена для BI-скрипта. Не просто смотрит дашборды, а понимает, откуда каждая метрика, как считается и куда уходит при интеграции.

### Ключевые термины

- **API token** — строка для авторизации в API, заменяет пароль.
- **Scope** — права токена: что ему разрешено делать.
- **Rate limit** — ограничение частоты запросов (обычно 1000/мин).
- **Monaco** — CLI от Dynatrace для управления тенантом как кодом.
- **Configuration API** — endpoint-ы для настроек тенанта.
- **Metrics API** — endpoint-ы для получения метрик.
- **Events API** — endpoint-ы для создания custom events (например, deployment events).
- **Webhook vs Pull** — две модели получения алертов (push от Dynatrace или pull скриптом).
