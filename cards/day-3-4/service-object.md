---
topic_id: service-object
day_id: day-3-4
timing_min: 26
verified: 2026-07-12
---
## ГДЕ
Четыре экрана. Список сервисов: Application Observability → Services, route `/ui/services`.
Правила Full Web Services: Settings → Service Detection → Rules for Full Web Services, route `/ui/settings/builtin:service-detection.full-web-service`.
Правила External Web Services: Settings → Service Detection → Rules for External Web Services, route `/ui/settings/builtin:service-detection.external-web-service`.
Service splitting: Settings → Service Detection → Service splitting, route `/ui/settings/builtin:service-splitting-rules`.

## ЗАЧЕМ
Service, это логический образ работы процесса и центральное звено Smartscape: сверху Applications, снизу Process Groups и Hosts, по бокам другие сервисы.
Все PurePath создаются на уровне Service (span открывается на входе, закрывается на выходе), поэтому сервис это естественная единица анализа производительности.
Детекция определяет, во что превратится процесс: один Service или несколько, а правильная детекция это основа observability.

## ЦИФРЫ
- Список на снимке темы: 241 Services (у вашего тенанта цифры могут быть другими).
- Четыре экрана темы: Services, Rules for Full Web Services, Rules for External Web Services, Service splitting.
- Правила Full Web Services: переименование и объединение сервисов; базовая идентификация по имени сервиса и targetNamespace из WSDL.
- Splitting-пример: один Tomcat-процесс с 3 web-приложениями (`/retail-api`, `/corporate-api`, `/admin`) даёт три Service вместо одного.
- Механизм в Managed Classic: классический Service Detection v1 (SDv1); Service Detection v2 со сплиттингом по resource attributes для OpenTelemetry не задействован.

## ЕСЛИ→ТО
- ЕСЛИ правила splitting не заданы → один Java/Node.js процесс даёт один Service; ЕСЛИ процесс обслуживает несколько бизнес-функций → выделяю несколько Service по URL или endpoint.
- ЕСЛИ несколько инстансов одного приложения на разных хостах и контейнерах → это один Service с несколькими Process Groups под ним (три реплики payment-service это один Payment Service).
- ЕСЛИ инструментированное приложение вызывает наружу систему без OneAgent → вызов уходит в External Web Service (downstream в Service Flow), видно хост, URL, время ответа, статус, но не внутреннюю работу.
- ЕСЛИ под один вызов подходят несколько правил → срабатывает первое сверху (правила оцениваются сверху вниз): порядок правил имеет значение.

## ЗАПАСНОЙ ПЛАН
Rules-страницы (Full Web, External Web, splitting) на демо могут быть серыми или пустыми (нет write-прав): показываю снимок из курса, проговариваю логику на примере, не заявляю, что правило создано.
На списке Services проговариваю заголовок с числом сервисов и колонки; полный разбор структуры списка уже был в Дне 1 Тема 5 и Дне 2 Тема 7, здесь не повторяю.
Если спросят про Service Detection v2: честно говорю, что в изолированном Managed Classic он не задействован, работает классический SDv1, вся детекция локальна (правила хранятся в кластере, применяет OneAgent, внешних сервисов не нужно).

## ВОПРОСЫ АУДИТОРИИ
- «Чем Full Web Service отличается от обычного веб-сервиса?» Ответ: у Full Web Service интерфейс задан WSDL-контрактом (SOAP/JAX-WS), Dynatrace берёт имя и targetNamespace прямо из WSDL и точно узнаёт сервис и operation, а обычный Web request service опознаётся по триплету web server name + context root + web application ID.
- «Три реплики одного приложения на трёх хостах, это три сервиса?» Ответ: нет, это один Service с несколькими Process Groups под ним, несколько инстансов сворачиваются в одну логическую сущность.
- «Работает ли детекция сервисов в закрытом контуре?» Ответ: да, все правила детекции хранятся в кластере и применяются OneAgent локально, внешних сервисов не требуется.
