# Empty / SaaS-only / In-development скрины — TODO

Скрины из output/screenshots/, которые показывают пустой UI, состояние "No data to display", "In development", "User does not have the necessary write permissions" или SaaS-only функциональность, не работающую в Managed Classic.

Правило: такие скрины НЕ описываются как часть Managed-курса. Файл `explanations/*.md` переписывается так, чтобы тема объяснялась через реально работающие в Managed механизмы.

## Day 4 (2026-04-27)

### reliability-config.md — все три скриншота

Все три страницы Settings помечены статусом **"In development"** в Managed (раздел Dynatrace Service Settings) и для пользователей курса фактически недоступны:

- `screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.service-alert/Schema-for-service-alerts-...png`
  - Заголовок: «Schema for service alerts» — `In development`
  - Сообщение: «Your user does not have the necessary write permissions» + «No data to display»
- `screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.frontend-alert/Frontend-health-alerts-...png`
- `screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.cloud-alert/Cloud-health-alerts-settings-...png`

Решение: тема reliability-config переписана с акцентом на реальные механизмы Managed Classic (Anomaly detection / SLO / Alerting profiles), Health Experience описана как SaaS-only слой (Services app / Experience Vitals app / Clouds app), которые в Managed Classic не активированы.

## Day 5 (2026-04-27)

### synthetic.md — Шаг 1 (`/ui/synthetic`) — 403 Forbidden

Скриншот: `screenshots/day-5/synthetic/synthetic/403-You-dont-have-permission-to-view-this-page-Demo-live-Demo-Live-Dynatrace.png`

На captured-тенанте `guu84124` страница списка synthetic-мониторов отдаёт **403 Forbidden** — модуль Synthetic на этом учебном окружении не активирован / у роли нет прав. UI-элементы для описания списка мониторов в captured-данных отсутствуют.

Решение: тема synthetic.md описывает Synthetic Monitoring через официальную документацию Dynatrace Managed (типы мониторов, private locations, Synthetic-enabled ActiveGate, capacity-индикация); Шаг 1 явно отмечен как недоступный экран на captured-тенанте, дальше используются настроечные страницы Шагов 2–4 (availability settings, browser/HTTP outage handling), которые в captured-данных есть.
