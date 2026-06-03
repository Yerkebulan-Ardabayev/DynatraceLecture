> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 11 из 14: «SLI, SLO, SLA: подходы и реализация»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/slo -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27**

## 📚 Источники

- [Service-Level Objectives: Managed](https://docs.dynatrace.com/managed/shortlink/service-level-objectives)
- [SLO Classic basics](https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/slo-basics)
- [Configure and monitor SLOs](https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/configure-and-monitor-slo)
- [SLO Classic: definition examples](https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/slo-definition-configuration-examples)
- [Davis AI: anomaly detection](https://docs.dynatrace.com/managed/dynatrace-intelligence/anomaly-detection)

## 📍 КАРТА: три страницы про надёжность как сервис

Термины темы: `SLI / индикатор уровня сервиса`, `SLO / цель уровня сервиса`, `SLA / соглашение об уровне сервиса`, `Error budget / бюджет ошибок`, `Burn rate / скорость сжигания бюджета`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| SLO dashboard | **Automations → Service-Level Objectives** | `https://guu84124.live.dynatrace.com/ui/slo` |
| SLO definitions | **Settings → Service-level objectives → Definition** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:monitoring.slo` |
| SLO setup | **Settings → Service-level objectives → Setup** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:monitoring.slo.normalization` |

**Полное значение терминов:**

| Термин | Что значит | Пример |
|---|---|---|
| **SLI** (Service Level Indicator) | Измеряемая метрика работы сервиса | Availability = доля успешных API-вызовов |
| **SLO** (Service Level Objective) | Целевое значение SLI за период | Availability ≥ 99.9% за 30 дней |
| **SLA** (Service Level Agreement) | Контрактное обязательство перед клиентом, с санкциями | «Гарантируем Availability ≥ 99.5%, при нарушении: компенсация» |

---

## 🎬 Работа с SLO на трёх экранах

### Шаг 1: SLO dashboard

![Service-level objectives: список всех SLO с их статусом](screenshots/day-3-4/sli-slo-sla/slo/Service-level-objectives-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/slo`.

**Центральная страница работы с SLO.** Показывает все настроенные SLO в окружении с их текущим статусом:
- Имя SLO (например, `retail-api-availability`).
- Target (99.9%).
- Current value (99.97%: в пределах target).
- Error budget remaining (сколько осталось «нарушать» до срыва SLO).
- Trend (растёт или падает).
- Warning/Critical/OK: цвет статуса.

**Каждый SLO** имеет карточку с историей изменения, с графиком budget burn rate.

### Шаг 2: SLO definitions

![SLO definitions: управление определениями SLO](screenshots/day-3-4/sli-slo-sla/settings/builtinmonitoring.slo/Service-level-objective-definitions-Environment-Settings-Demo-live-Demo-Live-Dyn.png)

Путь: `/ui/settings/builtin:monitoring.slo`.

**Здесь создаются SLO.** Удобный сценарий: SLO wizard с готовыми шаблонами. Доступные шаблоны:

- **Service-level availability**: отношение успешных вызовов сервиса к общему количеству.
- **Service-method availability**: то же на уровне отдельного key request.
- **Service performance**: доля вызовов с откликом меньше порога.
- **User experience**: на базе Apdex.
- **Mobile crash-free users**: доля сессий без сбоев.
- **Synthetic availability**: успешность Synthetic-чеков.

Структура одного SLO:

- **Имя**: `retail-api-availability`.
- **SLI** (Service-Level Indicator): метрика, по которой считается; для service availability это `builtin:service.successes` / `builtin:service.requestCount.total`.
- **Target**: 99.9%.
- **Evaluation timeframe**: за какой срок считается.
- **Error budget** и **burn rate**: Dynatrace вычисляет автоматически; burn rate = 1 означает «при текущем темпе budget будет полностью израсходован за длительность SLO».
- **Alerting**: два типа: status alert (статус упал ниже target) и burn rate alert (budget съедается слишком быстро).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/configure-and-monitor-slo -->

### Шаг 3: SLO setup (нормализация)

![SLO setup: настройка нормализации SLO](screenshots/day-3-4/sli-slo-sla/settings/builtinmonitoring.slo.normalization/Service-level-objective-setup-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:monitoring.slo.normalization`.

**Дополнительные параметры расчёта SLO:**

- **Normalize error budget**: глобальный тумблер. Когда включён, остаток бюджета считается по формуле `(status − target) ÷ (100 − target) × 100`. Например, при target 95% и текущем статусе 96% normalized error budget = 20%. Без нормализации сравнивать budget между SLO с разными target неудобно: нормализация приводит всё к 0–100% и упрощает дашборды.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/slo-basics -->

---

## 🎓 ТЕОРИЯ: SLI/SLO/SLA в банковской практике

### Типовые SLI

| Сервис | Типовой SLI |
|---|---|
| Интернет-банк (UI) | % успешных загрузок страниц с HTTP 200 |
| API аутентификации | % успешных вызовов `/auth/login` |
| Платёжный сервис | % успешных платежей < 3 секунд |
| Мобильный банк | Crash rate < 0.5% |
| Карточный процессинг | Доля транзакций < 500 мс |

### Типовые уровни SLO

- **Внутренние (технические)**: 99.9% / 99.95%. Строго контролируются командой эксплуатации.
- **Клиентские (внешние)**: 99.5% / 99.9%. Фигурируют в маркетинге и SLA.
- **Критические (real-time платежи)**: 99.99% или даже 99.999%. Обычно для процессинга.

### Error budget как управленческий инструмент

*Error budget* = допустимое количество «нарушений» SLO за период.

*Пример расчёта.* Target = 99.9% за 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты** даунтайма в месяц.

*Как используется.* Если в начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки **замораживает выкатки** рискованных изменений до конца месяца. Если budget не израсходован: можно тестировать новые фичи активно.

Это баланс между **надёжностью** и **скоростью инноваций**.

### SLA vs SLO

- **SLO**: внутренний контракт. Цель команды. Может быть ужесточён или смягчён по ситуации.
- **SLA**: внешний контракт с клиентом. При нарушении: финансовые санкции. Обычно **слабее SLO**, чтобы был запас.

*Пример.* SLA = 99.5%, SLO = 99.9%. Команда нарушила SLO (уровень 99.7%): внутренний сигнал «что-то не так, копаем». Клиенту SLA не нарушен, санкций нет. Если нарушили SLA (99.3%): санкции + серьёзный разбор полётов.

### Air-gapped нюансы

Все SLO вычисляются локально в кластере на метриках из Cassandra. Внешних сервисов нет. SLO-дашборды живут в кластере, статус и burn rate тянутся через Service-level objectives API во внутренние BI-системы банка.
