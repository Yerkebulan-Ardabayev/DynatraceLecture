> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 4 из 14: «Анализ отклика, деградаций и аномалий»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/services -->
<!-- revision: 2026-04-27 -->

🔖 Редакция от 2026-04-27.

Путь в UI: **Application Observability → Services**, **Settings → Anomaly detection → Services**, **Settings → Server-side service monitoring → Failure detection / parameters / rules**.

## 📚 Источники

- [Configure service failure detection (Managed)](https://docs.dynatrace.com/managed/observe/application-observability/services/service-detection/service-detection-v1/configure-service-failure-detection)
- [Service detection v1 (Managed)](https://docs.dynatrace.com/managed/observe/application-observability/services/service-detection/service-detection-v1)
- [Services (Managed)](https://docs.dynatrace.com/managed/shortlink/services)
- [Davis AI и anomaly detection (Managed)](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services)
- [Distributed traces (Managed)](https://docs.dynatrace.com/managed/observe-and-explore/distributed-traces)

## 📍 КАРТА: пять страниц про отклик и детекцию ошибок

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

### Шаг 1: Services

![Services: 241 сервис](screenshots/day-3-4/response-analysis/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/services`, видно 241 Services. Точка входа для анализа.

### Шаг 2: Anomaly detection for services

![Anomaly detection for services: пороги деградаций Response time и Failure rate](screenshots/day-3-4/response-analysis/settings/builtinanomaly-detection.services/Anomaly-detection-for-services-Environment-Settings-Demo-live-Demo-Live-Dynatrac.png)

Путь: `/ui/settings/builtin:anomaly-detection.services`.

Разбирался в Дне 1 (baselines) и Дне 2 (service-cards). В контексте «анализ отклика» это страница, где задаются пороги детекции для четырёх типов аномалий сервиса.

Dynatrace детектит для сервиса четыре типа аномалий, каждый ведёт свой Problem и свой алерт:

- **Response time degradations / деградация времени отклика.** Оценивается в двух категориях: **All responses** (медиана по всем запросам) и **Slowest 10%** (10% самых медленных). Для каждой категории два порога: relative (% от baseline) и absolute (в мс).
- **Failure rate increase / рост частоты ошибок.** Два порога: relative % и absolute %.
- **Service load drops / падение нагрузки** и **Service load spikes / всплеск нагрузки.** Нормальный профиль нагрузки Davis выучивает за reference period.
- **Reference period / эталонный период.** По умолчанию последние 7 дней. Кнопка **Reset** сбрасывает baseline (нужно после крупного релиза, чтобы не сыпались ложные алерты на новой норме).

Для сервисов с малым трафиком есть параметр исключения low-load (**actions/min**): сервисы ниже этого порога нагрузки исключаются из оценки, чтобы не алертить на единичных запросах.
<!-- last-verified: 2026-06-02 source: https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services -->

**ЕСЛИ → ТО на порогах отклика.** Алерт по деградации отклика заводится только при одновременном нарушении обоих порогов категории:

- ЕСЛИ нарушены **и relative, и absolute** порог (например, отклик All responses вырос и относительно baseline, и выше абсолютной планки в мс) → Davis заводит Problem по этому сервису.
- ЕСЛИ нарушен **только один** порог (выросло относительно baseline, но в абсолюте всё ещё в норме, либо наоборот) → Davis молчит, Problem нет. Это и отсекает «шумовые» скачки на быстрых сервисах, где +50% это всё равно единицы миллисекунд.
<!-- last-verified: 2026-06-02 source: https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services (All responses / Slowest 10%: alert is raised if response time degrades beyond both the absolute and relative thresholds) -->

**ЕСЛИ → ТО на Sensitivity (для fixed thresholds).** Для режима фиксированных порогов есть переключатель чувствительности Low / Medium / High, он задаёт, насколько статистически уверенным должно быть нарушение:

- ЕСЛИ выставить **High** → статистическая уверенность не требуется, Problem заводится на каждом нарушении порога (ловит всё, но шумит на коротких всплесках нагрузки).
- ЕСЛИ выставить **Medium** → используется разумная статистическая уверенность, Davis не алертит на каждом единичном нарушении.
- ЕСЛИ выставить **Low** → требуется высокая статистическая уверенность, кратковременные нарушения (например, из-за разового всплеска трафика) Problem не создают.
<!-- last-verified: 2026-06-02 source: https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services (Sensitivity Low/Medium/High: high / reasonable / no statistical confidence) -->

### Шаг 3: Failure detection parameters

![Failure detection parameters: глобальные параметры классификации failures](screenshots/day-3-4/response-analysis/settings/builtinfailure-detection.environment.parameters/Failure-detection-parameters-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Server-side service monitoring → Failure detection parameters**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection.environment.parameters`.

*Что такое Failure detection.* Механизм, который определяет, **какой запрос считать «упавшим»**. Anomaly detection ловит отклонения метрик от нормы. Failure detection задаёт саму основу метрики Failure rate: какие запросы идут в знаменатель, а какие: в числитель «упавших».

**По умолчанию Dynatrace детектит failure** через:

- Programming exceptions (Java / .NET / Node.js / PHP), прерывающие service call.
- Error pages, отдаваемые web container.
- HTTP 500–599 (ошибки на стороне сервера).
- HTTP 400–599: со стороны клиента (client-side perspective).

**Глобальные параметры на странице (HTTP + General):**

- Override какие коды считать server-side / client-side failures.
- Поведение при отсутствующем HTTP response code.
- Отдельная политика для HTTP 404 (broken link).
- Список **success-forcing exceptions** (технические исключения, не считающиеся failure).
- Список **ignored exceptions** (handled gracefully).
- Custom error rules на основе request attributes.

*Типовой подход.* Обычно дефолт работает. Настройка нужна для особых случаев: если 400 Bad Request надо вернуть в success (клиент сам ошибся), либо наоборот: отдельные 200 с ошибочным телом помечать как failure.

**ЕСЛИ → ТО на failure detection.** От этих параметров зависит, какие запросы вообще попадут в числитель Failure rate:

- По умолчанию **5xx** считаются server-side ошибкой, а **4xx** трактуются как client-side (вина клиента, не сервиса). ЕСЛИ оставить дефолт → Failure rate сервиса собирает только серверные сбои (5xx, exception, error page), клиентские 4xx в него не идут. ЕСЛИ через **HTTP response codes** добавить диапазон 4xx в server-side errors → те же клиентские 400-е начнут поднимать Failure rate и Davis может завести Problem там, где раньше было тихо.
- По умолчанию **HTTP 404** классифицируется как client-side (битая ссылка), а не как server-side failure. ЕСЛИ включить **Consider 404 HTTP response codes as failures** → 404 начнут считаться отказом сервера и влиять на Failure rate; ЕСЛИ не включать → 404 остаются на стороне вызывающего и в метрику не идут.
<!-- last-verified: 2026-06-02 source: https://docs.dynatrace.com/managed/observe/application-observability/services/service-detection/service-detection-v1/configure-service-failure-detection (By default: HTTP 500-599 server-side, HTTP 400-599 client-side; HTTP-4XX usually client-side; 404 classified client-side unless 'Consider 404 ... as failures' is enabled) -->
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/application-observability/services/service-detection/service-detection-v1/configure-service-failure-detection -->

### Шаг 4: Failure detection rules

![Failure detection rules: правила кастомной классификации failure](screenshots/day-3-4/response-analysis/settings/builtinfailure-detection.environment.rules/Failure-detection-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Server-side service monitoring → Failure detection rules**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection.environment.rules`.

*Когда нужно.* Когда дефолтная логика не подходит. Пример: для `auth-service` HTTP-код 401 (Unauthorized), это НЕ failure, а ожидаемое поведение (клиент вводит неправильный пароль). Правило: «для auth-service, 401 не считать failure».

**Структура правила:**

- **Service scope**: к каким сервисам применяется.
- **Condition**: что считать ошибкой: HTTP-коды, exception types, request attributes.
- **Action**: считать failure / не считать / forced success.

Правила оцениваются **сверху вниз, срабатывает первое совпавшее**; per-service override доступен через **Services → выбрать сервис → More (...) → Settings → Failure detection → Override global failure detection settings**.

*Типовое правило.* Exclude пользовательских ошибок из Failure rate для authentication-сервисов. Без этого в пиковые часы Failure rate взлетает от неправильных паролей и создаёт ложные алерты.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/application-observability/services/service-detection/service-detection-v1/configure-service-failure-detection -->

### Шаг 5: Failure detection (rulesets)

![Failure detection: общая страница rulesets](screenshots/day-3-4/response-analysis/settings/builtinfailure-detection-rulesets/Failure-detection-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Server-side service monitoring → Failure detection**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:failure-detection-rulesets`.

Общая страница управления всеми failure detection rulesets. Показывает список всех scope-ов со своими правилами. В большой инсталляции разные подсистемы могут иметь свои rulesets: API-бэкенды с одной логикой, публичные веб-сайты с другой.

**Что на странице:**

- Список rulesets с их scope (какие сервисы).
- Приоритет применения (какой ruleset побеждает при пересечении).
- Ссылки на детальные правила (Шаг 4).

---

## ⚙️ COOKBOOK: настройка анализа отклика в банке

### Отделить ожидаемые 401 от реальных проблем

*Задача.* `auth-service` показывает Failure rate 15%, это нормально, клиенты часто вводят неправильные пароли. Ложные алерты.

*Решение:*

1. Failure detection rules → правило: scope = `auth-service`, condition = `HTTP response code = 401`, action = `Ignored (not failure)`.
2. Перезапускать OneAgent не нужно, правило применяется автоматически.
3. Через 10-15 минут Failure rate падает до реального уровня (0.1-0.5%).

### Custom-protocol сервис с ошибками в теле ответа

*Задача.* Сервис отвечает бинарным ответом с полем `status` в теле. HTTP всегда 200. Failure rate = 0, но бизнес страдает.

*Решение.* Failure detection rules: scope = `custom-service`, condition = `Response body contains "status":"error"`, action = `Mark as failure`. После применения Dynatrace корректно классифицирует ответы.

### Снизить чувствительность anomaly для тестового сервиса

*Задача.* `dev-service` часто имеет спайки response time (нестабильное тестовое окружение), шум.

*Решение.* Anomaly detection для services, override для конкретного сервиса в его карточке: поднять порог Slowest 10% с 1000 до 5000 мс. Для dev допустимо.

---

## 🎓 ТЕОРИЯ: различие механизмов

### Anomaly detection vs Failure detection

- **Anomaly detection**: про **статистические отклонения**. Сравнивает текущую метрику с baseline (history-based). Если Response time обычно 100 мс, а сейчас 400 мс: аномалия, даже если все 400 мс запросов успешные.
- **Failure detection**: про **явные ошибки**. Классифицирует каждый запрос: успех или неудача, по заданной логике (HTTP-код, exception, custom condition). Failure rate: доля неудач.

**Работают вместе.** Davis AI создаёт Problem, когда:

- Response time **аномально высокий** (Anomaly detection), или
- Failure rate **аномально высокий** (Failure detection + Anomaly detection на метрике Failure rate).

То есть Failure detection определяет, **что считать ошибкой**. Anomaly detection определяет, **когда рост ошибок: аномалия, требующая внимания**.

### Почему важна тонкая настройка

Без настройки Failure detection метрика Failure rate может быть:

- Слишком строгой: все 4xx → failures, ночные алерты от ботов.
- Слишком слабой: кастомные ошибки в теле не учитываются.

Без настройки Anomaly detection алерты либо срабатывают по мелочи (Response time подскочил на 10% → Problem), либо молчат при реальных инцидентах (пороги слишком высокие).

*Сроки.* Тонкая настройка после первичного деплоя занимает 1-2 недели. По каждому критичному сервису: корректировка rules и thresholds под реальный профиль трафика.

### Air-gapped specifics

Все настройки локальны, хранятся в кластере, применяются OneAgent без внешних вызовов.
