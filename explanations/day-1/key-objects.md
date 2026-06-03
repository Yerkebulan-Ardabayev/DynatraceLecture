> 📅 **День 1: Введение в систему Dynatrace** → Тема 7 из 11: «Хосты, процессы, сервисы, приложения: обзор ключевых объектов»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/entity/list/HOST -->
>
> 🔖 **Редакция от 2026-04-27.** Блок Источников переведён в строгий Managed-режим: ссылки на /docs/ удалены, оставлены только страницы из раздела `/managed/`. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (Dynatrace Managed: air-gapped):**
>
> - [Welcome to Dynatrace Managed Documentation](https://docs.dynatrace.com/managed): корень раздела для air-gapped инсталляций
> - [Smartscape](https://docs.dynatrace.com/managed/shortlink/smartscape): иерархия 5 уровней (Apps / Services / Processes / Hosts / Data Centers), вертикальные и горизонтальные связи
> - [Observe](https://docs.dynatrace.com/managed/observe): корень раздела с экранами Hosts / Services / Process Groups / Applications
> - [Service Detection v1](https://docs.dynatrace.com/managed/observe/application-observability/services/service-detection/service-detection-v1): типы сервисов (Web request services, Web services WSDL, Database, Messaging, Remoting, Background activity, Custom services), правила Service detection
> - [Digital Experience](https://docs.dynatrace.com/managed/observe/digital-experience): Application-уровень (frontend), Web/Mobile RUM, Session segmentation
> - [Management zones](https://docs.dynatrace.com/managed/shortlink/management-zones): сегментация сущностей по зонам ответственности, до 5 000 MZ на окружение
> - [Manage your Dynatrace Managed](https://docs.dynatrace.com/managed/manage): администрирование, где живут Settings 2.0 для Process Group detection и Service Detection

## 📍 КАРТА: четыре типа ключевых объектов

| Сущность | Путь в меню | Прямая ссылка |
|---|---|---|
| **Hosts / хосты** | **Infrastructure Observability → Hosts** | `https://guu84124.live.dynatrace.com/ui/entity/list/HOST` |
| **Process Groups / группы процессов** | **Infrastructure Observability → Technologies & Processes** | `https://guu84124.live.dynatrace.com/ui/technologies` |
| **Services / сервисы** | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` |
| **Applications / приложения** | **Application Observability → Frontend** | `https://guu84124.live.dynatrace.com/ui/applications` |

**Термины темы.**

- **Entity / сущность**: любой мониторимый объект в Dynatrace с уникальным ID.
- **Host / хост**: физическая или виртуальная машина с установленным OneAgent.
- **Process Group / группа процессов**: логическое объединение одинаковых процессов (все инстансы одного Java-приложения на всех хостах).
- **Service / сервис**: backend-единица, обрабатывающая запросы.
- **Application / приложение**: frontend-единица, веб- или мобильное приложение.

**Иерархия сущностей.**

```
Application (что видит пользователь в браузере)
    ↓ вызывает
Service (что обрабатывает запрос на бэкенде)
    ↓ выполняется в
Process Group (группа одинаковых процессов)
    ↓ работает на
Host (физическая или виртуальная машина)
    ↓ находится в
Data Center (ДЦ или облачный регион)
```

Связи строит OneAgent автоматически. У каждой сущности свой уникальный ID вида `HOST-ABC123DEF`. Через него на сущность ссылаются в API, дашбордах, алертах.

---

## 🎬 Работа с ключевыми объектами на трёх экранах

### Шаг 1: Services / список backend-сервисов

![Services: список сервисов с фильтрами и метриками](screenshots/day-1/key-objects/services/Services-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Services** → `https://guu84124.live.dynatrace.com/ui/services`.

**Что на экране.** Список всех обнаруженных backend-сервисов. На этом демо-тенанте их 244, это конкретная цифра момента захвата, на боевой зависит от того, сколько систем под мониторингом.

**Как Dynatrace определяет сервис.** Сервис: логическая единица backend, обрабатывающая запросы одного типа. Один Java-процесс Tomcat может содержать несколько сервисов (один на каждый REST-эндпоинт или контекст). Несколько процессов могут формировать один сервис, если они: инстансы одной логической единицы.

**Слева: панель фильтров.**

- **Service type / тип сервиса**: Web service, Web request service (входящий HTTP), Custom service (описанный вручную), Messaging service (очереди), Background activity и ещё шесть опций.
- **Problem impact**: Any / Impacted (есть активная проблема Davis) / Not impacted.
- **Technology / технология**: язык и фреймворк: .NET, Java, Kafka, Node.js: всего 50+ опций в выпадающем списке.

**Таблица.** Колонки:
- **Name**: имя сервиса.
- **Response time median / медианное время отклика**.
- **Slowest 10% / время отклика топ-10% самых медленных**.
- **Failure rate / процент ошибок**.
- **Requests / запросов в минуту**.
- **Actions**: контекстное меню и переход в карточку.

На демо-тенанте в именах видны характерные признаки: `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 nginx ingress-nginx-controller-*`: автообнаружение nginx-сервисов и Kubernetes ingress-контроллеров.

**Карточка сервиса.** Клик по имени: ключевой инструмент расследования. В карточке:
- Графики Response time, Throughput, Failure rate за период, с наложением проблем.
- **Service flow / поток вызовов**: карта, показывающая, кто вызывает сервис и кого вызывает он.
- **Top requests / топ HTTP-эндпоинтов**: самые частые и самые медленные.
- **Top database statements / топ SQL-запросов**.
- Список процессов, обслуживающих сервис.
- Активные проблемы.

**Response time и перцентили.** Метрика отдаётся с несколькими агрегациями: среднее, медиана, 90-й / 95-й / 99-й перцентили. Для большинства случаев важнее медиана и 90-й перцентиль. Среднее сильно искажается отдельными очень медленными запросами. Пример: «сколько отвечает сервис платежей»: медиана, например 120 мс. «Как у самых медленных клиентов»: 90-й перцентиль, например 450 мс.

### Шаг 2: Applications / список приложений

![Applications: на демо страница с плашкой Connection issues](screenshots/day-1/key-objects/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Frontend** → `https://guu84124.live.dynatrace.com/ui/applications`.

**Что на экране.** На этом демо-тенанте центральная область занята технической заглушкой `Connection issues / Too many requests`: демо-окружение временно превысило лимит запросов. На боевой инсталляции здесь был бы список веб- и мобильных приложений под RUM-мониторингом.

**Что есть на боевой инсталляции.** Подробнее эта страница разобрана в Теме 4 (Digital Experience Monitoring): там механика RUM-сниппета, Application Settings, связка с сервисами.

**Разница между сервисом и приложением.**

- **Service / сервис**: backend-объект, живёт на хосте под OneAgent, обрабатывает запросы.
- **Application / приложение**: frontend-объект, живёт в браузере или на мобильном устройстве, определяется доменом и конфигурацией RUM.

Одно приложение опирается на несколько сервисов. Интернет-банк использует сервис аутентификации, сервис счетов, сервис платежей, сервис выписок. Один сервис может обслуживать несколько приложений: сервис аутентификации отвечает и интернет-банку, и мобильному приложению, и корпоративному порталу.

Связь между приложением и сервисами видна в карточке приложения через **User actions**. OneAgent автоматически добавляет заголовок `x-dynatrace` в каждый XHR-запрос браузера, это и связывает клиентский клик с серверным PurePath.

### Шаг 3: Entity list / универсальный список сущностей (статус 404)

![Entity list: страница возвращает 404](screenshots/day-1/key-objects/entity/list/404-We-cant-find-this-page-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/entity/list`.

**Что на экране.** 404. Универсальный список сущностей вида «покажи всё подряд» в новых сборках Dynatrace Managed больше не поддерживается. Вместо него: **типизированные списки** для каждого типа сущности:

- Хосты: `https://guu84124.live.dynatrace.com/ui/entity/list/HOST`
- Сервисы: `https://guu84124.live.dynatrace.com/ui/services`
- Приложения: `https://guu84124.live.dynatrace.com/ui/applications`
- Базы данных: `https://guu84124.live.dynatrace.com/ui/databases`
- Группы процессов: `https://guu84124.live.dynatrace.com/ui/technologies`
- Контейнеры: `https://guu84124.live.dynatrace.com/ui/entity/list/CONTAINER_GROUP`
- Kubernetes workloads: `https://guu84124.live.dynatrace.com/ui/entity/list/CLOUD_APPLICATION`

**Адаптация учебного плана.** Где в старых материалах сказано «открой Entity list», в текущей сборке используется типизированный список нужного уровня или глобальный поиск Ctrl+Shift+F.

### Хосты и группы процессов на текущем тенанте

На этом демо-тенанте страницы Hosts и Technologies & Processes не попали в captured-набор: скриншотов нет. Описание ниже: что инженер увидит на этих экранах на боевом окружении.

**Hosts.** Таблица хостов с колонками: имя хоста, OS, версия OneAgent, CPU, Memory, Network, число процессов, теги, Management Zone. Фильтры слева по OS, тегам, MZ, состоянию OneAgent. Клик на хост открывает карточку с графиками и списком процессов.

**Technologies & Processes.** Группы процессов, сгруппированные по технологии (Java, .NET, Node.js, Python, nginx, Apache). Для каждой группы: число инстансов, CPU, память. Клик открывает карточку группы с графиками и списком экземпляров.

---

## 🎓 ТЕОРИЯ: зачем знать иерархию сущностей

Иерархия сущностей описана в разделе [Smartscape](https://docs.dynatrace.com/managed/analyze-explore-automate/smartscape-classic) (топология сущностей): четыре уровня (Applications / Services / Process Groups / Hosts) плюс Data Centers как логическая группировка.

**Сквозной анализ инцидента.** При падении сервиса важно быстро ответить: какие приложения пострадали (уровень вверх), на каких хостах проблема (уровень вниз). Иерархия Application → Service → Process Group → Host, это и есть цепочка анализа.

**Правильный scope алертов.** Alert profile с фильтром `type(SERVICE)` включает только сервисные проблемы, `type(HOST)`: только хостовые. Разные команды отвечают за разные уровни: SRE: за хосты, разработчики: за сервисы. Сегментация алертов по типу сущности важна для правильной маршрутизации. Раздел [Process group detection](https://docs.dynatrace.com/managed/observe/infrastructure-observability/process-groups/configuration/pg-detection) объясняет, по каким правилам OneAgent объединяет процессы в одну группу и как это влияет на алерты на уровне Process Group.

**Правильный выбор метрик.** Метрики разных уровней разные. `builtin:host.cpu.usage`, это метрика хоста. `builtin:service.response.time`: метрика сервиса. `builtin:apps.web.actionDuration`: метрика приложения. Путать их нельзя: они живут в разных measurement scope.

**Management Zones.** [Management zones](https://docs.dynatrace.com/managed/shortlink/management-zones): сегментация сущностей по зонам ответственности (Retail Banking, Corporate Banking, Treasury): работает на всех уровнях одновременно. Выбрал в верхнем фильтре zone «Retail»: видны только хосты, процессы, сервисы, приложения этой зоны. По умолчанию в окружении можно создать до **5 000 management zones**; правила задаются через UI или текстом через entity selector Environment API v2. <!-- last-verified: 2026-04-27 source: docs.dynatrace.com/managed/shortlink/management-zones -->
