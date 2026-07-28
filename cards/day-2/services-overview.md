---
topic_id: services-overview
day_id: day-2
timing_min: 25
verified: 2026-07-12
---
## ГДЕ
Три экрана.
Список сервисов: Application Observability → Services, route `/ui/services`. Все обнаруженные сервисы с типами, технологиями и метриками.
Правила детекции: Settings → Service Detection → Service detection rules, route `/ui/settings/builtin:service-detection-rules`. Классический механизм (SDv1), как разбить процесс на сервисы.
Новый механизм: Settings → Service Detection → Service Detection v2 for OneAgent, route `/ui/settings/builtin:service-detection-v2-for-oneagent`.

## ЗАЧЕМ
Service это логическая backend-единица (процесс или его часть). Тип сервиса (Web request, Database, Messaging, Queue listener, Remote call, External, Background activity, Custom) это метка, по которой строишь алерты и дашборды и понимаешь, какие метрики применимы.
Service detection это правила, по которым OneAgent режет процесс на логические сервисы: один Tomcat можно разбить по URL-префиксам на отдельные бизнес-сервисы.
Отвечает на «почему один процесс показывается как несколько сервисов» и «какие метрики к сервису применимы».

## ЦИФРЫ
- Services на снимке темы: 239 сервисов, днём раньше было 244 (у вашего тенанта цифры могут быть другими); количество плавает при деплойментах и удалениях.
- Service Detection v2 доступен в Managed с Cluster version 1.318+, в первую очередь для OpenTelemetry-сервисов и Adobe Experience Manager.
- Дефолт даёт один Service на процесс, хотя внутри одного Tomcat живут 10-20 бизнес-endpoint'ов: без разбиения их метрики смешиваются.
- Разбить monolith: 15 URL-паттернов → 15 Web request service detection rules → 15 отдельных Services, каждый со своими метриками.
- На демо-тенанте два nginx-ingress-controller висят на разных портах (9024 и 80,443), поэтому Dynatrace завёл два отдельных Service.

## ЕСЛИ→ТО
- ЕСЛИ сервис инструментирован OneAgent (Java / .NET / Node) → детектируется через SDv1, правила на экране Service Detection v2 на него не влияют (v2 берёт OpenTelemetry-сервисы и Adobe Experience Manager).
- ЕСЛИ дефолтная детекция дала один Service на весь Tomcat → пишем Web request service detection rule по URL-префиксу, и метрики, PurePath, проблемы делятся по логическим сервисам.
- ЕСЛИ код без входящего вызова (ночной batch, cron) → по умолчанию он не Service, нужно правило Custom service, чтобы попал в мониторинг.
- ЕСЛИ ни один сенсор не сработал → процесс падает в Generic service с минимальным набором метрик, значит технология не поддержана или нужен Custom service.

## ЗАПАСНОЙ ПЛАН
Экран Services пуст или нужных сервисов не видно: показываю снимок из курса (239 сервисов) и проговариваю левую панель фильтров, точнее фильтр Service type.
На страницах Service detection нет write-прав (демо): показываю снимок правил и проговариваю пример, как один Tomcat разбивается по URL-префиксам (`/api/payments/*`, `/api/accounts/*`, `/admin/*`) на три логических сервиса.
Тумблер Service Detection v2 серый: проговариваю, что это глобальный переключатель тенанта, а не пофазное включение по хостам; включают планово, предварительно проверив на dev-потоке OpenTelemetry, потому что названия Service могут поменяться и это заденет Alerting profiles и Dashboards.
Лекторский сценарий: workshop/day-2.md, блок 4. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Чем Web service отличается от Web request service?» Ответ: Web request service это прямой входящий HTTP (современные backend-ы), а Web service (full) остался для WSDL-описанных SOAP / JAX-WS.
- «Почему один Tomcat показывается как несколько сервисов?» Ответ: правило Service detection группирует входящие HTTP по URL-префиксу, и каждый префикс становится отдельным логическим Service со своими метриками, PurePath и проблемами.
- «На хосте nginx, Java-бэкенд и cron-скрипт: сколько сервисов увидит Dynatrace?» Ответ: скорее всего два, а не три: сервис рождается из запросов, у cron без входящих вызовов сервиса нет (его видно на уровне процесса; в мониторинг сервисов он попадёт только через Custom service).
- «Чем SDv1 отличается от SDv2 в Managed?» Ответ: SDv1 это классический механизм для OneAgent-сервисов (Java / .NET / Node), а SDv2 (Cluster 1.318+) применяется в первую очередь к OpenTelemetry-сервисам и Adobe Experience Manager.
