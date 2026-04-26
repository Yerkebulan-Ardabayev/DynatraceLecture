> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 12 из 14: «Настройка измерения надёжности на уровне сервисов и приложений»

## 📍 КАРТА — три страницы про Health Experience

Термины темы: `Health Experience / опыт надёжности` (расширенный alerting слой), `Severity / серьёзность` (Critical / Warning / Informational), `Bus context / бизнес-контекст`, `Intelligent grouping / умная группировка`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Service-level health alerts | **Settings → Server-side service monitoring → Health experience → Service alerts** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.service-alert` |
| Frontend health alerts | **Settings → Web and mobile monitoring → Health experience → Frontend alerts** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.frontend-alert` |
| Cloud health alerts | **Settings → Cloud and virtualization → Health experience → Cloud alerts** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:health-experience.cloud-alert` |

---

## 🎬 Работа с health alerts на трёх экранах

### Шаг 1 — Service-level health alerts

![Schema for service alerts — настройка health-сигналов для сервисов](screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.service-alert/Schema-for-service-alerts-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:health-experience.service-alert`.

*Что такое Health Experience.* Расширенный механизм alerting. Каждый тип сигнала (slow response, error, availability issue) имеет свою настройку — не только пороги, но и бизнес-категории, severity classification, intelligent grouping.

**Что настраивается:**

- Какие типы health issue детектировать для сервисов (slowdowns, error spikes, availability drops).
- Severity mapping — какой тип проблемы в какую категорию (Critical / Warning / Informational).
- Custom rules для специфичных сервисов.

*Отличие от Anomaly detection.* Anomaly detection — массовый и глобальный. Health Experience — более тонкий, с бизнес-контекстом. Работают параллельно.

### Шаг 2 — Frontend health alerts

![Frontend health alerts — health-сигналы для фронтенда](screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.frontend-alert/Frontend-health-alerts-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:health-experience.frontend-alert`.

Для Applications (web / mobile). Сигналы:

- High error rate in sessions.
- Slow page loads.
- Crash rate spikes.
- User experience degradation.

### Шаг 3 — Cloud health alerts

![Cloud health alerts — health для облачных ресурсов](screenshots/day-3-4/reliability-config/settings/builtinhealth-experience.cloud-alert/Cloud-health-alerts-settings-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:health-experience.cloud-alert`.

Для облачных ресурсов (Kubernetes, AWS, Azure):

- K8s cluster resource pressure.
- Cloud resource provisioning failures.
- Cost spikes (если настроено).

---

## 🎓 ТЕОРИЯ — Health Experience как слой поверх базовых сигналов

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Service-Level Objectives (SLO)](https://docs.dynatrace.com/docs/shortlink/service-level-objectives)

Health Experience — не замена anomaly detection, а **слой бизнес-семантики** поверх него.

- **Классический anomaly detection** даёт: «метрика X выросла на Y% относительно baseline».
- **Health Experience** даёт: «в сервисе `retail-api` произошёл slowdown (категория = Critical), затронул 15 downstream сервисов, был triggered деплоем 10 минут назад».

Информации больше, принимать решения проще.

*Типовое применение.* Включают для критичных сервисов после первичной настройки базовых anomaly detection — как второй слой улучшения observability.

### Air-gapped specifics

Все правила хранятся локально. Никаких внешних сервисов.
