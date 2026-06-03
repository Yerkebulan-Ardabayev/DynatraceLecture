> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 3 из 10: «Анализ путей пользователей (Journey, Funnel)»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/user-sessions -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Custom queries, segmentation, and aggregation of session data (USQL)](https://docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/custom-queries-segmentation-and-aggregation-of-session-data)
> - [Create custom user action names for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/initial-setup/create-custom-names-for-user-actions)
> - [Leverage user action and user session properties for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/analyze-and-use/action-and-session-properties)
> - [User actions](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-actions)
> - [Real User Monitoring (RUM)](https://docs.dynatrace.com/managed/shortlink/rum)

## 📍 КАРТА: две страницы для анализа путей пользователей

Термины темы: `Journey / путь пользователя` (абстрактная карта), `Funnel / воронка / последовательность шагов`, `Bounce / сессия с одной страницей`, `Conversion / достижение цели`, `Drop-off / потеря на шаге`, `User action rule / правило именования действий`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions (обзор с фильтрами воронки) | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| User session query (USQL для funnel и path analysis) | **Application Observability → Frontend → User sessions query** | `https://guu84124.live.dynatrace.com/ui/user-sessions/query` |

---

## 🎬 Работа с путями пользователей на двух экранах

### Шаг 1: User sessions с фильтрами Conversions and bounces

![User sessions: список сессий с фильтром Conversions and bounces](screenshots/day-5/journeys/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions`.

**Ключевые фильтры для journey-анализа:**

- **Conversions and bounces**: разделяет сессии: с конверсией (дошёл до цели), без конверсии (ушёл), bounce (одна страница и уход).
- **User experience score**: разделяет Satisfied / Tolerating / Frustrated.

*Типовой сценарий.* Выбираем фильтр «сессии без конверсии на странице оплаты». Клик по конкретной сессии: открывается хронология user actions. Видно: пользователь открыл главную → выбрал товар → добавил в корзину → пошёл на checkout → 4 раза прожал кнопку «Оплатить», получил rage click-и → закрыл вкладку.

Это **journey-анализ на уровне одной сессии**: смотрим реальный путь одного пользователя, находим точку боли.

**ЕСЛИ → ТО: фильтр сегмента и conversion goal.** Список сессий это прямое следствие того, что задано в фильтрах и в настройках приложения:

- ЕСЛИ задать условие сегмента (например, `Conversions and bounces` = `Converted: No` плюс `Application type: Web`) → в списке останутся только подходящие сессии и нужную видно сразу; ЕСЛИ фильтр не задавать → отдаётся весь трафик, первые 500 сессий по времени старта, и нужную теряешь в общей массе.
- ЕСЛИ в настройках приложения (**Web → приложение → More (…) → Edit → Behavior analytics → Conversion goals**) заведена цель (по destination URL, по конкретному user action, по длительности сессии или числу действий в ней) → сессия, где цель достигнута, помечается converted, и фильтры `Converted` и `Conversion goal` начинают отбирать именно её; ЕСЛИ цель не заведена → колонка Conversions пустая, отделить «дошёл до цели» от «ушёл» нечем. На приложение можно задать максимум 20 conversion goals.
<!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/digital-experience/web-applications/analyze-and-use/define-conversion-goals -->
<!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/new-user-sessions -->

### Шаг 2: User session query для funnel-анализа

![User session query: редактор USQL для построения funnel](screenshots/day-5/journeys/user-sessions/query/User-Session-Query-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/query`.

**Что здесь делать.** Пишем USQL-запрос, который считает количество user actions / сессий, прошедших через каждый шаг funnel'а. USQL даёт несколько таблиц: `usersession`, `useraction`, `userevent`, `usererror`; для funnel удобно считать действия из таблицы `useraction` по имени:

```sql
SELECT
  count(*)
FROM useraction
WHERE name = 'Click on "Add to cart"'
  AND startTime > now() - 1d;
```

Запрос повторяется для каждого шага (Add to cart, Checkout, Pay, Page /thank-you): получаем число сессий, дошедших до соответствующего действия. Сравнение этих чисел показывает потери на каждом шаге.

*Пример вывода для бизнеса.* Из 5000 сессий товар в корзину положили в 1200. До checkout дошли 800 (потеря 33%). До оплаты 450 (потеря 44%). Успешно заплатили 420 (потеря 7%). Ключевая утечка: между checkout и кнопкой Pay. Там и надо копать.

*Особенности USQL.* Запрос видит только закрытые сессии (live-сессии не учитываются). По умолчанию возвращается 50 строк, максимум через `LIMIT`: 5000. Доступ к данным: через UI или REST endpoints `/table` (плоский результат) и `/tree` (иерархический), c API token.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-segmentation/custom-queries-segmentation-and-aggregation-of-session-data -->

*Почему USQL, а не готовый UI.* В классическом UI Managed funnel-аналитика доступна именно через USQL: те же шаги (USQL-запрос на каждый шаг + сравнение). Apps-формат Funnels-диаграмм относится к SaaS-стэку и в air-gapped Managed не активен. Результат USQL можно сохранить в dashboard через API (тема API в Дне 5, Тема 10: dashboards создаются через API).

---

## 🎓 ТЕОРИЯ: journey analysis и funnel analysis

### Разница между journey и funnel

- **Journey (путь)**: абстрактная карта, как пользователь ходит по приложению. Без привязки к цифрам. Пример: «пользователь приходит из поиска → читает статью → переходит на главную → регистрируется → делает заказ». Описывает поведение в целом.
- **Funnel (воронка)**: конкретная последовательность шагов с подсчётом, сколько пользователей прошло каждый. Жёсткий порядок: шаг 1 → шаг 2 → шаг 3.

Journey полезен для проектирования (разработчик смотрит, какие экраны нужны). Funnel: для операционки (команда видит, где теряются деньги).

### Три категории метрик путей

- **Bounce rate**: процент сессий с одной страницей. «Насколько привлекателен вход». Высокий bounce на landing page: несоответствие ожиданий (пришёл за одним, увидел другое).
- **Conversion rate**: процент сессий с конверсией. Главная метрика для бизнеса. Падает: меньше денег.
- **Drop-off rate на каждом шаге funnel**: где теряется больше всего. Форма воронки показывает bottleneck.

### Типичные сценарии

**Funnel входа в ДБО:**

1. Открытие app / login page.
2. Ввод логина.
3. Ввод пароля.
4. Запрос OTP.
5. Ввод OTP.
6. Открытие главного экрана.

*Метрика.* Процент сессий, прошедших от шага 1 до шага 6. Типовая норма: 80-90%. Значительно ниже → сломан auth-pipeline.

**Funnel перевода средств:**

1. Клик «Новый перевод».
2. Выбор получателя.
3. Ввод суммы.
4. Подтверждение.
5. Ввод OTP.
6. Успех.

*Метрика.* Процент сессий с шагом 1, дошедших до шага 6. Типовая норма: 70-80%. Падение ниже 50%: инцидент.

**Funnel открытия депозита:**

1. Клик «Открыть депозит».
2. Выбор продукта.
3. Ввод суммы и срока.
4. Согласие с условиями.
5. Подписание через OTP или биометрию.
6. Успех.

На шаге 4 часто отваливаются. Dynatrace помогает отличить ожидаемое поведение (2 минуты листания условий) от проблемы (2 минуты тапов по кнопке «Согласен», которая не срабатывает: rage click и сломанный обработчик).

### Как user actions именуются

Чтобы funnel работал, user actions должны быть **именованы осмысленно**. По умолчанию Dynatrace детектирует имя действия в порядке: атрибут `data-dtname` → `nodeName` → `innerText`/`textContent` элемента. Это даёт автоматические имена вроде `Click on "Submit"`, `Load of /checkout`, `Touch on "Оплатить"`. В реальном банковском приложении этих автоматических имён обычно недостаточно: нужно настроить **user action naming rules**:

- Naming rules **отдельно для load actions и для XHR actions** (две вкладки в настройках приложения).
- Имена строятся из placeholder'ов (`{pageUrl}`, `{sourceUrl}`, `{xhrUrl}`) и пользовательских placeholder'ов (до 50 на приложение).
- Доступны processing-шаги: Extract (по разделителю), Replace (текст или ID), Regular expression.
- Лимит: до 250 правил на приложение, c приоритетом по порядку.

Rules настраиваются в Application settings → Capturing → User actions → User action naming rules. После переименования funnel-запросы становятся стабильными: даже если разработчик переделал HTML-класс кнопки, rule можно обновить, USQL не изменится.

**ЕСЛИ → ТО: нормализация имён.** От именования напрямую зависит, сойдётся ли статистика по шагу:

- ЕСЛИ имена не нормализованы → одно и то же действие, выполненное через разные UI-элементы или на разных языках интерфейса, дробится на несколько разных имён, и счётчики по шагу funnel'а размазываются; ЕСЛИ настроены naming rules → Dynatrace сводит эти варианты в одну логическую группу, и шаг funnel'а считается как одно действие.
<!-- last-verified: 2026-06-03 source: docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-actions -->

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/initial-setup/create-custom-names-for-user-actions -->

### Связь с бэкендом

Journey analysis силён именно тем, что каждый user action связан с backend-транзакциями. Если пользователь завис на шаге 4 funnel'а, Dynatrace показывает не только факт задержки, а **в каком backend-сервисе она произошла**:

```
User action: "Confirm payment" (2800 ms)
  └── XHR /api/payment/confirm (2700 ms)
        └── PurePath: payment-service → 2500 ms (95% времени)
              └── Service method: ConfirmPaymentUseCase.execute
                    └── SQL SELECT account_balance FROM ... (2300 ms) ← вот тут
```

Это называется **end-to-end tracing**: от клика пользователя до конкретного SQL-запроса. Каждый user action связан с серверным PurePath через `x-dynatrace`-заголовок, поэтому шаг funnel'а и backend-задержку под ним видно в одном trace, без перехода в отдельный инструмент.

### DEM-концепция Dynatrace

**DEM (Digital Experience Monitoring)**: зонтичный термин в Dynatrace для всего, что касается пользовательского опыта: RUM + Synthetic + Session Replay + Business Analytics + Mobile. Journey analysis: один из инструментов DEM.

Логика DEM: измерять не только то, что работает в дата-центре, а то, **что испытывает пользователь**. DEM-страницу мы видели в Дне 1, Тема 4: там общие дашборды. Сейчас мы разбираем конкретные инструменты DEM-платформы.

### User flow vs Session flow

В Dynatrace есть два визуальных инструмента, связанных с journey:

- **User flow** (в классическом UI: часть Real user monitoring карточки приложения). Диаграмма Sankey, показывает как пользователи переходят между страницами. Хорошо видны основные маршруты и точки ухода.
- **Service flow** (разбирали в Дне 3-4, Тема 2). То же самое, но для backend-сервисов: как запросы текут между микросервисами.

Два представления одного и того же factа: «система, это сеть, где узлы связаны ребрами трафика».

### Ограничения journey-анализа в Dynatrace

- **Сессии без RUM-agent не видны.** Если кто-то отключил JavaScript: нас нет. Если мобильное приложение без SDK: нас нет.
- **Приватные режимы** (incognito) могут сбрасывать session cookie.
- **Кросс-приложения journey** (пользователь начал в мобильном, продолжил в web) по умолчанию считаются разными сессиями. Чтобы связать: нужен user-ID tagging через RUM JavaScript / Mobile SDK API (передача стабильного userId, который видит и web, и mobile).
- **Классический UI ограничен** в визуализации funnel: USQL даёт цифры по шагам, без готовой диаграммы. Для визуального funnel нужен либо custom-dashboard через Dynatrace API, либо внешний BI (Grafana, Power BI), который тянет метрики через Dynatrace API.

### Ключевые термины

- **Journey**: абстрактный путь пользователя по приложению.
- **Funnel**: последовательность конверсионных шагов с подсчётом прохождения.
- **Bounce rate**: доля одностраничных сессий.
- **Conversion rate**: доля сессий с достижением цели.
- **Drop-off**: точка максимальной потери пользователей в funnel'е.
- **User action rules**: правила именования действий.
- **End-to-end tracing**: сквозное отслеживание от клика до SQL-запроса.
- **DEM (Digital Experience Monitoring)**: зонтичный термин Dynatrace для всего клиентского опыта.
