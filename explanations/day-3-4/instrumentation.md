> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 5 из 14: «Инструментирование приложений: Web, Mobile»

## 📍 КАРТА — пять страниц настройки RUM-инструментации

Термины темы: `RUM / Real User Monitoring / мониторинг реальных пользователей`, `Web RUM / веб-RUM через JavaScript`, `Mobile RUM / мобильный RUM через SDK`, `Session / сессия`, `Cost control / контроль расхода лицензии`, `Core Web Vitals / ключевые метрики веб-производительности`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Web RUM — включение и cost control | **Settings → Web and mobile monitoring → Web → Enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.enablement` |
| Mobile RUM — включение и cost control | **Settings → Web and mobile monitoring → Mobile → Enablement and cost control** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.mobile.enablement` |
| RUM JavaScript — имя файла | **Settings → Web and mobile monitoring → Web → RUM JavaScript → File name** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.rum-javascript-file-name` |
| Custom RUM JavaScript version | **Settings → Web and mobile monitoring → Web → RUM JavaScript → Version** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.custom-rum-javascript-version` |
| RUM JavaScript updates | **Settings → Web and mobile monitoring → Web → RUM JavaScript → Updates** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.rum-javascript-updates` |

---

## 🎬 Работа с RUM-инструментацией на пяти экранах

### Шаг 1 — Web RUM: Enablement and cost control

![Web Enablement and cost control — главный тумблер Web RUM](screenshots/day-3-4/instrumentation/settings/builtinrum.web.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.enablement`.

**Что настраивается:**

- **Главный тумблер RUM for Web** — сбор данных от RUM-сниппетов в браузерах.
- **Cost control** — ограничение объёма (лимиты сессий в месяц). Даёт предсказуемость DDU-лицензий.
- **Session durations** — как долго считать одну сессию. По умолчанию пока пользователь активен.

*Типовое применение.* RUM включён для клиентских веб-приложений (интернет-банк) и внутренних корпоративных порталов.

### Шаг 2 — Mobile RUM: Enablement and cost control

![Mobile Enablement and cost control — главный тумблер Mobile RUM](screenshots/day-3-4/instrumentation/settings/builtinrum.mobile.enablement/Enablement-and-cost-control-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.mobile.enablement`.

**Что настраивается** (аналогично Web, но для мобильных):

- Главный тумблер Mobile RUM.
- Cost control для мобильных сессий.
- Настройки iOS / Android: crash reporting, network monitoring.

*Установка Mobile RUM* требует интеграции Dynatrace SDK в мобильное приложение на этапе сборки. Swift Package Manager для iOS, Gradle для Android. OneAgent напрямую на мобильных устройствах не работает.

### Шаг 3 — RUM monitoring code filename

![RUM monitoring code filename — имя файла RUM JavaScript](screenshots/day-3-4/instrumentation/settings/builtinrum.web.rum-javascript-file-name/RUM-monitoring-code-filename-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.rum-javascript-file-name`.

*Что настраивает.* Имя файла JavaScript-сниппета, который OneAgent внедряет в HTML-ответы. По умолчанию `ruxitagentjs_*.js`. Можно переименовать для скрытия technology fingerprint.

*Когда меняют.* В инсталляциях с повышенными требованиями к безопасности переименовывают в нейтральное `site-analytics.js` или аналогичное, чтобы технологию нельзя было опознать из HTML.

### Шаг 4 — Custom RUM JavaScript version

![Custom RUM JavaScript version — выбор версии RUM JS](screenshots/day-3-4/instrumentation/settings/builtinrum.web.custom-rum-javascript-version/Custom-RUM-JavaScript-version-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.custom-rum-javascript-version`.

*Что настраивает.* Версия RUM-JavaScript, которая внедряется. По умолчанию Latest stable. Можно зафиксировать на Previous stable (если новая вызывает проблемы) или на конкретной кастомной версии.

*Зачем нужно.* Новая версия RUM-JS может оказаться несовместимой с редкой версией браузера (старый корпоративный IE и аналоги). В таких случаях временно откатывают.

### Шаг 5 — RUM JavaScript updates

![RUM JavaScript updates — политика обновлений RUM JS](screenshots/day-3-4/instrumentation/settings/builtinrum.web.rum-javascript-updates/RUM-JavaScript-updates-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.rum-javascript-updates`.

*Что настраивает.* Политика обновления RUM-JS:

- **Automatic updates** — новая версия применяется автоматически при выпуске.
- **Manual** — только по действию администратора.
- **Delayed** — с задержкой в N дней от релиза.

*Типовая политика.* Delayed на 7-14 дней. Даёт Dynatrace время выловить ранние баги у других клиентов, прежде чем версия дойдёт до production.

---

## 🎓 ТЕОРИЯ — как работает инструментация RUM

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [OneAgent — инструментация](https://docs.dynatrace.com/docs/shortlink/oneagent)

### Web RUM — через JavaScript snippet

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

### Mobile RUM — через SDK

**Механика.** В мобильное приложение при сборке встраивается Dynatrace SDK (`com.dynatrace.android:agent:X.Y.Z` для Android, `DynatraceSwift.framework` для iOS). SDK при старте приложения:
1. Регистрирует crash handler.
2. Перехватывает сетевые запросы (через URLSession / OkHttp).
3. Собирает данные о пользовательских сессиях.
4. Пересылает в ActiveGate.

### Air-gapped RUM

- **Web RUM.** RUM-JS отдаётся с веб-сервера (OneAgent там стоит). Данные идут в ActiveGate (обычно в DMZ). Внешний интернет не нужен.
- **Mobile RUM.** При сборке приложения SDK-библиотека скачивается с customer portal на машине с интернетом, пушится в внутренний Maven / CocoaPods. CI/CD собирает приложение с внутренним SDK.
- **Публикация ActiveGate.** Для публичного Web RUM (пользователи из интернета) ActiveGate должен быть опубликован наружу через reverse-proxy или DMZ. Одна из немногих точек, где air-gapped контур открывается наружу, строго контролируется.
