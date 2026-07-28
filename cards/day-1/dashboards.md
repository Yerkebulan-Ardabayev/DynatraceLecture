---
topic_id: dashboards
day_id: day-1
timing_min: 20
verified: 2026-07-12
---
## ГДЕ
Список панелей: Observe and explore → Dashboards, route `/ui/dashboards`.
Три страницы настроек: General settings (`/ui/settings/builtin:dashboards.general`), Preset settings (`/ui/settings/builtin:dashboards.presets`), Allowed URL pattern rules (`/ui/settings/builtin:dashboards.image.allowlist`).

## ЗАЧЕМ
Дашборд это страница виджетов; в банке их делят на три слоя по аудитории (оперативные, бизнесовые, инженерные).
Зрелый подход это dashboard as code: хранить JSON в Git и накатывать через API, чтобы правки шли через change-management.

## ЦИФРЫ
- На снимке темы: 618 дашбордов, свыше 260 авторов, свыше 500 тегов (у вашего тенанта цифры могут быть другими).
- Allowed URL pattern rules поддерживает ровно два типа правил: Starts with и Exact (Equals); опции Regular expression в документации нет.
- Пресет править нельзя, только Clone (копия в свои); виджет из Data Explorer переносится на панель кнопкой Pin to dashboard.
- Диапазон времени по умолчанию Last 2 hours, фильтр Management zones в шапке влияет на все виджеты разом.

## ЕСЛИ→ТО
- ЕСЛИ включить Allow anonymous access → автор сможет открыть дашборд по ссылке без логина, и любой с этой ссылкой увидит имена сервисов и метрики; оставить выключенным → дашборд откроется только после авторизации.
- ЕСЛИ добавить домен в Allowed URL pattern rules → картинки с него в виджетах Markdown и Image подгружаются; не добавить → Dynatrace не загрузит картинку, и встроенный внешний запрос с неё не уйдёт.
- ЕСЛИ хранить дашборды в Git как JSON (dashboard as code) → изменения едут через pull request и накат скриптом; для банковского change-management это требование.
- ЕСЛИ переключить Management zone в шапке → все виджеты всех дашбордов показывают только данные этой зоны, один дашборд обслуживает несколько команд.

## ЗАПАСНОЙ ПЛАН
Home dashboards и Limit preset visibility на демо без правил (No data to display): это ожидаемо, показываю по снимку, где стоит + Add mapping на боевом окружении.
Allowed URL pattern rules помечен Early adopter, набор опций может отличаться по сборке; на демо одно остаточное правило на dropbox, проговариваю, что в бою его убирают.
Если список дашбордов не грузится: показываю снимок с 618 и разбираю колонки (Popularity, дата изменения, Owner, метка Preset).
Лекторский сценарий: workshop/day-3.md, блок 7 и workshop/day-4.md, блок 7. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Можно ли править пресет?» Ответ: нет, только Clone (копия в свои), её уже редактируют; удобный сбор виджета через Pin to dashboard из Data Explorer.
- «Зачем белый список URL для картинок?» Ответ: без него редактор с правом Edit вставит в Markdown ссылку на свой сервер, и при каждом просмотре к нему уйдёт запрос (факт просмотра, IP, через редиректы cookies).
- «Как один дашборд обслуживает разные команды?» Ответ: через Management zone в шапке: retail видит Retail, corporate видит Corporate, дашборд один, контекст у каждого свой.
