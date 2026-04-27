> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 8 из 14: «Ключевые пользовательские действия + дополнительные свойства»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:user-action-custom-metrics -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [Real User Monitoring — Managed](https://docs.dynatrace.com/managed/shortlink/rum)
- [User actions — RUM concepts](https://docs.dynatrace.com/managed/shortlink/user-actions)
- [Applications — Web/Mobile/Custom](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/applications)
- [Custom applications — OpenKit](https://docs.dynatrace.com/managed/observe/digital-experience/custom-applications)
- [Create calculated metrics for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/rum-calculated-metrics-web)

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

*Что такое User Action.* В RUM — взаимодействие пользователя с интерфейсом, обычно сопровождающееся обращением к серверу. Dynatrace автоматически распознаёт три основных типа:

- **Load actions** — переход на URL: загрузка страницы со всеми ресурсами (HTML, CSS, JS, картинки). Длительность измеряется от navigation start до завершения `onload`.
- **XHR actions** — действие, инициировавшее `XMLHttpRequest` или `fetch()`. Длительность охватывает все асинхронные запросы и связанные DOM-изменения.
- **Custom actions** — программно создаются через RUM JavaScript API (для измерения чисто JS-логики без сетевых вызовов).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/user-actions -->

*User action custom metrics* — механизм **дополнительных метрик**, вычисляемых на основе user actions. Создаются через **Web → application → Impact of user actions on performance → Analyze performance → Create metric**. Лимиты: до 500 метрик на окружение и до 100 метрик на приложение. Только новые данные попадают в метрику — историю задним числом не пересчитывают.

Примеры:

- `payment_amount` — сумма платежа, извлекается из user action отправки формы.
- `login_method` — способ логина (SMS, биометрия, пароль).
- `product_page_views` — количество просмотров страниц продуктов.

*Польза.* Метрики важны для бизнес-аналитики, доступны в Data Explorer и могут служить SLI.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/rum-calculated-metrics-web -->

### Шаг 2 — Custom RUM Enablement

![Custom RUM Enablement — включение Custom apps RUM](screenshots/day-3-4/key-actions/settings/builtinrum.custom.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.custom.enablement`.

*Custom applications* — тип RUM для всех «цифровых точек контакта», которые не Web и не Mobile: rich client (десктоп), IoT-устройства, голосовые интерфейсы (например, Alexa Skills) и тому подобные. Инструментирование делается через **Dynatrace OpenKit** — открытые библиотеки на GitHub с API для разработчиков.

**На странице:** главный тумблер Custom RUM и cost control.

*Типовое применение в банке.* Банкоматы с кастомным UI, десктопные приложения для кассиров — там, где нет браузера и нет нативного мобильного OneAgent.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/custom-applications -->

### Шаг 3 — Resource types

![Resource types — настройка типов ресурсов, отслеживаемых в RUM](screenshots/day-3-4/key-actions/settings/builtinrum.web.resource-types/Resource-types-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.resource-types`.

*Что такое Resources в RUM.* При загрузке страницы браузер подгружает ресурсы: CSS, JS, картинки, шрифты, XHR-запросы. RUM собирает по каждому: URL, время загрузки, размер, статус.

*Resource types.* По умолчанию Dynatrace определяет тип ресурса по расширению файла. Эта настройка нужна, когда расширения нет или оно нестандартное (например, REST endpoint без `.json`, OpenDocument-файлы, динамические URL): через Java regex прописываем правило — какие URL получают какой Primary resource type и опциональный Secondary resource type. Это override классификации, не enable/disable отдельных категорий.

### Шаг 4 — Resource URL cleanup rules

![Resource URL cleanup rules — правила нормализации URL ресурсов](screenshots/day-3-4/key-actions/settings/builtinrum.web.resource-cleanup-rules/Resource-URL-cleanup-rules-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.resource-cleanup-rules`.

*Проблема.* Многие URL содержат динамические элементы — IDs из REST API, query strings (например, случайные cache-busting аргументы) и session-данные. Без нормализации каждый такой ресурс уникален — нельзя агрегировать метрики «сколько в среднем грузится main.js».

*Cleanup rules* — правила нормализации URL. Примеры:

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

- **Business events** — отдельный поток событий, отправляемый приложением через API. Каждое событие — атомарная запись с произвольными атрибутами.
- **Custom metrics** — дополнительные метрики, привязанные к user actions RUM.

**Когда что.** Business events — когда важны атомарные события с полной трассировкой (каждый совершённый платёж как отдельная запись с суммой, ID транзакции, признаком фрода). Custom metrics — для агрегированных показателей по user actions, которые нужно строить графиками и использовать в SLO.

### Air-gapped specifics

Всё локально. Custom metrics хранятся в Cassandra как любые метрики Dynatrace. OpenKit-библиотеки (для Custom applications) распространяются как отдельный артефакт — банку нужно держать их в своём внутреннем Maven / npm / GitHub-зеркале.
