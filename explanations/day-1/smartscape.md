> 📅 **День 1: Введение в систему Dynatrace** → Тема 6 из 11: «Топология Smartscape»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/diagnostictools/purepaths -->
>
> 🔖 **Редакция от 2026-04-27.** Тех-факты сверены с `docs.dynatrace.com/docs/shortlink/smartscape` (Smartscape — общая концепция OneAgent для Managed и SaaS). При перепроверке найдено и исправлено: stale-entity timeout — по docs **72 часа без активности** (плюс пунктирная линия для 2 часов), а не 30 минут. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (официальная документация Dynatrace):**
>
> **Общая (Managed + SaaS):**
> - [Smartscape — auto-discovered topology](https://docs.dynatrace.com/docs/shortlink/smartscape) — корневая страница про Smartscape: 4 уровня (Applications / Services / Process Groups / Hosts), вертикальные и горизонтальные связи
> - [Hosts](https://docs.dynatrace.com/docs/shortlink/hosts) — Hosts-уровень Smartscape, перечень и фильтры
> - [Services](https://docs.dynatrace.com/docs/observe/application-observability/services) — Services-уровень, типы, метрики
> - [Distributed traces](https://docs.dynatrace.com/docs/observe/application-observability/distributed-traces) — раздел Distributed Traces, где живут PurePath (горизонтальные связи между сервисами)
> - [Process group detection](https://docs.dynatrace.com/docs/observe/infrastructure-observability/process-groups/configuration/pg-detection) — Process Groups-уровень: как OneAgent объединяет процессы в одну сущность
> - [Extensions 2.0](https://docs.dynatrace.com/docs/extend-dynatrace/extensions20) — расширения для систем без OneAgent (SNMP / JMX / JDBC / Prometheus), узлы которых появляются в Smartscape
> - [Davis AI Root cause analysis](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis) — как Davis использует Smartscape для определения корневой причины

## 📍 КАРТА — Smartscape в интерфейсе

| Что показать | Путь в меню | Прямая ссылка | Состояние на этом тенанте |
|---|---|---|---|
| Smartscape Topology (классический вид) | **Observe and explore → Smartscape Topology** | `https://guu84124.live.dynatrace.com/ui/apps/dynatrace.classic.smartscape` | **404** — на свежих сборках Managed классический вид убран |
| Hosts / хосты | **Infrastructure Observability → Hosts** | `https://guu84124.live.dynatrace.com/ui/entity/list/HOST` | Замена уровня хостов |
| Services / сервисы | **Application Observability → Services** | `https://guu84124.live.dynatrace.com/ui/services` | Замена уровня сервисов |
| Process Groups / группы процессов | **Infrastructure Observability → Technologies & Processes** | `https://guu84124.live.dynatrace.com/ui/technologies` | Процессы и группы |
| Distributed Traces / распределённые трейсы | **Application Observability → Distributed Traces** | `https://guu84124.live.dynatrace.com/ui/diagnostictools/purepaths` | Карта вызовов между сервисами |

**Термины темы.**

- **Smartscape / карта топологии** — автоматически построенная карта зависимостей всей инфраструктуры.
- **Entity / сущность** — узел карты: хост, сервис, процесс, приложение.
- **Process Group / группа процессов** — логическое объединение одинаковых процессов на разных хостах.
- **PurePath / сквозной трейс** — трассировка одного запроса через все сервисы.

---

## 🎬 Работа со Smartscape на текущей версии тенанта

### Шаг 1 — Классический Smartscape Topology (статус 404)

![Smartscape Topology — страница возвращает 404](screenshots/day-1/smartscape/apps/dynatrace.classic.smartscape/404-We-cant-find-this-page-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Observe and explore → Smartscape Topology** → `https://guu84124.live.dynatrace.com/ui/apps/dynatrace.classic.smartscape`.

**Что на экране.** 404 с сообщением `We can't find this page`. Внизу идентификатор окружения `guu84124` и версия платформы `1.336.55.20260417-205630`.

**Почему 404.** Classic Smartscape был единым графическим приложением, отрисовывающим всю инфраструктуру в виде четырёх горизонтальных слоёв (Applications → Services → Process Groups → Hosts → Data Centers). На больших инсталляциях такой монолитный вид становится нечитаемым: тысячи сервисов в одном графе превращаются в месиво. Поэтому в новых сборках Dynatrace Managed Smartscape разбит на специализированные экраны — отдельный для каждого уровня, с переходами между ними по клику на сущность.

**Как работать с топологией сейчас.** Вместо одного экрана Smartscape используется комбинация:
- Список **Hosts**: `https://guu84124.live.dynatrace.com/ui/entity/list/HOST`.
- Список **Process Groups**: `https://guu84124.live.dynatrace.com/ui/technologies`.
- Список **Services**: `https://guu84124.live.dynatrace.com/ui/services`.
- Список **Applications**: `https://guu84124.live.dynatrace.com/ui/applications`.
- Карта вызовов между сервисами: **Distributed Traces** `https://guu84124.live.dynatrace.com/ui/diagnostictools/purepaths`.

В карточке каждой сущности есть раздел **Service flow** или **Topology** — показывает прямые связи этой сущности (кто её вызывает и кого она вызывает). Это локальный вид того, что классический Smartscape давал глобально.

Поиск по имени — глобальный поиск в верхней панели (Ctrl+Shift+F). Начинаем вводить имя хоста, сервиса или приложения, выбираем из выпадающего списка, открывается карточка.

---

## 🎓 ТЕОРИЯ — что такое Smartscape и зачем он нужен

### Принцип

[Smartscape](https://docs.dynatrace.com/docs/shortlink/smartscape) — это **карта зависимостей всей инфраструктуры**, которая обновляется непрерывно на основе данных OneAgent. Никаких конфигурационных файлов, никакой ручной прорисовки связей.

Что OneAgent видит на каждом хосте:
- **Сетевые соединения процессов** — кто к кому подключается, на какой порт, с какой интенсивностью.
- **Вызовы внутри приложений** — через инструментацию кода OneAgent фиксирует каждый входящий и исходящий HTTP-запрос, каждый SQL-вызов, каждую отправку в очередь.
- **Ресурсная топология** — какой процесс на каком хосте, в каком контейнере, в каком Kubernetes-поде, на какой VM.

Эти данные OneAgent отправляет в кластер через ActiveGate. Кластер собирает данные со всех хостов в единый граф и обновляет его постоянно: новое соединение появляется на карте сразу. Если соединение или сервис не получают активности **более 72 часов**, узел исчезает с карты Smartscape Classic; промежуточный сигнал — пунктирная линия для соединений без трафика последние 2 часа. <!-- last-verified: 2026-04-27 source: docs.dynatrace.com/docs/shortlink/smartscape -->

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/docs/shortlink/smartscape -->

### Четыре уровня Smartscape

| Уровень | Что это | Пример |
|---|---|---|
| **Applications / приложения** | Frontend — веб- и мобильные приложения | Интернет-банк, мобильное приложение, корпоративный портал |
| **Services / сервисы** | Backend — логические единицы обработки запросов | PaymentService, AccountService, AuthService |
| **Process Groups / группы процессов** | Группы одинаковых процессов ОС | `java -jar payment.jar` × 4 инстанса на трёх хостах |
| **Hosts / хосты** | Физические или виртуальные машины | `app-prod-01.bank.local`, `vm-db-03.aws.region` |

Плюс **Data Centers** — логическая группировка хостов по дата-центрам и облачным регионам.

**Вертикальные связи** идут сверху вниз: приложение вызывает сервисы, сервис работает в одной или нескольких группах процессов, группа процессов — на одном или нескольких хостах, хост — в дата-центре.

**Горизонтальные связи** — вызовы между сущностями одного уровня. Самое важное — между сервисами: PaymentService вызывает AccountService, AccountService вызывает CoreBanking-базу. Из таких связей собирается PurePath — сквозная трассировка в разделе [Distributed Traces](https://docs.dynatrace.com/docs/observe/application-observability/distributed-traces).

### Зачем Smartscape нужен на практике

[Davis AI Root cause analysis](https://docs.dynatrace.com/docs/discover-dynatrace/platform/davis-ai/root-cause-analysis) опирается именно на топологию Smartscape, чтобы в момент аномалии автоматически построить цепочку причин — от симптома на верхнем уровне до сущности-источника внизу.

**Анализ влияния инцидента.** На хосте `app-prod-03` проблема с диском. Открываем карточку хоста → видим список Process Groups → от каждого связи к Services → от Services к Applications. Сразу понятно, какие приложения пострадают и через них — какие команды. Без Smartscape пришлось бы руками разбираться с CMDB.

**Поиск корневой причины.** Пользователи жалуются на медленный интернет-банк. Идём Applications → карточка интернет-банка → график задержки. Спускаемся на Services → видим медленный payment-service. Спускаемся на Process Groups → все три инстанса медленные. Спускаемся на Hosts → все три в одном дата-центре, и в этом дата-центре у всех хостов одновременно вырос latency к базе. Корневая причина найдена за пять шагов вниз по Smartscape.

**Контроль изменений после релиза.** Смотрим Smartscape: появились ли все новые сервисы, связи такие, как проектировали, нет ли неожиданных зависимостей. Если новый релиз случайно ходит в legacy-базу, которую должны были отключить, это сразу видно.

**Инвентаризация для аудита.** Регулятор спрашивает: «сколько сервисов работает с персональными данными? на каких хостах они живут? из какого ДЦ идут запросы?». Smartscape даёт готовый граф с привязкой к моменту времени.

### Ограничения в air-gapped

Smartscape не зависит от интернета. Всё строится на данных OneAgent и ActiveGate внутри контура — работает одинаково с облачной версией.

Единственное ограничение — сущности **без OneAgent** (старые сетевые маршрутизаторы, legacy-системы без поддержки агента). Они видны только как дальний конец соединения («какой-то наш сервис ходит на IP X»), без деталей. Чтобы дополнить картину, используются [Extensions 2.0](https://docs.dynatrace.com/docs/extend-dynatrace/extensions20) — плагины на ActiveGate, снимающие данные через SNMP, JMX, SQL. Данные от Extensions появляются в Smartscape как отдельные узлы, и карта становится полной.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/docs/extend-dynatrace/extensions20 -->
