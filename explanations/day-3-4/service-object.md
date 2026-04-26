> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 3 из 14: «Логический объект Service: полное описание интерфейса»

## 📍 КАРТА — Service как сущность и правила его детекции

Термины темы: `Service / сервис / логическая backend-единица`, `Full Web Service / SOAP-сервис с WSDL-контрактом`, `External Web Service / внешний вызов наружу`, `Service splitting / разбиение процесса на несколько сервисов`, `Process Group / группа процессов`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Список сервисов | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` |
| Правила детекции Full Web Services | **Settings → Service Detection → Rules for Full Web Services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection.full-web-service` |
| Правила детекции External Web Services | **Settings → Service Detection → Rules for External Web Services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection.external-web-service` |
| Service splitting | **Settings → Service Detection → Service splitting** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-splitting-rules` |

---

## 🎬 Работа с детекцией сервисов на четырёх экранах

### Шаг 1 — Services (список сервисов как точка входа)

![Services — список 239 сервисов](screenshots/day-3-4/service-object/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Services**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/services`.

Captured: **239Services**. Полный разбор структуры списка — в Дне 1, Тема 5 и Дне 2, Тема 7.

### Шаг 2 — Service detection rules for Full Web Services

![Service detection rules for Full Web Services — правила детекции для Full Web Services](screenshots/day-3-4/service-object/settings/builtinservice-detection.full-web-service/Service-detection-rules-for-Full-Web-Services-Environment-Settings-Demo-live-Dem.png)

Путь: **Settings → Service Detection → Rules for Full Web Services**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection.full-web-service`.

*Что такое Full Web Service.* Тип сервиса в Dynatrace для серверов, **принимающих входящие SOAP / JAX-WS / REST с явной схемой**. Отличается от обычного Web request service более детальными метаданными — Dynatrace видит operation name, WSDL-контракт, типы запросов и ответов.

**Типы правил на странице** — как разбить сервисы:

- Имя WSDL-сервиса и operation.
- SOAP-action header.
- URL-паттерн с параметрами.
- Имя Java-класса SOAP-endpoint.

*Типовое применение.* Интеграции с legacy-системами (АБС, T24 Temenos, карточный процессинг). Часто используется SOAP или WSDL-based REST. Тонкие правила разбиения разделяют бизнес-операции одного endpoint-а на отдельные Service.

### Шаг 3 — Service detection rules for External Web Services

![Service detection rules for External Web Services — правила детекции external-вызовов](screenshots/day-3-4/service-object/settings/builtinservice-detection.external-web-service/Service-detection-rules-for-External-Web-Services-Environment-Settings-Demo-live.png)

Путь: **Settings → Service Detection → Rules for External Web Services**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-detection.external-web-service`.

*Что такое External Web Service.* Сервис на другой стороне исходящих вызовов. Инструментированное приложение делает HTTP-запрос наружу к системе без OneAgent — SaaS API, сторонний сервис, партнёрская система.

Dynatrace не видит внутреннюю работу таких систем, но видит **вызов с нашей стороны**: хост, URL, время ответа, статус. External web services попадают в Service Flow справа от нашего сервиса (downstream).

**Правила на странице** — как разбивать external-сервисы. Например, вызовы к `https://api.example.com/*` → в External Service `Example API`, вызовы к `https://partner.example.org/*` → в отдельный `Partner API`. Без правил все external-вызовы попадают в один обобщённый «External services».

### Шаг 4 — Service splitting

![Service splitting — правила разбиения процесса на несколько Service](screenshots/day-3-4/service-object/settings/builtinservice-splitting-rules/Service-splitting-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Service Detection → Service splitting**. Прямая ссылка: `https://guu84124.live.dynatrace.com/ui/settings/builtin:service-splitting-rules`.

**Что такое Service splitting.** Механизм для **разбиения одного процесса на несколько Service** внутри Dynatrace. По дефолту один Java/Node.js процесс даёт один Service. Service splitting позволяет внутри процесса выделить несколько логических сервисов — обычно по URL-паттерну или endpoint.

**Пример типового правила.** Java-процесс Tomcat, внутри 3 web-приложения: `/retail-api`, `/corporate-api`, `/admin`. Без splitting — один Service `Tomcat @ host:port`. С правилами splitting — три Service: `Retail API`, `Corporate API`, `Admin Interface`.

**Отличие от Service Detection rules (Тема 7 Дня 2):**
- Service Detection rules — это универсальный механизм создания Services.
- Service splitting — его частный случай для **разделения по URL внутри одного процесса**.

На этой странице админ управляет правилами splitting для всех процессов в окружении.

---

## 🎓 ТЕОРИЯ — что такое Service в модели Dynatrace

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Services — сущность сервиса](https://docs.dynatrace.com/docs/shortlink/services)

### Service как логическая, а не физическая сущность

**Service — это «логический образ работы процесса».** Физически на хосте работает JVM (например, Tomcat), но в Dynatrace это может быть представлено:
- Одним Service (если правила splitting не заданы).
- Или несколькими Service (если Tomcat обслуживает несколько бизнес-функций).

Противоположный случай: **несколько инстансов одного приложения** на разных хостах и в разных контейнерах представляются как **один Service** с несколькими Process Groups под ним. Это логическая абстракция — «три реплики payment-service — это один Payment Service».

### Роль Service в Smartscape

Service — это **центральное звено Smartscape**. Над ним — Applications (frontend, откуда приходят запросы). Под ним — Process Groups и Hosts (где он работает). По бокам — другие Service (куда он ходит и откуда ему приходит трафик).

Все PurePath-ы создаются на уровне Service: span открывается при входе в Service и закрывается при выходе. Таким образом Service — это естественная единица анализа производительности.

### Детекция как основа observability

Правильно настроенная детекция Service — основа качественной observability. Типовые ошибки:

- **Недоразбиение** (один Service на весь Tomcat) — метрики бизнес-функций смешиваются, невозможно раздельное SLI.
- **Переизбыток разбиения** (каждый endpoint как Service) — Smartscape захламляется, метрики фрагментируются.
- **Неправильное именование** — Service появляются и исчезают при перевыкатке приложения, ломают исторические дашборды.

### Air-gapped specifics

Все правила детекции хранятся в кластере, применяются OneAgent локально. Никаких внешних сервисов не требуется.
