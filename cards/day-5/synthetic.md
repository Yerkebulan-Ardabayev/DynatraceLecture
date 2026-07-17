---
topic_id: synthetic
day_id: day-5
timing_min: 30
verified: 2026-07-12
---
## ГДЕ
Четыре экрана. Список мониторов: Application Observability → Frontend → Synthetic, route `/ui/synthetic` (на демо отдаёт 403, см. запасной план).
Три страницы Settings → Web and mobile monitoring: Synthetic availability settings `/ui/settings/builtin:synthetic.synthetic-availability-settings`, Browser outage handling `/ui/settings/builtin:synthetic.browser.outage-handling`, HTTP outage handling `/ui/settings/builtin:synthetic.http.outage-handling`.

## ЗАЧЕМ
Synthetic это искусственный трафик роботами по расписанию: бьёт 24/7 независимо от реальной нагрузки и ловит падение до жалоб клиентов, тогда как RUM молчит ночью и на редких страницах.
Нужны оба: RUM для аналитики реального опыта, Synthetic для SLO, на который вы отчитываетесь.
Четыре типа мониторов: Single-URL Browser, Browser clickpath, HTTP (в т.ч. Multi-step), Network Availability Monitoring (NAM). NAM работает только на private locations.

## ЦИФРЫ
- Четыре типа мониторов: Single-URL Browser, Browser clickpath, HTTP (в т.ч. Multi-step цепочка с извлечением токена), NAM (ICMP-ping · TCP-connect · DNS-lookup, только private locations).
- Single-URL Browser: минимальная частота 5 минут или реже; потолок любого монитора 1 запуск в минуту.
- Availability settings на env-уровне: один тумблер; правила падений и ретраи задаются в настройках самих мониторов.
- Browser/HTTP outage handling: тумблеры global/local outage; численные пороги задаются в настройках мониторов, дефолты в публичной доке не зафиксированы.
- Допустимые коды ответа (настройка самого HTTP-монитора): по умолчанию 2xx; 401 можно назначить успехом для защищённого endpoint (сервис жив, просто требует auth).
- Synthetic-enabled ActiveGate: Environment 1.169+ или Cluster 1.176+, держит и browser, и HTTP; capacity локации в UI: зелёный <80%, красный >90%.

## ЕСЛИ→ТО
- ЕСЛИ проверка дешёвая (HTTP health endpoint) → ставят часто, каждую минуту, Davis заметит падение почти сразу; ЕСЛИ дорогая (browser clickpath) → частоту снижают до каждых 15-30 минут, потолок всё равно 1 запуск в минуту.
- ЕСЛИ HTTP-endpoint'а нет, а важна сетевая связность (ping, TCP-порт, DNS) → берут NAM, но он только на private locations.
- ЕСЛИ защищённый endpoint штатно отдаёт 401 → в HTTP outage handling 401 назначают успехом, иначе живой сервис будет считаться упавшим.
- ЕСЛИ один Synthetic-enabled ActiveGate в одном ЦОД → доступность видна только оттуда, падение сети между ЦОД-1 и ЦОД-2 не поймать; ставят минимум 2 в разных зонах.

## ЗАПАСНОЙ ПЛАН
Страница `/ui/synthetic` на демо-тенанте отдаёт 403 (модуль не активирован или у роли нет прав на synthetic-зону): показываю снимок 403 из курса и проговариваю, что на боевом Managed здесь список всех мониторов, а доступ настраивается через IAM (Management zones, Permissions).
Четыре типа и метрики монитора (Availability, Response time, Location) разбираю по общему знанию платформы плюс снятые настройки.
Три страницы Settings (availability settings, browser и HTTP outage handling) на демо открываются: показываю их живьём; дефолты (retry, consecutive failures, expected codes) читаю прямо со страницы тенанта, если поля серые из-за отсутствия write-прав.

## ВОПРОСЫ АУДИТОРИИ
- «RUM уже стоит, зачем ещё Synthetic?» Ответ: RUM молчит, когда нет трафика (ночь, редкие страницы), synthetic бьёт по расписанию 24/7 и ловит падение до жалоб; RUM для аналитики опыта, synthetic для SLO.
- «Как synthetic работает в закрытом контуре без интернета?» Ответ: через private locations на своих Synthetic-enabled ActiveGate внутри сети (Environment 1.169+ / Cluster 1.176+); public-локации Dynatrace в air-gapped недоступны, поэтому именно private.
- «Почему демо отдаёт 403 на /ui/synthetic?» Ответ: Synthetic это отдельный лицензируемый модуль; если он не активирован или у роли нет прав на synthetic-зону, UI возвращает 403, на боевом доступ открывают через IAM.
