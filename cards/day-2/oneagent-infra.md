---
topic_id: oneagent-infra
day_id: day-2
timing_min: 20
verified: 2026-07-12
---
## ГДЕ
Возможности агента: Settings → Preferences → OneAgent features, route `/ui/settings/builtin:oneagent.features`.
Аномалии внешних дисков: Settings → Anomaly detection → Disk Edge, route `/ui/settings/builtin:infrastructure.disk.edge.anomaly-detectors`.

## ЗАЧЕМ
OneAgent собирает инфраструктуру тремя слоями (OS, Process, Feature) без ручной настройки метрик.
На звонке важно показать, где включаются расширенные сенсоры (eBPF, SNMP-edge, container runtimes) и где живёт retention данных.

## ЦИФРЫ
- Три слоя сбора: OS (CPU, Memory, Disk, Network), Process, Feature (eBPF, SNMP, container runtimes).
- Metrics Classic хранятся до 5 лет с лестницей: 0-14 дней шаг 1 мин, 14-28 дней 5 мин, 28-400 дней 1 час, 400 дней до 5 лет 1 день.
- Трейсы до 365 дней (настраивается), Code-level insights 10 дней фикс.
- RUM-сессии 35 дней фикс, Log Monitoring Classic настраивается, максимум 90 дней.
- Davis problems и events 14 месяцев; OneAgent diagnostics по умолчанию 30 дней.

## ЕСЛИ→ТО
- ЕСЛИ фича помечена Opt-In → по умолчанию выключена, админ включает явно; облачные Opt-In (AWS Lambda sensor, Azure Functions sensor) в air-gapped включать бессмысленно, ресурсов в контуре нет.
- ЕСЛИ включить Log monitoring глобально, но не на dev → на dev-хост-группе делаю override и выключаю: prod получает логи, dev нет.
- ЕСЛИ нужны метрики самого хранилища (RAID, LUN, контроллер) → это Disk Edge через ActiveGate (SNMP или Extension); обычный Disk monitoring видит только файловую систему на хосте.
- ЕСЛИ приложение падает после инструментации → через Filter на OneAgent features выключаю сенсор библиотеки глобально либо делаю override на конкретном хосте.

## ЗАПАСНОЙ ПЛАН
Disk Edge на демо без правил (нет реального оборудования): это нормально, показываю снимок и проговариваю смысл, правила аномалий для метрик массивов, опрашиваемых с ActiveGate.
OneAgent features: показываю таблицу с колонками Enabled, Summary, Min. OneAgent version, Details, фильтрую поле по eBPF, чтобы показать группу сенсоров.
Про retention: не называю числа по памяти наугад, опираюсь на строки страницы Data retention и на снимок.

## ВОПРОСЫ АУДИТОРИИ
- «Чем Disk Edge отличается от обычного Disk monitoring?» Ответ: обычный видит файловую систему на хосте с OneAgent, Disk Edge видит само хранилище уровнем ниже (RAID, LUN, контроллер) опросом от ActiveGate.
- «Зачем часть фич сделали Opt-In?» Ответ: чтобы не нагружать свежий агент лишними сенсорами; в изолированном контуре облачные Opt-In включать незачем, соответствующих ресурсов нет.
- «Сколько хранятся данные?» Ответ: метрики Classic до 5 лет с прореживанием, трейсы до 365 дней, RUM-сессии 35 дней, Davis-проблемы 14 месяцев.
