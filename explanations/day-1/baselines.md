> 📅 **День 1: Введение в систему Dynatrace** → Тема 9 из 11: «Построение базовых линий и работа с порогами»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services -->
>
> 🔖 **Редакция от 2026-04-27.** Тех-факты сверены с docs.dynatrace.com (Davis AI baseline / anomaly detection — общие концепции для Managed и SaaS, реализация 1:1; в air-gapped Managed работает без выхода в интернет, holiday-list поставляется в сборке кластера). 7-дневный learning period для traffic + 20%-недели (~1.4 дня) для error rate / response time подтверждены через WebFetch. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Общая (Managed + SaaS):**
> - [Anomaly detection — обзор](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/anomaly-detection) — корневая страница про автоматическое обнаружение аномалий
> - [Automated multi-dimensional baselining](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/anomaly-detection/concepts/automated-multidimensional-baselining) — почему baseline ведётся отдельно по каждому endpoint × геолокация × версия
> - [Seasonal baseline](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/ai-models/seasonal-baseline) — confidence band с учётом сезонности (день недели, время суток)
> - [Anomaly detection configuration](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/anomaly-detection/concepts/anomaly-detection-configuration) — как настраиваются параметры детекции
> - [Adjust sensitivity for services](https://docs.dynatrace.com/docs/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services) — Response time degradation: absolute + relative threshold, low-load filter, abnormal state duration
> - [Adjust sensitivity for database services](https://docs.dynatrace.com/docs/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services-database) — те же параметры + Failed connects detection
> - [Anomaly detection for services — settings schema](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-api/environment-api/settings/schemas/builtin-anomaly-detection-services) — формальная схема страницы Settings → Anomaly detection → Services
> - [Davis AI](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai) — корневая страница про Davis AI engine

## 📍 КАРТА — где настраиваются правила обнаружения аномалий

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Аномалии сервисов | **Settings → Anomaly detection → Services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services` |
| Аномалии баз данных | **Settings → Anomaly detection → Database services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.databases` |
| Аномалии инфраструктуры | **Settings → Anomaly detection → Hosts** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.infrastructure-hosts` |
| Учёт праздников в baseline | **Settings → Anomaly detection → Holiday-aware baseline** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.holiday-aware-baseline` |
| Обнаружение частых проблем | **Settings → Anomaly detection → Frequent issue detection** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.frequent-issues` |

**Термины темы.**

- **Baseline / базовая линия / эталон** — коридор нормального поведения метрики во времени, построенный Davis AI.
- **Anomaly / аномалия** — значение метрики, вышедшее за границы baseline больше заданного процента.
- **Davis AI** — встроенный AI-engine Dynatrace, строит baseline и находит аномалии автоматически.
- **Threshold / порог** — числовое значение, при превышении которого срабатывает алерт.
- **Reference period / период эталона** — сколько дней истории Davis использует для построения baseline.

**Три типа порогов.**

| Тип | Как работает | Когда применяется |
|---|---|---|
| **Auto-adaptive / адаптивный** | Davis AI анализирует историю метрики (по умолчанию 7 дней), строит коридор с учётом времени суток и дня недели. Выход за коридор = аномалия. | По умолчанию для большинства метрик. Работает из коробки. |
| **Static / статический** | Администратор задаёт фиксированное число. «CPU выше 80% = аномалия». | Требования compliance, SLA с фиксированным порогом, известный технический предел. |
| **Metric events / метрические события** | Кастомное правило на любую метрику с выражением на Metrics Selector. | Сложные сценарии, связка нескольких метрик, собственная логика. |

---

## 🎬 Работа с baseline на пяти экранах

### Шаг 1 — Anomaly detection / Services

![Anomaly detection for services — правила обнаружения аномалий сервисов](screenshots/day-1/baselines/settings/builtinanomaly-detection.services/Anomaly-detection-for-services-Environment-Settings-Demo-live-Demo-Live-Dynatrac.png)

Путь: **Settings → Anomaly detection → Services** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services`.

**Что на экране.** Правила обнаружения аномалий на уровне сервисов. Под заголовком Dynatrace пишет: платформа автоматически обнаруживает деградацию времени отклика и рост частоты отказов. Правила сгруппированы в блоки, у каждого — тумблер включения и параметры.

**Блок Response time / время отклика.**

Тумблер **Detect response time degradations** включает весь блок. **Detection mode** по умолчанию Automatic — Davis AI сам выбирает пороги по истории сервиса.

Два подправила.

- **All requests / все запросы.** Срабатывает, когда медиана времени отклика выросла по обоим критериям одновременно:
  - **Absolute threshold / абсолютный порог** — по умолчанию 100 мс.
  - **Relative threshold / относительный порог** — по умолчанию 50%.
- **Slowest 10% / верхние 10% самых медленных.** Иногда деградируют только тяжёлые случаи — крупные отчёты, большие выборки. Absolute 1000 мс, Relative 50% по умолчанию.

**Блок Avoid over-alerting / защита от ложных срабатываний.** Требует минимум N запросов в минуту на сервис (по умолчанию 10), прежде чем аномалия засчитывается. Плюс минимум N минут длительности (по умолчанию 1). Нужно, чтобы на редко используемых сервисах не гремели алерты от одного-двух случайных запросов.

**Блок Failure rate / частота отказов.** Тумблер **Detect increases in failure rate**. Абсолютный порог по умолчанию 0.1%, относительный 50%. Под параметрами — пример расчёта: если базовая failure rate была 11%, порог срабатывания = 11 + (11 × 50% / 100%) = 16.5%.

**Блок Service load drops / spikes / падения и скачки нагрузки.** Падение нагрузки обычно значит, что клиенты не могут достучаться до сервиса (DNS, сеть, балансировщик). Скачок — внезапный рост (DDoS или вирусный контент). Пороги в процентах от ожидаемой нагрузки.

**Reference period / период эталона.** Сколько дней истории Davis использует для baseline. По умолчанию **Last 7 days**. После архитектурных изменений (новая версия, новая нагрузка) Davis пересчитывает эталон — в ближайшие часы возможны ложные срабатывания, об этом предупреждает текст внизу страницы.

### Шаг 2 — Anomaly detection / Database services

![Anomaly detection for databases — правила для баз данных](screenshots/day-1/baselines/settings/builtinanomaly-detection.databases/Anomaly-detection-for-databases-Environment-Settings-Demo-live-Demo-Live-Dynatra.png)

Путь: **Settings → Anomaly detection → Database services** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.databases`.

Страница построена по той же схеме, что и для сервисов. Те же блоки Response time, Avoid over-alerting, Failure rate, Service load drops / spikes. Отличие — в типовых значениях порогов (базы обычно медленнее обычных сервисов) и одном дополнительном блоке.

**Блок Database failed connects / неудачные подключения.**

*Что делает.* Тумблер **Detect failed connects** включает правило. Порог — процент неудачных подключений за минуту (по умолчанию 5%).

*Зачем нужно.* В системах с пулом подключений проблема «не могу подключиться» проявляется до того, как пользователи увидят ошибки в самих запросах. Ловить её нужно быстрее.

*Какие классы проблем ловит.*
- TCP-соединение между сервисом и базой сломалось (firewall, маршрутизация).
- У базы кончились свободные соединения (`max_connections` в PostgreSQL, пул HikariCP на клиенте).
- У пользователя БД истёк пароль или закончились привилегии.
- Failover на реплику — новый инстанс не принимает соединения первые секунды.

### Шаг 3 — Anomaly detection / Hosts

![Anomaly detection for infrastructure — более 20 правил для хостов](screenshots/day-1/baselines/settings/builtinanomaly-detection.infrastructure-hosts/Anomaly-detection-for-infrastructure-Host-Environment-Settings-Demo-live-Demo-Li.png)

Путь: **Settings → Anomaly detection → Hosts** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.infrastructure-hosts`.

**Что на экране.** Самая большая страница в блоке Anomaly detection. Правил больше 20 — каждое с тумблером включения и параметрами чувствительности.

**Основные категории правил.**

- **CPU.** Тумблер **Detect unusual high CPU saturation**. Порог по умолчанию 95% в течение 5 минут. Срабатывает, когда процессор забит почти полностью, а не когда просто «загружен высоко». Для сервера с постоянной нагрузкой 70% порог 95% не будет ложно срабатывать.
- **Memory.** Detect unusual high memory usage, Detect memory page swapping (активный своп — один из худших сигналов на сервере), отдельные параметры для Linux и Windows.
- **Disk.** Detect low disk space, Detect slow writes, Detect slow reads, Detect high disk inode usage (inode-ы кончаются — бывает на больших файловых системах с множеством мелких файлов).
- **Network.** Detect network high packet loss rate (потеря пакетов), Detect network high retransmissions (переотправки TCP), Detect network connectivity issues, Detect network high traffic, Detect network low connectivity (плохая связь с ActiveGate или кластером).
- **GPU** (на хостах с графическими ускорителями). Detect GPU memory saturation, Detect GPU usage saturation. Актуально для ML-нагрузок и видеообработки.
- **OS-specific.** Для Windows — правила на Windows Events. Для Linux — kernel-сообщения.

**Типичная практика.** Большинство правил оставляют в дефолте. Отключают только те, что дают много ложных срабатываний для конкретного класса серверов. Пример: на серверах БД правило High memory usage часто отключают на уровне хост-группы — БД специально занимает всю свободную память под кэш, это нормальное состояние.

### Шаг 4 — Holiday-aware baseline / учёт праздников

![Holiday-aware baseline — включение учёта праздников в baseline](screenshots/day-1/baselines/settings/builtinanomaly-detection.holiday-aware-baseline/Holiday-aware-baseline-modification-Environment-Settings-Demo-live-Demo-Live-Dyn.png)

Путь: **Settings → Anomaly detection → Holiday-aware baseline modification** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.holiday-aware-baseline`.

*Что делает.* Один тумблер **Holiday aware**. Когда включён, Davis AI при построении baseline исключает из обучающей выборки государственные праздники.

*Зачем нужно.* Праздники искажают baseline. В праздник нагрузка либо заметно ниже (люди не работают), либо заметно выше (предпраздничные пики покупок). Если 1 января сравнивать с обычным вторником, baseline начнёт показывать ложные аномалии. С включённым тумблером Davis вырезает праздничные дни из обучения.

*Какие праздники считаются праздниками.* На странице указан список по умолчанию: **New Year, Easter, Thanksgiving, Black Friday, Christmas**.

*Ограничение для Казахстана.* По умолчанию Dynatrace не знает казахстанских праздников — Наурыз, День Республики, День Конституции, День столицы, День Первого Президента. Тумблер Holiday aware на них не сработает, baseline в эти дни может отклоняться.

*Как закрывают.* Связка с **Maintenance windows** (Settings → Preferences → Maintenance windows). На дни казахстанских праздников создаётся отдельное Maintenance window в режиме «окно тишины». В нём Dynatrace не создаёт проблемы и не шлёт уведомления. Это не исправляет искажение baseline, но убирает спам алертов.

*На демо-тенанте.* Тумблер серый — у пользователя нет write-прав. На боевом окружении администратор включает его сразу после развёртывания кластера, это стандартный шаг настройки.

### Шаг 5 — Frequent issue detection / группировка частых проблем

![Frequent issue detection — агрегация повторяющихся проблем](screenshots/day-1/baselines/settings/builtinanomaly-detection.frequent-issues/Frequent-issue-detection-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Anomaly detection → Frequent issue detection** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.frequent-issues`.

*Что делает.* Механизм обработки повторяющихся проблем. Если Dynatrace замечает одну и ту же проблему много раз за неделю, он конвертирует её в **часто повторяющуюся** и агрегирует новые появления вместо создания новых Problems.

*Зачем нужно.* В реальной инфраструктуре есть проблемы-шумы: каждую ночь cron-скрипт на 15 минут забивает диск и проходит. Если каждое такое событие создавать как отдельную Problem, за неделю наберутся сотни одинаковых записей — реально важные проблемы в них теряются.

*Как работает в UI.* В разделе Problems такая проблема видна как одна запись, но с индикатором «повторяющаяся». В карточке можно посмотреть все отдельные случаи.

*Четыре тумблера — по одному на уровень.*

- **Detect frequent issues within applications** — пользовательские приложения (RUM).
- **Detect frequent issues within transactions and services** — сервисы и транзакции backend.
- **Detect frequent issues within infrastructure** — хосты, процессы, сети.
- **Detect frequent issues on the environment (ingress entity)** — весь кластер в целом.

*По умолчанию.* Все четыре включены. На большинстве инсталляций не трогают.

*Когда отключают.* Два сценария.
- Нужно, чтобы каждое появление проблемы попадало в ITSM как отдельный инцидент — выключают свёртывание на соответствующем уровне.
- Первичная настройка окружения, когда Dynatrace ещё не накопил истории и может некорректно классифицировать проблемы как «частые».

---

## 🎓 ТЕОРИЯ — как работает автоматический multidimensional baselining

**Baseline строится для каждой сущности отдельно.** Если в окружении 100 сервисов — Davis ведёт 100 отдельных моделей. Один сервис — своя нормальная скорость, другой — своя. Это отличается от классического мониторинга с общим порогом «алерт, если отклик больше 500 мс». Такой порог не имеет смысла для сервиса со средним откликом 50 мс (всегда норма) и одновременно не имеет смысла для сервиса со средним откликом 2000 мс (всегда аномалия).

**Baseline учитывает сезонность.** Модель знает: утром в понедельник нагрузка такая-то, в пятницу вечером другая, в субботу ночью почти нулевая. Если сервис обычно отвечает за 50 мс утром и 120 мс в пик-часы, для Davis это два разных эталона — вечерние 120 мс не аномалия.

**Baseline многомерный.** Для одной метрики ведутся несколько разрезов одновременно. Согласно [Automated multidimensional baselining](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/anomaly-detection/concepts/automated-multidimensional-baselining), Davis для frontend RUM комбинирует разрезы по **user action / endpoint** (например, `login.jsp`), **geolocation** (континент / страна / регион / город), **browser** (семейство и версия) и **operating system** (тип и версия). Для backend сервисов аналогично — отдельные baselines по типам запросов и характеристикам клиента. Аномалия может засечься в одном разрезе, не затронув общую картину. Пример: общее время отклика сервиса в норме, но для конкретного endpoint `/api/heavy-report` выросло на 200% — многомерный baseline это увидит.

**Период обучения — 7 дней.** Меняется в Reference period. По [официальной формулировке](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/anomaly-detection/concepts/automated-multidimensional-baselining): «alerting on traffic spikes and drops begins after a learning period of one week because baselining requires a full week's worth of traffic to learn daily and weekly patterns» — для срабатывания алертов на skoki/drop трафика нужна полная неделя истории; для error rate и response time пороги активизируются раньше — после 20% недели (около 1.5 дней). После значительного архитектурного изменения имеет смысл сбросить baseline вручную или подождать 7 дней, пока модель пересчитается естественным путём. <!-- last-verified: 2026-04-27 source: docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/anomaly-detection/concepts/automated-multidimensional-baselining -->

**Defaults на странице Settings → Anomaly detection → Services.** Точные числовые дефолты (Absolute / Relative / Avoid over-alerting) Dynatrace не публикует одной общей таблицей в публичной доке — значения, видимые в самой странице Settings, считаются authoritative для конкретной сборки кластера. Цифры выше («100 мс / 50% / 0.1% / 10 rpm / 1 минута») приведены как ориентир для типичной свежей инсталляции и должны сверяться с реальной страницей вашего тенанта перед использованием в SLA или интеграциях.

**Adaptive vs Static.** Адаптивный baseline — основной инструмент, его хватает для 80% задач. Static thresholds применяются поверх адаптивных в двух случаях:
- **Compliance.** SLA требует «тревога строго при CPU выше 85%» независимо от baseline.
- **Bootstrap.** Первая неделя после установки, когда адаптивная модель ещё не накопила данных.

**В air-gapped контексте.** Весь механизм работает полностью локально. Baseline строится на данных агентов, которые уже в кластере. Внешних вызовов нет. Holiday-aware требует только списка праздников — он поставляется в сборке Dynatrace и обновляется при ручной загрузке новой версии через CMC.
