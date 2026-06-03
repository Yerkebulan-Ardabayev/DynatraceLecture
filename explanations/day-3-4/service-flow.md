> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 2 из 14: «Связи сервисов и Service Flow»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/services -->
<!-- revision: 2026-04-27 -->

🔖 Редакция от 2026-04-27.

Путь в UI: **Application Observability → Services** → клик на сервис → блок **Understand dependencies → View service flow**.

## 📚 Источники

- [Service flow (Managed)](https://docs.dynatrace.com/managed/shortlink/service-flow)
- [Services (Managed)](https://docs.dynatrace.com/managed/shortlink/services)
- [Smartscape topology (Managed)](https://docs.dynatrace.com/managed/shortlink/smartscape)
- [Distributed traces (Managed)](https://docs.dynatrace.com/managed/observe-and-explore/distributed-traces)

## 📍 КАРТА: Service Flow как инструмент анализа зависимостей

Термины темы: `Service Flow / граф вызовов сервиса`, `Upstream / восходящие / кто вызывает`, `Downstream / нисходящие / кого вызывает`, `Blast radius / радиус воздействия`, `PurePath / сквозной трейс запроса`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Список сервисов → вход в карточку → Service Flow | **Application Observability → Services** → клик на сервис | `https://guu84124.live.dynatrace.com/ui/services` |

**Отличие Service Flow от Smartscape:**

| Аспект | Smartscape | Service Flow |
|---|---|---|
| Что показывает | Все сущности и их связи в окружении за окно ~72 часа | Цепочки вызовов между конкретными сервисами |
| Ориентация | Пять уровней: Applications → Services → Processes → Hosts → Data centers | Только Service-level |
| Контекст | Near real-time снимок зависимостей за окно | Агрегация за выбранный timeframe |
| Основа данных | Авто-обнаружение топологии (OneAgent + Service Discovery) | Реальные PurePath-ы за выбранный период |
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/smartscape -->

---

## 🎬 Работа со Service Flow на captured экране

### Шаг 1: Services (вход в Service Flow через карточку)

![Services: 239 сервисов, вход в карточку → раздел Service Flow](screenshots/day-3-4/service-flow/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь в меню: **Application Observability → Services**.
Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/services`.

На экране заголовок **239 Services**. Service Flow открывается не с отдельного URL, а из **карточки конкретного сервиса**.

**Как попасть в Service Flow.**
1. Открыть список Services.
2. Кликнуть на любой сервис (например, `EasytravelService`).
3. В карточке сервиса найти блок **Understand dependencies** → нажать **View service flow**.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/service-flow -->

**Что показывает Service Flow.** Graph, где:
- **Слева**: клиенты этого сервиса (кто его вызывает): другие сервисы, приложения RUM, synthetic monitors.
- **Центр**: текущий сервис.
- **Справа**: backend-зависимости (сервисы, базы данных, внешние API, очереди).

**Ширина рёбер**: пропорциональна частоте вызовов за выбранный период.
**Цвет рёбер**: раскраска по состоянию: зелёный = норма, жёлтый = замедление, красный = активная проблема.

**Дополнительная информация на каждом ребре.** Наведение курсора показывает: число вызовов за период, среднее время, процент ошибок. Клик: drill down к конкретным запросам между этой парой.

### Типовые сценарии работы

**Зависимости перед изменением.** Команда планирует изменить `auth-service`. Перед деплоем открываем его Service Flow: 15 сервисов его вызывают. Оцениваем blast radius и заранее предупреждаем владельцев зависимых сервисов.

**«Забытые» вызовы.** В Service Flow виден вызов к legacy-системе, которая должна была быть отключена месяц назад. Значит какой-то код продолжает её использовать. Найти ответственных, починить.

**Анализ замедления.** Service Flow показывает красное ребро от сервиса к БД `accounts-db`. Медиана вызова 2000 мс. Остальные рёбра зелёные. Корень: БД, а не сам сервис. Переход в карточку БД для дальнейшего анализа.

**Неожиданные зависимости.** У сервиса `retail-api` в Service Flow внезапно появился вызов к `corporate-db`. По архитектуре это недопустимо. Сигнал: в коде непредусмотренное обращение. Инцидент для разработки.

---

## 🎓 ТЕОРИЯ: как Service Flow агрегирует данные

### Источник данных

Service Flow строится **на основе распределённых трейсов (PurePath)**. За выбранный временной период Dynatrace анализирует все PurePath, в которых участвовал текущий сервис:
- **Входящие вызовы**: кто инициировал запросы, попадающие в этот сервис (upstream).
- **Исходящие вызовы**: куда сервис ходил для обработки запросов (downstream).

Каждая пара (caller, callee) агрегируется: число вызовов, среднее время, частота ошибок. Сервисы с малым вкладом группируются автоматически (метки вида «2 services» или «4 instances»).
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/service-flow -->

### Агрегация по времени

Период, для которого строится Service Flow, определяется **верхним селектором timeframe** (Last 2 hours / Last 24 hours и т.д.). Все PurePath за период учитываются.

**Нюанс:** Service Flow **отражает фактические вызовы**, не потенциальные. Если сервис теоретически может ходить в 10 баз, но за последние 2 часа ходил только в 3, в Service Flow будут только 3. Это помогает отфильтровать редкие/маргинальные зависимости.

### Отличие от Smartscape на практике

- **Smartscape**: **структурный** взгляд. Near real-time-снимок зависимостей за окно ~72 часа. Подходит для общей архитектуры.
- **Service Flow**: **операционный** взгляд. Что реально происходит за выбранный timeframe. Подходит для анализа инцидентов и планирования изменений.

Типовое использование параллельно: Smartscape: ревизия ландшафта раз в неделю, Service Flow: ежедневно при работе с конкретными сервисами.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/smartscape -->

### Air-gapped specifics

Service Flow полностью работает на локальных данных. PurePath-ы хранятся в Cassandra кластера, агрегация: на лету при открытии карточки. Внешних вызовов нет.
