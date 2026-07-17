> 📅 **День 1: Введение в систему Dynatrace** → Тема 10 из 11: «Функционал Problems: автоматическая детекция инцидентов»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/problems -->
>
> 🔖 **Редакция от 2026-04-27.** Блок Источников переведён в строгий Managed-режим: ссылки на /docs/, /platform/, /apps/, /workflows/ удалены, оставлены только страницы из раздела `/managed/`. В air-gapped контуре уведомления уходят во внутренние ITSM/SMTP/Teams/Slack без выхода в интернет. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (Dynatrace Managed: air-gapped):**
>
> - [Welcome to Dynatrace Managed Documentation](https://docs.dynatrace.com/managed): корень раздела для air-gapped инсталляций
> - [Davis AI](https://docs.dynatrace.com/managed/discover-dynatrace/platform/davis-ai): корневая страница про anomaly detection, root cause analysis, AI-модели baseline
> - [Root cause analysis](https://docs.dynatrace.com/managed/dynatrace-intelligence/root-cause-analysis): context-aware RCA через causal topology, ранжирование аномалий, объединение связанных в Problem
> - [Manage your Dynatrace Managed](https://docs.dynatrace.com/managed/manage): администрирование, в котором живут Settings 2.0 для Alerting profiles, Problem notifications и Maintenance windows
> - [Identity & access management](https://docs.dynatrace.com/managed/manage/identity-access-management): RBAC для управления Alerting profiles и Problem notifications
> - [Access tokens: Dynatrace Managed](https://docs.dynatrace.com/managed/manage/access-control/access-tokens): токены, которыми внешние ITSM (Jira, ServiceNow) опрашивают Problems API

## 📍 КАРТА: где живут Problems и их настройки

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Список всех инцидентов | **Observe and explore → Problems** | `https://guu84124.live.dynatrace.com/ui/problems` |
| Настройка уведомлений | **Settings → Integration → Problem notifications** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications` |
| Категоризация готовых алертов | **Settings → Anomaly detection → Ready-made alerts category update** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly.detection.alerts-category-update` |
| Alerting profiles / профили алертинга | **Settings → Alerting → Alerting profiles** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.profile` |
| Maintenance windows / окна обслуживания | **Settings → Maintenance windows** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:maintenance-window` |

**Термины темы.**

- **Problem / проблема / инцидент**: сущность Dynatrace, агрегирующая несколько связанных симптомов в один инцидент.
- **Davis AI**: движок автоматической детекции, группировки и определения корневой причины.
- **Root cause / корневая причина**: первопричина инцидента, которую Davis вывел из графа зависимостей.
- **Alerting profile / профиль алертинга**: правило маршрутизации «какие проблемы в какие интеграции отправлять».
- **Impact level / уровень влияния**: Infrastructure / Services / Application / Environment.

**Чем Problem отличается от классического алерта.**

| Zabbix / Nagios / Prometheus | Dynatrace Problem |
|---|---|
| Одна метрика → одно уведомление | Много симптомов на разных сущностях → одна проблема |
| При инциденте: 50–200 писем | Одно письмо с Problem ID |
| Оператор вручную собирает картину | Davis AI сам определяет корневую причину |
| Каждый алерт живёт отдельно | Проблема связывает все симптомы и события |

---

## 🎬 Работа с Problems на трёх экранах

### Шаг 1: Список Problems

![Problems: активные проблемы окружения с таблицей и временной гистограммой](screenshots/day-1/problems-feature/problems/Problems-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Problems** → `https://guu84124.live.dynatrace.com/ui/problems`.

**Что на экране.** Главный экран работы с инцидентами. На этом демо-тенанте он заполнен тестовыми проблемами, что позволяет разобрать интерфейс.

Сверху: промо-плашка с предложением перейти в новое приложение Problems из Dynatrace Apps. В Managed-инсталляциях работаем с классическим интерфейсом, который на скриншоте.

**Временная гистограмма** под плашкой. Красные столбцы = число проблем в момент времени. Равномерная заливка на всей длине, как на этом демо: следствие синтетических аномалий демо-тенанта. На боевой инсталляции график обычно разреженный, и новый красный столбец: повод для внимания дежурной смены.

**Слева: панель фильтров.**

- **Status**: Any / Open (открытые, активные сейчас) / Closed (закрытые, Davis зафиксировал восстановление). По умолчанию показываются открытые.
- **Severity**: характер нарушения: Monitoring unavailable (потеря мониторинга), Availability (недоступность), Error (ошибки), Slowdown (замедление), Resource (исчерпание ресурсов), Custom (пользовательские правила).
- **Impact level**: Infrastructure / Services / Application / Environment.
- **Maintenance**: Any / Under maintenance / Not under maintenance. Отделить ожидаемые проблемы от неожиданных.

**Таблица проблем.** Колонки:

- **Problem**: заголовок и сквозной идентификатор `P-NNNNNNNN`. На этом демо видны реальные примеры: `Mobile app unexpected low usage P-26048535`, `Potential DDoS attack on the Oracle DB P-26048536`, `Multiple infrastructure problems P-26048537`.
- **Impacted**: имя главной затронутой сущности.
- **Affected**: число затронутых сущностей.
- **Root cause**: корневая причина, если Davis AI её установил.
- **Start date**: когда Davis создал проблему.
- **Duration**: продолжительность. Для открытой: сколько длится сейчас. Для закрытой: сколько длилась всего.
- **Alerting profiles**: какие профили алертинга сработали. По этой колонке сразу видно, в какие интеграции ушла проблема.

**Карточка проблемы** открывается кликом по строке. В ней: всё для расследования:
- Полная хронология: когда и какие события добавились.
- Какие сущности в какой момент были затронуты.
- Вывод Davis о корневой причине.
- Прямые переходы к графикам метрик, трейсам, логам, карточкам сервисов.

**Ключевая логика.** Каждая проблема: единое событие, а не набор алертов. При деградации базы одновременно стали медленными десять сервисов: Davis не создаст одиннадцать проблем. Он создаст одну, определит корневой причиной базу, и все остальные симптомы включит в её состав как следствия.

### Шаг 2: Problem notifications / уведомления о проблемах

![Problem notifications: настройка интеграций](screenshots/day-1/problems-feature/settings/builtinproblem.notifications/Problem-notifications-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Settings → Integration → Problem notifications** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:problem.notifications`.

**Что на экране.** Настройка интеграций с внешними системами, куда Dynatrace шлёт уведомления о проблемах. На этом демо-тенанте сами интеграции не настроены и не разбираются визуально: привязываться к скриншоту при объяснении нужно аккуратно.

**AutomationEngine / Workflows в Managed.** Новый механизм уведомлений поверх классического Problem notifications, часть Apps-платформы Dynatrace SaaS. В Managed он не активен, поэтому рабочий механизм здесь классический: Problem notifications.

**Strict firewall policy в air-gapped.** В корпоративных контурах с частичным выходом в интернет требуется явный allowlist для исходящих соединений от кластера Dynatrace: список IP-диапазонов, куда managed-кластер может отправлять трафик. В полностью изолированном air-gapped контуре интернет-связи нет: уведомления уходят во внутренний SMTP-сервер банка, внутренний Jira или корпоративный Teams. Этот список IP не нужен.

**Что настраивается на production.** На боевой инсталляции под баннерами обычно есть таблица интеграций: по одной строке на каждую. У каждой тумблер включения, краткое описание и раскрывающаяся карточка с параметрами. Плюс кнопка **+ Set up notifications** для новой интеграции.

*Если экран пуст (как на этом демо).* Чтобы показать механику вживую, нажмите **+ Set up notifications** и выберите тип (например, Email или Slack): откроется форма параметров. Её можно показать и закрыть без сохранения. Так слушатель увидит, какие поля заполняются, даже когда готовых интеграций в окружении ещё нет.

**Типовые интеграции в банке.**

- **Email**: отправка на групповой ящик дежурной смены через внутренний SMTP-сервер.
- **Jira** через REST API: автоматическое создание задачи в проекте дежурных инженеров, с обновлением статуса.
- **ServiceNow / ITSM**: создание инцидента в корпоративной системе управления инцидентами.
- **Slack / Microsoft Teams**: сообщение в канал команды со ссылкой на карточку в Dynatrace.
- **Webhook**: произвольный HTTP POST с JSON-описанием проблемы в любую внешнюю систему. Используется при нестандартных ITSM или собственных скриптах автоматизации.

**Связка с Alerting profiles.** Каждая интеграция привязывается к Alerting profile: набору правил «какие проблемы сюда попадают». Типовой сценарий: профиль для проблем высокого приоритета (только Impact = Application на production-сервисах), в нём интеграции email руководителю и Teams в канал дежурных: срабатывают только на эти проблемы. Профили настраиваются отдельно в `https://guu84124.live.dynatrace.com/ui/settings/builtin:alerting.profile`.

### Шаг 3: Ready-made alerts category update

![Ready-made alerts category update: один тумблер для принятия новой классификации встроенных алертов](screenshots/day-1/problems-feature/settings/builtinanomaly.detection.alerts-category-update/Ready-made-alerts-category-update-Environment-Settings-Demo-live-Demo-Live-Dynat.png)

Путь: **Settings → Anomaly detection → Ready-made alerts category update** → `https://guu84124.live.dynatrace.com/ui/settings/builtin:anomaly.detection.alerts-category-update`.

*Что делает.* Один тумблер `Updated classification for select ready-made alerts`. Включён: к новым Problems применяется обновлённая классификация. Выключен: поведение как до обновления сборки кластера.

*Зачем нужно.* Dynatrace периодически пересматривает внутренние правила. Пример: «высокий CPU сам по себе» переходит из категории Services impact в Infrastructure impact. Если автоматически применить новую классификацию на всех клиентах, Alerting profiles у тех, кто завязан на старую логику, перестанут срабатывать корректно.

*Какой риск.* От классификации зависит, как проблема группируется, какой у неё Impact Level, попадает ли она в конкретный Alerting profile. Неподготовленное включение → у тех, кто ждал алерт, алерт не приходит.

*Как решают.* Изменения поставляются отдельным тумблером. Администратор сначала сверяет свои Alerting profiles с новой классификацией, потом включает.

*Типичная практика.* Тумблер в дефолте (обычно выключен). Включают в рамках планового ревью системы мониторинга: раз в квартал или полгода. Перед включением инженер проходит по всем Alerting profiles и убеждается, что каждое правило под новой классификацией работает как задумано.

---

## 🎓 ТЕОРИЯ: жизненный цикл Problem

Пример: деградация времени отклика сервиса платежей.

**Фаза 1. Детекция.** В 14:03 медиана времени отклика `payment-service` растёт со 120 мс до 800 мс. Davis AI, опираясь на baseline с учётом времени дня и дня недели, определяет это как аномалию. Превышает абсолютный и относительный пороги Response time на странице Anomaly detection for services.

**Фаза 2. Агрегация.** Davis замечает ту же деградацию на трёх зависимых сервисах: они ждут ответа от `payment-service`. На хосте, где живёт `payment-service`, вырос iowait. Все наблюдения Davis складывает в одну Problem.

**Фаза 3. Определение корневой причины.** Davis анализирует граф зависимостей Smartscape и временные корреляции через механизм [Root cause analysis](https://docs.dynatrace.com/managed/dynatrace-intelligence/root-cause-analysis): context-aware подход, использующий причинную топологию для определения коренных причин. Видит: хост, на котором живёт `payment-service`, начал страдать от iowait за минуту до того, как сервис стал медленным. Устанавливает корневую причину: «проблема с диском на хосте `payment-host-03`». <!-- last-verified: 2026-04-27 source: docs.dynatrace.com/managed/dynatrace-intelligence/root-cause-analysis -->

**Фаза 4. Уведомление.** Davis создаёт Problem, отправляет в активные проблемы. Привязанные Alerting profiles срабатывают. В профиль `prod-high-priority` (сервис Production, Impact Application) попадает эта проблема. Все интеграции профиля: email дежурному, Teams в канал `#prod-incidents`, Jira-тикет в проект `DEVOPS`: получают уведомление. Одно на всю проблему, а не пять на разные симптомы.

**Фаза 5. Работа оператора.** Дежурный получает уведомление, открывает карточку проблемы. Видит: корневая причина: диск на `payment-host-03`. Проваливается в карточку хоста, смотрит метрики диска, замечает заполнение 99%. Логинится на хост, очищает временные файлы. В 14:28 iowait спадает, сервис возвращается к нормальному отклику.

**Фаза 6. Закрытие.** Davis, убедившись в устойчивом восстановлении, помечает проблему Closed. Jira-интеграция закрывает тикет, в Teams приходит сообщение «проблема разрешена». Проблема уходит из Open-списка, остаётся в истории для постмортема.

**Автоматизация.** Вся цепочка работает сама. Администратор один раз настроил:
- **Anomaly detection**: пороги.
- **Alerting profiles**: кому и о чём сообщать.
- **Problem notifications**: куда слать (раздел [Notifications and alerting](https://docs.dynatrace.com/managed/analyze-explore-automate/notifications-and-alerting)).

Дальше система работает без вмешательства. В air-gapped банковском контуре весь цикл локальный: интеграции ходят во внутренние системы банка (SMTP, внутренний Jira, корпоративный Slack/Teams).
