# Tech-claims inventory для dtkb-верификации

Всего: **550 claims** по **8 классам**. Сгенерировано `scripts/extract_tech_claims.py`.

Для каждого claim — проверить через `dtkb search` (fallback: `docs.dynatrace.com/managed/`). Занести в `tech_claims_verification.md` решение: **подтверждён** / **смягчён** / **удалён** с ссылкой на источник.

## [CPU_OVERHEAD]  — 2 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-2/hosts-processes.md:11` | `1% CPU` | …т окна, 60 мин/день, 100 процессов), trigger при ≥1% CPU/RAM/network |
| `explanations/day-2/hosts-processes.md:206` | `1% CPU` | - ЕСЛИ процесс превысил 1% CPU, памяти или сети при включённом тумблере → ТО сни… |

## [DISK_RETENTION]  — 234 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:10` | `365 дней` | …eriods): Classic retention (traces и synthetic до 365 дней + code-level 10 дней, logs до 90 дней, RUM-сессии… |
| `explanations/day-1/architecture.md:10` | `10 дней` | …tion (traces и synthetic до 365 дней + code-level 10 дней, logs до 90 дней, RUM-сессии/SR 35 дней, Davis pr… |
| `explanations/day-1/architecture.md:10` | `90 дней` | …nthetic до 365 дней + code-level 10 дней, logs до 90 дней, RUM-сессии/SR 35 дней, Davis problems 14 месяцев… |
| `explanations/day-1/architecture.md:10` | `35 дней` | …ode-level 10 дней, logs до 90 дней, RUM-сессии/SR 35 дней, Davis problems 14 месяцев, metrics 5 лет с лестн… |
| `explanations/day-1/architecture.md:10` | `14 месяцев` | …до 90 дней, RUM-сессии/SR 35 дней, Davis problems 14 месяцев, metrics 5 лет с лестницей 1мин→5мин→1час→1день) |
| `explanations/day-1/architecture.md:10` | `1час` | …s 14 месяцев, metrics 5 лет с лестницей 1мин→5мин→1час→1день) |
| `explanations/day-1/architecture.md:25` | `5 минут` | …еский пример: правило «если CPU больше 80% дольше 5 минут: алерт». |
| `explanations/day-1/architecture.md:226` | `5 минут` | …твий пользователя по расписанию. Например, каждые 5 минут проверять, что страница логина в интернет-банке о… |
| `explanations/day-1/architecture.md:474` | `2 месяца` | …л по очереди перезагружается. Применяются раз в 1-2 месяца. |
| `explanations/day-1/architecture.md:476` | `4 недели` | …анках обычно делают по плану, согласованному за 2–4 недели. |
| `explanations/day-1/architecture.md:486` | `4 часа` | …C: если что-то пойдёт не так, восстановление за 2-4 часа. |
| `explanations/day-1/architecture.md:488` | `2 недели` | …обслуживания** с владельцами критичных систем за 2 недели. |
| `explanations/day-1/architecture.md:527` | `2 часа` | …ксы Elasticsearch бэкапятся инкрементально каждые 2 часа (старые инкременты убираются после пяти суток). В… |
| `explanations/day-1/architecture.md:552` | `365 дней` | \| **Distributed traces** \| configurable, максимум 365 дней \| Сами трассы доступны до года; конкретный срок з… |
| `explanations/day-1/architecture.md:553` | `10 дней` | \| **Code-level insights в traces** \| 10 дней (fixed) \| Метод-уровень детализация PurePath; пос… |
| `explanations/day-1/architecture.md:554` | `14 дней` | …до 5 лет с понижением гранулярности \| Лестница: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 ча… |
| `explanations/day-1/architecture.md:554` | `1 минут` | …с понижением гранулярности \| Лестница: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400… |
| `explanations/day-1/architecture.md:554` | `28 дней` | …гранулярности \| Лестница: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400 дней до 5 ле… |
| `explanations/day-1/architecture.md:554` | `5 минут` | …ости \| Лестница: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400 дней до 5 лет: 1 день… |
| `explanations/day-1/architecture.md:554` | `400 дней` | …ица: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400 дней до 5 лет: 1 день. \| |
| `explanations/day-1/architecture.md:554` | `1 час` | …дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400 дней до 5 лет: 1 день. \| |
| `explanations/day-1/architecture.md:555` | `90 дней` | …og Monitoring Classic)** \| configurable, максимум 90 дней \| В SaaS через Grail Log Management: configurable… |
| `explanations/day-1/architecture.md:556` | `35 дней` | \| **User sessions (RUM)** \| 35 дней \| Классический RUM. \| |
| `explanations/day-1/architecture.md:557` | `35 дней` | \| **Session Replay** \| configurable, максимум 35 дней \| Дольше не настраивается в Classic-стеке. \| |
| `explanations/day-1/architecture.md:558` | `365 дней` | \| **Synthetic** \| configurable, максимум 365 дней \| Результаты синтетических мониторов хранятся до… |
| `explanations/day-1/architecture.md:559` | `14 месяцев` | \| **Davis Problems и события** \| 14 месяцев \| Сами инциденты, не сырые данные. \| |
| `explanations/day-1/architecture.md:560` | `30 дней` | …eAgent diagnostics** \| configurable, по умолчанию 30 дней \| Диагностика агента (не метрики, а логи установк… |
| `explanations/day-1/architecture.md:566` | `14 дней` | - ЕСЛИ метрика свежая (до 14 дней) → шаг хранения 1 минута, видны короткие всплески… |
| `explanations/day-1/architecture.md:566` | `1 минут` | - ЕСЛИ метрика свежая (до 14 дней) → шаг хранения 1 минута, видны короткие всплески; ЕСЛИ метрике от 14 до… |
| `explanations/day-1/architecture.md:566` | `28 дней` | …а, видны короткие всплески; ЕСЛИ метрике от 14 до 28 дней → шаг уже 5 минут, минутные пики усредняются; от… |
| `explanations/day-1/architecture.md:566` | `5 минут` | …всплески; ЕСЛИ метрике от 14 до 28 дней → шаг уже 5 минут, минутные пики усредняются; от 28 до 400 дней → 1… |
| `explanations/day-1/architecture.md:566` | `400 дней` | …уже 5 минут, минутные пики усредняются; от 28 до 400 дней → 1 час; от 400 дней до 5 лет → 1 день. Поэтому м… |
| `explanations/day-1/architecture.md:566` | `1 час` | …т, минутные пики усредняются; от 28 до 400 дней → 1 час; от 400 дней до 5 лет → 1 день. Поэтому минутный… |
| `explanations/day-1/architecture.md:567` | `35 дней` | …пользовательская сессия или Session Replay старше 35 дней → их уже нет: в Managed (Classic) RUM-сессии и Se… |
| `explanations/day-1/architecture.md:739` | `4 ТБ` | …: основные данные. Минимум 500 ГБ NVMe для малых, 4 ТБ для больших |
| `explanations/day-1/architecture.md:801` | `60 минут` | …ssandra и Elasticsearch с первым узлом. Время: 30-60 минут на первичную репликацию данных. |
| `explanations/day-1/architecture.md:930` | `3 минут` | …Status**: новый хост должен появиться в течение 2-3 минут после установки. |
| `explanations/day-1/architecture.md:1045` | `1 минут` | \| Davis compute lag \| < 1 минута \| Davis отстаёт от реального времени \| |
| `explanations/day-1/architecture.md:1182` | `2 минут` | ## 📝 Практика (2 минуты, без тенанта) |
| `explanations/day-1/architecture.md:1186` | `35 дней` | …ё доступны, а какие уже нет? (RUM-сессии уже нет: 35 дней; метрики огрубели; трейс без code-level деталей:… |
| `explanations/day-1/architecture.md:1186` | `10 дней` | …; метрики огрубели; трейс без code-level деталей: 10 дней; карточка Davis-проблемы жива: 14 месяцев.) |
| `explanations/day-1/architecture.md:1186` | `14 месяцев` | …l деталей: 10 дней; карточка Davis-проблемы жива: 14 месяцев.) |
| `explanations/day-1/auto-tagging.md:50` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно… |
| `explanations/day-1/baselines.md:37` | `7 дней` | …AI анализирует историю метрики (период обучения: 7 дней по multidimensional baselining), строит коридор с… |
| `explanations/day-1/baselines.md:68` | `7 дней` | …зует для baseline. Стандартный период обучения: **7 дней** (см. раздел Davis AI multidimensional baselinin… |
| `explanations/day-1/baselines.md:135` | `15 минут` | …ре есть проблемы-шумы: каждую ночь cron-скрипт на 15 минут забивает диск и проходит. Если каждое такое событ… |
| `explanations/day-1/baselines.md:162` | `7 дней` | **Период обучения: 7 дней.** Меняется в Reference period. ЕСЛИ метрика, это… |
| `explanations/day-1/baselines.md:162` | `4 дня` | …активизируются раньше, после 20% недели (около 1.4 дня). Многомерный baseline для frontend RUM строится… |
| `explanations/day-1/baselines.md:176` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/components.md:234` | `90 дней` | …Токены выпускают с ограниченным сроком (например, 90 дней) под конкретную волну развёртывания шлюзов и спок… |
| `explanations/day-1/components.md:316` | `3 минут` | ## 📝 Практика (2-3 минуты, без тенанта) |
| `explanations/day-1/dashboards.md:204` | `3 минут` | ## 📝 Практика (3 минуты; на demo-тенанте аккаунт read-only, поэтому в пр… |
| `explanations/day-1/data-explorer.md:9` | `1час` | …Metrics Classic (0-14д→1мин, 14-28д→5мин, 28-400д→1час, 400д-5лет→1день) |
| `explanations/day-1/data-explorer.md:82` | `1 минут` | - **Resolution / разрешение по времени**: Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:82` | `5 минут` | …tion / разрешение по времени**: Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:82` | `1 час` | …решение по времени**: Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:96` | `14 дней` | …минутами. Лестница прореживания метрик Classic (0–14 дней: 1 мин, 14–28 дней: 5 мин, 28–400 дней: 1 час, 40… |
| `explanations/day-1/data-explorer.md:96` | `28 дней` | …прореживания метрик Classic (0–14 дней: 1 мин, 14–28 дней: 5 мин, 28–400 дней: 1 час, 400 дней–5 лет: 1 ден… |
| `explanations/day-1/data-explorer.md:96` | `400 дней` | …Classic (0–14 дней: 1 мин, 14–28 дней: 5 мин, 28–400 дней: 1 час, 400 дней–5 лет: 1 день): отдельный механи… |
| `explanations/day-1/data-explorer.md:96` | `1 час` | …0–14 дней: 1 мин, 14–28 дней: 5 мин, 28–400 дней: 1 час, 400 дней–5 лет: 1 день): отдельный механизм rete… |
| `explanations/day-1/data-explorer.md:103` | `7 дней` | …зывчив; ЕСЛИ вручную зажать одну минуту на окне в 7 дней → запрос тяжёлый, а на данных старше двух недель… |
| `explanations/day-1/data-explorer.md:103` | `14 дней` | …ух недель всё равно вернётся свёрнутый шаг (после 14 дней минимальный шаг хранения уже 5 минут). |
| `explanations/day-1/data-explorer.md:103` | `5 минут` | …й шаг (после 14 дней минимальный шаг хранения уже 5 минут). |
| `explanations/day-1/data-explorer.md:201` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/dem.md:14` | `35 дней` | …ged/shortlink/data-retention-periods): RUM-сессии 35 дней, Session Replay configurable max 35 дней, Synthet… |
| `explanations/day-1/dem.md:14` | `365 дней` | …figurable max 35 дней, Synthetic configurable max 365 дней (Classic) |
| `explanations/day-1/installation.md:68` | `3 минут` | ## 📝 Практика (2-3 минуты; на demo-тенанте только вход в мастер) |
| `explanations/day-1/key-objects.md:156` | `3 минут` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/management-zones.md:57` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно… |
| `explanations/day-1/oneagent-principles.md:169` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/problems-feature.md:58` | `2 часа` | …о: смотреть только открытые проблемы за последние 2 часа; ночная проблема к утру закрылась и «исчезла». Пр… |
| `explanations/day-1/problems-feature.md:58` | `72 часов` | …у закрылась и «исчезла». Приём: расширить окно до 72 часов и переключить Status на Closed: проблема найдётся… |
| `explanations/day-1/problems-feature.md:154` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/problems-feature.md:157` | `72 часов` | 2. Кнопкой **Edit timeframe** расширить окно до 72 часов. |
| `explanations/day-1/smartscape.md:4` | `72 часа` | …ницы из раздела `/managed/`. Stale-entity timeout 72 часа (с пунктирной линией для 2 часов) подтверждено в… |
| `explanations/day-1/smartscape.md:4` | `2 часов` | …e-entity timeout 72 часа (с пунктирной линией для 2 часов) подтверждено в Сессии 4. Все ссылки проверены `s… |
| `explanations/day-1/smartscape.md:70` | `72 часа` | …martscape) карта отображает данные за **последние 72 часа** (timeframe selector не применяется); если соеди… |
| `explanations/day-1/smartscape.md:70` | `72 часов` | …динение или сервис не получают активности более **72 часов**, узел или связь исчезает. Промежуточный сигнал:… |
| `explanations/day-1/smartscape.md:70` | `2 часов` | …ирная линия** для соединений без запросов более **2 часов**. <!-- last-verified: 2026-04-27 source: docs.dy… |
| `explanations/day-1/smartscape.md:74` | `2 часов` | - ЕСЛИ соединение без запросов дольше **2 часов** → ТО связь рисуется **пунктирной линией**: проц… |
| `explanations/day-1/smartscape.md:75` | `72 часов` | - ЕСЛИ активности нет дольше **72 часов** → ТО узел или связь **пропадает** с карты: верн… |
| `explanations/day-1/smartscape.md:76` | `72 часов` | - ЕСЛИ нужно событие старше **72 часов** (вчерашний релиз, ночной сбой) → ТО Smartscape… |
| `explanations/day-1/smartscape.md:113` | `3 минут` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/ui-overview.md:221` | `10 минут` | …к должен уметь без подсказки пройти по тенанту за 10 минут: |
| `explanations/day-2/containers.md:102` | `5 минут` | …build-контейнеры Jenkins / GitLab-Runner живут по 5 минут, но забивают списки. Правило: `image matches jenk… |
| `explanations/day-2/databases.md:15` | `7 дней` | …-sensitivity-services-database): Reference period 7 дней, response time / failure rate / failed connects |
| `explanations/day-2/databases.md:123` | `3 недели` | …ение: по результатам наблюдения baseline первые 2-3 недели. |
| `explanations/day-2/databases.md:182` | `3 Дня` | …о идут рука об руку с проблемами хостов (Темы 1 и 3 Дня 2) и ошибками бизнес-сервисов (Темы 7-8 Дня 2). М… |
| `explanations/day-2/databases.md:182` | `8 Дня` | …ы 1 и 3 Дня 2) и ошибками бизнес-сервисов (Темы 7-8 Дня 2). Маршрут расследования: жалоба на сервис → в к… |
| `explanations/day-2/databases.md:186` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/hosts-processes.md:11` | `20 минут` | …oring): host metrics, process instance snapshots (20 минут окна, 60 мин/день, 100 процессов), trigger при ≥1… |
| `explanations/day-2/hosts-processes.md:44` | `1 Дня` | …t на этом тенанте возвращает 404 (аналогично Теме 1 Дня 2). На снимке курса для хостов работал типизирова… |
| `explanations/day-2/hosts-processes.md:192` | `20 минут` | …load в течение 90 секунд). Один снимок содержит **20 минут данных: 10 минут до триггера и 10 минут после**.… |
| `explanations/day-2/hosts-processes.md:192` | `10 минут` | …секунд). Один снимок содержит **20 минут данных: 10 минут до триггера и 10 минут после**. <!-- last-verifie… |
| `explanations/day-2/hosts-processes.md:201` | `60 минут` | **Лимит на хост:** каждый хост шлёт суммарно **до 60 минут** таких метрик в сутки. Метрики собираются с мину… |
| `explanations/day-2/hosts-processes.md:203` | `60 минут` | **ЕСЛИ → ТО: тумблер enabled и квота 60 минут.** |
| `explanations/day-2/hosts-processes.md:206` | `20 минут` | …яти или сети при включённом тумблере → ТО снимок (20 минут: 10 до и 10 после триггера) пишется автоматически… |
| `explanations/day-2/hosts-processes.md:207` | `60 минут` | - ЕСЛИ за сутки триггеры уже выбрали 60 минут метрик на этом хосте → ТО следующий триггер в это… |
| `explanations/day-2/hosts-processes.md:235` | `15 минут` | …Процесс прогрева кэша стартует в 02:00, работает 15 минут, корректно завершается. Dynatrace каждую ночь соз… |
| `explanations/day-2/hosts-processes.md:237` | `20 минут` | …ion: не создавать Problem, если отсутствие меньше 20 минут. Ложный алерт исчезает. |
| `explanations/day-2/hosts-processes.md:275` | `7 дней` | …ая Process Group: новая модель Davis AI. Ей нужно 7 дней истории для baseline. ЕСЛИ на экране Process grou… |
| `explanations/day-2/kubernetes.md:155` | `3 Дня` | …но мониторить и обычными Host-правилами (Темы 1 и 3 Дня 2). Но K8s-специфичные правила ловят K8s-события,… |
| `explanations/day-2/kubernetes.md:224` | `15 минут` | 6. Через 10-15 минут кластер появляется в интерфейсе со всеми ресурсам… |
| `explanations/day-2/oneagent-infra.md:88` | `5 минут` | - RAID-массив в состоянии degraded более 5 минут → Problem. |
| `explanations/day-2/oneagent-infra.md:108` | `14 дней` | …events, привязана к timeframe запроса: ближайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 ча… |
| `explanations/day-2/oneagent-infra.md:108` | `1 минут` | …привязана к timeframe запроса: ближайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше… |
| `explanations/day-2/oneagent-infra.md:108` | `28 дней` | …imeframe запроса: ближайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше: 1 день (см.… |
| `explanations/day-2/oneagent-infra.md:108` | `5 минут` | …запроса: ближайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше: 1 день (см. лестницу… |
| `explanations/day-2/oneagent-infra.md:108` | `400 дней` | …жайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше: 1 день (см. лестницу Metrics Clas… |
| `explanations/day-2/oneagent-infra.md:108` | `1 час` | …дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше: 1 день (см. лестницу Metrics Classic ниж… |
| `explanations/day-2/oneagent-infra.md:149` | `365 дней` | - **Distributed traces**: конфигурируется, **до 365 дней** максимум. Code-level insights детальные сохраня… |
| `explanations/day-2/oneagent-infra.md:149` | `10 дней` | …имум. Code-level insights детальные сохраняются **10 дней (фикс)**, дальше остаются агрегаты. |
| `explanations/day-2/oneagent-infra.md:150` | `365 дней` | …s and request attributes**: конфигурируется, **до 365 дней** максимум. |
| `explanations/day-2/oneagent-infra.md:151` | `365 дней` | …**RUM: User action data**: конфигурируется, **до 365 дней** максимум. |
| `explanations/day-2/oneagent-infra.md:152` | `35 дней` | - **RUM: User sessions**: **35 дней (фикс)**. |
| `explanations/day-2/oneagent-infra.md:153` | `35 дней` | - **RUM: Mobile crashes**: **35 дней (фикс)**. |
| `explanations/day-2/oneagent-infra.md:154` | `35 дней` | - **RUM: Session Replay**: конфигурируется, **до 35 дней** максимум. |
| `explanations/day-2/oneagent-infra.md:155` | `90 дней` | …**Log Monitoring Classic**: конфигурируется, **до 90 дней** максимум. Хранятся в Elasticsearch в зоне класт… |
| `explanations/day-2/oneagent-infra.md:156` | `14 дней` | …Classic**: **5 лет** с лестницей гранулярности: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1… |
| `explanations/day-2/oneagent-infra.md:156` | `1 минут` | …**5 лет** с лестницей гранулярности: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400… |
| `explanations/day-2/oneagent-infra.md:156` | `28 дней` | …лестницей гранулярности: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет… |
| `explanations/day-2/oneagent-infra.md:156` | `5 минут` | …гранулярности: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. |
| `explanations/day-2/oneagent-infra.md:156` | `400 дней` | …и: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. |
| `explanations/day-2/oneagent-infra.md:156` | `1 час` | …й → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. |
| `explanations/day-2/oneagent-infra.md:157` | `14 месяцев` | - **Davis problems и events**: **14 месяцев**. |
| `explanations/day-2/oneagent-infra.md:158` | `30 дней` | …port archives)**: конфигурируется, по умолчанию **30 дней**. |
| `explanations/day-2/os-monitoring.md:16` | `35 дней` | …ов (Metrics Classic 5 лет, Log Monitoring Classic 35 дней) |
| `explanations/day-2/os-monitoring.md:138` | `10 ТБ` | *Типовой случай.* Диск под бэкапы СУБД, 10 ТБ. Бэкапы пишутся пачками и занимают 60-70% диска.… |
| `explanations/day-2/os-monitoring.md:213` | `3 минут` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/problems-navigation.md:48` | `10 минут` | …ravelService`. Началась 21 апреля в 11:11, длится 10 минут. Вторая: `Postgres Availability P-26049003`, Impa… |
| `explanations/day-2/problems-navigation.md:48` | `16 минут` | …wsqmnv8.us-east-1.rds.amazonaws.com:5432`, длится 16 минут. Каждая запись: потенциальная точка входа в рассл… |
| `explanations/day-2/problems-navigation.md:134` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/problems-navigation.md:136` | `72 часов` | …м списке расширить окно кнопкой Edit timeframe до 72 часов. |
| `explanations/day-2/service-cards.md:73` | `24 часа` | …hours: Dynatrace показывает метрики за последние 24 часа и параллельно сравнивает с предыдущими 24 часами… |
| `explanations/day-2/service-cards.md:122` | `30 дней` | …lability `/api/auth/login` должна быть ≥ 99.9% за 30 дней». Для измерения нужна метрика именно этого endpoi… |
| `explanations/day-2/service-cards.md:160` | `10 минут` | …ailure rate за последний час: пик 5% в конкретные 10 минут. |
| `explanations/day-2/service-cards.md:173` | `365 дней` | …s: Requests and request attributes» хранятся **до 365 дней** (configurable). Долгосрочно метрика идёт также… |
| `explanations/day-2/service-cards.md:173` | `14 дней` | …s Classic с собственной лестницей прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1… |
| `explanations/day-2/service-cards.md:173` | `1 минут` | …с собственной лестницей прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400… |
| `explanations/day-2/service-cards.md:173` | `28 дней` | …лестницей прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет… |
| `explanations/day-2/service-cards.md:173` | `5 минут` | …прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день.… |
| `explanations/day-2/service-cards.md:173` | `400 дней` | …я: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. <!-- last-ver… |
| `explanations/day-2/service-cards.md:173` | `1 час` | …й → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. <!-- last-verified: 2… |
| `explanations/day-2/service-cards.md:199` | `2 часа` | *Нюанс: сезонность.* Сравнение с «2 часа назад» может обманывать: если переход между пиком… |
| `explanations/day-2/service-cards.md:199` | `7 дня` | …imeframe `same time last week` сравнивает ровно с 7 днями назад: часто даёт более осмысленную картину для… |
| `explanations/day-2/service-cards.md:205` | `365 дней` | …e time. Distributed traces: конфигурируется, **до 365 дней** максимум; код-уровень insights детально 10 дней… |
| `explanations/day-2/service-cards.md:205` | `10 дней` | …65 дней** максимум; код-уровень insights детально 10 дней (фикс). Services: Requests and request attributes… |
| `explanations/day-2/service-cards.md:211` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/services-overview.md:158` | `2 недель` | 4. После 1-2 недель стабильной работы распространять на остальной Ope… |
| `explanations/day-2/services-overview.md:194` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/app-cards.md:113` | `2 минут` | ## 📝 Практика (2 минуты; состав живой карточки приложения сверяется на п… |
| `explanations/day-3-4/app-detection.md:145` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте + бумага) |
| `explanations/day-3-4/appsec.md:149` | `4 недели` | *Типовая политика.* Сначала Monitor на 2-4 недели, затем Block для критичных endpoint'ов (платежи,… |
| `explanations/day-3-4/incident-lifecycle.md:151` | `5 минут` | …op → немедленное уведомление. Slowdown → задержка 5 минут, чтобы отделить шум. |
| `explanations/day-3-4/instrumentation.md:141` | `3 минут` | ## 📝 Практика (3 минуты, обычный браузер + мониторимая страница) |
| `explanations/day-3-4/key-actions.md:141` | `2 минут` | ## 📝 Практика (2 минуты; кнопка пометки на демо может быть недоступна из… |
| `explanations/day-3-4/mlt-concepts.md:149` | `14 дней` | - 0–14 дней → гранулярность 1 минута |
| `explanations/day-3-4/mlt-concepts.md:149` | `1 минут` | - 0–14 дней → гранулярность 1 минута |
| `explanations/day-3-4/mlt-concepts.md:150` | `28 дней` | - 14–28 дней → 5 минут |
| `explanations/day-3-4/mlt-concepts.md:150` | `5 минут` | - 14–28 дней → 5 минут |
| `explanations/day-3-4/mlt-concepts.md:151` | `400 дней` | - 28–400 дней → 1 час |
| `explanations/day-3-4/mlt-concepts.md:151` | `1 час` | - 28–400 дней → 1 час |
| `explanations/day-3-4/mlt-concepts.md:152` | `400 дней` | - 400 дней – 5 лет → 1 день |
| `explanations/day-3-4/mlt-concepts.md:153` | `90 дней` | …actor 2. Срок хранения: настраивается, максимум **90 дней**. |
| `explanations/day-3-4/mlt-concepts.md:154` | `365 дней` | …строго поиска. Полные транзакционные детали: **до 365 дней (настраивается)**. Code-Level Insights (детальный… |
| `explanations/day-3-4/mlt-concepts.md:154` | `10 дней` | …*. Code-Level Insights (детальный код-профиль): **10 дней** в исходном виде, дальше данные оптимизируются п… |
| `explanations/day-3-4/mlt-concepts.md:155` | `14 месяцев` | - **Davis problems & events.** 14 месяцев (фиксировано). |
| `explanations/day-3-4/mlt-concepts.md:160` | `90 дней` | …тарше настроенного срока хранения логов (максимум 90 дней) → ТО лог-строки по нему уже удалены, расследоват… |
| `explanations/day-3-4/mlt-concepts.md:161` | `365 дней` | …месячной давности → ТО он ещё доступен (трейсы до 365 дней), но детальный код-профиль уже нет (Code-Level In… |
| `explanations/day-3-4/mlt-concepts.md:161` | `10 дней` | …й код-профиль уже нет (Code-Level Insights только 10 дней): для разбора кода реагировать в первые дни. |
| `explanations/day-3-4/mlt-concepts.md:162` | `400 дней` | - ЕСЛИ строите график за период старше 400 дней → ТО точки будут с шагом 1 день, а не 1 минута (м… |
| `explanations/day-3-4/mlt-concepts.md:162` | `1 минут` | …ше 400 дней → ТО точки будут с шагом 1 день, а не 1 минута (метрики старше 400 дней прорежены до суточной г… |
| `explanations/day-3-4/mlt-concepts.md:164` | `15 месяцев` | Цифры из retention для SaaS / Grail (10 лет, 15 месяцев и т.п.) к Managed Classic не относятся. |
| `explanations/day-3-4/mlt-concepts.md:175` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/reliability-config.md:88` | `7 дня` | Davis AI с baseline по 7 дням: для key performance metrics, failure rate, traf… |
| `explanations/day-3-4/reliability-config.md:100` | `0 минут` | …го сервиса должно уйти в Telegram дежурного через 0 минут, а Warning для тестового стенда: никогда. |
| `explanations/day-3-4/request-attributes.md:15` | `365 дней` | …ion-таблицах («Requests and request attributes до 365 дней»: см. темы Дня 2); здесь их собственный экран и м… |
| `explanations/day-3-4/request-attributes.md:54` | `365 дней` | …quests and request attributes» конфигурируются до 365 дней (retention-лестница разобрана в темах Дня 2). |
| `explanations/day-3-4/request-attributes.md:58` | `2 минут` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно… |
| `explanations/day-3-4/response-analysis.md:52` | `7 дней` | …riod / эталонный период.** По умолчанию последние 7 дней. Кнопка **Reset** сбрасывает baseline (нужно посл… |
| `explanations/day-3-4/response-analysis.md:148` | `15 минут` | 3. Через 10-15 минут Failure rate падает до реального уровня (0.1-0.5%… |
| `explanations/day-3-4/response-analysis.md:187` | `2 недели` | …нкая настройка после первичного деплоя занимает 1-2 недели. По каждому критичному сервису: корректировка rul… |
| `explanations/day-3-4/service-flow.md:28` | `72 часа` | …ет \| Все сущности и их связи в окружении за окно ~72 часа \| Цепочки вызовов между конкретными сервисами \| |
| `explanations/day-3-4/service-flow.md:94` | `2 часа` | …оретически может ходить в 10 баз, но за последние 2 часа ходил только в 3, в Service Flow будут только 3.… |
| `explanations/day-3-4/service-flow.md:98` | `72 часа` | …гляд. Near real-time-снимок зависимостей за окно ~72 часа. Подходит для общей архитектуры. |
| `explanations/day-3-4/service-flow.md:110` | `3 минут` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/service-object.md:78` | `7 Дня` | **Отличие от Service Detection rules (Тема 7 Дня 2):** |
| `explanations/day-3-4/sessions.md:88` | `35 дней` | …(compliance, аудит). В Dynatrace сессии живут до 35 дней (RUM Classic retention), для юридических требован… |
| `explanations/day-3-4/sessions.md:116` | `30 минут` | - **Web**: после **30 минут** браузерной неактивности, либо при закрытии вкла… |
| `explanations/day-3-4/sessions.md:117` | `10 минут` | - **Mobile (нативные iOS / Android)**: после **10 минут** неактивности либо при закрытии / force-stop при… |
| `explanations/day-3-4/sessions.md:118` | `10 минут` | - **Custom apps (через OpenKit)**: после **10 минут** без новых custom actions. |
| `explanations/day-3-4/sessions.md:119` | `6 часа` | …чае максимальная длительность сессии ограничена **6 часами**: после этого автоматически открывается новая. |
| `explanations/day-3-4/sessions.md:161` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/sli-slo-sla.md:30` | `30 дней` | …значение SLI за период \| Availability ≥ 99.9% за 30 дней \| |
| `explanations/day-3-4/sli-slo-sla.md:119` | `30 дней` | *Пример расчёта.* Target = 99.9% за 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты*… |
| `explanations/day-3-4/sli-slo-sla.md:119` | `2 минут` | …а 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты** даунтайма в месяц. |
| `explanations/day-3-4/sli-slo-sla.md:121` | `40 минут` | *Как используется.* Если в начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки… |
| `explanations/day-3-4/sli-slo-sla.md:121` | `2 минут` | …чале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки **замораживает выкатки** ри… |
| `explanations/day-3-4/sli-slo-sla.md:138` | `3 минут` | ## 📝 Практика (3 минуты, счёт на бумаге + один экран) |
| `explanations/day-3-4/sli-slo-sla.md:140` | `30 дней` | 1. Посчитать бюджет ошибок для цели 99.5% за 30 дней: 30 × 24 × 60 × 0.005 = **216 минут** допустимого… |
| `explanations/day-3-4/sli-slo-sla.md:140` | `216 минут` | …я цели 99.5% за 30 дней: 30 × 24 × 60 × 0.005 = **216 минут** допустимого даунтайма (сверить с примером 99.9%… |
| `explanations/day-3-4/sli-slo-sla.md:140` | `2 минут` | …устимого даунтайма (сверить с примером 99.9% → 43.2 минуты выше). |
| `explanations/day-3-4/thresholds.md:44` | `7 дней` | …тся на реперном периоде: по умолчанию **последние 7 дней**) или **fixed thresholds** (фиксированные пороги… |
| `explanations/day-5/alerting-logic.md:161` | `10 минут` | …елать escalation («если никто не взял в работу за 10 минут: эскалировать уровень выше»). Это делают специали… |
| `explanations/day-5/alerting-profiles.md:159` | `7 дней` | …каждой метрики автоматически (референсный период: 7 дней). |
| `explanations/day-5/alerting-profiles.md:186` | `3 часа` | - PagerDuty триггерит в 3 часа ночи 4 раза за месяц: на пятый телефон выключен. |
| `explanations/day-5/alerting-profiles.md:193` | `5 минут` | - **Delay.** 3-5 минут перед первым уведомлением. Проблема «мигнула и уш… |
| `explanations/day-5/alerting-profiles.md:251` | `3 минут` | ## 📝 Практика (3 минуты, на бумаге) |
| `explanations/day-5/api.md:52` | `30 дней` | 2. Срок действия: 1 день / 30 дней / 1 год / unlimited. Для production обычно 1 год… |
| `explanations/day-5/api.md:52` | `1 год` | 2. Срок действия: 1 день / 30 дней / 1 год / unlimited. Для production обычно 1 год с напоми… |
| `explanations/day-5/api.md:76` | `90 дней` | …on**: максимальный срок действия. Если политика = 90 дней, пользователь не может создать токен «на 1 год».… |
| `explanations/day-5/api.md:76` | `1 год` | …90 дней, пользователь не может создать токен «на 1 год». Реализация требования «регулярная ротация секре… |
| `explanations/day-5/api.md:174` | `90 дней` | - **Expiration date.** Всегда. Ротировать каждые 90 дней по политике безопасности. |
| `explanations/day-5/api.md:187` | `5 минут` | …ко меняющиеся результаты (список сущностей: раз в 5 минут, не на каждый запрос). |
| `explanations/day-5/api.md:228` | `2 минут` | ## 📝 Практика (2 минуты, на бумаге) |
| `explanations/day-5/journeys.md:126` | `4 час` | На шаге 4 часто отваливаются. Dynatrace помогает отличить ожида… |
| `explanations/day-5/journeys.md:126` | `2 минут` | …Dynatrace помогает отличить ожидаемое поведение (2 минуты листания условий) от проблемы (2 минуты тапов по… |
| `explanations/day-5/rum.md:168` | `30 минут` | - **Web**: после 30 минут бездействия (inactivity timeout). |
| `explanations/day-5/rum.md:169` | `10 минут` | - **Mobile / Custom**: после 10 минут бездействия. |
| `explanations/day-5/rum.md:171` | `30 минут` | …ель сделал паузу дольше таймаута бездействия (Web 30 минут, Mobile 10 минут) и вернулся → ТО Dynatrace закро… |
| `explanations/day-5/rum.md:171` | `10 минут` | …дольше таймаута бездействия (Web 30 минут, Mobile 10 минут) и вернулся → ТО Dynatrace закроет прежнюю сессию… |
| `explanations/day-5/rum.md:198` | `2026 год` | …ческий (stable в Managed) и новый (SaaS-first). В 2026 году Managed ещё полностью не мигрировал на Apps-моде… |
| `explanations/day-5/synthetic.md:41` | `5 минут` | …ных или **private** локаций; периодичность: раз в 5 минут или реже. |
| `explanations/day-5/synthetic.md:128` | `5 минут` | - Минимальная частота: 5 минут или реже. |
| `explanations/day-5/synthetic.md:198` | `5 минут` | - DNS resolution (каждые 5 минут). |
| `explanations/day-5/synthetic.md:202` | `5 минут` | - Authentication flow (каждые 5 минут). |
| `explanations/day-5/synthetic.md:207` | `15 минут` | - Login + главная (каждые 15 минут). |
| `explanations/day-5/synthetic.md:208` | `30 минут` | - Критичный end-to-end сценарий (каждые 30 минут). |
| `explanations/day-5/synthetic.md:209` | `30 минут` | - Проверка мобильного веб-интерфейса (каждые 30 минут). |
| `explanations/day-5/synthetic.md:211` | `30 минут` | …льным браузером) → ТО частоту снижаете (каждые 15-30 минут), иначе ActiveGate перегрузится, ведь потолок все… |
| `explanations/day-5/usql.md:144` | `2022 год` | DQL: новый язык, появившийся в 2022 году для работы с **Grail**, облачным хранилищем Dyna… |
| `explanations/day-5/usql.md:212` | `5 минут` | …аивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversion… |
| `explanations/day-5/usql.md:221` | `35 дней` | …ессиям ограничена retention RUM/Sessions Classic (35 дней). Для долгосрочного хранения: экспорт в Elasticse… |
| `explanations/day-5/usql.md:282` | `3 минут` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |

## [DYNATRACE_VERSION]  — 38 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:13` | `1.328` | …hats-new/release-notes/managed): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) с фактическо… |
| `explanations/day-1/architecture.md:13` | `1.330` | …/release-notes/managed): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) с фактической каденц… |
| `explanations/day-1/architecture.md:13` | `1.332` | …-notes/managed): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) с фактической каденцией по д… |
| `explanations/day-1/architecture.md:13` | `1.334` | …anaged): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) с фактической каденцией по датам сбо… |
| `explanations/day-1/architecture.md:13` | `1.336` | …выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) с фактической каденцией по датам сборок (вес… |
| `explanations/day-1/architecture.md:472` | `1.270.10` | …равления внутри одной минорной версии (например, `1.270.10 → 1.270.11`). Применяются без перезагрузки класте… |
| `explanations/day-1/architecture.md:472` | `1.270.11` | …утри одной минорной версии (например, `1.270.10 → 1.270.11`). Применяются без перезагрузки кластера, без дау… |
| `explanations/day-1/architecture.md:474` | `1.270` | …Minor updates.** Обновления внутри major-версии (`1.270 → 1.271`). Обычно требуют rolling restart узлов:… |
| `explanations/day-1/architecture.md:474` | `1.271` | …dates.** Обновления внутри major-версии (`1.270 → 1.271`). Обычно требуют rolling restart узлов: кластер… |
| `explanations/day-1/architecture.md:476` | `1.260` | **Major upgrades.** Большие обновления (`1.260 → 1.270`). Раз в полгода. Требуют полного просмот… |
| `explanations/day-1/architecture.md:476` | `1.270` | **Major upgrades.** Большие обновления (`1.260 → 1.270`). Раз в полгода. Требуют полного просмотра relea… |
| `explanations/day-1/architecture.md:478` | `1.334` | …2026 сборки выходили примерно раз в месяц и чаще (1.334 март → 1.336 апрель → 1.338 май → 1.340 июнь). Сб… |
| `explanations/day-1/architecture.md:478` | `1.336` | …ыходили примерно раз в месяц и чаще (1.334 март → 1.336 апрель → 1.338 май → 1.340 июнь). Сборка выкатыва… |
| `explanations/day-1/architecture.md:478` | `1.338` | …о раз в месяц и чаще (1.334 март → 1.336 апрель → 1.338 май → 1.340 июнь). Сборка выкатывается клиентам ч… |
| `explanations/day-1/architecture.md:478` | `1.340` | …ц и чаще (1.334 март → 1.336 апрель → 1.338 май → 1.340 июнь). Сборка выкатывается клиентам через CMC. Те… |
| `explanations/day-1/components.md:12` | `1.328` | …hats-new/release-notes/managed): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) |
| `explanations/day-1/components.md:12` | `1.330` | …/release-notes/managed): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) |
| `explanations/day-1/components.md:12` | `1.332` | …-notes/managed): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) |
| `explanations/day-1/components.md:12` | `1.334` | …anaged): выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) |
| `explanations/day-1/components.md:12` | `1.336` | …выпуски Managed (1.328 / 1.330 / 1.332 / 1.334 / 1.336 ...) |
| `explanations/day-2/databases.md:14` | `1.173` | …sic/database-insights): Oracle Database Insights (1.173+) через Environment ActiveGate |
| `explanations/day-2/databases.md:180` | `1.173` | …tiveGate** (доступен начиная с OneAgent/AG версии 1.173); этот канал внутренний и не выходит за пределы к… |
| `explanations/day-2/hosts-processes.md:15` | `1.259` | …ы `$prefix`/`$suffix`/`$eq`/`$contains`, OneAgent 1.259+ для Report process group option |
| `explanations/day-2/os-monitoring.md:60` | `1.336.55` | …e old and no longer available`. Версия платформы `1.336.55.20260417-205630`. Универсальный entity list замен… |
| `explanations/day-2/services-overview.md:13` | `1.318` | …ces/services/service-detection-v2): SDv2 (cluster 1.318+), для OpenTelemetry-сервисов и Adobe Experience… |
| `explanations/day-2/services-overview.md:107` | `1.318` | …, доступный в Managed начиная с **Cluster version 1.318+**. SDv2 спроектирован для **OpenTelemetry-сервис… |
| `explanations/day-2/services-overview.md:155` | `1.318` | …что кластер обновлён до версии с поддержкой SDv2 (1.318+). |
| `explanations/day-2/services-overview.md:190` | `1.318` | …. Service Detection v2 (SDv2) появилась с Cluster 1.318+ и применяется в первую очередь для OpenTelemetry… |
| `explanations/day-3-4/appsec.md:157` | `1.241` | …Protection (блокировка атак)**: Java 8+ (OneAgent 1.241+; только Windows x86 и Linux x86), .NET Framework… |
| `explanations/day-3-4/appsec.md:157` | `1.289` | …), .NET Framework 4.5+ и .NET Core 3.0+ (OneAgent 1.289+), Go (OneAgent 1.311+). Только 64-битные процесс… |
| `explanations/day-3-4/appsec.md:157` | `1.311` | …и .NET Core 3.0+ (OneAgent 1.289+), Go (OneAgent 1.311+). Только 64-битные процессы. |
| `explanations/day-3-4/instrumentation.md:94` | `1.294` | …речаются только в окружениях, созданных до версии 1.294: поддержка IE 11 прекращена в RUM JS 1.293. В нов… |
| `explanations/day-3-4/instrumentation.md:94` | `1.293` | …версии 1.294: поддержка IE 11 прекращена в RUM JS 1.293. В новых установках их в списке нет, в банковском… |
| `explanations/day-5/rum.md:159` | `1.293` | …t Explorer 11 прекращена начиная с RUM JavaScript 1.293: для legacy-приложений на IE остаются только OneA… |
| `explanations/day-5/session-replay.md:186` | `1.193` | - **OneAgent 1.193+** требуется на хостах: эта версия поддерживает в… |
| `explanations/day-5/synthetic.md:126` | `1.331` | …кается современный браузер (на Linux ActiveGate с 1.331: Chrome for Testing с авто-обновлением, можно отк… |
| `explanations/day-5/synthetic.md:148` | `1.169` | - **Версии:** Environment ActiveGate **1.169+** или Cluster ActiveGate (с Managed **1.176+**). |
| `explanations/day-5/synthetic.md:148` | `1.176` | …te **1.169+** или Cluster ActiveGate (с Managed **1.176+**). |

## [LATENCY]  — 170 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:25` | `5 минут` | …еский пример: правило «если CPU больше 80% дольше 5 минут: алерт». |
| `explanations/day-1/architecture.md:226` | `5 минут` | …твий пользователя по расписанию. Например, каждые 5 минут проверять, что страница логина в интернет-банке о… |
| `explanations/day-1/architecture.md:226` | `2 секунды` | …о страница логина в интернет-банке открывается за 2 секунды. Эти проверки запускаются с ActiveGate, потому чт… |
| `explanations/day-1/architecture.md:517` | `10 ms` | …х дата-центрах с low-latency связью между ними (< 10 ms ping). |
| `explanations/day-1/architecture.md:554` | `1 минута` | …с понижением гранулярности \| Лестница: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400… |
| `explanations/day-1/architecture.md:554` | `5 минут` | …ости \| Лестница: 0–14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, от 400 дней до 5 лет: 1 день… |
| `explanations/day-1/architecture.md:566` | `1 минута` | - ЕСЛИ метрика свежая (до 14 дней) → шаг хранения 1 минута, видны короткие всплески; ЕСЛИ метрике от 14 до 2… |
| `explanations/day-1/architecture.md:566` | `5 минут` | …всплески; ЕСЛИ метрике от 14 до 28 дней → шаг уже 5 минут, минутные пики усредняются; от 28 до 400 дней → 1… |
| `explanations/day-1/architecture.md:591` | `10 мс` | - **Сетевая задержка между узлами: максимум 10 мс** (не только пропускная способность). |
| `explanations/day-1/architecture.md:721` | `10 мс` | - Сеть между узлами с задержкой не выше 10 мс (см. `docs.dynatrace.com/managed/managed-cluster/… |
| `explanations/day-1/architecture.md:801` | `60 минут` | …ssandra и Elasticsearch с первым узлом. Время: 30-60 минут на первичную репликацию данных. |
| `explanations/day-1/architecture.md:930` | `3 минут` | …Status**: новый хост должен появиться в течение 2-3 минут после установки. |
| `explanations/day-1/architecture.md:1045` | `1 минута` | \| Davis compute lag \| < 1 минута \| Davis отстаёт от реального времени \| |
| `explanations/day-1/architecture.md:1182` | `2 минуты` | ## 📝 Практика (2 минуты, без тенанта) |
| `explanations/day-1/auto-tagging.md:50` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно) |
| `explanations/day-1/baselines.md:135` | `15 минут` | …ре есть проблемы-шумы: каждую ночь cron-скрипт на 15 минут забивает диск и проходит. Если каждое такое событ… |
| `explanations/day-1/baselines.md:156` | `500 мс` | …оринга с общим порогом «алерт, если отклик больше 500 мс». Такой порог не имеет смысла для сервиса со сред… |
| `explanations/day-1/baselines.md:156` | `50 мс` | …г не имеет смысла для сервиса со средним откликом 50 мс (всегда норма) и одновременно не имеет смысла для… |
| `explanations/day-1/baselines.md:156` | `2000 мс` | …о не имеет смысла для сервиса со средним откликом 2000 мс (всегда аномалия). |
| `explanations/day-1/baselines.md:158` | `50 мс` | …чью почти нулевая. Если сервис обычно отвечает за 50 мс утром и 120 мс в пик-часы, для Davis это два разн… |
| `explanations/day-1/baselines.md:158` | `120 мс` | …вая. Если сервис обычно отвечает за 50 мс утром и 120 мс в пик-часы, для Davis это два разных эталона: веч… |
| `explanations/day-1/baselines.md:176` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/components.md:263` | `30 секунд` | …ssandra, Elasticsearch). UI может «мигнуть» на 10–30 секунд, данные не теряются: они буферизуются в ActiveGat… |
| `explanations/day-1/components.md:316` | `3 минуты` | ## 📝 Практика (2-3 минуты, без тенанта) |
| `explanations/day-1/dashboards.md:204` | `3 минуты` | ## 📝 Практика (3 минуты; на demo-тенанте аккаунт read-only, поэтому в пре… |
| `explanations/day-1/data-explorer.md:82` | `1 минута` | - **Resolution / разрешение по времени**: Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:82` | `5 минут` | …tion / разрешение по времени**: Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:103` | `5 минут` | …й шаг (после 14 дней минимальный шаг хранения уже 5 минут). |
| `explanations/day-1/data-explorer.md:201` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/dem.md:170` | `2 секунды` | …загрузка домашней страницы должна укладываться в 2 секунды, а сложный поиск приемлем и за 6 секунд. Отсюда: |
| `explanations/day-1/dem.md:170` | `6 секунд` | …ваться в 2 секунды, а сложный поиск приемлем и за 6 секунд. Отсюда: |
| `explanations/day-1/dem.md:172` | `1 секунда` | - ЕСЛИ задать пороги жёстко (например, Tolerating 1 секунда) → больше действий уйдёт в Tolerating и Frustrate… |
| `explanations/day-1/dem.md:173` | `5 секунд` | - ЕСЛИ задать пороги мягко (например, Tolerating 5 секунд) → почти всё попадёт в Satisfied, Apdex будет выс… |
| `explanations/day-1/installation.md:68` | `3 минуты` | ## 📝 Практика (2-3 минуты; на demo-тенанте только вход в мастер) |
| `explanations/day-1/key-objects.md:87` | `120 мс` | …лько отвечает сервис платежей»: медиана, например 120 мс. «Как у самых медленных клиентов»: 90-й перцентил… |
| `explanations/day-1/key-objects.md:87` | `450 мс` | …ых медленных клиентов»: 90-й перцентиль, например 450 мс. |
| `explanations/day-1/key-objects.md:156` | `3 минуты` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/management-zones.md:57` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно) |
| `explanations/day-1/oneagent-principles.md:169` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/problems-feature.md:133` | `120 мс` | …диана времени отклика `payment-service` растёт со 120 мс до 800 мс. Davis AI, опираясь на baseline с учёто… |
| `explanations/day-1/problems-feature.md:133` | `800 мс` | …ени отклика `payment-service` растёт со 120 мс до 800 мс. Davis AI, опираясь на baseline с учётом времени… |
| `explanations/day-1/problems-feature.md:154` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/smartscape.md:113` | `3 минуты` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-1/ui-overview.md:221` | `10 минут` | …к должен уметь без подсказки пройти по тенанту за 10 минут: |
| `explanations/day-2/containers.md:102` | `5 минут` | …build-контейнеры Jenkins / GitLab-Runner живут по 5 минут, но забивают списки. Правило: `image matches jenk… |
| `explanations/day-2/databases.md:69` | `2.09 ms` | …ые показатели `TradeManagement` на демо: медиана `2.09 ms`, Slowest 10% `10.1 ms`, 0% ошибок, 248 запросов… |
| `explanations/day-2/databases.md:69` | `10.1 ms` | …agement` на демо: медиана `2.09 ms`, Slowest 10% `10.1 ms`, 0% ошибок, 248 запросов в минуту. |
| `explanations/day-2/databases.md:172` | `60 секунд` | …апрос вызывается раз в час и занимает минуту, это 60 секунд нагрузки в час. Сто запросов в секунду по 100 мс… |
| `explanations/day-2/databases.md:172` | `100 мс` | …секунд нагрузки в час. Сто запросов в секунду по 100 мс дают ту же нагрузку. Первый виден по времени откл… |
| `explanations/day-2/databases.md:186` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/hosts-processes.md:11` | `20 минут` | …oring): host metrics, process instance snapshots (20 минут окна, 60 мин/день, 100 процессов), trigger при ≥1… |
| `explanations/day-2/hosts-processes.md:174` | `60 секунд` | …орогом 60 → ТО короткие плановые рестарты (меньше 60 секунд) Problem не порождают, а реальное падение (отсутс… |
| `explanations/day-2/hosts-processes.md:181` | `60 секунд` | …ило: не создавать Problem, если отсутствие меньше 60 секунд. |
| `explanations/day-2/hosts-processes.md:192` | `90 секунд` | …ot now» (данные появляются после reload в течение 90 секунд). Один снимок содержит **20 минут данных: 10 мину… |
| `explanations/day-2/hosts-processes.md:192` | `20 минут` | …load в течение 90 секунд). Один снимок содержит **20 минут данных: 10 минут до триггера и 10 минут после**.… |
| `explanations/day-2/hosts-processes.md:192` | `10 минут` | …секунд). Один снимок содержит **20 минут данных: 10 минут до триггера и 10 минут после**. <!-- last-verifie… |
| `explanations/day-2/hosts-processes.md:201` | `60 минут` | **Лимит на хост:** каждый хост шлёт суммарно **до 60 минут** таких метрик в сутки. Метрики собираются с мину… |
| `explanations/day-2/hosts-processes.md:203` | `60 минут` | **ЕСЛИ → ТО: тумблер enabled и квота 60 минут.** |
| `explanations/day-2/hosts-processes.md:206` | `20 минут` | …яти или сети при включённом тумблере → ТО снимок (20 минут: 10 до и 10 после триггера) пишется автоматически… |
| `explanations/day-2/hosts-processes.md:207` | `60 минут` | - ЕСЛИ за сутки триггеры уже выбрали 60 минут метрик на этом хосте → ТО следующий триггер в это… |
| `explanations/day-2/hosts-processes.md:235` | `15 минут` | …Процесс прогрева кэша стартует в 02:00, работает 15 минут, корректно завершается. Dynatrace каждую ночь соз… |
| `explanations/day-2/hosts-processes.md:237` | `20 минут` | …ion: не создавать Problem, если отсутствие меньше 20 минут. Ложный алерт исчезает. |
| `explanations/day-2/kubernetes.md:224` | `15 минут` | 6. Через 10-15 минут кластер появляется в интерфейсе со всеми ресурсам… |
| `explanations/day-2/oneagent-infra.md:88` | `5 минут` | - RAID-массив в состоянии degraded более 5 минут → Problem. |
| `explanations/day-2/oneagent-infra.md:108` | `1 минута` | …привязана к timeframe запроса: ближайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше:… |
| `explanations/day-2/oneagent-infra.md:108` | `5 минут` | …запроса: ближайшие 14 дней: 1 минута, 14–28 дней: 5 минут, 28–400 дней: 1 час, дальше: 1 день (см. лестницу… |
| `explanations/day-2/oneagent-infra.md:156` | `1 минута` | …**5 лет** с лестницей гранулярности: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 д… |
| `explanations/day-2/oneagent-infra.md:156` | `5 минут` | …гранулярности: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день. |
| `explanations/day-2/os-monitoring.md:213` | `3 минуты` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/problems-navigation.md:48` | `10 минут` | …ravelService`. Началась 21 апреля в 11:11, длится 10 минут. Вторая: `Postgres Availability P-26049003`, Impa… |
| `explanations/day-2/problems-navigation.md:48` | `16 минут` | …wsqmnv8.us-east-1.rds.amazonaws.com:5432`, длится 16 минут. Каждая запись: потенциальная точка входа в рассл… |
| `explanations/day-2/problems-navigation.md:134` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/service-cards.md:86` | `800 мс` | …я поиска bottleneck. *Пример вывода:* общее время 800 мс, из них 620 мс: один SQL-запрос в БД X. Дальше: S… |
| `explanations/day-2/service-cards.md:86` | `620 мс` | …neck. *Пример вывода:* общее время 800 мс, из них 620 мс: один SQL-запрос в БД X. Дальше: SQL оптимизирова… |
| `explanations/day-2/service-cards.md:134` | `120 мс` | 1. Overview → Response time вырос с 120 мс до 450 мс за последний час. |
| `explanations/day-2/service-cards.md:134` | `450 мс` | 1. Overview → Response time вырос с 120 мс до 450 мс за последний час. |
| `explanations/day-2/service-cards.md:136` | `150 мс` | …замедлился больше всех. `/api/payment/process`: с 150 мс до 600 мс. |
| `explanations/day-2/service-cards.md:136` | `600 мс` | …больше всех. `/api/payment/process`: с 150 мс до 600 мс. |
| `explanations/day-2/service-cards.md:137` | `500 мс` | 4. Открываем endpoint → PurePath waterfall → 500 мс, это один SQL-запрос к БД `account-db`. |
| `explanations/day-2/service-cards.md:149` | `45 мс` | 3. Response time: медиана выросла с 30 до 45 мс. Приемлемо. |
| `explanations/day-2/service-cards.md:160` | `10 минут` | …ailure rate за последний час: пик 5% в конкретные 10 минут. |
| `explanations/day-2/service-cards.md:173` | `1 минута` | …с собственной лестницей прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 д… |
| `explanations/day-2/service-cards.md:173` | `5 минут` | …прореживания: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней – 5 лет → 1 день.… |
| `explanations/day-2/service-cards.md:211` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-2/services-overview.md:167` | `100 мс` | …анде: «все Database service со временем отклика > 100 мс». Kafka-команде: «все Messaging service с отстава… |
| `explanations/day-2/services-overview.md:194` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/app-cards.md:101` | `2 секунды` | 1. **Performance** (page load, LCP): 2 секунды. Не супер медленно. |
| `explanations/day-3-4/app-cards.md:113` | `2 минуты` | ## 📝 Практика (2 минуты; состав живой карточки приложения сверяется на пр… |
| `explanations/day-3-4/app-detection.md:145` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте + бумага) |
| `explanations/day-3-4/incident-lifecycle.md:151` | `5 минут` | …op → немедленное уведомление. Slowdown → задержка 5 минут, чтобы отделить шум. |
| `explanations/day-3-4/instrumentation.md:141` | `3 минуты` | ## 📝 Практика (3 минуты, обычный браузер + мониторимая страница) |
| `explanations/day-3-4/key-actions.md:141` | `2 минуты` | ## 📝 Практика (2 минуты; кнопка пометки на демо может быть недоступна из-… |
| `explanations/day-3-4/mlt-concepts.md:20` | `500 мс` | …й вопрос: метрика говорит «response time вырос до 500 мс», но не говорит, где именно; лог показывает ошибк… |
| `explanations/day-3-4/mlt-concepts.md:103` | `5 секунд` | …пользования.* Жалоба «оформление платежа занимает 5 секунд». Без трейсов инженер видит только «клиент ждал 5… |
| `explanations/day-3-4/mlt-concepts.md:103` | `500 мс` | …нер видит только «клиент ждал 5 сек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (о… |
| `explanations/day-3-4/mlt-concepts.md:103` | `200 мс` | …«клиент ждал 5 сек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (ожидание LDAP), 13… |
| `explanations/day-3-4/mlt-concepts.md:103` | `3000 мс` | …ек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (ожидание LDAP), 1300 мс payment-ser… |
| `explanations/day-3-4/mlt-concepts.md:103` | `1300 мс` | …мс gateway, 3000 мс auth-service (ожидание LDAP), 1300 мс payment-service. Корень: медленный LDAP. Без ручн… |
| `explanations/day-3-4/mlt-concepts.md:114` | `500 мс` | …time растёт. В Data Explorer: одна общая линия до 500 мс. Вопрос: равномерно по всем клиентам или только у… |
| `explanations/day-3-4/mlt-concepts.md:149` | `1 минута` | - 0–14 дней → гранулярность 1 минута |
| `explanations/day-3-4/mlt-concepts.md:150` | `5 минут` | - 14–28 дней → 5 минут |
| `explanations/day-3-4/mlt-concepts.md:162` | `1 минута` | …ше 400 дней → ТО точки будут с шагом 1 день, а не 1 минута (метрики старше 400 дней прорежены до суточной гр… |
| `explanations/day-3-4/mlt-concepts.md:175` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/reliability-config.md:100` | `0 минут` | …го сервиса должно уйти в Telegram дежурного через 0 минут, а Warning для тестового стенда: никогда. |
| `explanations/day-3-4/request-attributes.md:58` | `2 минуты` | ## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно) |
| `explanations/day-3-4/response-analysis.md:148` | `15 минут` | 3. Через 10-15 минут Failure rate падает до реального уровня (0.1-0.5%… |
| `explanations/day-3-4/response-analysis.md:160` | `5000 мс` | …его карточке: поднять порог Slowest 10% с 1000 до 5000 мс. Для dev допустимо. |
| `explanations/day-3-4/response-analysis.md:168` | `100 мс` | …seline (history-based). Если Response time обычно 100 мс, а сейчас 400 мс: аномалия, даже если все 400 мс… |
| `explanations/day-3-4/response-analysis.md:168` | `400 мс` | …ased). Если Response time обычно 100 мс, а сейчас 400 мс: аномалия, даже если все 400 мс запросов успешные… |
| `explanations/day-3-4/service-flow.md:73` | `2000 мс` | …бро от сервиса к БД `accounts-db`. Медиана вызова 2000 мс. Остальные рёбра зелёные. Корень: БД, а не сам се… |
| `explanations/day-3-4/service-flow.md:110` | `3 минуты` | ## 📝 Практика (2-3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/sessions.md:92` | `30 секунд` | …ссий, или объём bulk превысил ~896 KB, или прошло 30 секунд без новых завершений: что наступит первым. |
| `explanations/day-3-4/sessions.md:116` | `30 минут` | - **Web**: после **30 минут** браузерной неактивности, либо при закрытии вкла… |
| `explanations/day-3-4/sessions.md:117` | `10 минут` | - **Mobile (нативные iOS / Android)**: после **10 минут** неактивности либо при закрытии / force-stop при… |
| `explanations/day-3-4/sessions.md:118` | `10 минут` | - **Custom apps (через OpenKit)**: после **10 минут** без новых custom actions. |
| `explanations/day-3-4/sessions.md:161` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-3-4/sli-slo-sla.md:67` | `3 секунд` | …важна скорость, а не только факт ответа (платёж < 3 секунд). |
| `explanations/day-3-4/sli-slo-sla.md:105` | `3 секунд` | \| Платёжный сервис \| % успешных платежей < 3 секунд \| |
| `explanations/day-3-4/sli-slo-sla.md:107` | `500 мс` | \| Карточный процессинг \| Доля транзакций < 500 мс \| |
| `explanations/day-3-4/sli-slo-sla.md:119` | `43.2 минуты` | …% за 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты** даунтайма в месяц. |
| `explanations/day-3-4/sli-slo-sla.md:121` | `40 минут` | *Как используется.* Если в начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки… |
| `explanations/day-3-4/sli-slo-sla.md:121` | `3.2 минуты` | …начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки **замораживает выкатки** рис… |
| `explanations/day-3-4/sli-slo-sla.md:138` | `3 минуты` | ## 📝 Практика (3 минуты, счёт на бумаге + один экран) |
| `explanations/day-3-4/sli-slo-sla.md:140` | `216 минут` | …я цели 99.5% за 30 дней: 30 × 24 × 60 × 0.005 = **216 минут** допустимого даунтайма (сверить с примером 99.9%… |
| `explanations/day-3-4/sli-slo-sla.md:140` | `43.2 минуты` | …допустимого даунтайма (сверить с примером 99.9% → 43.2 минуты выше). |
| `explanations/day-3-4/thresholds.md:125` | `200 мс` | Медиана времени загрузки может быть хорошей (200 мс), но **хвост распределения** (P99): ужасным (5 се… |
| `explanations/day-3-4/thresholds.md:125` | `5 секунд` | …0 мс), но **хвост распределения** (P99): ужасным (5 секунд). Это реальные пользователи с плохой сетью или ст… |
| `explanations/day-5/alerting-logic.md:161` | `10 минут` | …елать escalation («если никто не взял в работу за 10 минут: эскалировать уровень выше»). Это делают специали… |
| `explanations/day-5/alerting-logic.md:185` | `30 секунд` | …а **pull-model**: внутренний сервис-poller каждые 30 секунд спрашивает Dynatrace API «есть ли новые проблемы»… |
| `explanations/day-5/alerting-profiles.md:193` | `5 минут` | - **Delay.** 3-5 минут перед первым уведомлением. Проблема «мигнула и уш… |
| `explanations/day-5/alerting-profiles.md:193` | `90 секунд` | …первым уведомлением. Проблема «мигнула и ушла» за 90 секунд: не тревожить дежурного. |
| `explanations/day-5/alerting-profiles.md:251` | `3 минуты` | ## 📝 Практика (3 минуты, на бумаге) |
| `explanations/day-5/api.md:187` | `5 минут` | …ко меняющиеся результаты (список сущностей: раз в 5 минут, не на каждый запрос). |
| `explanations/day-5/api.md:228` | `2 минуты` | ## 📝 Практика (2 минуты, на бумаге) |
| `explanations/day-5/app-segments.md:106` | `500 мс` | …загрузки: норма, для торговой платформы критично 500 мс. Одним Apdex не мониторить. |
| `explanations/day-5/app-segments.md:144` | `800 мс` | …ом регионе».** По региону: медиана 1.2 сек против 800 мс в других. По провайдерам: 80% трафика через один… |
| `explanations/day-5/app-segments.md:144` | `250 мс` | …через один мелкий ISP, у него пинг до дата-центра 250 мс против 60 мс у крупного. Решение: переговоры с IS… |
| `explanations/day-5/app-segments.md:144` | `60 мс` | …кий ISP, у него пинг до дата-центра 250 мс против 60 мс у крупного. Решение: переговоры с ISP или CDN. |
| `explanations/day-5/app-segments.md:148` | `300 мс` | …делают deep packet inspection для SSL: добавляет 300 мс. Решение: мониторить SSL handshake time отдельно,… |
| `explanations/day-5/journeys.md:126` | `2 минуты` | …Dynatrace помогает отличить ожидаемое поведение (2 минуты листания условий) от проблемы (2 минуты тапов по… |
| `explanations/day-5/rum.md:7` | `35 мс` | …видно лишь время обработки на сервере (например, 35 мс), а реальное ожидание пользователя (например, 730… |
| `explanations/day-5/rum.md:7` | `730 мс` | …мс), а реальное ожидание пользователя (например, 730 мс) и его причина (медленная сеть, тяжёлый JavaScrip… |
| `explanations/day-5/rum.md:137` | `15 мс` | …аемость. Серверный агент видит: «запрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользовате… |
| `explanations/day-5/rum.md:137` | `20 мс` | …ент видит: «запрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, п… |
| `explanations/day-5/rum.md:137` | `35 мс` | …апрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, потому что: |
| `explanations/day-5/rum.md:137` | `730 мс` | …ёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, потому что: |
| `explanations/day-5/rum.md:139` | `200 мс` | - 200 мс запрос шёл до дата-центра (мобильный интернет, пл… |
| `explanations/day-5/rum.md:140` | `35 мс` | - 35 мс обрабатывал сервер. |
| `explanations/day-5/rum.md:141` | `250 мс` | - 250 мс ответ шёл обратно. |
| `explanations/day-5/rum.md:142` | `245 мс` | - 245 мс браузер парсил HTML, исполнял JavaScript, рендери… |
| `explanations/day-5/rum.md:144` | `35 мс` | Без RUM видно только 35 мс. С RUM: все 730 с разбивкой на каждый этап. |
| `explanations/day-5/rum.md:168` | `30 минут` | - **Web**: после 30 минут бездействия (inactivity timeout). |
| `explanations/day-5/rum.md:169` | `10 минут` | - **Mobile / Custom**: после 10 минут бездействия. |
| `explanations/day-5/rum.md:171` | `30 минут` | …ель сделал паузу дольше таймаута бездействия (Web 30 минут, Mobile 10 минут) и вернулся → ТО Dynatrace закро… |
| `explanations/day-5/rum.md:171` | `10 минут` | …дольше таймаута бездействия (Web 30 минут, Mobile 10 минут) и вернулся → ТО Dynatrace закроет прежнюю сессию… |
| `explanations/day-5/synthetic.md:41` | `5 минут` | …ных или **private** локаций; периодичность: раз в 5 минут или реже. |
| `explanations/day-5/synthetic.md:128` | `5 минут` | - Минимальная частота: 5 минут или реже. |
| `explanations/day-5/synthetic.md:198` | `5 минут` | - DNS resolution (каждые 5 минут). |
| `explanations/day-5/synthetic.md:202` | `5 минут` | - Authentication flow (каждые 5 минут). |
| `explanations/day-5/synthetic.md:207` | `15 минут` | - Login + главная (каждые 15 минут). |
| `explanations/day-5/synthetic.md:208` | `30 минут` | - Критичный end-to-end сценарий (каждые 30 минут). |
| `explanations/day-5/synthetic.md:209` | `30 минут` | - Проверка мобильного веб-интерфейса (каждые 30 минут). |
| `explanations/day-5/synthetic.md:211` | `30 минут` | …льным браузером) → ТО частоту снижаете (каждые 15-30 минут), иначе ActiveGate перегрузится, ведь потолок все… |
| `explanations/day-5/usql.md:212` | `5 минут` | …аивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversion… |
| `explanations/day-5/usql.md:282` | `3 минуты` | ## 📝 Практика (3 минуты, выполнимо на demo-тенанте) |
| `explanations/day-5/ux-metrics.md:69` | `2 секунды` | …ь без задержек интернета означает, что задержка в 2 секунды у внутреннего пользователя, это уже плохо. Apdex… |
| `explanations/day-5/ux-metrics.md:89` | `5 секунд` | …ель заполняет форму перевода, жмёт «Подтвердить», 5 секунд ничего не происходит. Кнопка не задизейблилась, о… |
| `explanations/day-5/ux-metrics.md:97` | `200 мс` | …общем языке. Фраза разработчика «API отвечает за 200 мс» бизнесу ничего не говорит. Фраза «Apdex упал с 0… |
| `explanations/day-5/ux-metrics.md:119` | `5 секунд` | …висят от типа приложения.** Для системы аналитики 5 секунд на загрузку: норма, для платёжного виджета на кас… |
| `explanations/day-5/ux-metrics.md:157` | `200 мс` | …т не про производительность (страница грузится за 200 мс), а про **недостаток обратной связи в UI**. Польз… |

## [LIMIT_COUNT]  — 15 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:11` | `10 HU` | …e.com/managed/shortlink/host-unit): лестница от 0.10 HU (1.6 GiB) до 1.0 HU (16 GiB), далее +1 HU за кажд… |
| `explanations/day-1/architecture.md:584` | `600 HU` | …блица для геораспределённого кластера: Large = до 600 HU (32 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU… |
| `explanations/day-1/architecture.md:584` | `250 HU` | …rge = до 600 HU (32 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU / 512 ГБ). В этом режиме суммарная ёмкос… |
| `explanations/day-1/architecture.md:609` | `10 HU` | - до **1.6 GiB** RAM → **0.10 HU** |
| `explanations/day-1/architecture.md:610` | `25 HU` | - до **4 GiB** → **0.25 HU** |
| `explanations/day-1/architecture.md:611` | `50 HU` | - до **8 GiB** → **0.50 HU** |
| `explanations/day-1/architecture.md:1116` | `500 HU` | - Например: купили 500 HU → дали Production 400, Dev 50, Staging 50 <!-- qc… |
| `explanations/day-1/data-explorer.md:111` | `3000 метрик` | …-тенанте: **3.1k Metrics, showing 500**: примерно 3000 метрик, в отображаемой странице первые 500. На боевой ин… |
| `explanations/day-2/containers.md:173` | `25 микросервисов` | *Задача.* 25 микросервисов retail-команды, все в namespace `retail-*`. На да… |
| `explanations/day-2/hosts-processes.md:61` | `50 хоста` | …мер, 200 копий `java -jar payment-service.jar` на 50 хостах) и свернуть в **одну Process Group**. В интерфей… |
| `explanations/day-2/hosts-processes.md:261` | `50 хоста` | …вная ценность: 200 копий `payment-service.jar` на 50 хостах превращаются в одну сущность в интерфейсе. Метри… |
| `explanations/day-2/oneagent-infra.md:124` | `200 хостов` | **Первое развёртывание на 100-200 хостов.** Администратор не трогает OneAgent features: пр… |
| `explanations/day-5/api.md:186` | `1000 метрик` | - **Батчинг.** Если можно получить 1000 метрик в одном запросе: не слать 1000 отдельных. |
| `explanations/day-5/journeys.md:68` | `5000 сессий` | *Пример вывода для бизнеса.* Из 5000 сессий товар в корзину положили в 1200. До checkout дошл… |
| `explanations/day-5/rum.md:175` | `14 сессий` | …5 сессий. Если на одном устройстве дважды в день: 14 сессий. Это важно для биллинга (цена в лицензии за user… |

## [MEMORY]  — 23 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:9` | `64 ГБ RAM` | …nstraints, latency между узлами, IOPS, требование 64 ГБ RAM при включённом Log Monitoring |
| `explanations/day-1/architecture.md:251` | `2 ГБ RAM` | - **2 ГБ RAM** (рекомендуется 4 ГБ) |
| `explanations/day-1/architecture.md:251` | `4 ГБ` | - **2 ГБ RAM** (рекомендуется 4 ГБ) |
| `explanations/day-1/architecture.md:253` | `600 МБ` | - Диск, по странице требований ActiveGate: **600 МБ** на установку, до **2 ГБ** под extensions, **1.2… |
| `explanations/day-1/architecture.md:253` | `2 ГБ` | …бований ActiveGate: **600 МБ** на установку, до **2 ГБ** под extensions, **1.2 ГБ** на операционные логи… |
| `explanations/day-1/architecture.md:253` | `4 ГБ` | …ационные логи, **600 МБ** на автообновление, до **4 ГБ** на временные файлы |
| `explanations/day-1/architecture.md:259` | `4 ГБ` | \| Малый (~c6i.large) \| 2 \| ~4 ГБ \| ~800 \| |
| `explanations/day-1/architecture.md:260` | `8 ГБ` | \| Средний (~c6i.xlarge) \| 4 \| ~8 ГБ \| ~1 800 \| |
| `explanations/day-1/architecture.md:261` | `15 ГБ` | \| Большой (~c6i.2xlarge) \| 8 \| ~15 ГБ \| ~2 500 \| |
| `explanations/day-1/architecture.md:578` | `32 ГБ` | \| Micro \| 50 \| 1 000 \| 4 \| 32 ГБ \| 500 \| |
| `explanations/day-1/architecture.md:579` | `64 ГБ` | \| Small \| 300 \| 10 000 \| 8 \| 64 ГБ \| 3 000 \| |
| `explanations/day-1/architecture.md:580` | `128 ГБ` | \| Medium \| 600 \| 25 000 \| 16 \| 128 ГБ \| 5 000 \| |
| `explanations/day-1/architecture.md:581` | `256 ГБ` | \| Large \| 1 250 \| 50 000 \| 32 \| 256 ГБ \| 7 500 \| |
| `explanations/day-1/architecture.md:582` | `512 ГБ` | \| XLarge \| 2 500 \| 100 000 \| 64 \| 512 ГБ \| 10 000 \| |
| `explanations/day-1/architecture.md:584` | `256 ГБ` | …еделённого кластера: Large = до 600 HU (32 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU / 512 ГБ). В этом… |
| `explanations/day-1/architecture.md:584` | `512 ГБ` | …2 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU / 512 ГБ). В этом режиме суммарная ёмкость кластера ниже,… |
| `explanations/day-1/architecture.md:590` | `64 ГБ RAM` | - **Log Monitoring включён** → минимум 64 ГБ RAM на всех узлах (даже если HU-лимит попадает в Micr… |
| `explanations/day-1/architecture.md:738` | `50 ГБ` | - `/` (корень): 50 ГБ (для ОС и Dynatrace бинарников) |
| `explanations/day-1/architecture.md:739` | `500 ГБ` | …/opt/dynatrace-managed`: основные данные. Минимум 500 ГБ NVMe для малых, 4 ТБ для больших |
| `explanations/day-1/architecture.md:740` | `500 ГБ` | …ed/elasticsearch`: индексы, отдельный том минимум 500 ГБ |
| `explanations/day-1/architecture.md:941` | `4 ГБ RAM` | - Минимум 4 ГБ RAM, 2 ядра, 32 ГБ диска (для боевой нагрузки подбира… |
| `explanations/day-1/architecture.md:941` | `32 ГБ` | - Минимум 4 ГБ RAM, 2 ядра, 32 ГБ диска (для боевой нагрузки подбирается по [sizing… |
| `explanations/day-2/kubernetes.md:228` | `160 GB` | …`retail-prod` с CPU quota 40 cores, Memory quota 160 GB. Нужен алерт при приближении к лимиту. |

## [PORT]  — 57 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:25` | `80` | …т». Классический пример: правило «если CPU больше 80% дольше 5 минут: алерт». |
| `explanations/day-1/architecture.md:283` | `порту 8021` | …ерфейсом мониторинга. По умолчанию открывается на порту 8021 (адрес вида `https://<кластер>:8021/cmc`). В CMC… |
| `explanations/day-1/architecture.md:283` | `8021` | …ом мониторинга. По умолчанию открывается на порту 8021 (адрес вида `https://<кластер>:8021/cmc`). В CMC… |
| `explanations/day-1/architecture.md:326` | `9999` | \| OneAgent \| Environment ActiveGate \| 9999 (по умолчанию) или 443 \| HTTPS \| Отправка данных… |
| `explanations/day-1/architecture.md:326` | `443` | …Environment ActiveGate \| 9999 (по умолчанию) или 443 \| HTTPS \| Отправка данных мониторинга \| |
| `explanations/day-1/architecture.md:327` | `443` | \| OneAgent \| Cluster (если без AG) \| 443 \| HTTPS \| Прямое подключение к кластеру \| |
| `explanations/day-1/architecture.md:328` | `443` | \| Environment ActiveGate \| Cluster ActiveGate \| 443 или 8443 \| HTTPS \| Передача данных и метаданных \| |
| `explanations/day-1/architecture.md:328` | `8443` | …ronment ActiveGate \| Cluster ActiveGate \| 443 или 8443 \| HTTPS \| Передача данных и метаданных \| |
| `explanations/day-1/architecture.md:329` | `443` | \| Браузер пользователя \| Cluster (UI) \| 443 \| HTTPS \| Веб-интерфейс \| |
| `explanations/day-1/architecture.md:330` | `8021` | \| Администратор \| CMC \| 8021 \| HTTPS \| Cluster Management Console \| |
| `explanations/day-1/architecture.md:331` | `9091` | \| Cluster ⇆ Cluster (multi-node) \| Внутри \| 9091, 9100, 9300, 7001 и др. \| TCP \| Внутрикластерная… |
| `explanations/day-1/architecture.md:331` | `9300` | …ter ⇆ Cluster (multi-node) \| Внутри \| 9091, 9100, 9300, 7001 и др. \| TCP \| Внутрикластерная синхронизаци… |
| `explanations/day-1/architecture.md:331` | `7001` | …Cluster (multi-node) \| Внутри \| 9091, 9100, 9300, 7001 и др. \| TCP \| Внутрикластерная синхронизация Cass… |
| `explanations/day-1/architecture.md:333` | `порт 443` | …ия администратора и пользователей Dynatrace UI на порт 443. Телеметрия всегда идёт исходящими соединениями:… |
| `explanations/day-1/architecture.md:333` | `443` | …министратора и пользователей Dynatrace UI на порт 443. Телеметрия всегда идёт исходящими соединениями:… |
| `explanations/day-1/architecture.md:449` | `8021` | …в Cluster Management Console (`https://<кластер>:8021/cmc`), раздел **Settings → Automatic update**. |
| `explanations/day-1/architecture.md:732` | `7000` | - Открыты внутренние порты Cassandra: 7000, 7001, 9042 |
| `explanations/day-1/architecture.md:732` | `7001` | - Открыты внутренние порты Cassandra: 7000, 7001, 9042 |
| `explanations/day-1/architecture.md:732` | `9042` | - Открыты внутренние порты Cassandra: 7000, 7001, 9042 |
| `explanations/day-1/architecture.md:733` | `9200` | - Порты Elasticsearch: 9200, 9300 |
| `explanations/day-1/architecture.md:733` | `9300` | - Порты Elasticsearch: 9200, 9300 |
| `explanations/day-1/architecture.md:734` | `8021` | - Порты Server: 8021, 8443, 9091 |
| `explanations/day-1/architecture.md:734` | `8443` | - Порты Server: 8021, 8443, 9091 |
| `explanations/day-1/architecture.md:734` | `9091` | - Порты Server: 8021, 8443, 9091 |
| `explanations/day-1/architecture.md:735` | `443` | - Порт NGINX: 443 |
| `explanations/day-1/architecture.md:785` | `8021` | Открой в браузере: `https://<DNS-имя-кластера>:8021/cmc` |
| `explanations/day-1/architecture.md:942` | `порт 443` | - Сетевая связность до Cluster (порт 443) и до мониторируемых систем |
| `explanations/day-1/architecture.md:942` | `443` | - Сетевая связность до Cluster (порт 443) и до мониторируемых систем |
| `explanations/day-1/architecture.md:1015` | `8021` | `https://<кластер>:8021/cmc` → **Cluster overview** → **Health**. |
| `explanations/day-1/architecture.md:1043` | `80` | \| Disk usage \| < 80% \| Срочно добавить диск или сократить retention \| |
| `explanations/day-1/baselines.md:38` | `80` | …министратор задаёт фиксированное число. «CPU выше 80% = аномалия». \| Требования compliance, SLA с фикс… |
| `explanations/day-1/baselines.md:168` | `80` | …ый baseline: основной инструмент, его хватает для 80% задач. Static thresholds применяются поверх адап… |
| `explanations/day-1/components.md:27` | `8021` | …Cluster Management Console** \| `https://<кластер>:8021/cmc` \| |
| `explanations/day-1/components.md:33` | `порту 8021` | …uster Management Console / CMC**: отдельный UI на порту 8021 для администрирования самого кластера. |
| `explanations/day-1/components.md:33` | `8021` | …Management Console / CMC**: отдельный UI на порту 8021 для администрирования самого кластера. |
| `explanations/day-1/components.md:255` | `8021` | 1. Открыть CMC (`https://<кластер>:8021/cmc`). |
| `explanations/day-1/components.md:296` | `443` | …верить исходящую связность с хоста до кластера на 443: `curl -vk https://<кластер>/api/v1/deployment`. |
| `explanations/day-1/components.md:302` | `порт 9999` | - Проверить, что порт 9999 открыт от хоста до шлюза. |
| `explanations/day-1/components.md:302` | `9999` | - Проверить, что порт 9999 открыт от хоста до шлюза. |
| `explanations/day-1/key-objects.md:77` | `80` | …ах видны характерные признаки: `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 ng… |
| `explanations/day-1/key-objects.md:77` | `443` | …видны характерные признаки: `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 nginx… |
| `explanations/day-1/ui-overview.md:90` | `53` | …g, Kafka, ActiveMQ Artemis, ActiveMQ Client и ещё 53 опции. |
| `explanations/day-2/kubernetes.md:230` | `80` | …etection → правило `Resource quota usage exceeded 80%`. Alerting profile `retail-ops` шлёт команде. Пр… |
| `explanations/day-2/service-cards.md:161` | `80` | …oint даёт больше всего ошибок. `/api/auth/login`: 80% ошибок. |
| `explanations/day-2/services-overview.md:58` | `80` | …ых сервисов на демо-тенанте:** `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 ng… |
| `explanations/day-2/services-overview.md:58` | `443` | …сервисов на демо-тенанте:** `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 nginx… |
| `explanations/day-2/services-overview.md:60` | `80` | …-controller deployment'а на разных портах (9024 и 80,443), Dynatrace создаёт два Service, по одному на… |
| `explanations/day-2/services-overview.md:60` | `443` | …ntroller deployment'а на разных портах (9024 и 80,443), Dynatrace создаёт два Service, по одному на каж… |
| `explanations/day-3-4/sessions.md:84` | `9200` | …тер Elasticsearch банка (URL вида `https://<host>:9200/_bulk`, NDJSON). Аутентификация: Basic auth или O… |
| `explanations/day-5/app-segments.md:46` | `порты 80` | …тают на URL вида `scheme://host:port/path?query` (порты 80/443 опускаются). Правила могут опираться на host… |
| `explanations/day-5/app-segments.md:46` | `80` | …а URL вида `scheme://host:port/path?query` (порты 80/443 опускаются). Правила могут опираться на host… |
| `explanations/day-5/app-segments.md:46` | `443` | …RL вида `scheme://host:port/path?query` (порты 80/443 опускаются). Правила могут опираться на host (дом… |
| `explanations/day-5/app-segments.md:144` | `80` | …а 1.2 сек против 800 мс в других. По провайдерам: 80% трафика через один мелкий ISP, у него пинг до да… |
| `explanations/day-5/journeys.md:104` | `80` | …ий, прошедших от шага 1 до шага 6. Типовая норма: 80-90%. Значительно ниже → сломан auth-pipeline. |
| `explanations/day-5/journeys.md:115` | `80` | …с шагом 1, дошедших до шага 6. Типовая норма: 70-80%. Падение ниже 50%: инцидент. |
| `explanations/day-5/synthetic.md:155` | `80` | - Зелёный: загрузка <80%. |
| `explanations/day-5/synthetic.md:156` | `80` | - Жёлтый: >80% или нет failover-резерва. |

## [SAMPLING_INTERVAL]  — 11 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:226` | `каждые 5 мин` | …ия действий пользователя по расписанию. Например, каждые 5 минут проверять, что страница логина в интернет-банке… |
| `explanations/day-5/alerting-logic.md:185` | `каждые 30 сек` | …рейти на **pull-model**: внутренний сервис-poller каждые 30 секунд спрашивает Dynatrace API «есть ли новые пробле… |
| `explanations/day-5/api.md:151` | `каждые 30 сек` | **Pull-модель для алертов.** Скрипт каждые 30 сек: `GET /api/v2/problems?from=now-1m&status=OPEN`,… |
| `explanations/day-5/api.md:187` | `раз в 5 мин` | …ть редко меняющиеся результаты (список сущностей: раз в 5 минут, не на каждый запрос). |
| `explanations/day-5/synthetic.md:41` | `раз в 5 мин` | …публичных или **private** локаций; периодичность: раз в 5 минут или реже. |
| `explanations/day-5/synthetic.md:198` | `каждые 5 мин` | - DNS resolution (каждые 5 минут). |
| `explanations/day-5/synthetic.md:202` | `каждые 5 мин` | - Authentication flow (каждые 5 минут). |
| `explanations/day-5/synthetic.md:207` | `каждые 15 мин` | - Login + главная (каждые 15 минут). |
| `explanations/day-5/synthetic.md:208` | `каждые 30 мин` | - Критичный end-to-end сценарий (каждые 30 минут). |
| `explanations/day-5/synthetic.md:209` | `каждые 30 мин` | - Проверка мобильного веб-интерфейса (каждые 30 минут). |
| `explanations/day-5/usql.md:212` | `каждые 5 мин` | …ос встраивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversi… |
