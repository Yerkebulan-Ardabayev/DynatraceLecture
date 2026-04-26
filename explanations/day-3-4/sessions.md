> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 9 из 14: «Сессии пользователей: структура, атрибуты, Session Replay»

## 📍 КАРТА — пять страниц про сессии и Session Replay

Термины темы: `Session / сессия`, `Session Replay / воспроизведение сессии / запись действий пользователя`, `DOM snapshot / снимок DOM`, `Masking / маскирование sensitive-элементов`, `Consent banner / баннер согласия`, `ПД / персональные данные`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| Session Replay — вход | **Application Observability → Frontend → Session Replay** | `https://guu84124.live.dynatrace.com/ui/user-sessions/replay-landing` |
| Session Replay cookie | **Settings → Web and mobile monitoring → Session Replay → Cookie** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.cookie` |
| Session Replay resource capturing | **Settings → Web and mobile monitoring → Session Replay → Resource capturing** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.web.resource-capturing` |
| User session exports | **Settings → Web and mobile monitoring → User session exports** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:elasticsearch.user-session-export-settings-v2` |

---

## 🎬 Работа с сессиями на пяти экранах

### Шаг 1 — User sessions (список сессий)

![User sessions — список пользовательских сессий](screenshots/day-3-4/sessions/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/user-sessions`. Разбирался в Дне 1, Тема 4 (DEM). Содержит список всех сессий с фильтрами (Analysis over time, Application type, Application versions, Applications, User experience score, Errors and annoyances, Conversions and bounces, Users, Browsers, Internet service provider, Operating systems, Locations).

### Шаг 2 — Session Replay landing

![Session Replay landing — страница входа в Session Replay](screenshots/day-3-4/sessions/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/user-sessions/replay-landing`.

*Что такое Session Replay.* Функциональность записи и воспроизведения пользовательских сессий. Dynatrace перехватывает все DOM-изменения в браузере, сохраняет серией snapshots и позволяет воспроизвести сессию как фильм — клики, перемещение курсора, прокрутка.

*Зачем.* Жалоба «не могу войти, кнопка не работает». Без Session Replay инженер гадает. С Session Replay видит точно: куда пользователь кликал, как отвечала страница, что появлялось, что нет. Минута просмотра заменяет часы диагностики.

### Шаг 3 — Session Replay cookie

![Session Replay cookie — настройка состояния записи сессии](screenshots/day-3-4/sessions/settings/builtinsessionreplay.cookie/Session-Replay-state-cookie-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:sessionreplay.cookie`.

*Что настраивает.* Имя и параметры cookie, в которой хранится состояние записи Session Replay. Пользователь явно соглашается или отказывается — это записывается в cookie.

*Для compliance* (GDPR, закон о персональных данных). Пользователь должен иметь возможность управлять согласием. Session Replay может фиксировать чувствительные данные — пароли, CVV, адрес. Даже с маскированием риск остаётся. Поэтому запись включается только с явного согласия через cookie consent banner.

### Шаг 4 — Session Replay resource capturing

![Session Replay resource capturing — настройка захвата ресурсов для Replay](screenshots/day-3-4/sessions/settings/builtinsessionreplay.web.resource-capturing/Resource-capture-for-Session-Replay-Environment-Settings-Demo-live-Demo-Live-Dyn.png)

Путь: `/ui/settings/builtin:sessionreplay.web.resource-capturing`.

*Зачем.* Для корректного воспроизведения Session Replay должен захватывать не только DOM, но и **внешние ресурсы**: CSS, шрифты, картинки. Иначе через неделю ресурсы могут быть недоступны (cache invalidated), и запись выглядит криво.

**Что настраивается:**

- Какие типы ресурсов захватывать: CSS почти всегда, картинки зависят от объёма.
- Лимит размера захваченных ресурсов.
- Ignore-правила для sensitive ресурсов.

*Trade-off.* Больше захвата — точнее воспроизведение и больший объём данных. Типовое решение: захватывают CSS и шрифты, картинки отключают (слишком тяжело).

### Шаг 5 — User session exports

![User session exports — экспорт сессий во внешние системы](screenshots/day-3-4/sessions/settings/builtinelasticsearch.user-session-export-settings-v2/User-session-exports-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:elasticsearch.user-session-export-settings-v2`.

*Что это.* Экспорт данных сессий во внешнюю Elasticsearch или другую систему. Используется для:

- **Долгосрочного хранения** (compliance, аудит). В Dynatrace сессии живут недели, для юридических требований нужны годы.
- **Интеграции с корпоративной аналитикой.** BI-системы анализируют сессии.
- **Fraud detection.** Детальные сессии помогают SOC.

*Типовое применение.* Включается опционально с учётом compliance-требований.

---

## 🎓 ТЕОРИЯ — анатомия пользовательской сессии в Dynatrace

### Структура одной сессии

Сессия = все действия одного пользователя в одном браузере от открытия сайта до ухода (или до истечения inactivity timeout). Содержит:
- **Session ID** — уникальный идентификатор.
- **User ID** — идентификатор пользователя (если авторизован).
- **Session start/end timestamp**.
- **Duration** — длительность.
- **User actions** — последовательность действий.
- **Pages visited** — страницы.
- **Errors** — JavaScript-ошибки.
- **XHR/fetch requests** — все сетевые запросы.
- **Session Replay recording** (если включено).

### Связь с сервисной стороной

Каждый XHR-запрос из сессии связан с backend PurePath через `x-dynatrace` header. В карточке сессии при клике на запрос открывается full trace от браузера до базы данных — это **end-to-end observability**, уникальное для Dynatrace.

### Session Replay — этические и юридические аспекты

- **Персональные данные в записи.** Запись может содержать всё, что видит пользователь: имя, email, телефон, адрес, частично номер карты. Это ПД.
- **Masking.** Dynatrace маскирует sensitive элементы через CSS-классы или правила. Поля с паролями (`input type=password`) маскируются автоматически.
- **Согласие.** Рекомендуется явное согласие через consent banner. Без согласия — юридический риск.

*Типовая политика.* Session Replay включается для внутренних корпоративных приложений (портал для сотрудников) и редко для клиентских — там нужна сложная схема получения согласия. Клиентские сайты часто ограничиваются метриками без визуального Replay.

### Air-gapped specifics

Session Replay storage — в кластере, локально. Никаких внешних вызовов. ПД остаются внутри контура, compliance упрощается по сравнению с SaaS.
