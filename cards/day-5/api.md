---
topic_id: api
day_id: day-5
timing_min: 25
verified: 2026-07-12
---
## ГДЕ
Два живых экрана. Список токенов: User menu → Access tokens, route `/ui/access-tokens`.
Общая политика: Settings → Security → Access token settings, route `/ui/settings/builtin:tokens.token-settings`.

## ЗАЧЕМ
Dynatrace API это REST поверх HTTPS с JSON-ответами: через него метрики уезжают в BI, CI/CD шлёт custom deployment-events, ansible/terraform проставляет теги, а скрипт забирает проблемы для мессенджера.
Токен заменяет логин/пароль, а scope ограничивает, что этому токену разрешено. Тема показывает, где токены живут, какая на них политика и какие сценарии интеграции типичны.

## ЦИФРЫ
- Токен это три части через точку prefix.public.secret: public-портион 24 символа, secret-портион 64 символа; secret хранится на уровне пароля, при утечке ротируем немедленно.
- Префиксы токенов на экране: dt0s01 (API tokens, авторизация и SCIM), dt0s02 (OAuth2 clients для Dynatrace Apps), dt0s16 (Platform tokens для programmatic access); в заголовке запроса идёт `Authorization: Api-Token dt0s01.ABC***XYZ`.
- Срок действия токена на выбор: 1 день, 30 дней, 1 год или unlimited; для production обычно 1 год.
- Ротация секретов по политике каждые 90 дней; Token settings через Maximum token expiration режет максимум (политика 90 дней → токен «на 1 год» создать нельзя).
- Last used: если токен не использовался 6+ месяцев, это кандидат на удаление.
- Rate limit: превышение отдаёт HTTP 429 с заголовком Retry-After; точная цифра «N запросов в минуту» одной таблицей в /managed/-доке не зафиксирована. Разгрузка: батч до 1000 метрик одним запросом, кэш списка сущностей раз в 5 минут, pull-опрос раз в 30 сек.

## ЕСЛИ→ТО
- ЕСЛИ токен утёк → отзываем только его, остальные интеграции продолжают работать (отдельный токен на интеграцию с минимальным scope); один общий токен пришлось бы перегенерировать и переписать всюду разом.
- ЕСЛИ Maximum token expiration в Token settings = 90 дней → пользователь не создаст токен «на 1 год», регулярная ротация секретов выполняется принудительно.
- ЕСЛИ air-gapped и исходящие соединения от Dynatrace закрыты → алерты берём pull-моделью (скрипт сам раз в 30 сек дергает `GET /api/v2/problems?status=OPEN`), а не webhook'ом наружу.
- ЕСЛИ превышен rate limit → приходит HTTP 429 с Retry-After: ждём указанные секунды и повторяем (backoff), запросы заранее батчим и кэшируем.

## ЗАПАСНОЙ ПЛАН
Если `/ui/access-tokens` закрыт (на демо нет прав на управление токенами), вживую токен не создаю: показываю снимок Access tokens из курса, проговариваю колонки Token name и Last used и кнопку Generate new token.
Строение токена prefix.public.secret объясняю на маскированном примере `dt0s01.ABC***XYZ`, реальный secret-портион на экран не вывожу.
Экран Token settings при отсутствии доступа тоже разбираю по снимку из курса: Maximum token expiration, Require expiration date, Token audit logging.

## ВОПРОСЫ АУДИТОРИИ
- «Чем отличаются префиксы dt0s01, dt0s02, dt0s16?» Ответ: dt0s01 это API tokens для авторизации и SCIM, dt0s02 это OAuth2 clients для Dynatrace Apps, dt0s16 это Platform tokens для programmatic access; для обычного вызова API идёт dt0s01 в заголовке Authorization.
- «Какой у API rate limit?» Ответ: точная цифра «N запросов в минуту» одной таблицей в /managed/-доке не зафиксирована (зависит от endpoint'а и версии), признак превышения это HTTP 429 с заголовком Retry-After, на который и делаем backoff.
- «Как держать конфиг тенанта как код в закрытом контуре?» Ответ: Monaco (Monitoring as Code), CLI держит alerting profiles, dashboards и monitor settings в Git и применяет один набор YAML к нескольким тенантам (основной ЦОД + резервный), исключая ручной drift.
