> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 9 из 14: «Сессии пользователей: структура, атрибуты, Session Replay»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/user-sessions -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [User sessions: Managed RUM](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-session)
- [Session Replay: overview](https://docs.dynatrace.com/managed/shortlink/session-replay)
- [Configure Session Replay for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/configure-session-replay-web)
- [Export user sessions](https://docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/export-session-data)
- [Real User Monitoring: Managed](https://docs.dynatrace.com/managed/shortlink/rum)

## 📍 КАРТА: пять страниц про сессии и Session Replay

Термины темы: `Session / сессия`, `Session Replay / воспроизведение сессии / запись действий пользователя`, `DOM snapshot / снимок DOM`, `Masking / маскирование sensitive-элементов`, `Consent banner / баннер согласия`, `ПД / персональные данные`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| Session Replay: вход | **Application Observability → Frontend → Session Replay** | `https://guu84124.live.dynatrace.com/ui/user-sessions/replay-landing` |
| Session Replay cookie | **Settings → Web and mobile monitoring → Session Replay → Cookie** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.cookie` |
| Session Replay resource capturing | **Settings → Web and mobile monitoring → Session Replay → Resource capturing** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.web.resource-capturing` |
| User session exports | **Settings → Web and mobile monitoring → User session exports** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:elasticsearch.user-session-export-settings-v2` |

---

## 🎬 Работа с сессиями на пяти экранах

### Шаг 1: User sessions (список сессий)

![User sessions: список пользовательских сессий](screenshots/day-3-4/sessions/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/user-sessions`. Разбирался в Дне 1, Тема 4 (DEM). Содержит список всех сессий с фильтрами (Analysis over time, Application type, Application versions, Applications, User experience score, Errors and annoyances, Conversions and bounces, Users, Browsers, Internet service provider, Operating systems, Locations).

### Шаг 2: Session Replay landing

![Session Replay landing: страница входа в Session Replay](screenshots/day-3-4/sessions/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/user-sessions/replay-landing`.

*Что такое Session Replay.* Функциональность записи и воспроизведения пользовательских сессий. Dynatrace перехватывает все DOM-изменения в браузере, сохраняет серией snapshots и позволяет воспроизвести сессию как фильм: клики, перемещение курсора, прокрутка.

*Зачем.* Жалоба «не могу войти, кнопка не работает». Без Session Replay инженер гадает. С Session Replay видит точно: куда пользователь кликал, как отвечала страница, что появлялось, что нет. Минута просмотра заменяет часы диагностики.

*Ограничения по платформам.* Session Replay поддерживается для Web и Mobile (нативные iOS / Android). На гибридных и кросс-платформенных фреймворках Cordova, React Native, Flutter, Xamarin, .NET MAUI запись сессий недоступна.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/session-replay -->

### Шаг 3: Session Replay cookie

![Session Replay cookie: настройка состояния записи сессии](screenshots/day-3-4/sessions/settings/builtinsessionreplay.cookie/Session-Replay-state-cookie-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:sessionreplay.cookie`.

*Что настраивает.* Имя и параметры cookie, в которой хранится состояние согласия пользователя на запись Session Replay. Связка типовая: на странице приложения опубликован consent banner; при согласии в cookie кладётся положительное значение, и приложение вызывает `dtrum.enableSessionReplay(...)`: запись начинается. При отказе или удалении cookie вызывается `dtrum.disableSessionReplay()`.

*Для compliance* (GDPR, закон РК о персональных данных). Пользователь должен иметь возможность управлять согласием. Session Replay может фиксировать чувствительные данные: содержимое полей формы, баланс, частично адрес. Даже с маскированием риск остаётся. Поэтому в строгих компаниях запись включается только в **Opt-in mode**: до явного согласия Session Replay не пишет ничего.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/configure-session-replay-web -->

### Шаг 4: Session Replay resource capturing

![Session Replay resource capturing: настройка захвата ресурсов для Replay](screenshots/day-3-4/sessions/settings/builtinsessionreplay.web.resource-capturing/Resource-capture-for-Session-Replay-Environment-Settings-Demo-live-Demo-Live-Dyn.png)

Путь: `/ui/settings/builtin:sessionreplay.web.resource-capturing`.

*Зачем.* Для корректного воспроизведения Session Replay должен захватывать не только DOM, но и **внешние ресурсы**: CSS, шрифты, картинки. Иначе через неделю ресурсы могут быть недоступны (cache invalidated), и запись выглядит криво.

Стили (stylesheets) захватываются автоматически: без них ни одна запись не будет выглядеть как реальный экран пользователя. На этой странице настраивается дополнительный захват картинок и шрифтов с правилами URL: что включить, что исключить.

*Trade-off.* Больше захвата: точнее воспроизведение и больший объём данных. Типовое решение: stylesheets оставляют по умолчанию, шрифты добавляют выборочно, картинки чаще отключают (слишком тяжело).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/configure-session-replay-web -->

### Шаг 5: User session exports

![User session exports: экспорт сессий во внешние системы](screenshots/day-3-4/sessions/settings/builtinelasticsearch.user-session-export-settings-v2/User-session-exports-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:elasticsearch.user-session-export-settings-v2`.

*Что это.* Стриминг данных завершённых сессий во внешний HTTPS-endpoint. Endpoint должен принимать `PUT` или `POST`, возвращать `200`, contentType: `application/json` или `application/x-ndjson`. Распространённый сценарий: собственный кластер Elasticsearch банка (URL вида `https://<host>:9200/_bulk`, NDJSON). Аутентификация: Basic auth или OAuth 2.0 client credentials. До трёх endpoint'ов на тенант, можно ограничить export по management zones.

Типовые применения:

- **Долгосрочного хранения** (compliance, аудит). В Dynatrace сессии живут до 35 дней (RUM Classic retention), для юридических требований нужны годы.
- **Интеграции с корпоративной аналитикой.** BI-системы анализируют сессии.
- **Fraud detection.** Детальные сессии помогают SOC.

*Триггеры отправки batch'а.* 1000 завершённых сессий, или объём bulk превысил ~896 KB, или прошло 30 секунд без новых завершений: что наступит первым.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/export-session-data -->

---

## 🎓 ТЕОРИЯ: анатомия пользовательской сессии в Dynatrace

### Структура одной сессии

Сессия = все действия одного пользователя в одном браузере от открытия сайта до ухода. Содержит:

- **Session ID**: уникальный идентификатор.
- **User ID**: идентификатор пользователя (если авторизован).
- **Session start/end timestamp**.
- **Duration**: длительность.
- **User actions**: последовательность действий.
- **Pages visited**: страницы.
- **Errors**: JavaScript-ошибки.
- **XHR/fetch requests**: все сетевые запросы.
- **Session Replay recording** (если включено).

### Когда заканчивается сессия

- **Web**: после **30 минут** браузерной неактивности, либо при закрытии вкладки/браузера.
- **Mobile (нативные iOS / Android)**: после **10 минут** неактивности либо при закрытии / force-stop приложения.
- **Custom apps (через OpenKit)**: после **10 минут** без новых custom actions.
- В любом случае максимальная длительность сессии ограничена **6 часами**: после этого автоматически открывается новая.
- Сессия может быть завершена явно из приложения через JS API: `dtrum.endSession()`.

Дополнительно: если за сессию накапливается ~200 user actions, Dynatrace автоматически разрезает её на части: для предсказуемости анализа и без дополнительной оплаты.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-session -->

### Связь с сервисной стороной

Каждый XHR-запрос из сессии связан с backend PurePath через `x-dynatrace` header. В карточке сессии при клике на запрос открывается full trace от браузера до базы данных, это **end-to-end observability**, уникальное для Dynatrace.

### Session Replay: этические и юридические аспекты

- **Персональные данные в записи.** Запись может содержать всё, что видит пользователь: имя, email, телефон, адрес, частично номер карты. Это ПД.
- **Masking modes.** Доступно несколько режимов: **Mask all** (по умолчанию максимально жёсткий: маскируется весь текст, ввод, атрибуты и картинки), **Mask user input**, **Allow list** (разрешаем только перечисленное), **Block list** (маскируем только перечисленное). Для отдельных элементов: атрибут `data-dtrum-mask` прямо в HTML.
- **Recording vs Playback masking.** Маскирование настраивается отдельно при записи (данные не покидают браузер) и при воспроизведении (дополнительный слой для оператора). Просмотр без маскирования контролируется отдельным permission.
- **Что маскируется автоматически.** Поля для ввода паролей (`input type=password`).
- **Согласие.** Рекомендуется явное согласие через consent banner и Opt-in mode. Без согласия: юридический риск.

*Типовая политика.* Session Replay включается для внутренних корпоративных приложений (портал для сотрудников) и редко для клиентских: там нужна сложная схема получения согласия. Клиентские сайты часто ограничиваются метриками без визуального Replay.

*Cost / traffic control.* Доля записанных сессий ограничивается двумя параметрами: общим cost control RUM и cost control Session Replay. Реальная доля = произведение двух процентов: например 50% × 20% = 10% всех сессий с записью.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/configure-session-replay-web -->

### Air-gapped specifics

Session Replay storage: в кластере, локально. Никаких внешних вызовов. ПД остаются внутри контура, compliance упрощается по сравнению с SaaS. User session export, если нужен, на собственный Elasticsearch внутри банка.
