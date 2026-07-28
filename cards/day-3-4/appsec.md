---
topic_id: appsec
day_id: day-3-4
timing_min: 30
verified: 2026-07-12
---
## ГДЕ
Центральный экран: Application Security → Security Overview, route `/ui/security/overview`.
Четыре рабочих экрана модуля: Security Overview, Third-Party Vulnerabilities (`/ui/security/vulnerabilities`), Code-Level Vulnerabilities (`/ui/security/code-vulnerabilities`), Attacks (`/ui/security/attacks`).
Остальные экраны, это настройки в Settings → Application Security (Application Protection, Vulnerability Analytics, alerting profiles).

## ЗАЧЕМ
AppSec это инструмент безопасности, работающий в runtime прямо в production: находит уязвимости в библиотеках (third-party) и в собственном коде (code-level), детектирует активные атаки и показывает реальную эксплуатируемость (Actual exposure), а не сырой список CVE.
Отвечает на два вопроса: «какие из тысяч найденных CVE реально опасны именно у нас» и «атакуют ли нас прямо сейчас».

## ЦИФРЫ
- Модуль это 14 страниц: 4 рабочих экрана (Security Overview, Third-Party, Code-Level, Attacks) и остальные 10, это экраны настроек.
- Runtime Application Protection детектирует и опционально блокирует ровно 4 класса атак: SQL injection, JNDI injection, Command injection, SSRF. XSS в этот список не входит.
- Davis Security Score: уровни Critical / High / Medium / Low / None. DSS пересчитывает базовый CVSS под окружение (доступность из интернета, достижимые хранилища данных) и только понижает балл или оставляет как есть, выше базового CVSS никогда не поднимает.
- Runtime Application Protection работает на Java 8+ (OneAgent 1.241+), .NET Framework 4.5+ (OneAgent 1.289+), Go (OneAgent 1.311+); только Windows x86 и Linux x86, только 64-битные процессы.
- Third-party уязвимость авто-закрывается после двухчасового окна «компонент не загружается»; code-level закрывается, когда процесс перезапущен и OneAgent больше не видит опасных потоков данных.
- Типовая политика Attack Protection: сначала Monitor на 2-4 недели (увидеть false positives), затем Block для критичных endpoint'ов (платежи, аутентификация), остальные остаются в Monitor.

## ЕСЛИ→ТО
- ЕСЛИ базовый CVSS у CVE = High, но затронутый сервис недоступен из интернета и без достижимой БД → Davis понижает балл (например до Medium), уязвимость уходит ниже в очереди; выше базового CVSS балл не поднимется.
- ЕСЛИ Application Protection в режиме Monitor → атака детектируется и логируется, запрос проходит; ЕСЛИ Block → похожий на атаку запрос блокируется, Dynatrace работает как частичный WAF.
- ЕСЛИ уязвимый код библиотеки в runtime не вызывается (Actual exposure отрицательный) → риск низкий даже при высоком CVSS, исправление уходит в конец очереди.
- ЕСЛИ стек не поддержан модулем (Ruby, Erlang, Cobol) → AppSec по нему не работает, закрываю сторонними SAST / DAST / WAF.

## ЗАПАСНОЙ ПЛАН
В air-gapped проговариваю сетевое требование: feed уязвимостей приходит только при доступе кластера к Mission Control (endpoint mcsvc.dynatrace.com/vulnerabilityFeed/*), офлайн-доставка feed в публичной документации не описана; без доступа к этому endpoint новые CVE в анализ не попадут.
Application Protection blocking выполняется на стороне OneAgent внутри контура, без обращения наружу: показываю это как рабочий сценарий для закрытого контура.
Уведомления во внутренний SOC завожу через Webhook / Email / ServiceNow, те же каналы, что в incident-lifecycle.
Если экран на демо серый или нет write-прав: показываю снимок из курса и проговариваю сценарий словами.
Лекторский сценарий: workshop/day-3.md, блок 10. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Чем это отличается от SAST и DAST?» Ответ: SAST читает исходный код без запуска, DAST шлёт тестовые атаки в тестовой среде, Dynatrace анализирует runtime в production и видит, что реально вызывается и реально эксплуатируется.
- «Блокирует ли Dynatrace XSS?» Ответ: нет, Runtime Application Protection закрывает ровно 4 класса (SQL injection, JNDI injection, Command injection, SSRF), XSS в этот список не входит.
- «Откуда база уязвимостей в закрытом контуре?» Ответ: Dynatrace Vulnerability feed либо NVD (по типу компонента), кластер забирает их через Mission Control; в полностью изолированном контуре нужен явный сетевой доступ к endpoint feed, офлайн-механизм в доке не описан.
