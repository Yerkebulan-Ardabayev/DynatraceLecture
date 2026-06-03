> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 14 из 14: «Обзор Security Module (Application Security)»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/security/overview -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [Application Security: Managed](https://docs.dynatrace.com/managed/secure/application-security)
- [Runtime Vulnerability Analytics](https://docs.dynatrace.com/managed/secure/application-security/vulnerability-analytics)
- [Runtime Application Protection](https://docs.dynatrace.com/managed/secure/application-security/application-protection)
- [Application Security FAQ](https://docs.dynatrace.com/managed/secure/faq)
- [Application Security monitoring (ASUs): Managed](https://docs.dynatrace.com/managed/license/monitoring-consumption-classic/application-security-units)

## 📍 КАРТА: 14 страниц модуля Application Security

Термины темы: `Vulnerability / уязвимость`, `CVE / Common Vulnerabilities and Exposures / идентификатор известной уязвимости`, `CVSS / Common Vulnerability Scoring System`, `Third-party vulnerability / уязвимость в библиотеке`, `Code-level vulnerability / уязвимость в собственном коде`, `SAST / статический анализ`, `DAST / динамический анализ`, `WAF / web application firewall`, `Actual exposure / реальная эксплуатируемость`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Security overview | **Application Security → Security Overview** | `https://guu84124.live.dynatrace.com/ui/security/overview` |
| Security (общая) | **Application Security** | `https://guu84124.live.dynatrace.com/ui/security` |
| Third-party vulnerabilities | **Application Security → Third-Party Vulnerabilities** | `https://guu84124.live.dynatrace.com/ui/security/vulnerabilities` |
| Code-level vulnerabilities | **Application Security → Code-Level Vulnerabilities** | `https://guu84124.live.dynatrace.com/ui/security/code-vulnerabilities` |
| Attacks | **Application Security → Attacks** | `https://guu84124.live.dynatrace.com/ui/security/attacks` |
| Vulnerability Analytics: Rules for third-party | **Settings → Application Security → Monitoring rules for third-party vulnerabilities** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.rule-settings` |
| Application Protection: General settings | **Settings → Application Security → Application Protection → General settings** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.attack-protection-settings` |
| Application Protection: Monitoring rules | **Settings → Application Security → Application Protection → Monitoring rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.attack-protection-advanced-config` |
| Application Protection: Allowlist | **Settings → Application Security → Application Protection → Allowlist** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.attack-protection-allowlist-config` |
| Vulnerability Analytics: General | **Settings → Application Security → Vulnerability Analytics → General settings** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.runtime-vulnerability-detection` |
| Vulnerability Analytics: Rules for code-level | **Settings → Application Security → Monitoring rules for code-level vulnerabilities** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.code-level-vulnerability-rule-settings` |
| Vulnerability Analytics: Rules for third-party (extended) | **Settings → Application Security → Third-party rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.third-party-vulnerability-rule-settings` |
| Vulnerability alerting profiles | **Settings → Application Security → Vulnerability alerting profiles** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.notification-alerting-profile` |
| Attack alerting profiles | **Settings → Application Security → Attack alerting profiles** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:appsec.notification-attack-alerting-profile` |

---

## 🎬 Работа с Application Security на ключевых экранах

### Шаг 1: Security overview (главная страница)

![Security overview: сводка по безопасности приложений](screenshots/day-3-4/appsec/security/overview/Security-overview-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/security/overview`.

**Центральная страница** для работы с Application Security. Показывает сводку:
- Общее число уязвимостей (third-party + code-level).
- Разбивка по Severity (Critical / High / Medium / Low).
- Число активных атак за период.
- Топ наиболее критичных уязвимостей.
- Тренды.

### Шаг 2: Third-party vulnerabilities

![Third-party vulnerabilities: уязвимости в библиотеках приложений](screenshots/day-3-4/appsec/security/vulnerabilities/Third-party-vulnerabilities-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/security/vulnerabilities`.

*Third-party*: уязвимости в используемых библиотеках. Dynatrace при инструментации видит все загруженные библиотеки (jar'ы в Java, packages в .NET, npm-модули в Node) и сопоставляет с базой известных уязвимостей (CVE).

**На странице:**

- Список уязвимостей с CVE-идентификаторами.
- Severity по CVSS score.
- Affected libraries (jackson-databind 2.10.1, log4j 2.14.0 и т.п.).
- Affected entities: в каких сервисах и процессах используется библиотека.
- **Actual exposure**: эксплуатируется ли уязвимость в runtime. Критично: не все CVE одинаково опасны, если уязвимый код не вызывается.

*Роль для compliance.* Регулятор требует отчёты по уязвимостям. `Actual exposure` помогает приоритизировать исправления.

### Шаг 3: Code-level vulnerabilities

![Code-level vulnerabilities: уязвимости в собственном коде](screenshots/day-3-4/appsec/security/code-vulnerabilities/Code-level-vulnerabilities-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/security/code-vulnerabilities`.

*Code-level*: уязвимости в собственном коде, не в библиотеках. Dynatrace анализирует поведение приложения в runtime и ищет типовые проблемы (SQL injection, command injection, SSRF, JNDI injection и подобные insecure data flow). Code-level detection поддерживается на **Java 8+, .NET Framework 4.5+, Go**.

*Отличие от SAST.* Runtime-анализ, не статический. Видно, что уязвимость **реально вызывается** в работающем приложении, а не «теоретически есть в коде». Уязвимость автоматически закрывается, как только её root cause не появляется в системе более двух часов (или сразу при остановке всех затронутых процессов).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/secure/application-security/vulnerability-analytics -->

### Шаг 4: Attacks

![Attacks: детекция активных атак на приложения](screenshots/day-3-4/appsec/security/attacks/Attacks-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/security/attacks`.

*Активные атаки*: когда злоумышленник реально пытается эксплуатировать. Dynatrace инструментирует точки риска (SQL-вызов, выполнение команды ОС, исходящий HTTP-запрос, JNDI lookup) и видит подозрительные паттерны прямо в runtime, а не из логов WAF.

**На странице:**

- Список зафиксированных атак с временем.
- Тип атаки. По документации **Runtime Application Protection** в Managed детектирует и опционально блокирует ровно **4 класса атак**: **SQL injection**, **JNDI injection**, **Command injection**, **SSRF**.
- Source IP атакующего.
- Target: сервис, endpoint.
- Blocked / Allowed: если Application Protection активен.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/secure/application-security/application-protection -->

### Шаги 5-14: Settings страницы

Остальные 10 страниц, это настройки:
- **Monitoring rules for third-party** (`appsec.rule-settings`): какие правила детекции библиотечных CVE применять.
- **Attack Protection General** (`appsec.attack-protection-settings`): главный тумблер защиты (monitor-only vs block).
- **Attack Protection Monitoring** (`appsec.attack-protection-advanced-config`): какие типы атак детектировать.
- **Attack Protection Allowlist** (`appsec.attack-protection-allowlist-config`): белый список IP/URL для исключения из детекции.
- **Vulnerability Analytics General** (`appsec.runtime-vulnerability-detection`): главный тумблер обнаружения уязвимостей в runtime.
- **Code-level vulnerability rules** (`appsec.code-level-vulnerability-rule-settings`): правила детекции собственных уязвимостей.
- **Third-party vulnerability rules extended** (`appsec.third-party-vulnerability-rule-settings`): дополнительные правила для third-party.
- **Vulnerability alerting profiles** (`appsec.notification-alerting-profile`): маршрутизация уведомлений об уязвимостях.
- **Attack alerting profiles** (`appsec.notification-attack-alerting-profile`): маршрутизация уведомлений об атаках.

Каждая настройка имеет стандартную структуру: scope (на какие сервисы), условия, действия.

---

## 🎓 ТЕОРИЯ: Application Security как runtime-инструмент

### Отличие от классических SAST / DAST

- **SAST (Static Application Security Testing).** Анализ исходного кода без запуска. Примеры: SonarQube, Checkmarx. Находит потенциальные уязвимости, но не видит, что реально вызывается в production.
- **DAST (Dynamic Application Security Testing).** Тестирование с отправкой тестовых атак. Примеры: Burp Suite, OWASP ZAP. Находит уязвимости через имитацию атак, но требует тестовой среды.
- **Dynatrace Application Security**: runtime-анализ в production.

**Преимущества Dynatrace:**

- Не требует отдельной тестовой среды.
- Показывает **реальную эксплуатируемость** уязвимостей. CVE найдена в библиотеке, но если код уязвимого метода не вызывается: риск низкий.
- Детектирует **активные атаки** в реальном времени.

### Роль в compliance

Application Security: один из инструментов compliance:

- Регуляторы требуют регулярных отчётов по безопасности приложений.
- GDPR: для приложений с европейскими пользователями.
- PCI-DSS: для работы с карточными данными.

Автоматические отчёты экономят часы ручной работы по инвентаризации.

### Attack Protection: Monitor vs Block

- **Monitor.** Dynatrace детектирует и логирует атаку, не блокирует. Используется при первом запуске: увидеть false positives перед включением блокировки.
- **Block.** Dynatrace активно блокирует запросы, похожие на атаку. Превращает Dynatrace в частичный WAF.

*Типовая политика.* Сначала Monitor на 2-4 недели, затем Block для критичных endpoint'ов (платежи, аутентификация), остальные остаются Monitor.

### Поддерживаемые технологии

Это критично проверить на проекте: модуль AppSec в Managed Classic покрывает **не все** стеки:

- **Third-party vulnerabilities** (библиотеки): Java, .NET, Node.js, Python, Go, PHP.
- **Code-level vulnerabilities**: Java 8+, .NET Framework 4.5+, Go (для .NET, Go и Python требуется ручное включение deep monitoring).
- **Runtime Application Protection (блокировка атак)**: Java 8+ (OneAgent 1.241+), .NET Framework 4.5+ (OneAgent 1.289+), Go (OneAgent 1.311+). Только Windows x86 и Linux x86, только 64-битные процессы.

Для других технологий (Ruby, Erlang, Cobol) AppSec не работает: придётся опираться на сторонние SAST/DAST/WAF.

### Vulnerability feed и Mission Control

Для Managed-кластера обновления базы уязвимостей приходят через подключение к **Cloud Control / Mission Control** (закрытый канал Dynatrace). Источники feed: **Snyk** (для библиотек и runtime-компонентов в Kubernetes) и **NVD** (для .NET / Java / Node.js runtime). После публикации новой версии feed она доезжает до кластера в течение примерно двух часов; кластер сверяет окружение со свежими данными примерно раз в минуту.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/secure/faq -->

### Air-gapped нюансы

- В полностью air-gapped Managed-инсталляции обновление CVE-feed нужно явно прокидывать через разрешённый прокси к Mission Control либо организовывать оффлайн-импорт по согласованию с Dynatrace. Без свежего feed RVA продолжит работать на текущих данных, но новые CVE подхватятся только после следующего обновления.
- **Application Protection blocking** выполняется на стороне OneAgent внутри контура, без обращения наружу.
- **Внутренние SOC** интегрируются через Webhook / Email / ServiceNow notifications: те же каналы, что в incident-lifecycle.
