> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 4 из 14: «Анализ отклика, деградаций и аномалий»

## 📍 КАРТА — пять страниц про отклик и детекцию ошибок

Термины темы: `Response time / время отклика`, `Failure rate / частота ошибок`, `Failure detection / классификация ошибок`, `Anomaly detection / обнаружение аномалий`, `Baseline / базовая линия / эталон`, `Ruleset / набор правил`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Services | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` |
| Anomaly detection for services | **Settings → Anomaly detection → Services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services` |
| Failure detection parameters | **Settings → Server-side service monitoring → Failure detection parameters** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection.environment.parameters` |
| Failure detection rules | **Settings → Server-side service monitoring → Failure detection rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection.environment.rules` |
| Failure detection (общая страница) | **Settings → Server-side service monitoring → Failure detection** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection-rulesets` |

---

## 🎬 Работа с детекцией отклика и ошибок на пяти экранах

### Шаг 1 — Services

![Services — 239 сервисов](screenshots/day-3-4/response-analysis/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/services`. 239 Services на captured. Разбирался неоднократно; точка входа для анализа.

### Шаг 2 — Anomaly detection for services

![Anomaly detection for services — пороги деградаций Response time и Failure rate](screenshots/day-3-4/response-analysis/settings/builtinanomaly-detection.services/Anomaly-detection-for-services-Environment-Settings-Demo-live-Demo-Live-Dynatrac.png)

Путь: `/ui/settings/builtin:anomaly-detection.services`.

Разбирался в Дне 1 (baselines) и Дне 2 (service-cards). В контексте «анализ отклика» — это страница, где задаются пороги для детекции деградаций Response time (по All requests и Slowest 10%) и роста Failure rate. Ключевые блоки: Response time degradations, Failure rate increases, Service load drops/spikes, Reference period.

### Шаг 3 — Failure detection parameters

![Failure detection parameters — глобальные параметры классификации failures](screenshots/day-3-4/response-analysis/settings/builtinfailure-detection.environment.parameters/Failure-detection-parameters-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Server-side service monitoring → Failure detection parameters**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection.environment.parameters`.

*Что такое Failure detection.* Механизм, который определяет, **какой запрос считать «упавшим»**. Anomaly detection ловит отклонения метрик от нормы. Failure detection задаёт саму основу метрики Failure rate: какие запросы идут в знаменатель, а какие — в числитель «упавших».

**Глобальные параметры на странице:**

- Считать ли HTTP 4xx как failures (по умолчанию нет, только 5xx).
- Считать ли каждое исключение в коде failure или только необработанные.
- Минимальный порог срабатывания — чтобы единичный 500 не давал Failure rate 100% при низком трафике.

*Типовой подход.* Обычно дефолт работает. Настройка нужна для особых случаев: если 400 Bad Request считается признаком проблем (неправильная интеграция с партнёром), включают 4xx → failures для конкретных сервисов.

### Шаг 4 — Failure detection rules

![Failure detection rules — правила кастомной классификации failure](screenshots/day-3-4/response-analysis/settings/builtinfailure-detection.environment.rules/Failure-detection-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Server-side service monitoring → Failure detection rules**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection.environment.rules`.

*Когда нужно.* Когда дефолтная логика не подходит. Пример: для `auth-service` HTTP-код 401 (Unauthorized) — это НЕ failure, а ожидаемое поведение (клиент вводит неправильный пароль). Правило: «для auth-service, 401 не считать failure».

**Структура правила:**

- **Service scope** — к каким сервисам применяется.
- **Condition** — что считать ошибкой: HTTP-коды, exception types, HTTP headers.
- **Action** — считать failure / не считать / считать warning.

*Типовое правило.* Exclude пользовательских ошибок из Failure rate для authentication-сервисов. Без этого в пиковые часы Failure rate взлетает от неправильных паролей и создаёт ложные алерты.

### Шаг 5 — Failure detection (rulesets)

![Failure detection — общая страница rulesets](screenshots/day-3-4/response-analysis/settings/builtinfailure-detection-rulesets/Failure-detection-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Server-side service monitoring → Failure detection**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection-rulesets`.

Общая страница управления всеми failure detection rulesets. Показывает список всех scope-ов со своими правилами. В большой инсталляции разные подсистемы могут иметь свои rulesets — API-бэкенды с одной логикой, публичные веб-сайты с другой.

**Что на странице:**

- Список rulesets с их scope (какие сервисы).
- Приоритет применения (какой ruleset побеждает при пересечении).
- Ссылки на детальные правила (Шаг 4).

---

## ⚙️ COOKBOOK — настройка анализа отклика в банке

### Отделить ожидаемые 401 от реальных проблем

*Задача.* `auth-service` показывает Failure rate 15% — это нормально, клиенты часто вводят неправильные пароли. Ложные алерты.

*Решение:*

1. Failure detection rules → правило: scope = `auth-service`, condition = `HTTP response code = 401`, action = `Ignored (not failure)`.
2. Перезапускать OneAgent не нужно, правило применяется автоматически.
3. Через 10-15 минут Failure rate падает до реального уровня (0.1-0.5%).

### Custom-protocol сервис с ошибками в теле ответа

*Задача.* Сервис отвечает бинарным ответом с полем `status` в теле. HTTP всегда 200. Failure rate = 0, но бизнес страдает.

*Решение.* Failure detection rules: scope = `custom-service`, condition = `Response body contains "status":"error"`, action = `Mark as failure`. После применения Dynatrace корректно классифицирует ответы.

### Снизить чувствительность anomaly для тестового сервиса

*Задача.* `dev-service` часто имеет спайки response time (нестабильное тестовое окружение), шум.

*Решение.* Anomaly detection для services, override для конкретного сервиса в его карточке — поднять порог Slowest 10% с 1000 до 5000 мс. Для dev допустимо.

---

## 🎓 ТЕОРИЯ — различие механизмов

### Anomaly detection vs Failure detection

- **Anomaly detection** — про **статистические отклонения**. Сравнивает текущую метрику с baseline (history-based). Если Response time обычно 100 мс, а сейчас 400 мс — аномалия, даже если все 400 мс запросов успешные.
- **Failure detection** — про **явные ошибки**. Классифицирует каждый запрос: успех или неудача, по заданной логике (HTTP-код, exception, custom condition). Failure rate — доля неудач.

**Работают вместе.** Davis AI создаёт Problem, когда:

- Response time **аномально высокий** (Anomaly detection), или
- Failure rate **аномально высокий** (Failure detection + Anomaly detection на метрике Failure rate).

То есть Failure detection определяет, **что считать ошибкой**. Anomaly detection определяет, **когда рост ошибок — аномалия, требующая внимания**.

### Почему важна тонкая настройка

Без настройки Failure detection метрика Failure rate может быть:

- Слишком строгой — все 4xx → failures, ночные алерты от ботов.
- Слишком слабой — кастомные ошибки в теле не учитываются.

Без настройки Anomaly detection алерты либо срабатывают по мелочи (Response time подскочил на 10% → Problem), либо молчат при реальных инцидентах (пороги слишком высокие).

*Сроки.* Тонкая настройка после первичного деплоя занимает 1-2 недели. По каждому критичному сервису — корректировка rules и thresholds под реальный профиль трафика.

### Air-gapped specifics

Все настройки локальны, хранятся в кластере, применяются OneAgent без внешних вызовов.
