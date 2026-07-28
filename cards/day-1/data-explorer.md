---
topic_id: data-explorer
day_id: day-1
timing_min: 22
verified: 2026-07-12
---
## ГДЕ
Построение графиков: Observe and explore → Data Explorer, route `/ui/data-explorer`.
Каталог всех метрик: Observe and explore → Metrics, route `/ui/metrics`. Загрузка метрик через API `POST /api/v2/metrics/ingest`.

## ЗАЧЕМ
Метрики это первый столп observability: встроенные (OneAgent), Extensions (SNMP, JMX, JDBC), custom ingest.
Главный managed-акцент: сложные выражения пишутся на Metrics Selector, а не на DQL (DQL это SaaS-язык для Grail, в air-gapped Managed недоступен).

## ЦИФРЫ
- Каталог метрик на снимке темы: 3.1k метрик, показаны первые 500 (у вашего тенанта цифры могут быть другими).
- Лестница прореживания Metrics Classic: 0-14 дней шаг 1 мин, 14-28 дней 5 мин, 28-400 дней 1 час, 400 дней до 5 лет 1 день.
- Разрешение графика Resolution: Auto, 1 минута, 5 минут, 1 час.
- DDU-пулы кастомных метрик: уведомления на 90% и 100% квоты.

## ЕСЛИ→ТО
- ЕСЛИ по привычке из SaaS набрать в Advanced mode DQL → запрос не выполнится: в air-gapped Managed нет Grail, Data Explorer понимает только Metrics Selector.
- ЕСЛИ для процентной метрики (CPU usage) выбрать Space aggregation = Sum → получите бессмысленную сумму; для процентов корректны Average или Max, Sum уместен для счётных метрик.
- ЕСЛИ задать Split by `dt.entity.host` → отдельная линия по каждому хосту, сразу видно выброс; без разбивки одна усреднённая линия прячет проблему одного хоста.
- ЕСЛИ у кастомной метрики много dimensions с высокой вариативностью (ID запроса в значении) → cardinality explosion: десятки тысяч рядов, перерасход DDU, торможение UI.

## ЗАПАСНОЙ ПЛАН
Экран не построил график или пуст: показываю снимок Data Explorer из курса и проговариваю три зоны (слева запрос, центр график и шаблоны, справа отображение) и тумблер Advanced mode.
Про каталог: показываю снимок Metrics, объясняю связку «нашёл ключ в Metrics, вставил в Data Explorer, split by, Pin to dashboard».
Если кто-то тянется к DQL: сразу проговариваю, что в Managed это Metrics Selector, и показываю пример `builtin:service.response.time:avg`.
Лекторский сценарий: workshop/day-1.md, блок 8. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Почему тут нет DQL, как в облаке?» Ответ: DQL работает поверх Grail, это SaaS-платформа; в air-gapped Managed её нет, сложные запросы к метрикам пишутся на Metrics Selector.
- «Где смотреть расход лицензии в закрытом контуре?» Ответ: в семействе `builtin:billing.*` (Host Units, DDU, User Sessions) прямо в собственном окружении, связи наружу не нужно.
- «Почему растёт расход DDU у нашей кастомной метрики?» Ответ: скорее всего cardinality explosion из-за высоковариативных dimensions; оставить только значимые (host, service, endpoint).
