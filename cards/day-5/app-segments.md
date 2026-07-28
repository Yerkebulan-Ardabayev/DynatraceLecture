---
topic_id: app-segments
day_id: day-5
timing_min: 24
verified: 2026-07-12
---
## ГДЕ
Три экрана в Settings → Web and mobile monitoring.
Application detection rules: Application detection → Detection rules, route `/ui/settings/builtin:rum.web.app-detection`.
Beacon origins for CORS: Application detection → Beacon CORS origins, route `/ui/settings/builtin:rum.web.beacon-domain-origins`.
Provider breakdown: Settings → Web and mobile monitoring → Provider breakdown, route `/ui/settings/builtin:rum.provider-breakdown`.

## ЗАЧЕМ
Сегментация разносит трафик одного домена на отдельные Dynatrace-приложения, у каждого свой Apdex, SLO и команда ответственных.
Без детекции Dynatrace видит одно гигантское приложение с общим Apdex, и провал одной части (например ДБО для юрлиц) растворяется в объёме публичного сайта.

## ЦИФРЫ
- Три экрана темы: Application detection rules, Beacon origins for CORS, Provider breakdown.
- Три способа задать структуру RUM-приложений: авто-инжекция плюс placeholder My web application, Application detection rules, Agentless RUM (ручной сниппет ruxit.js).
- Правила детекции идут сверху вниз, первое совпавшее выигрывает, более специфичные выше общих; лимит до 1000 правил на environment.
- В URL вида `scheme://host:port/path?query` порты 80 и 443 опускаются, правило матчит по host, path и query.
- Пример дашборда «Apdex по провайдерам»: у крупного ISP 0.95, у мелкого 0.62 (у вашего тенанта цифры могут быть другими).

## ЕСЛИ→ТО
- ЕСЛИ весь трафик сидит на одном домене без правил детекции → Dynatrace видит одно приложение с общим Apdex, провал одной части растворяется в объёме другой → разносим трафик path-based правилами по отдельным приложениям.
- ЕСЛИ URL не подошёл ни под одно правило → сессия оседает в служебное приложение My web application → регулярно заглядываем туда и разносим трафик новыми правилами (переименовывать placeholder не рекомендуется).
- ЕСЛИ домена нет в списке Beacon origins for CORS → ActiveGate не вернёт Access-Control-Allow-Origin, preflight падает, beacon отменяется → RUM-агент молчит, даже если всё остальное настроено.
- ЕСЛИ на медленную работу жалуется только часть пользователей → Provider breakdown показывает, что все они из одного ISP с плохой маршрутизацией до дата-центра → дальше переговоры с провайдером или перенос ближе к точке обмена трафиком.

## ЗАПАСНОЙ ПЛАН
Если на демо нет write-прав и правило не создать: показываю таблицу Detection rules по снимку и на примере домена с четырьмя частями (публичный сайт, ДБО для физлиц, ДБО для юрлиц, блог) проговариваю, как path-based правила разносят трафик по отдельным приложениям.
Кнопку Check URL проговариваю как способ проверить, какое правило сработает и активен ли RUM, даже без прав на изменение.
Beacon origins for CORS и Provider breakdown показываю по снимкам: подчёркиваю, что список origin-ов задаётся конкретными доменами без wildcard, а в Managed важно, на какой endpoint браузер шлёт beacon (при agentless это Cluster ActiveGate, путь `/bf`).
Лекторский сценарий: workshop/day-3.md, блок 2. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Чем приложение отличается от Management zone?» Ответ: application detection создаёт отдельную Dynatrace-сущность со своим Apdex, метриками и ID, а management zone только фильтрует существующие сущности и своих метрик не имеет; приложение это уровень фронта, management zone сквозной разрез фронт плюс бэк плюс инфра.
- «Почему одна сессия не тянется через несколько доменов?» Ответ: cookie технологически ограничен текущим доменом, поэтому при разделении приложения по поддоменам сессия между ними не склеится.
- «Как в air-gapped Managed браузер клиента доставляет beacon?» Ответ: при авто-инжекции beacon идёт на тот же web-сервер на root-relative путь с префиксом rb_ и OneAgent пересылает его в кластер, при agentless на endpoint Cluster ActiveGate (путь `/bf`), и этот endpoint должен быть достижим с устройств пользователей.
