> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 3 из 10: «Анализ путей пользователей (Journey, Funnel)»

## 📍 КАРТА — две страницы для анализа путей пользователей

Термины темы: `Journey / путь пользователя` (абстрактная карта), `Funnel / воронка / последовательность шагов`, `Bounce / сессия с одной страницей`, `Conversion / достижение цели`, `Drop-off / потеря на шаге`, `User action rule / правило именования действий`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions (обзор с фильтрами воронки) | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| User session query (USQL для funnel и path analysis) | **Application Observability → Frontend → User sessions query** | `https://guu84124.live.dynatrace.com/ui/user-sessions/query` |

---

## 🎬 Работа с путями пользователей на двух экранах

### Шаг 1 — User sessions с фильтрами Conversions and bounces

![User sessions — список сессий с фильтром Conversions and bounces](screenshots/day-5/journeys/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions`.

**Ключевые фильтры для journey-анализа:**

- **Conversions and bounces** — разделяет сессии: с конверсией (дошёл до цели), без конверсии (ушёл), bounce (одна страница и уход).
- **User experience score** — разделяет Satisfied / Tolerating / Frustrated.

*Типовой сценарий.* Выбираем фильтр «сессии без конверсии на странице оплаты». Клик по конкретной сессии — открывается хронология user actions. Видно: пользователь открыл главную → выбрал товар → добавил в корзину → пошёл на checkout → 4 раза прожал кнопку «Оплатить», получил rage click-и → закрыл вкладку.

Это **journey-анализ на уровне одной сессии**: смотрим реальный путь одного пользователя, находим точку боли.

### Шаг 2 — User session query для funnel-анализа

![User session query — редактор USQL для построения funnel](screenshots/day-5/journeys/user-sessions/query/User-Session-Query-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/query`.

**Что здесь делать.** Пишем USQL-запрос, который считает количество сессий на каждом шаге funnel'а. Пример для платёжного сценария:

```sql
SELECT
  count(*) AS total_sessions,
  sum(IF(matchesUserActionName(useraction, 'Click on Add to cart'), 1, 0)) AS step1_add_to_cart,
  sum(IF(matchesUserActionName(useraction, 'Click on Checkout'), 1, 0)) AS step2_checkout,
  sum(IF(matchesUserActionName(useraction, 'Click on Pay'), 1, 0)) AS step3_pay,
  sum(IF(matchesUserActionName(useraction, 'Page /thank-you'), 1, 0)) AS step4_success
FROM usersession
WHERE applicationType = 'WEB_APPLICATION'
  AND startTime > now() - 1d;
```

Результат в виде одной строки:
```
total_sessions: 5000
step1_add_to_cart: 1200  (24%)
step2_checkout: 800      (67% от step1)
step3_pay: 450           (56% от step2)
step4_success: 420       (93% от step3)
```

*Вывод для бизнеса.* Из 5000 посетителей товар в корзину положили 1200. До checkout дошли 800 (потеря 33%). До оплаты 450 (потеря 44%). Успешно заплатили 420 (потеря 7%). Ключевая утечка — между checkout и кнопкой Pay. Там и надо копать.

*Почему USQL, а не готовый UI.* В облачной Dynatrace есть отдельный app **Funnels** с визуальной диаграммой. В air-gapped Managed этого app нет — то же самое делается через USQL. Результат не красивый, но точный и воспроизводимый. Можно сохранить в dashboard как tile `Custom chart` (тема API в Дне 5, Тема 10 — dashboards создаются через API).

---

## 🎓 ТЕОРИЯ — journey analysis и funnel analysis

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Real User Monitoring — user journeys](https://docs.dynatrace.com/docs/shortlink/rum)

### Разница между journey и funnel

- **Journey (путь)** — абстрактная карта, как пользователь ходит по приложению. Без привязки к цифрам. Пример: «пользователь приходит из поиска → читает статью → переходит на главную → регистрируется → делает заказ». Описывает поведение в целом.
- **Funnel (воронка)** — конкретная последовательность шагов с подсчётом, сколько пользователей прошло каждый. Жёсткий порядок: шаг 1 → шаг 2 → шаг 3.

Journey полезен для проектирования (разработчик смотрит, какие экраны нужны). Funnel — для операционки (команда видит, где теряются деньги).

### Три категории метрик путей

- **Bounce rate** — процент сессий с одной страницей. «Насколько привлекателен вход». Высокий bounce на landing page — несоответствие ожиданий (пришёл за одним, увидел другое).
- **Conversion rate** — процент сессий с конверсией. Главная метрика для бизнеса. Падает — меньше денег.
- **Drop-off rate на каждом шаге funnel** — где теряется больше всего. Форма воронки показывает bottleneck.

### Типичные сценарии

**Funnel входа в ДБО:**

1. Открытие app / login page.
2. Ввод логина.
3. Ввод пароля.
4. Запрос OTP.
5. Ввод OTP.
6. Открытие главного экрана.

*Метрика.* Процент сессий, прошедших от шага 1 до шага 6. Типовая норма — 80-90%. Значительно ниже → сломан auth-pipeline.

**Funnel перевода средств:**

1. Клик «Новый перевод».
2. Выбор получателя.
3. Ввод суммы.
4. Подтверждение.
5. Ввод OTP.
6. Успех.

*Метрика.* Процент сессий с шагом 1, дошедших до шага 6. Типовая норма — 70-80%. Падение ниже 50% — инцидент.

**Funnel открытия депозита:**

1. Клик «Открыть депозит».
2. Выбор продукта.
3. Ввод суммы и срока.
4. Согласие с условиями.
5. Подписание через OTP или биометрию.
6. Успех.

На шаге 4 часто отваливаются. Dynatrace помогает отличить ожидаемое поведение (2 минуты листания условий) от проблемы (2 минуты тапов по кнопке «Согласен», которая не срабатывает — rage click и сломанный обработчик).

### Как user actions именуются

Чтобы funnel работал, user actions должны быть **именованы осмысленно**. По умолчанию Dynatrace даёт имена автоматически: `Click on "Submit"`, `Load of /checkout`, `Touch on "Оплатить"`. В реальном банковском приложении этих автоматических имён обычно недостаточно — нужно настроить **user action rules**:

- `Page /payment/process.html?stage=*` → переименовать в `Payment step {stage}`.
- `Click on #confirm-payment-btn` → переименовать в `Confirm payment`.

Rules настраиваются в Settings → Web and mobile monitoring → Application → User actions → Rules. После переименования funnel-запросы становятся стабильными: даже если разработчик переделал HTML-класс кнопки, rule можно обновить, USQL не изменится.

### Связь с бэкендом

Journey analysis силён именно тем, что каждый user action связан с backend-транзакциями. Если пользователь завис на шаге 4 funnel'а, Dynatrace показывает не только факт задержки, а **в каком backend-сервисе она произошла**:

```
User action: "Confirm payment" (2800 ms)
  └── XHR /api/payment/confirm (2700 ms)
        └── PurePath: payment-service → 2500 ms (95% времени)
              └── Service method: ConfirmPaymentUseCase.execute
                    └── SQL SELECT account_balance FROM ...  — 2300 ms ← вот тут
```

Это называется **end-to-end tracing** — от клика пользователя до конкретного SQL-запроса. Ключевое отличие Dynatrace от чистых продуктов аналитики (Google Analytics, Amplitude): те дают funnel, но не дают root cause для технической части.

### DEM-концепция Dynatrace

**DEM (Digital Experience Monitoring)** — зонтичный термин в Dynatrace для всего, что касается пользовательского опыта: RUM + Synthetic + Session Replay + Business Analytics + Mobile. Journey analysis — один из инструментов DEM.

Логика DEM: измерять не только то, что работает в дата-центре, а то, **что испытывает пользователь**. DEM-страницу мы видели в Дне 1, Тема 4 — там общие дашборды. Сейчас мы разбираем конкретные инструменты DEM-платформы.

### User flow vs Session flow

В Dynatrace есть два визуальных инструмента, связанных с journey:

- **User flow** (в классическом UI — часть Real user monitoring карточки приложения). Диаграмма Sankey, показывает как пользователи переходят между страницами. Хорошо видны основные маршруты и точки ухода.
- **Service flow** (разбирали в Дне 3-4, Тема 2). То же самое, но для backend-сервисов — как запросы текут между микросервисами.

Два представления одного и того же factа — «система — это сеть, где узлы связаны ребрами трафика».

### Ограничения journey-анализа в Dynatrace

- **Сессии без RUM-agent не видны.** Если кто-то отключил JavaScript — нас нет. Если мобильное приложение без SDK — нас нет.
- **Приватные режимы** (incognito) могут сбрасывать session cookie.
- **Кросс-приложения journey** (пользователь начал в мобильном, продолжил в web) по умолчанию считаются разными сессиями. Чтобы связать — нужен user ID tagging (RUM-API `dtrum.identifyUser(...)`).
- **Классический UI ограничен** в визуализации funnel: одна строка с числами. Для диаграмм нужен внешний BI (Grafana, Power BI), который тянет метрики через Dynatrace API.

### Ключевые термины

- **Journey** — абстрактный путь пользователя по приложению.
- **Funnel** — последовательность конверсионных шагов с подсчётом прохождения.
- **Bounce rate** — доля одностраничных сессий.
- **Conversion rate** — доля сессий с достижением цели.
- **Drop-off** — точка максимальной потери пользователей в funnel'е.
- **User action rules** — правила именования действий.
- **End-to-end tracing** — сквозное отслеживание от клика до SQL-запроса.
- **DEM (Digital Experience Monitoring)** — зонтичный термин Dynatrace для всего клиентского опыта.
