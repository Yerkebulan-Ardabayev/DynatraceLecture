> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 10 из 14: «Настройка порогов, аномалий и базовых линий (для apps)»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.rum-web -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [Anomaly detection — Managed](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection)
- [Adjust sensitivity for applications](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-applications)
- [Real User Monitoring — Managed](https://docs.dynatrace.com/managed/shortlink/rum)
- [Apdex ratings](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings)
- [Davis AI — anomaly detection concepts](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection)

## 📍 КАРТА — пять страниц anomaly detection для приложений

Термины темы: `Page load time / время загрузки страницы`, `User action duration / длительность действия пользователя`, `Crash rate / частота крашей`, `Apdex / индекс удовлетворённости`, `Percentile / перцентиль` (P95, P99).

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Anomaly detection for web applications | **Settings → Anomaly detection → RUM Web applications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.rum-web` |
| Anomaly detection for mobile applications | **Settings → Anomaly detection → RUM Mobile applications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.rum-mobile` |
| Anomaly detection for custom applications | **Settings → Anomaly detection → RUM Custom applications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.rum-custom` |
| Crash rate for custom apps | **Settings → Anomaly detection → RUM Custom → Crash rate increase** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.rum-custom-crash-rate-increase` |
| Crash rate for mobile apps | **Settings → Anomaly detection → RUM Mobile → Crash rate increase** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.rum-mobile-crash-rate-increase` |

---

## 🎬 Работа с порогами приложений на пяти экранах

### Шаг 1 — Anomaly detection for applications (web)

![Anomaly detection for applications — пороги для web-приложений](screenshots/day-3-4/thresholds/settings/builtinanomaly-detection.rum-web/Anomaly-detection-for-applications-Environment-Settings-Demo-live-Demo-Live-Dyna.png)

Путь: `/ui/settings/builtin:anomaly-detection.rum-web`.

**Что настраивается.** Глобальные пороги для web-приложений в RUM. По документации Dynatrace детектирует **четыре типа аномалий приложений**:

- **Key performance metric degradations** — деградация ключевых метрик user actions (включая user action duration и связанные показатели).
- **Traffic drops** — падение трафика.
- **Traffic spikes** — рост трафика.
- **Failure rate increases** — рост доли неуспешных user actions (туда же попадают JS-ошибки и request errors согласно настройкам error detection).

Каждый тип имеет два режима: **automated baselining** (Davis AI учится на реперном периоде — по умолчанию **последние 7 дней**) или **fixed thresholds** с тремя уровнями чувствительности — Low / Medium / High. При fixed thresholds для Failure rate должны нарушаться **оба** порога — относительный (%) и абсолютный (пп.).

*Критичность.* Страница — одна из ключевых для алертов по клиентским web-приложениям. Её настройка определяет, насколько быстро дежурный узнает о проблеме.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-applications -->

### Шаг 2 — Anomaly detection for mobile applications

![Anomaly detection for mobile applications — пороги для мобильных](screenshots/day-3-4/thresholds/settings/builtinanomaly-detection.rum-mobile/Anomaly-detection-for-mobile-applications-Environment-Settings-Demo-live-Demo-Li.png)

Путь: `/ui/settings/builtin:anomaly-detection.rum-mobile`.

Аналогично web, но для мобильных приложений. Те же 4 категории — деградация ключевых метрик user actions, traffic drops/spikes, рост failure rate. Crash rate выделен в отдельный детектор и настраивается на Шаге 5.

*Критичная метрика.* App startup time. Долгий запуск мобильного приложения = потеря клиента. Типовые пороги строгие, точные значения подбираются под продукт; начинать удобно с automated baselining, после двух-трёх недель данных переключаться на fixed thresholds, если нужны жёсткие SLO.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-applications -->

### Шаг 3 — Anomaly detection for custom applications

![Anomaly detection for custom applications — пороги для custom](screenshots/day-3-4/thresholds/settings/builtinanomaly-detection.rum-custom/Anomaly-detection-for-custom-applications-Environment-Settings-Demo-live-Demo-Li.png)

Путь: `/ui/settings/builtin:anomaly-detection.rum-custom`.

Для Custom applications (Smart TV, Desktop, IoT — см. Тема 8). Пороги аналогичные.

*Типовое применение.* Используется редко — только если есть уникальные устройства типа банкоматов с RUM SDK.

### Шаг 4 — Crash rate for custom applications

![Crash rate settings for custom applications](screenshots/day-3-4/thresholds/settings/builtinanomaly-detection.rum-custom-crash-rate-increase/Crash-rate-increase-settings-for-custom-applications-Environment-Settings-Demo-l.png)

Путь: `/ui/settings/builtin:anomaly-detection.rum-custom-crash-rate-increase`.

Отдельная страница настройки порогов Crash rate для custom apps.

*Что такое crash.* Приложение упало аварийно — необработанное исключение, OOM, segfault. Это отдельная метрика от обычных errors (где пользователь может продолжить работу).

**Пороги:** когда рост crash rate считать аномалией и создавать Problem.

### Шаг 5 — Crash rate for mobile applications

![Crash rate settings for mobile applications](screenshots/day-3-4/thresholds/settings/builtinanomaly-detection.rum-mobile-crash-rate-increase/Crash-rate-increase-settings-for-mobile-applications-Environment-Settings-Demo-l.png)

Путь: `/ui/settings/builtin:anomaly-detection.rum-mobile-crash-rate-increase`.

Та же механика, для мобильных. Критично для мобильного банкинга — crash = потеря клиента.

**Как работает по документации.** Dynatrace строит baseline числа крашей по версии приложения. Скользящее окно наблюдения — **10 минут**. Чтобы избежать ложных срабатываний на низком трафике, перед поднятием event требуется минимум **10 одновременных пользователей** на этой версии приложения. Чувствительность настраивается тремя уровнями — Low / Medium / High.

---

## 🎓 ТЕОРИЯ — специфика anomaly detection для RUM

### Отличие RUM от backend сервисов

- **Backend** — контролируемая среда, понятный baseline.
- **RUM** — пользователи везде: разные устройства, сети, сезонность.

**Специфика baseline для RUM:**

- **Сильная сезонность по часам** — утренний / дневной / вечерний паттерн.
- **Сильная сезонность по дням недели** — будни vs выходные.
- **Зависимость от геолокации** — пользователи из разных стран имеют разные baseline.
- **Зависимость от браузера** — Safari на iPhone и Chrome на Android = разные baseline.

### Почему перцентили важнее среднего для RUM

Медиана времени загрузки может быть хорошей (200 мс), но **хвост распределения** (P99) — ужасным (5 секунд). Это реальные пользователи с плохой сетью или старыми устройствами. Если смотреть только на среднее, их проблем не видно. Поэтому anomaly detection в RUM строится отдельно на разных перцентилях.

### Crash rate — отдельная метрика

- **Обычные ошибки** (JS exceptions, network errors) — пользователь продолжает работу.
- **Crash** — приложение упало полностью, пользователь вынужден перезапустить.

*Формула:* Crash rate = (crashes / sessions) × 100.

В Dynatrace baseline строится по версии приложения. Конкретный целевой уровень для каждого продукта подбирается под бизнес-контекст и SLO; Davis в режиме automated baselining ловит относительный рост, в режиме fixed thresholds — нарушение явного процента.

### Air-gapped specifics

Все пороги и baseline — локальные. Вычисляются в кластере на данных от RUM-сниппетов и Mobile SDK. Никаких внешних сервисов.
