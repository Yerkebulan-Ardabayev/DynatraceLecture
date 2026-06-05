> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 12 из 14: «Настройка измерения надёжности на уровне сервисов и приложений»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.service-alert -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [Anomaly detection: Managed](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection)
- [Adjust sensitivity for services](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services)
- [Adjust sensitivity for applications](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-applications)
- [Service-Level Objectives: Managed](https://docs.dynatrace.com/managed/shortlink/service-level-objectives)
- [Davis AI: anomaly detection concepts](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection)

## 📍 КАРТА: три страницы Health Experience (статус «In development»)

Термины темы: `Health Experience / опыт надёжности`: новый слой alerting в Dynatrace Apps platform; `Severity / серьёзность` (Critical / Warning / Info); `Anomaly detection / детектор аномалий`; `SLO / цель уровня сервиса`; `Alerting profile / профиль оповещений`. <!-- qc:ignore=SAAS -->

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Service-level health alerts | **Settings → Dynatrace Service Settings → Schema for service alerts** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.service-alert` |
| Frontend health alerts | **Settings → Dynatrace Service Settings → Frontend health alerts** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.frontend-alert` |
| Cloud health alerts | **Settings → Dynatrace Service Settings → Cloud health alerts settings** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.cloud-alert` |
| → Рабочая замена: Anomaly detection for services | **Settings → Anomaly detection → Services** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly-detection.services` |
| → Рабочая замена: SLO definitions | **Settings → Service-level objectives → Definition** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:monitoring.slo` |
| → Рабочая замена: Alerting profiles | **Settings → Alerting → Alerting profiles** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.profile` |

> **Важно для Managed Classic.** Эти три страницы Settings относятся к новому слою **Health Experience**, который реализован как часть SaaS Apps platform: Services app / Experience Vitals (Frontend) app / Clouds app. В Managed Classic эти Apps не включены. На снятых скриншотах все три экрана показывают состояние **«In development»** + **«No data to display»** + ошибку прав. Это означает, что в курсе мы их **не настраиваем**, а используем реально работающие в Managed Classic механизмы измерения надёжности: Anomaly detection, SLO и Alerting profiles.

---

## 🎬 Что видно на трёх экранах в Managed Classic

### Шаг 1: Schema for service alerts

![Schema for service alerts: статус In development](screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.service-alert/Schema-for-service-alerts-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:health-experience.service-alert`.

В заголовке страницы: пометка **«In development»**, тело страницы: «No data to display» + предупреждение о недостающих правах. Это не баг тенанта: схема `builtin:health-experience.service-alert` входит в Settings 2.0 для будущей синхронизации с Services app, но в Managed Classic UI-форма не активна.

**Что вместо этого использовать в Managed Classic:**

- **Anomaly detection for services** (`builtin:anomaly-detection.services`): настройка чувствительности для response time, slowest 10%, failure rate, traffic.
- **SLO** (`builtin:monitoring.slo`): измеримые цели (см. предыдущую тему «SLI, SLO, SLA»).
- **Alerting profiles** (`builtin:alerting.profile`): какие проблемы Davis AI пускать дальше, по каким правилам severity и каналам уведомлять (см. следующую тему «Incident Lifecycle»).

### Шаг 2: Frontend health alerts

![Frontend health alerts: пустой экран](screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.frontend-alert/Frontend-health-alerts-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:health-experience.frontend-alert`.

Та же история: схема для будущей **Experience Vitals app** (новая RUM Apps-платформа). В Managed Classic экран пустой.

**Что вместо этого использовать в Managed Classic:**

- **Anomaly detection for web applications** (`builtin:anomaly-detection.rum-web`): деградации key performance metrics, traffic drops/spikes, failure rate (см. тему «Настройка порогов»).
- **Anomaly detection for mobile applications** + отдельные настройки crash rate.
- **SLO с шаблонами «User experience»** (Apdex) и «Mobile crash-free users».

### Шаг 3: Cloud health alerts settings

![Cloud health alerts: пустой экран](screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.cloud-alert/Cloud-health-alerts-settings-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:health-experience.cloud-alert`.

Схема для будущей **Clouds app** (готовые health-оповещения по AWS / Azure / GCP-сервисам). В Managed Classic не активна.

**Что вместо этого использовать в Managed Classic:**

- **Anomaly detection for Kubernetes** (cluster, namespace, node, workload, PVC): было в Дне 2.
- **Anomaly detection for hosts / disk / processes**: настраивается на уровне инфраструктуры (см. День 2).
- Алертинг по облачным сервисам через стандартные **Cloud monitoring extensions**.

---

## 🎓 ТЕОРИЯ: как реально измеряется надёжность в Managed Classic

Связка из трёх слоёв (как они срабатывают по цепочке):

- **ЕСЛИ** настроите Anomaly detection (порог или baseline) → **ТО** Davis заведёт Problem при выходе метрики за порог, иначе отклонение останется незамеченным.
- **ЕСЛИ** определите SLO с target → **ТО** Dynatrace посчитает error budget и burn rate и заведёт status- или burn-rate-алерт при просадке, без SLO «здоровье» не измеряется в процентах.
- **ЕСЛИ** настроите Alerting profile под нужный severity и зону → **ТО** проблема уйдёт в указанный канал (email / webhook / ServiceNow / OpsGenie / Jira), иначе Davis-проблема создастся, но никого не оповестит.

### 1. Anomaly detection: что считать отклонением

Davis AI с baseline по 7 дням: для key performance metrics, failure rate, traffic. Альтернатива: fixed thresholds с уровнями Low / Medium / High. Для service-уровня: response time (median и slowest 10%) + failure rate + load drops/spikes. Для приложений: page load / user action duration + traffic + failure rate + crash rate (mobile). Конфигурация: глобальная и переопределяемая на уровне отдельных сервисов / приложений.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection/adjust-sensitivity-anomaly-detection/adjust-sensitivity-services -->

### 2. SLO: целевая надёжность сервиса

Сервис «здоров», если SLI достигает target за evaluation period. Для каждого сервиса/приложения определяется один или несколько SLO; Dynatrace считает текущий статус, остаток error budget и burn rate. Доступны два типа алертов: status alert (status упал ниже target) и burn rate alert (бюджет тает слишком быстро).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/configure-and-monitor-slo -->

### 3. Alerting profile: кому и когда сообщать

Тонкий фильтр поверх Davis-проблем: какие severity уровни, какие management zones, какие задержки до отправки в email / webhook / ServiceNow / OpsGenie / Jira. Здесь задаётся, что Critical для платежного сервиса должно уйти в Telegram дежурного через 0 минут, а Warning для тестового стенда: никогда.

### Health Experience и SaaS

Health Experience, это слой презентации этих сигналов в новых Dynatrace Apps (Services app, Experience Vitals app, Clouds app). На SaaS-платформе он даёт готовые health-дашборды и tweak-правила прямо в интерфейсе Apps. В Managed Classic эта функциональность не активна, но базовые сигналы те же: Davis-проблемы, рассчитанные anomaly detection и SLO. Когда (и если) Apps platform появится в Managed, эти три Settings-страницы получат полноценный UI.

### Air-gapped specifics

Все правила и состояние SLO хранятся локально в кластере (Cassandra). Никаких внешних сервисов не используется. Уведомления уходят только в системы, доступные изнутри контура: внутренний Telegram-бот, корпоративный SMTP, внутренний Webhook-приёмник.
