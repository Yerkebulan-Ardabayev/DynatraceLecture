---
topic_id: sessions
day_id: day-3-4
timing_min: 30
verified: 2026-07-12
---
## ГДЕ
Тема живёт на пяти экранах. Список сессий: Application Observability → Frontend → User sessions, route `/ui/user-sessions` (разбирался в Дне 1, Тема 4).
Session Replay landing: Frontend → Session Replay, route `/ui/user-sessions/replay-landing`.
Три страницы настроек: Settings → Web and mobile monitoring → Session Replay → Cookie `/ui/settings/builtin:sessionreplay.cookie`, Resource capturing `/ui/settings/builtin:sessionreplay.web.resource-capturing`, User session exports `/ui/settings/builtin:elasticsearch.user-session-export-settings-v2`.

## ЗАЧЕМ
Сессия это все действия одного пользователя в одном браузере от открытия сайта до ухода: Session ID, User actions, страницы, ошибки, XHR/fetch, при желании запись Session Replay.
Session Replay воспроизводит сессию как фильм (клики, курсор, прокрутка) и заменяет часы диагностики минутой просмотра.
Каждый XHR связан с backend PurePath через заголовок x-dynatrace: клик по запросу открывает full trace от браузера до базы, это end-to-end observability.

## ЦИФРЫ
- Web-сессия закрывается после 30 минут неактивности (или закрытия вкладки), Mobile и custom apps через OpenKit после 10 минут, максимум длительности 6 часов, дальше открывается новая.
- Около 200 user actions за сессию, и Dynatrace автоматически режет её на части, для предсказуемости анализа и без доплаты.
- RUM-сессии в Classic хранятся 35 дней; для аудита и юридических требований данные экспортируют наружу.
- Батч экспорта уходит по первому из трёх триггеров: 1000 завершённых сессий, объём bulk выше ~896 KB, либо 30 секунд без новых завершений.
- Реальная доля записанных сессий = RUM cost control × Session Replay cost control, например 50% × 20% = 10%.
- Export endpoint: PUT или POST, ответ 200, contentType application/json или application/x-ndjson, до трёх endpoint'ов на тенант.

## ЕСЛИ→ТО
- ЕСЛИ пользователь не дал согласия через consent banner (Opt-in mode) → `dtrum.enableSessionReplay(...)` не вызывается и Session Replay не пишет ничего; при отказе или удалении cookie срабатывает `dtrum.disableSessionReplay()`.
- ЕСЛИ приложение на Cordova, React Native, Flutter, Xamarin или .NET MAUI → Session Replay недоступен: запись поддерживается только для Web и нативных Mobile (iOS / Android).
- ЕСЛИ masking оставлен на дефолте Mask all → маскируется весь текст, ввод, атрибуты и картинки; переключение на Mask user input открывает всё, кроме пользовательского ввода (поля `input type=password` маскируются автоматически в любом режиме).
- ЕСЛИ включить в resource capturing захват картинок → воспроизведение точнее, но объём данных растёт; типовое решение: stylesheets по умолчанию, шрифты выборочно, картинки чаще отключить.

## ЗАПАСНОЙ ПЛАН
Если демо-тенант без write-прав и страницы Session Replay серые: показываю снимки из курса и проговариваю связку consent banner → cookie → `dtrum.enableSessionReplay(...)`.
Session Replay в демо на клиентских сайтах не включаю: проговариваю, что там нужна сложная схема согласия, а запись чаще берут для внутренних порталов сотрудников.
Про закрытый контур говорю честно: Session Replay хранится в кластере локально, ПД не покидают контур, внешних вызовов нет; user session export, если нужен, настраивают на собственный Elasticsearch банка.
Лекторский сценарий: workshop/day-3.md, блок 4 и workshop/day-4.md, блок 4. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Когда сессия считается завершённой?» Ответ: Web после 30 минут неактивности или закрытия вкладки, Mobile и custom apps после 10 минут, в любом случае максимум 6 часов, а явно закрыть можно через `dtrum.endSession()`.
- «Не утекут ли персональные данные в записи?» Ответ: в закрытом контуре запись лежит в кластере локально без внешних вызовов, плюс masking (дефолт Mask all прячет весь текст и ввод, поля password всегда), а без согласия через Opt-in mode Replay не пишет ничего.
- «Зачем экспортировать сессии наружу, если они уже в Dynatrace?» Ответ: в Classic сессии живут 35 дней, а для аудита и юридических требований нужны годы, поэтому их стримят на собственный Elasticsearch банка (PUT или POST, ответ 200, NDJSON).
