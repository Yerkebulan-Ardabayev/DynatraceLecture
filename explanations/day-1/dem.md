> 📅 **День 1: Введение в систему Dynatrace** → Тема 4 из 11: «Цифровой опыт (Digital Experience Monitoring): основные принципы»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/applications -->
>
> 🔖 **Редакция от 2026-04-27.** Блок Источников переведён в строгий Managed-режим: все ссылки на /docs/, /platform/ удалены, оставлены только страницы из раздела `/managed/`. В air-gapped Managed Apps-интерфейс «Users & Sessions» не активирован: используется Classic UI. Все ссылки проверены `scripts/link_check.py`. <!-- revision: 2026-04-27 -->

> 📚 **Источники (Dynatrace Managed: air-gapped):**
>
> - [Welcome to Dynatrace Managed Documentation](https://docs.dynatrace.com/managed): корень раздела для air-gapped инсталляций
> - [Digital Experience](https://docs.dynatrace.com/managed/observe/digital-experience): корневой раздел DEM в Managed: RUM-концепции, Web/Mobile/Custom apps, Session segmentation, Session Replay, Synthetic
> - [Apdex ratings](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings): 5-уровневая Apdex-шкала (Excellent 0.94-1.0 / Good 0.85-0.94 / Fair 0.7-0.85 / Poor 0.5-0.7 / Unacceptable <0.5) и 3-state user-action ratings (Satisfied / Tolerating / Frustrated)
> - [User experience score](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/user-experience-score): сессионный рейтинг Frustrating / Tolerable / Satisfying; веса элементов (User action 3 / Error 1 / Rage event 2 / Crash 5000); одно Frustrating-действие не даёт сессии стать Satisfying
> - [Session Replay](https://docs.dynatrace.com/managed/shortlink/session-replay): захват и воспроизведение сессий пользователя; поддержка Web, Android, iOS (за исключением Cordova / React Native / Flutter / Xamarin / .NET MAUI)
> - [Synthetic Monitoring](https://docs.dynatrace.com/managed/shortlink/synthetic-monitoring): 4 типа: single-URL browser monitor, browser clickpath, HTTP monitor, NAM monitor
> - [Data retention periods](https://docs.dynatrace.com/managed/shortlink/data-retention-periods): RUM 35 дней, Session Replay configurable max 35 дней, Synthetic max 35 дней (Classic)

## 📍 КАРТА: где живут данные цифрового опыта

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Список приложений | **Application Observability → Frontend → Applications** | `https://guu84124.live.dynatrace.com/#uemapplications` |
| Пользовательские сессии | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions` |
| Настройки RUM для приложения | **Settings → Web and mobile monitoring → Application settings** | `https://guu84124.live.dynatrace.com/ui/settings/applications-web` |
| Synthetic Monitoring | **Application Observability → Digital Experience → Synthetic** | `https://guu84124.live.dynatrace.com/ui/synthetic` |

**Термины темы.**

- **DEM / Digital Experience Monitoring / мониторинг цифрового опыта**: общий зонтик для всего, что связано с наблюдением за пользователем на стороне клиента.
- **RUM / Real User Monitoring / мониторинг реальных пользователей**: сбор данных с реальных пользователей через JavaScript-сниппет в браузере или SDK в мобильном приложении.
- **Synthetic Monitoring / синтетический мониторинг**: проверки роботами по расписанию, без реальных пользователей.
- **Session Replay / воспроизведение сессии**: видеозапись того, что видел и делал конкретный пользователь на экране.
- **Application / приложение**: frontend-сущность: веб- или мобильное приложение.
- **Apdex / индекс удовлетворённости**: число от 0 до 1, отражающее, насколько пользователям комфортно по скорости.

**Три источника данных DEM.**

| Источник | Как работает | Что показывает |
|---|---|---|
| RUM | JavaScript-сниппет OneAgent внедряется в HTML-страницы; данные собираются в браузере и шлются через ActiveGate в кластер | Реальная скорость страниц, JS-ошибки, клики, переходы, геопозиция, браузер, версия приложения |
| Mobile RUM | SDK OneAgent встраивается в iOS/Android-приложение при сборке | Crash reports, сетевые запросы, жесты, версии ОС |
| Synthetic | HTTP- или Browser-мониторы запускаются с ActiveGate по расписанию | Доступность, базовая скорость без реального трафика, проверка критичных путей 24×7 |

---

## 🎬 Работа с DEM на двух экранах

### Шаг 1: Applications / список приложений

![Applications: список из 24 приложений с типом и рейтингом Apdex по каждому](screenshots/day-1/dem/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Frontend → Applications** → `https://guu84124.live.dynatrace.com/#uemapplications`.

**Что на экране.** Заголовок **24 Applications** и кнопка **Monitoring settings**. Слева панель фильтров: **Status** (Monitored), **Application type** (Web applications, Mobile apps, Custom applications), **Injection type**, **Platform** (Android / iOS / Windows), **Tags**. Справа таблица приложений с колонками **Name / Application type / Performance**. В колонке Performance у каждого приложения рейтинг Apdex (Excellent / Good / Fair и далее); у проблемных строка подсвечена и подписана причиной (например, «Too many slow user actions»). Примеры на этом демо: Astroshop, www.angular.easytravel.com, easyTravel .NET, easyTravel mainframe, SAP_RUM. Клик по строке открывает дашборд конкретного приложения.

**Что внутри приложения.** Клик по строке открывает дашборд приложения, где видно:
- **Apdex / индекс удовлетворённости**: число от 0 до 1.
- **Число активных пользователей**: в реальном времени и за период.
- **Медианное и 90-й перцентиль времени загрузки**.
- **Процент сессий с ошибками**.
- **Распределение по браузерам, устройствам, странам**.

Там же видна динамика всех этих показателей во времени.

**Как приложение попадает сюда.** Нужно три условия:
1. OneAgent установлен на веб-сервере или reverse-proxy, через который идут пользовательские запросы (Nginx / Apache на DMZ-серверах).
2. В **Settings → Web and mobile monitoring → Application settings** создано приложение: указан домен, под которым оно доступно. Правила сопоставления URL настраиваются через Application detection rules (URL starts with / contains / equals): раздел [Web and mobile monitoring](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/application-detection-rules).
3. RUM (Real User Monitoring) включён. OneAgent автоматически добавляет в HTML-ответы ссылку на JavaScript-сниппет. Сниппет загружается в браузере пользователя, собирает данные и шлёт их через ActiveGate в кластер.

**Разница между приложением и сервисом.**

- **Сервис / Service**: backend-сущность. Живёт на хосте под OneAgent, обрабатывает HTTP или другие вызовы, обычно соответствует одному процессу.
- **Приложение / Application**: frontend-сущность. Живёт в браузере или в мобильном устройстве, идентифицируется доменом и конфигурацией RUM.

Связь между ними через `x-dynatrace`-заголовок: OneAgent автоматически добавляет его в каждый XHR-запрос браузера, и серверная обработка привязывается к клиентскому user action.

**ЕСЛИ → ТО: почему приложение появляется или нет.** Карточка в списке это прямое следствие настройки:

- ЕСЛИ все три условия выше выполнены → приложение появляется в списке через несколько минут после первого реального трафика.
- ЕСЛИ OneAgent на web-tier не установлен → RUM-сниппет не внедряется, приложения в списке нет вообще.
- ЕСЛИ OneAgent есть, но приложение в `Settings → Web and mobile monitoring → Application settings` не создано → сниппет работает «в никуда», данные не привязываются к карточке.
- ЕСЛИ Content-Security-Policy блокирует beacon или домен ActiveGate недоступен из сети пользователей → карточка приложения есть, но сессий в ней ноль.

### Шаг 2: User sessions / список сессий

![User sessions: список сессий с фильтрами и таблицей](screenshots/day-1/dem/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: **Application Observability → Frontend → User sessions** → `https://guu84124.live.dynatrace.com/ui/user-sessions`.

**Что на экране.** Список пользовательских сессий: отдельных визитов реальных людей в приложения с включённым RUM. Каждая строка: одна сессия.

В air-gapped Managed работаем с классическим списком сессий: новый Apps-интерфейс (Users & Sessions app) в Managed не активен.

Заголовок **User sessions**, счётчик **First 100 sessions**: по умолчанию выводятся первые сто сессий. Временной период: селектор в правом верхнем углу (на скрине Last 2 hours).

**Слева: панель фильтров.** Применяются кликом, сразу сужают таблицу.

- **Analysis over time**: переключиться с таблицы на график числа сессий по времени.
- **Application type**: веб, мобильное.
- **Application versions**: конкретная версия приложения. Полезно при разборе проблем в новом релизе.
- **Applications**: конкретное приложение, если их несколько.
- **User experience score / оценка пользовательского опыта**: рейтинг всей сессии, три значения **Frustrating / Tolerable / Satisfying** (разочарован / терпимо / доволен). Это сессионная оценка, не путать с рейтингом отдельного действия по Apdex (Satisfied / Tolerating / Frustrated). Как именно она считается, в блоке ТЕОРИЯ ниже. <!-- last-verified: 2026-06-02 source: docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/user-experience-score -->
- **Errors and annoyances**: только сессии с ошибками или поведенческими раздражителями (rage clicks, навязчивые перезагрузки).
- **Conversions and bounces**: сессии с бизнес-конверсией (успешный платёж) или отказом (ушёл с первой страницы).
- **Users**: фильтр по User ID (если в RUM настроен).
- **Browsers**: браузер и версия.
- **Internet service provider**: провайдер связи по IP.
- **Operating systems**: ОС устройства.
- **Locations**: страна и город.

**Пример расследования.** Жалоба: «пользователи с Safari на iPhone не могут войти в интернет-банк». Фильтры: **Browser = Safari** + **Operating system = iOS** + **Errors and annoyances = Yes**. В таблице остаются только такие сессии: открываем карточку, смотрим, что именно ломалось. Для воспроизведения конкретного визита используется Session Replay: запись DOM-состояния экрана, доступная по кнопке **Play** в карточке сессии (требует включённого Session Replay в настройках приложения).

ЕСЛИ выставить фильтр **User experience score = Frustrating** → в таблице останутся только сессии, которые Dynatrace уже признала проблемными: с крашем, ошибками или цепочкой медленных действий. Это быстрый вход в разбор, не нужно листать весь список вручную.

**Таблица справа.** Колонки:

- **Session start**: время начала визита.
- **Browser**: браузер и версия.
- **Application**: какое приложение.
- **User**: анонимный ID по cookie или реальный ID после авторизации.
- **Duration**: длительность от первой до последней активности.
- **Events**: сколько действий совершил пользователь.
- **Errors**: сколько ошибок.
- **Exits**: на скольких страницах заканчивалась сессия.
- **Conversions**: сколько бизнес-целей пройдено.

**Карточка сессии.** Клик на строку открывает подробную карточку. В ней:
- Полная хронология действий пользователя.
- Все страницы, которые он посетил.
- Все JavaScript-ошибки со стеком.
- Все XHR/fetch-запросы с временами и статусами.
- Все бизнес-события (если настроены).
- Кнопка **Play** для Session Replay, если включено для приложения.

**Связь с бэкендом.** На каждом XHR-запросе к backend-сервису Dynatrace связывает клиентский запрос с серверным PurePath. В карточке сессии клик на запрос открывает trace с полной цепочкой: браузер → web-tier → backend-сервис → база, с временами на каждом шаге. Видно, где именно медленно: на клиенте, в сети или на backend.

**Air-gapped контекст.** RUM-сниппет в браузере пользователя отправляет данные в ActiveGate. Если ActiveGate стоит в закрытом контуре, а пользователи: снаружи (клиенты, заходящие из интернета), то домен ActiveGate должен быть опубликован. Типичная схема банка: ActiveGate в DMZ с публичным доменом, либо reverse-proxy, принимающий RUM-трафик снаружи и проксирующий во внутренний ActiveGate. Для мобильных приложений аналогично: URL ActiveGate должен быть доступен с мобильных сетей.

**Synthetic как дополнение.** User sessions показывают только реальных пользователей. Если реального трафика мало (ночь, выходные) или нужна проверка критичного пути независимо от пользователей, используется Synthetic Monitoring: `https://guu84124.live.dynatrace.com/ui/synthetic`. Роботы ходят по приложению по скрипту раз в несколько минут. Synthetic-данные видны отдельно и не смешиваются с RUM: статистика не засоряется искусственным трафиком.

---

## 🎓 ТЕОРИЯ: две оценки качества, Apdex и User experience score

В цифровом опыте Dynatrace держит две разные оценки, и их легко перепутать. Apdex оценивает **отдельное действие** и **приложение по скорости**. User experience score оценивает **всю сессию целиком**, с учётом не только скорости, но и ошибок, крашей и раздражения пользователя. На лекции эти две оценки важно развести.

### Apdex: индекс удовлетворённости скоростью

Apdex (Application Performance Index, индекс производительности приложения) считается для каждого пользовательского действия и для приложения в целом. Это одно число от 0 до 1: по нему сразу видно, комфортно ли людям по скорости.

Шкала рейтинга приложения, пять уровней:

| Значение Apdex | Уровень |
|---|---|
| 0.94-1.0 | Excellent / отлично |
| 0.85-0.94 | Good / хорошо |
| 0.7-0.85 | Fair / приемлемо |
| 0.5-0.7 | Poor / плохо |
| < 0.5 | Unacceptable / недопустимо |

<!-- source: docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings -->

Значение 1.0 идеально, всё ниже 0.5 считается недопустимым.

**Откуда берётся рейтинг действия.** Для каждого типа действия задаются два порога: **Tolerating threshold** (порог терпимости) и **Frustrated threshold** (порог разочарования). По метрике скорости (по умолчанию длительность действия; можно выбрать Visually complete, Speed index, Largest contentful paint и другие) действие попадает в одну из трёх зон:

- быстрее порога Tolerating → **Satisfied / доволен**;
- между порогами → **Tolerating / терпимо**;
- медленнее порога Frustrated → **Frustrated / разочарован**.

Чем больше действий в зоне Satisfied, тем ближе Apdex приложения к 1.0.

**ЕСЛИ → ТО на порогах.** Пороги задаются под каждый тип действия отдельно. В документации пример: загрузка домашней страницы должна укладываться в 2 секунды, а сложный поиск приемлем и за 6 секунд. Отсюда:

- ЕСЛИ задать пороги жёстко (например, Tolerating 1 секунда) → больше действий уйдёт в Tolerating и Frustrated, Apdex приложения просядет, и на дашбордах и в SLO по Apdex сразу видно даже небольшие задержки;
- ЕСЛИ задать пороги мягко (например, Tolerating 5 секунд) → почти всё попадёт в Satisfied, Apdex будет высоким, но реальные тормоза спрячутся за зелёным.

Поэтому пороги подбираются под тип действия и целевой SLO, а не ставятся одинаковыми на всё.

**Ошибка важнее скорости.** ЕСЛИ на действии есть JavaScript-ошибка → ТО действие помечается Frustrated, даже когда оно быстрое и формально ниже порога. То же для request-ошибки: код HTTP-ответа, нарушение Content-Security-Policy или ошибка загрузки ресурса, настроенные как ошибки. Быстрое, но красное действие почти всегда означает ошибку, а не медленную сеть. При необходимости ошибки можно исключить из расчёта Apdex в настройках приложения.

**Где крутить.** Пороги Apdex меняются в настройках приложения: **Settings → Web and mobile monitoring → Application settings**, на тенанте `https://guu84124.live.dynatrace.com/ui/settings/applications-web`. Задаются для приложения целиком и отдельно для ключевых действий (key user actions).

### User experience score: оценка всей сессии

User experience score (оценка пользовательского опыта) категоризует не отдельное действие, а **всю сессию**. Три значения: **Frustrating / Tolerable / Satisfying** (разочарован / терпимо / доволен). Это не то же самое, что рейтинг действия по Apdex (Satisfied / Tolerating / Frustrated): здесь оценивается сессия в целом, и в расчёт идут ещё ошибки, раздражение и краши.

Считается из элементов сессии с весами:

| Элемент | Вес | Рейтинг элемента |
|---|---|---|
| User action / действие пользователя | 3 | Frustrating, Tolerable или Satisfying |
| Error / ошибка | 1 | всегда Frustrating |
| Rage event / приступ раздражения | 2 | всегда Frustrating |
| Crash / краш приложения | 5000 | всегда Frustrating |

<!-- source: docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/user-experience-score -->

Веса по каждой категории суммируются, делятся на общий вес, и по заданным порогам сессия получает итоговый рейтинг. Два следствия, которые лектор называет вслух:

- ЕСЛИ в сессии есть хотя бы одно Frustrating-действие → сессия уже не станет Satisfying, максимум Tolerable. Одна серьёзная заминка перечёркивает оценку всей сессии.
- ЕСЛИ в сессии случился краш → его вес 5000 перевешивает всё остальное, и сессия становится Frustrating, сколько бы успешных действий в ней ни было.

Практический ход для разбора: фильтр **User experience score = Frustrating** на экране User sessions это самый быстрый способ собрать сессии с критичными сбоями, не листая весь список вручную.

### Ключевые термины

- **Apdex / индекс удовлетворённости**: оценка скорости одного действия и приложения, число от 0 до 1, пять уровней рейтинга от Excellent до Unacceptable.
- **Tolerating threshold / Frustrated threshold**: два порога скорости, делящие действия на зоны Satisfied / Tolerating / Frustrated.
- **User experience score / оценка пользовательского опыта**: рейтинг всей сессии (Frustrating / Tolerable / Satisfying), считается из взвешенных элементов, а не только из скорости.
- **Rage event / приступ раздражения**: повторные частые клики или тапы в одно место (rage click, rage tap), признак того, что интерфейс не отвечает; всегда Frustrating.
