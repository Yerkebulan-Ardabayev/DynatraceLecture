---
topic_id: instrumentation
day_id: day-3-4
timing_min: 25
verified: 2026-07-12
---
## ГДЕ
Пять страниц Settings → Web and mobile monitoring.
Web RUM, включение и cost control: route `/ui/settings/builtin:rum.web.enablement`. Mobile RUM, включение и cost control: route `/ui/settings/builtin:rum.mobile.enablement`.
Три страницы RUM JavaScript (Web → RUM JavaScript): File name `/ui/settings/builtin:rum.web.rum-javascript-file-name`, Version `/ui/settings/builtin:rum.web.custom-rum-javascript-version`, Updates `/ui/settings/builtin:rum.web.rum-javascript-updates`.

## ЗАЧЕМ
Инструментация RUM это то, как данные о реальных пользователях вообще попадают в Dynatrace.
Web идёт через JavaScript-сниппет: OneAgent на веб-сервере сам вставляет `<script>` в исходящие HTML-ответы. Mobile идёт через SDK, встроенный в приложение при сборке.
Экраны отвечают на «как включить сбор с браузеров и мобильных, какую версию сниппета держать и как удержать расход лицензии».

## ЦИФРЫ
- Пять страниц темы: Web enablement, Mobile enablement и три страницы RUM JavaScript (File name, Version, Updates).
- Web RUM: OneAgent вставляет `<script>` в `<head>` каждого HTML-ответа, префикс файла по умолчанию `ruxitagent` (сегмент `ruxitagentjs_` остаётся для идентификации запроса).
- IE 11: поддержка прекращена в RUM JS 1.293, legacy-варианты Latest IE7-10 / Latest IE11 остаются только в окружениях, созданных до версии 1.294.
- Три варианта RUM JavaScript updates: Latest stable (динамическая), Previous stable (динамическая), Custom (фиксированная статическая версия из соседней страницы).
- Cost control: лимит сессий в месяц, даёт предсказуемость расхода DDU-лицензий.

## ЕСЛИ→ТО
- ЕСЛИ приложение мобильное → OneAgent напрямую не работает, нужен Dynatrace SDK, встроенный при сборке (iOS через Swift Package Manager, Android через Gradle).
- ЕСЛИ технологию нельзя опознавать из HTML → префикс `ruxitagent` меняют на нейтральный (`site-analytics`, `metrics-loader`), но частая смена временно снижает объём собираемых данных, поэтому делается редко.
- ЕСЛИ новая версия RUM JS конфликтует с редким окружением → в Custom RUM JavaScript version вписывают рабочую версию, а в Updates ставят Custom: обновления приостановлены.
- ЕСЛИ окружение прод → выставляют Previous stable, одна версия буфера к регрессиям; ЕСЛИ dev или QA → удобнее Latest stable.

## ЗАПАСНОЙ ПЛАН
Тумблеры на демо серые (нет write-прав) или страница не открывается: показываю снимок из курса и проговариваю по нему.
На Web enablement показываю главный тумблер RUM for Web и блок Cost control, на RUM JavaScript updates проговариваю три политики версии (Latest stable, Previous stable, Custom).
Mobile показываю как аналог Web, отдельно проговариваю, что установка Mobile RUM это интеграция SDK при сборке, а не тумблер в UI.
Конкретные версии RUM JS сверх задокументированных по памяти не называю, отсылаю к значению на самой странице тенанта.
Лекторский сценарий: workshop/day-4.md, блок 3. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Как RUM-скрипт попадает на страницу?» Ответ: OneAgent на веб-сервере (Apache, Nginx, IIS) перехватывает HTML-ответы и сам вставляет `<script src="/ruxitagentjs_...">` в `<head>`, вручную встраивать ничего не нужно.
- «Чем инструментируется мобильное приложение, если OneAgent там не работает?» Ответ: Dynatrace SDK при сборке (iOS через Swift Package Manager, Android через Gradle plugin), гибридные стэки (Cordova, Flutter, React Native, Xamarin, .NET MAUI) подключаются через свои плагины.
- «Как RUM собирать в закрытом контуре?» Ответ: Web RUM отдаётся с веб-сервера, данные идут в ActiveGate в DMZ, внешний интернет не нужен; для публичного Web RUM ActiveGate публикуют наружу через reverse-proxy, а Mobile SDK кладут во внутренний Maven.
