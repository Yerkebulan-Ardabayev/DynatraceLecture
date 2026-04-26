> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 8 из 14: «Ключевые пользовательские действия + дополнительные свойства»

## 📍 КАРТА — четыре страницы про настройку user actions и resources

Термины темы: `User action / действие пользователя / клик или переход`, `Custom metric / кастомная метрика`, `Resource / ресурс / CSS / JS / картинка / XHR`, `Custom RUM / RUM для нестандартных приложений` (ATM, Smart TV, Electron).

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User action custom metrics | **Settings → Web and mobile monitoring → User action custom metrics** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:user-action-custom-metrics` |
| Custom RUM Enablement | **Settings → Web and mobile monitoring → Custom app → Enablement** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.custom.enablement` |
| Resource types | **Settings → Web and mobile monitoring → Web → Resource types** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.resource-types` |
| Resource URL cleanup rules | **Settings → Web and mobile monitoring → Web → Resource URL cleanup rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.resource-cleanup-rules` |

---

## 🎬 Работа с user actions на четырёх экранах

### Шаг 1 — User action custom metrics

![User action custom metrics — кастомные метрики для действий пользователей](screenshots/day-3-4/key-actions/settings/builtinuser-action-custom-metrics/User-action-custom-metrics-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:user-action-custom-metrics`.

*Что такое User Action.* В RUM — каждое осознанное действие пользователя: клик по кнопке, переход на страницу, отправка формы, XHR-запрос. Dynatrace распознаёт и трекует автоматически.

*User action custom metrics* — механизм **дополнительных метрик**, вычисляемых на основе user actions. Примеры:

- `payment_amount` — сумма платежа, извлекается из user action отправки формы.
- `login_method` — способ логина (SMS, биометрия, пароль).
- `product_page_views` — количество просмотров страниц продуктов.

*Польза.* Метрики важны для бизнес-аналитики, доступны в Data Explorer и могут служить SLI.

### Шаг 2 — Custom RUM Enablement

![Custom RUM Enablement — включение Custom apps RUM](screenshots/day-3-4/key-actions/settings/builtinrum.custom.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.custom.enablement`.

*Custom applications* — тип RUM для нестандартных приложений: Smart TV app, десктопный Electron-клиент, IoT-устройство. Используется Custom RUM SDK с ручной инструментацией.

**На странице:** главный тумблер Custom RUM и cost control.

*Типовое применение.* Применяется редко. Случаи: банкоматы с кастомным UI, десктопные приложения для кассиров.

### Шаг 3 — Resource types

![Resource types — настройка типов ресурсов, отслеживаемых в RUM](screenshots/day-3-4/key-actions/settings/builtinrum.web.resource-types/Resource-types-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.resource-types`.

*Что такое Resources в RUM.* При загрузке страницы браузер подгружает ресурсы: CSS, JS, картинки, шрифты, XHR-запросы. RUM собирает по каждому: URL, время загрузки, размер, статус.

*Resource types.* Настройка, какие типы ресурсов трекать. По умолчанию почти всё включено: images, scripts, stylesheets, XHR, fetch, fonts. Можно отключить, например, tracking картинок — для снижения объёма данных.

### Шаг 4 — Resource URL cleanup rules

![Resource URL cleanup rules — правила нормализации URL ресурсов](screenshots/day-3-4/key-actions/settings/builtinrum.web.resource-cleanup-rules/Resource-URL-cleanup-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.resource-cleanup-rules`.

*Проблема.* Многие URL содержат уникальные параметры (`?v=12345`, `/cache/abc-xyz.js`, `?sessionId=...`). Без нормализации каждый ресурс в статистике уникален — нельзя агрегировать метрики «сколько в среднем грузится main.js».

*Cleanup rules* — правила нормализации. Примеры:

- Убрать query parameters `?v=*` — единый URL для всех версий.
- Убрать hash в пути `/cache/hash-*.js` — общий паттерн.
- Убрать session ID из path.

После применения ресурс группируется по каноническому URL, статистика становится осмысленной.

---

## 🎓 ТЕОРИЯ — роль user actions в бизнес-мониторинге

### Обычные user actions vs Custom metrics

**Обычные user actions** — это базовая часть RUM, автоматически трекается: клики, переходы, timing каждого действия. Это основа метрик типа User experience score, conversions, bounce rate.

**Custom metrics** — это бизнес-слой поверх user actions. Они позволяют извлекать из каждого действия дополнительные данные (сумма платежа, выбранный продукт) и строить по ним бизнес-срезы.

### Business events vs Custom metrics

В Dynatrace есть два похожих механизма:
- **Business events** — отдельный поток данных, отправляемый приложением через API в Grail (в SaaS) или в event storage (в Managed). Используется для серьёзной бизнес-аналитики.
- **Custom metrics** — дополнительные метрики, привязанные к user actions RUM.

**Когда что.** Business events — когда важны атомарные события с полной трассировкой (каждый совершённый платёж как отдельная запись). Custom metrics — для агрегированных показателей по user actions.

### Air-gapped specifics

Всё локально. Custom metrics хранятся в Cassandra как любые метрики. Custom RUM SDK распространяется через customer portal → внутренний Maven/CocoaPods репозиторий банка.
