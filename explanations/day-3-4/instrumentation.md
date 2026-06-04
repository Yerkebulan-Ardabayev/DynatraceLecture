> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 5 из 14: «Инструментирование приложений: Web, Mobile»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement -->
<!-- revision: 2026-04-27 -->

🔖 Редакция от 2026-04-27.

Путь в UI: **Settings → Web and mobile monitoring → Web (или Mobile) → Enablement and cost control / RUM JavaScript → File name / Version / Updates**.

## 📚 Источники

- [Web Applications RUM (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications)
- [Mobile Applications RUM (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/mobile-applications)
- [Configure RUM monitoring code source (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/configure-monitoring-code-source)
- [Control the RUM JavaScript version (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/rum-javascript-version)

## 📍 КАРТА: пять страниц настройки RUM-инструментации

Термины темы: `RUM / Real User Monitoring / мониторинг реальных пользователей`, `Web RUM / веб-RUM через JavaScript`, `Mobile RUM / мобильный RUM через SDK`, `Session / сессия`, `Cost control / контроль расхода лицензии`, `Core Web Vitals / ключевые метрики веб-производительности`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Web RUM: включение и cost control | **Settings → Web and mobile monitoring → Web → Enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement` |
| Mobile RUM: включение и cost control | **Settings → Web and mobile monitoring → Mobile → Enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.mobile.enablement` |
| RUM JavaScript: имя файла | **Settings → Web and mobile monitoring → Web → RUM JavaScript → File name** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.rum-javascript-file-name` |
| Custom RUM JavaScript version | **Settings → Web and mobile monitoring → Web → RUM JavaScript → Version** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.custom-rum-javascript-version` |
| RUM JavaScript updates | **Settings → Web and mobile monitoring → Web → RUM JavaScript → Updates** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.rum-javascript-updates` |

---

## 🎬 Работа с RUM-инструментацией на пяти экранах

### Шаг 1: Web RUM: Enablement and cost control

![Web Enablement and cost control: главный тумблер Web RUM](screenshots/day-3-4/instrumentation/settings/builtinrum.web.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.enablement`.

**Что настраивается:**

- **Главный тумблер RUM for Web**: сбор данных от RUM-сниппетов в браузерах.
- **Cost control**: ограничение объёма (лимиты сессий в месяц). Даёт предсказуемость DDU-лицензий.
- **Session durations**: как долго считать одну сессию. По умолчанию пока пользователь активен.

*Типовое применение.* RUM включён для клиентских веб-приложений (интернет-банк) и внутренних корпоративных порталов.

### Шаг 2: Mobile RUM: Enablement and cost control

![Mobile Enablement and cost control: главный тумблер Mobile RUM](screenshots/day-3-4/instrumentation/settings/builtinrum.mobile.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.mobile.enablement`.

**Что настраивается** (аналогично Web, но для мобильных):

- Главный тумблер Mobile RUM.
- Cost control для мобильных сессий.
- Настройки iOS / Android: crash reporting, network monitoring.

*Установка Mobile RUM* требует интеграции Dynatrace SDK в мобильное приложение на этапе сборки. Swift Package Manager для iOS, Gradle для Android. OneAgent напрямую на мобильных устройствах не работает.

### Шаг 3: RUM monitoring code filename

![RUM monitoring code filename: имя файла RUM JavaScript](screenshots/day-3-4/instrumentation/settings/builtinrum.web.rum-javascript-file-name/RUM-monitoring-code-filename-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.rum-javascript-file-name`.

*Что настраивает.* Префикс имени файла JavaScript-сниппета, который OneAgent внедряет в HTML-ответы. По умолчанию префикс **`ruxitagent`** (полное имя: например `/ruxitagentjs_ICA7NQVfqrtux_10307250124095659.js`, где после префикса идёт хеш активных модулей и версия). Префикс можно заменить на свой; сегмент `ruxitagentjs_` после префикса остаётся для идентификации запроса.

*Когда меняют.* В инсталляциях с повышенными требованиями к безопасности префикс заменяют на нейтральный (`site-analytics`, `metrics-loader`), чтобы технологию нельзя было опознать из HTML. Частая смена префикса временно снижает объём собираемых данных, поэтому делается редко.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/configure-monitoring-code-source -->

### Шаг 4: Custom RUM JavaScript version

![Custom RUM JavaScript version: выбор версии RUM JS](screenshots/day-3-4/instrumentation/settings/builtinrum.web.custom-rum-javascript-version/Custom-RUM-JavaScript-version-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.custom-rum-javascript-version`.

*Что настраивает.* Конкретная статическая версия RUM-JavaScript, на которую можно сослаться, если в RUM JavaScript updates выбран вариант **Custom**.

*Зачем нужно.* Когда новая версия конфликтует с редким окружением (старый корпоративный IE и аналоги), сюда вписывают известную рабочую версию, а в **RUM JavaScript updates** выставляют Custom: обновления приостановлены.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/rum-javascript-version -->

### Шаг 5: RUM JavaScript updates

![RUM JavaScript updates: политика обновлений RUM JS](screenshots/day-3-4/instrumentation/settings/builtinrum.web.rum-javascript-updates/RUM-JavaScript-updates-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.rum-javascript-updates`.

*Что настраивает.* Политика версии RUM-JS, выбирается из набора:

- **Latest stable**: самая свежая стабильная (динамическая, обновляется автоматически).
- **Previous stable**: предыдущая стабильная (тоже динамическая).
- **Custom**: фиксированная статическая версия из соседней страницы Custom RUM JavaScript version.

> Legacy IE-варианты (Latest IE7-10 / Latest IE11) встречаются только в окружениях, созданных до версии 1.294: поддержка IE 11 прекращена в RUM JS 1.293. В новых установках их в списке нет, в банковском контуре они не используются.

*Типовая политика.* В прод-приложениях выставляют Previous stable: одна версия буфера к выловленным регрессиям. Latest stable удобен в dev/QA-окружениях. Custom применяют только если найдена конкретная несовместимость и нужна стабильная привязка.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/rum-javascript-version -->

---

## 🎓 ТЕОРИЯ: как работает инструментация RUM

### Web RUM: через JavaScript snippet

**Механика.** OneAgent на веб-сервере (Apache/Nginx/IIS) перехватывает исходящие HTML-ответы. В каждом ответе он автоматически вставляет в `<head>` тег:

```html
<script src="/ruxitagentjs_CONFIG_HASH.js" crossorigin="anonymous"></script>
```

Этот JS при загрузке страницы в браузере пользователя:
1. Собирает данные о загрузке страницы (Core Web Vitals: LCP, FID, CLS).
2. Отслеживает пользовательские действия (клики, переходы, формы).
3. Перехватывает XHR/fetch-запросы (с каким временем, какой статус).
4. Ловит JavaScript-ошибки.
5. Отправляет всё это батчами в ActiveGate по HTTPS.

### Mobile RUM: через SDK

**Механика.** В мобильное приложение при сборке встраивается Dynatrace SDK:

- **Android.** Основной путь: Dynatrace Android Gradle plugin (auto-instrumentation). Для тонкой интеграции есть OneAgent SDK for Android (manual).
- **iOS.** Основной путь: OneAgent for iOS auto-instrumentation, подключение через Swift Package Manager или CocoaPods. Для SwiftUI-приложений есть отдельный SwiftUI instrumentor.
- **Гибридные стэки.** Поддерживаются Apache Cordova, Flutter, React Native, Xamarin, .NET MAUI через соответствующие плагины.

SDK при старте приложения:
1. Регистрирует crash handler.
2. Перехватывает сетевые запросы (URLSession на iOS, OkHttp / HttpURLConnection на Android).
3. Собирает данные о пользовательских сессиях и user actions.
4. Шлёт в ActiveGate (или Cluster ActiveGate для агентless-схемы).
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/mobile-applications -->

### Air-gapped RUM

- **Web RUM.** RUM-JS отдаётся с веб-сервера (OneAgent там стоит). Данные идут в ActiveGate (обычно в DMZ). Внешний интернет не нужен.
- **Mobile RUM.** При сборке приложения SDK-библиотека скачивается с customer portal на машине с интернетом, пушится в внутренний Maven / CocoaPods. CI/CD собирает приложение с внутренним SDK.
- **Публикация ActiveGate.** Для публичного Web RUM (пользователи из интернета) ActiveGate должен быть опубликован наружу через reverse-proxy или DMZ. Одна из немногих точек, где air-gapped контур открывается наружу, строго контролируется.
