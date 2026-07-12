---
topic_id: reliability-config
day_id: day-3-4
timing_min: 24
verified: 2026-07-12
---
## ГДЕ
Формально тема живёт на трёх Settings-страницах Health Experience: Service-level health alerts, route `/ui/settings/builtin:health-experience.service-alert`; Frontend health alerts, `builtin:health-experience.frontend-alert`; Cloud health alerts, `builtin:health-experience.cloud-alert`.
В Managed Classic все три в статусе «In development», их не настраиваем. Реально работаем на трёх других экранах: Anomaly detection for services `/ui/settings/builtin:anomaly-detection.services`, SLO definitions `builtin:monitoring.slo`, Alerting profiles `builtin:alerting.profile`.

## ЗАЧЕМ
Измеряем надёжность на уровне сервиса и приложения: в норме ли метрика, достигает ли сервис своей цели, узнает ли о просадке дежурный.
Health Experience это витрина этих сигналов в новых Dynatrace Apps (Services, Frontend, Clouds). В Managed Classic эти Apps не включены, поэтому надёжность настраиваем через сами сигналы: Anomaly detection, SLO, Alerting profiles.

## ЦИФРЫ
- Три страницы Health Experience (Service / Frontend / Cloud health alerts): все три показывают «In development», «No data to display» и ошибку прав, в Managed Classic не настраиваются.
- Три рабочих слоя надёжности вместо них: Anomaly detection → SLO → Alerting profiles.
- Baseline Davis: 7 дней истории для key performance metrics, failure rate и traffic.
- Порог response time на сервисе ставится отдельно на median и на slowest 10%.
- SLO даёт два типа алертов: status alert (статус упал ниже target) и burn rate alert (error budget тает слишком быстро).

## ЕСЛИ→ТО
- ЕСЛИ открыть любую из трёх Health Experience страниц в Managed Classic → «In development» и «No data to display», настраивать нечего, иду на Anomaly detection / SLO / Alerting profiles.
- ЕСЛИ настроен Anomaly detection (порог или baseline) → Davis заводит Problem при выходе метрики за коридор, иначе отклонение остаётся незамеченным.
- ЕСЛИ задан SLO с target → Dynatrace считает error budget и burn rate и шлёт status- или burn-rate-алерт при просадке, без SLO надёжность не меряется в процентах.
- ЕСЛИ настроен Alerting profile под severity и зону → проблема уходит в канал (email / webhook / ServiceNow / OpsGenie / Jira), иначе Davis-проблема создаётся, но никого не будит.

## ЗАПАСНОЙ ПЛАН
Три Health Experience экрана на демо серые: «In development», «No data to display», ошибка прав. Проговариваю честно, что это не баг тенанта, а неактивные в Managed Classic Settings-оболочки, и не пытаюсь их настроить.
Показываю рабочую тройку: открываю Anomaly detection for services, SLO definitions и Alerting profiles, на них демонстрирую реальную настройку надёжности.
Если и эти страницы серые (нет write-прав на демо): пороги по памяти не называю, показываю снимок и говорю, что на боевом окружении админ задаёт значения на самой странице тенанта.

## ВОПРОСЫ АУДИТОРИИ
- «Почему страница Service-level health alerts пустая, это баг?» Ответ: нет, это схема Health Experience для нового Apps-слоя, в Managed Classic UI-форма не активна («In development»), а надёжность настраивается через Anomaly detection, SLO и Alerting profiles.
- «Работает ли всё это в закрытом контуре?» Ответ: да, правила и статус SLO хранятся локально в кластере (Cassandra), уведомления уходят только внутрь контура: внутренний Telegram-бот, корпоративный SMTP, внутренний Webhook-приёмник.
- «Чем SLO-алерт отличается от anomaly-алерта?» Ответ: anomaly detection ловит выход метрики за коридор нормы, SLO следит за выполнением цели, status alert срабатывает при падении ниже target, а burn rate alert когда error budget тает слишком быстро.
