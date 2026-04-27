# Tech-claims inventory для dtkb-верификации

Всего: **414 claims** по **7 классам**. Сгенерировано `scripts/extract_tech_claims.py`.

Для каждого claim — проверить через `dtkb search` (fallback: `docs.dynatrace.com/managed/`). Занести в `tech_claims_verification.md` решение: **подтверждён** / **смягчён** / **удалён** с ссылкой на источник.

## [DISK_RETENTION]  — 150 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:3` | `7 дней` | …проверены `scripts/link_check.py` (HTTP 200, кэш 7 дней). При изменении источника редакция переcборки фик… |
| `explanations/day-1/architecture.md:15` | `10 дней` | …ия для Classic-стека (применимы к Managed: traces 10 дней, logs/RUM/SR/synthetic 35 дней, problems 14 месяц… |
| `explanations/day-1/architecture.md:15` | `35 дней` | …к Managed: traces 10 дней, logs/RUM/SR/synthetic 35 дней, problems 14 месяцев) |
| `explanations/day-1/architecture.md:15` | `14 месяцев` | …10 дней, logs/RUM/SR/synthetic 35 дней, problems 14 месяцев) |
| `explanations/day-1/architecture.md:26` | `5 минут` | …еский пример: правило «если CPU больше 80% дольше 5 минут — алерт». |
| `explanations/day-1/architecture.md:216` | `5 минут` | …твий пользователя по расписанию. Например, каждые 5 минут проверять, что страница логина в интернет-банке о… |
| `explanations/day-1/architecture.md:395` | `90 дней` | Хранится по умолчанию 90 дней, можно настроить дольше. В банках обычно ставят 1… |
| `explanations/day-1/architecture.md:395` | `1 год` | …й, можно настроить дольше. В банках обычно ставят 1 год + выгрузку в SIEM (Security Information and Event… |
| `explanations/day-1/architecture.md:460` | `2 месяца` | …л по очереди перезагружается. Применяются раз в 1-2 месяца. |
| `explanations/day-1/architecture.md:462` | `4 недели` | …анках обычно делают по плану, согласованному за 2–4 недели. |
| `explanations/day-1/architecture.md:466` | `1 год` | …ong Term Support) — раз в полгода, поддерживается 1 год |
| `explanations/day-1/architecture.md:475` | `4 часа` | …— если что-то пойдёт не так, восстановление за 2-4 часа. |
| `explanations/day-1/architecture.md:477` | `2 недели` | …обслуживания** с владельцами критичных систем за 2 недели. |
| `explanations/day-1/architecture.md:517` | `4 часа` | - Конфигурация — каждые 4 часа |
| `explanations/day-1/architecture.md:528` | `1 ТБ` | …ремя восстановления зависит от объёма данных: для 1 ТБ обычно 2–4 часа |
| `explanations/day-1/architecture.md:528` | `4 часа` | …ления зависит от объёма данных: для 1 ТБ обычно 2–4 часа |
| `explanations/day-1/architecture.md:530` | `4 часов` | …целевая точка отката) составляет обычно не больше 4 часов потери конфигурации и 24 часов потери метрик. При… |
| `explanations/day-1/architecture.md:530` | `24 часов` | …ет обычно не больше 4 часов потери конфигурации и 24 часов потери метрик. При наличии репликации backup на у… |
| `explanations/day-1/architecture.md:542` | `10 дней` | …Трейсы (PurePath, Distributed traces Classic)** \| 10 дней \| В SaaS через Grail — configurable 10 дней — 10… |
| `explanations/day-1/architecture.md:544` | `35 дней` | \| **Логи (Log Monitoring Classic)** \| 35 дней \| В SaaS через Grail Log Management — configurabl… |
| `explanations/day-1/architecture.md:545` | `35 дней` | \| **User sessions (RUM)** \| 35 дней \| Классический RUM. \| |
| `explanations/day-1/architecture.md:546` | `35 дней` | \| **Session Replay** \| 35 дней \| Дольше не настраивается в Classic-стеке. \| |
| `explanations/day-1/architecture.md:547` | `35 дней` | \| **Synthetic** \| 35 дней \| — \| |
| `explanations/day-1/architecture.md:548` | `14 месяцев` | \| **Davis Problems и события** \| 14 месяцев \| Сами инциденты, не сырые данные. \| |
| `explanations/day-1/architecture.md:549` | `30 дней` | \| **OneAgent diagnostics** \| 30 дней \| Диагностика агента (не метрики, а логи установк… |
| `explanations/day-1/architecture.md:724` | `4 ТБ` | …— основные данные. Минимум 500 ГБ NVMe для малых, 4 ТБ для больших |
| `explanations/day-1/architecture.md:788` | `60 минут` | …sandra и Elasticsearch с первым узлом. Время — 30-60 минут на первичную репликацию данных. |
| `explanations/day-1/architecture.md:876` | `2 недели` | …ддерживается, но обновления выходят с задержкой 1-2 недели после Linux версий. |
| `explanations/day-1/architecture.md:917` | `3 минут` | …tatus** — новый хост должен появиться в течение 2-3 минут после установки. |
| `explanations/day-1/architecture.md:1032` | `1 минут` | \| Davis compute lag \| < 1 минута \| Davis отстаёт от реального времени \| |
| `explanations/day-1/baselines.md:39` | `7 дней` | …avis AI анализирует историю метрики (по умолчанию 7 дней), строит коридор с учётом времени суток и дня нед… |
| `explanations/day-1/baselines.md:104` | `5 минут` | …PU saturation**. Порог по умолчанию 95% в течение 5 минут. Срабатывает, когда процессор забит почти полност… |
| `explanations/day-1/baselines.md:139` | `15 минут` | …ре есть проблемы-шумы: каждую ночь cron-скрипт на 15 минут забивает диск и проходит. Если каждое такое событ… |
| `explanations/day-1/baselines.md:166` | `7 дней` | **Период обучения — 7 дней.** Меняется в Reference period. По [официальной ф… |
| `explanations/day-1/baselines.md:166` | `5 дней` | …активизируются раньше — после 20% недели (около 1.5 дней). После значительного архитектурного изменения им… |
| `explanations/day-1/baselines.md:168` | `1 минут` | …тера. Цифры выше («100 мс / 50% / 0.1% / 10 rpm / 1 минута») приведены как ориентир для типичной свежей инс… |
| `explanations/day-1/components.md:16` | `30 минут` | …c updates at earliest convenience, проверка раз в 30 минут, статусы (Up to date / Update available / Update… |
| `explanations/day-1/components.md:165` | `3 часов` | **Почему окно не меньше 3 часов.** Агент начинает скачивание в границах окна, к к… |
| `explanations/day-1/components.md:167` | `1 час` | В хост-группе с десятками хостов короткое окно (1 час) физически не даёт завершить цикл. Рекомендованны… |
| `explanations/day-1/components.md:167` | `3 часа` | …не даёт завершить цикл. Рекомендованный минимум — 3 часа, оптимум 4–5. |
| `explanations/day-1/components.md:237` | `90 дней` | …Токены выпускают с ограниченным сроком (например, 90 дней) под конкретную волну развёртывания шлюзов и спок… |
| `explanations/day-1/data-explorer.md:86` | `1 минут` | - **Resolution / разрешение по времени** — Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:86` | `5 минут` | …ion / разрешение по времени** — Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:86` | `1 час` | …ешение по времени** — Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:99` | `2 часа` | - За 2 часа — шаг в одну минуту. |
| `explanations/day-1/data-explorer.md:100` | `24 часа` | - За 24 часа — шаг в 5 минут. |
| `explanations/day-1/data-explorer.md:100` | `5 минут` | - За 24 часа — шаг в 5 минут. |
| `explanations/day-1/data-explorer.md:101` | `7 дней` | - За 7 дней — шаг в 1 час. |
| `explanations/day-1/data-explorer.md:101` | `1 час` | - За 7 дней — шаг в 1 час. |
| `explanations/day-1/dem.md:16` | `35 дней` | …ессии и Session Replay в Managed Classic хранятся 35 дней (фиксированно, в SaaS Grail настраивается до 10 л… |
| `explanations/day-1/problems-feature.md:147` | `5 минут` | **Фаза 6. Закрытие.** Davis через 5 минут стабильной работы помечает проблему Closed. Jira-… |
| `explanations/day-1/smartscape.md:71` | `30 минут` | …ение появляется на карте сразу, исчезнувшее через 30 минут без активности помечается устаревшим. |
| `explanations/day-1/ui-overview.md:213` | `10 минут` | …к должен уметь без подсказки пройти по тенанту за 10 минут: |
| `explanations/day-2/containers.md:104` | `5 минут` | …build-контейнеры Jenkins / GitLab-Runner живут по 5 минут, но забивают списки. Правило: `image matches jenk… |
| `explanations/day-2/databases.md:128` | `3 недели` | …ние — по результатам наблюдения baseline первые 2-3 недели. |
| `explanations/day-2/databases.md:188` | `3 Дня` | …о идут рука об руку с проблемами хостов (Темы 1 и 3 Дня 2) и ошибками бизнес-сервисов (Темы 7-8 Дня 2). М… |
| `explanations/day-2/databases.md:188` | `8 Дня` | …ы 1 и 3 Дня 2) и ошибками бизнес-сервисов (Темы 7-8 Дня 2). Маршрут расследования: жалоба на сервис → в к… |
| `explanations/day-2/hosts-processes.md:47` | `1 Дня` | …t на этом тенанте возвращает 404 (аналогично Теме 1 Дня 2). Для работы с хостами используется типизирован… |
| `explanations/day-2/hosts-processes.md:199` | `5 минут` | - **Frequency** — каждую минуту / каждые 5 минут / каждые 10 минут. Чаще — больше данных для диагн… |
| `explanations/day-2/hosts-processes.md:199` | `10 минут` | …uency** — каждую минуту / каждые 5 минут / каждые 10 минут. Чаще — больше данных для диагностики и больше на… |
| `explanations/day-2/hosts-processes.md:201` | `7 дней` | …* — сколько дней хранятся снимки. По умолчанию до 7 дней. |
| `explanations/day-2/hosts-processes.md:229` | `15 минут` | …Процесс прогрева кэша стартует в 02:00, работает 15 минут, корректно завершается. Dynatrace каждую ночь соз… |
| `explanations/day-2/hosts-processes.md:231` | `20 минут` | …on — не создавать Problem, если отсутствие меньше 20 минут. Ложный алерт исчезает. |
| `explanations/day-2/hosts-processes.md:269` | `7 дней` | …я Process Group — новая модель Davis AI. Ей нужно 7 дней истории для baseline. Если плохие правила создают… |
| `explanations/day-2/kubernetes.md:148` | `3 Дня` | …но мониторить и обычными Host-правилами (Темы 1 и 3 Дня 2). Но K8s-специфичные правила ловят K8s-события,… |
| `explanations/day-2/kubernetes.md:210` | `15 минут` | 6. Через 10-15 минут кластер появляется в интерфейсе со всеми ресурсам… |
| `explanations/day-2/oneagent-infra.md:92` | `5 минут` | - RAID-массив в состоянии degraded более 5 минут → Problem. |
| `explanations/day-2/oneagent-infra.md:153` | `10 дней` | …ic** — полные детали каждой транзакции хранятся **10 дней** (после 10 дней детализация падает, остаются агр… |
| `explanations/day-2/oneagent-infra.md:154` | `35 дней` | …ие метрик сервиса для multidimensional-анализа: **35 дней**. Гранулярность зависит от timeframe (от 10 секу… |
| `explanations/day-2/oneagent-infra.md:154` | `20 минут` | …лярность зависит от timeframe (от 10 секунд для < 20 минут до 1 минуты для > 1 часа). |
| `explanations/day-2/oneagent-infra.md:154` | `1 минут` | …исит от timeframe (от 10 секунд для < 20 минут до 1 минуты для > 1 часа). |
| `explanations/day-2/oneagent-infra.md:154` | `1 часа` | …me (от 10 секунд для < 20 минут до 1 минуты для > 1 часа). |
| `explanations/day-2/oneagent-infra.md:155` | `35 дней` | …ions / Session Replay / mobile crashes — все по **35 дней**. |
| `explanations/day-2/oneagent-infra.md:157` | `14 дней` | …теншн до **5 лет**. Гранулярность по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1… |
| `explanations/day-2/oneagent-infra.md:157` | `1 минут` | …*5 лет**. Гранулярность по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400… |
| `explanations/day-2/oneagent-infra.md:157` | `28 дней` | …нулярность по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней–5 лет →… |
| `explanations/day-2/oneagent-infra.md:157` | `5 минут` | …по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней–5 лет → 1 день. |
| `explanations/day-2/oneagent-infra.md:157` | `400 дней` | …e: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней–5 лет → 1 день. |
| `explanations/day-2/oneagent-infra.md:157` | `1 час` | …й → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней–5 лет → 1 день. |
| `explanations/day-2/os-monitoring.md:129` | `10 ТБ` | *Типовой случай.* Диск под бэкапы СУБД, 10 ТБ. Бэкапы пишутся пачками и занимают 60-70% диска.… |
| `explanations/day-2/problems-navigation.md:53` | `10 минут` | …ravelService`. Началась 21 апреля в 11:11, длится 10 минут. Вторая — `Postgres Availability P-26049003`, Aff… |
| `explanations/day-2/problems-navigation.md:53` | `16 минут` | …wsqmnv8.us-east-1.rds.amazonaws.com:5432`, длится 16 минут. Каждая запись — потенциальная точка входа в расс… |
| `explanations/day-2/service-cards.md:66` | `24 часа` | …hours — Dynatrace показывает метрики за последние 24 часа и параллельно сравнивает с предыдущими 24 часами… |
| `explanations/day-2/service-cards.md:122` | `30 дней` | …lability `/api/auth/login` должна быть ≥ 99.9% за 30 дней». Для измерения нужна метрика именно этого endpoi… |
| `explanations/day-2/service-cards.md:160` | `10 минут` | …ilure rate за последний час — пик 5% в конкретные 10 минут. |
| `explanations/day-2/service-cards.md:173` | `20 минут` | …й от timeframe запроса (10 секунд для timeframe < 20 минут, до 1 минуты для timeframe > 1 часа), и хранится… |
| `explanations/day-2/service-cards.md:173` | `1 минут` | …e запроса (10 секунд для timeframe < 20 минут, до 1 минуты для timeframe > 1 часа), и хранится 35 дней. Дол… |
| `explanations/day-2/service-cards.md:173` | `1 часа` | …timeframe < 20 минут, до 1 минуты для timeframe > 1 часа), и хранится 35 дней. Долгосрочно метрика идёт та… |
| `explanations/day-2/service-cards.md:173` | `35 дней` | …, до 1 минуты для timeframe > 1 часа), и хранится 35 дней. Долгосрочно метрика идёт также в Metrics Classic… |
| `explanations/day-2/service-cards.md:197` | `2 часа` | *Нюанс — сезонность.* Сравнение с «2 часа назад» может обманывать: если переход между пиком… |
| `explanations/day-2/service-cards.md:197` | `7 дня` | …imeframe `same time last week` сравнивает ровно с 7 днями назад — часто даёт более осмысленную картину дл… |
| `explanations/day-2/service-cards.md:203` | `14 дней` | …ятся до **5 лет** с прореживанием по timeframe (0–14 дней — 1-минутная гранулярность, 14–28 дней — 5 минут,… |
| `explanations/day-2/service-cards.md:203` | `28 дней` | …meframe (0–14 дней — 1-минутная гранулярность, 14–28 дней — 5 минут, 28–400 дней — 1 час, 400 дней–5 лет —… |
| `explanations/day-2/service-cards.md:203` | `5 минут` | …–14 дней — 1-минутная гранулярность, 14–28 дней — 5 минут, 28–400 дней — 1 час, 400 дней–5 лет — 1 день). Д… |
| `explanations/day-2/service-cards.md:203` | `400 дней` | …-минутная гранулярность, 14–28 дней — 5 минут, 28–400 дней — 1 час, 400 дней–5 лет — 1 день). Для request at… |
| `explanations/day-2/service-cards.md:203` | `1 час` | …ранулярность, 14–28 дней — 5 минут, 28–400 дней — 1 час, 400 дней–5 лет — 1 день). Для request attributes… |
| `explanations/day-2/service-cards.md:203` | `35 дней` | …1 день). Для request attributes / services data — 35 дней с переменной гранулярностью; PurePath-детализация… |
| `explanations/day-2/service-cards.md:203` | `10 дней` | …переменной гранулярностью; PurePath-детализация — 10 дней. Точные параметры подтверждены в [Data retention… |
| `explanations/day-2/services-overview.md:162` | `2 недель` | 4. После 1-2 недель стабильной работы — обновить prod-агенты постепен… |
| `explanations/day-3-4/appsec.md:138` | `4 недели` | *Типовая политика.* Сначала Monitor на 2-4 недели, затем Block для критичных endpoint'ов (платежи,… |
| `explanations/day-3-4/incident-lifecycle.md:119` | `5 минут` | …op → немедленное уведомление. Slowdown → задержка 5 минут, чтобы отделить шум. |
| `explanations/day-3-4/instrumentation.md:79` | `14 дней` | *Типовая политика.* Delayed на 7-14 дней. Даёт Dynatrace время выловить ранние баги у друг… |
| `explanations/day-3-4/mlt-concepts.md:122` | `1 час` | …колько дней, дальше прореживание (1 мин → 5 мин → 1 час → 1 день). По умолчанию 13 месяцев, настраивается… |
| `explanations/day-3-4/mlt-concepts.md:122` | `13 месяцев` | …ие (1 мин → 5 мин → 1 час → 1 день). По умолчанию 13 месяцев, настраивается. |
| `explanations/day-3-4/mlt-concepts.md:123` | `7 дней` | …Срок зависит от объёма и лицензии. По умолчанию 5-7 дней, часто поднимают до 30. |
| `explanations/day-3-4/mlt-concepts.md:124` | `35 дней` | …Cassandra с индексами для быстрого поиска. Обычно 35 дней для полных PurePath. Долгосрочные агрегаты (Throu… |
| `explanations/day-3-4/reliability-config.md:69` | `10 минут` | …нул 15 downstream сервисов, был triggered деплоем 10 минут назад». |
| `explanations/day-3-4/response-analysis.md:91` | `15 минут` | 3. Через 10-15 минут Failure rate падает до реального уровня (0.1-0.5%… |
| `explanations/day-3-4/response-analysis.md:130` | `2 недели` | …нкая настройка после первичного деплоя занимает 1-2 недели. По каждому критичному сервису — корректировка ru… |
| `explanations/day-3-4/service-flow.md:78` | `2 часа` | …оретически может ходить в 10 баз, но за последние 2 часа ходил только в 3, в Service Flow будут только 3.… |
| `explanations/day-3-4/service-object.md:65` | `7 Дня` | **Отличие от Service Detection rules (Тема 7 Дня 2):** |
| `explanations/day-3-4/sli-slo-sla.md:18` | `30 дней` | …значение SLI за период \| Availability ≥ 99.9% за 30 дней \| |
| `explanations/day-3-4/sli-slo-sla.md:94` | `30 дней` | *Пример расчёта.* Target = 99.9% за 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты*… |
| `explanations/day-3-4/sli-slo-sla.md:94` | `2 минут` | …а 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты** даунтайма в месяц. |
| `explanations/day-3-4/sli-slo-sla.md:96` | `40 минут` | *Как используется.* Если в начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки… |
| `explanations/day-3-4/sli-slo-sla.md:96` | `2 минут` | …чале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки **замораживает выкатки** ри… |
| `explanations/day-3-4/thresholds.md:82` | `15 минут` | *Типовой порог.* Crash rate > 1% за 15 минут → Problem. Для сравнения: Google Play считает пло… |
| `explanations/day-5/alerting-logic.md:158` | `10 минут` | …елать escalation («если никто не взял в работу за 10 минут — эскалировать уровень выше»). Это делают специал… |
| `explanations/day-5/alerting-profiles.md:59` | `10 минут` | …. Полезно для plan-release, когда в ходе деплоя 5-10 минут «хаоса» — норма. |
| `explanations/day-5/alerting-profiles.md:95` | `3 минут` | …олько времени должно держаться условие (например, 3 минуты). |
| `explanations/day-5/alerting-profiles.md:132` | `7 дней` | …ное значение) для каждой метрики автоматически за 7 дней. |
| `explanations/day-5/alerting-profiles.md:159` | `3 часа` | - PagerDuty триггерит в 3 часа ночи 4 раза за месяц — на пятый телефон выключен. |
| `explanations/day-5/alerting-profiles.md:166` | `5 минут` | - **Delay.** 3-5 минут перед первым уведомлением. Проблема «мигнула и уш… |
| `explanations/day-5/api.md:38` | `30 дней` | 2. Срок действия — 1 день / 30 дней / 1 год / unlimited. Для production обычно 1 год… |
| `explanations/day-5/api.md:38` | `1 год` | 2. Срок действия — 1 день / 30 дней / 1 год / unlimited. Для production обычно 1 год с напоми… |
| `explanations/day-5/api.md:62` | `90 дней` | …n** — максимальный срок действия. Если политика = 90 дней, пользователь не может создать токен «на 1 год».… |
| `explanations/day-5/api.md:62` | `1 год` | …90 дней, пользователь не может создать токен «на 1 год». Реализация требования «регулярная ротация секре… |
| `explanations/day-5/api.md:160` | `90 дней` | - **Expiration date.** Всегда. Ротировать каждые 90 дней по политике безопасности. |
| `explanations/day-5/api.md:173` | `5 минут` | …о меняющиеся результаты (список сущностей — раз в 5 минут, не на каждый запрос). |
| `explanations/day-5/journeys.md:118` | `4 час` | На шаге 4 часто отваливаются. Dynatrace помогает отличить ожида… |
| `explanations/day-5/journeys.md:118` | `2 минут` | …Dynatrace помогает отличить ожидаемое поведение (2 минуты листания условий) от проблемы (2 минуты тапов по… |
| `explanations/day-5/rum.md:143` | `30 минут` | …умолчанию session завершается, если пользователь 30 минут неактивен (inactivity timeout). Новая session с т… |
| `explanations/day-5/rum.md:160` | `2026 год` | …ческий (stable в Managed) и новый (SaaS-first). В 2026 году Managed ещё полностью не мигрировал на Apps-моде… |
| `explanations/day-5/session-replay.md:87` | `1 TB` | …длительности. При 500 000 сессий в день это около 1 TB в день только на Session Replay. Поэтому Session… |
| `explanations/day-5/session-replay.md:174` | `1 час` | …**Максимальная длина записанной сессии** — обычно 1 час (настраивается). |
| `explanations/day-5/synthetic.md:116` | `1 минут` | - Частота: от 1 минуты до 60 минут. |
| `explanations/day-5/synthetic.md:116` | `60 минут` | - Частота: от 1 минуты до 60 минут. |
| `explanations/day-5/synthetic.md:124` | `5 минут` | - Частота: от 5 минут до 60 минут (дороже HTTP, ресурсы браузера). |
| `explanations/day-5/synthetic.md:124` | `60 минут` | - Частота: от 5 минут до 60 минут (дороже HTTP, ресурсы браузера). |
| `explanations/day-5/synthetic.md:174` | `5 минут` | - DNS resolution (каждые 5 минут). |
| `explanations/day-5/synthetic.md:178` | `5 минут` | - Authentication flow (каждые 5 минут). |
| `explanations/day-5/synthetic.md:183` | `15 минут` | - Login + главная (каждые 15 минут). |
| `explanations/day-5/synthetic.md:184` | `30 минут` | - Критичный end-to-end сценарий (каждые 30 минут). |
| `explanations/day-5/synthetic.md:185` | `30 минут` | - Проверка мобильного веб-интерфейса (каждые 30 минут). |
| `explanations/day-5/usql.md:82` | `2016 год` | …льским сессиям и user actions. Создан Dynatrace в 2016 году, когда формировалась RUM-функциональность. |
| `explanations/day-5/usql.md:114` | `2022 год` | DQL — новый язык, появившийся в 2022 году для работы с **Grail**, облачным хранилищем Dyna… |
| `explanations/day-5/usql.md:181` | `5 минут` | …аивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversion… |
| `explanations/day-5/usql.md:190` | `35 дней` | …срочные тренды.** По умолчанию USQL держит данные 35 дней. Старше — нет. Для долгосрочного хранения — экспо… |
| `explanations/day-5/ux-metrics.md:101` | `2004 год` | Apdex разработан в 2004 году консорциумом Apdex Alliance (Compuware, HP, Merc… |
| `explanations/day-5/ux-metrics.md:161` | `5 минут` | …*Performance.** Apdex ≥ 0.85 на 95% интервалов по 5 минут. |

## [DYNATRACE_VERSION]  — 9 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:353` | `1.260` | …ове OAuth 2.0. Поддерживается с Dynatrace Managed 1.260+. |
| `explanations/day-1/architecture.md:458` | `1.270.10` | …равления внутри одной минорной версии (например, `1.270.10 → 1.270.11`). Применяются без перезагрузки класте… |
| `explanations/day-1/architecture.md:458` | `1.270.11` | …утри одной минорной версии (например, `1.270.10 → 1.270.11`). Применяются без перезагрузки кластера, без дау… |
| `explanations/day-1/architecture.md:460` | `1.270` | …Minor updates.** Обновления внутри major-версии (`1.270 → 1.271`). Обычно требуют rolling restart узлов —… |
| `explanations/day-1/architecture.md:460` | `1.271` | …dates.** Обновления внутри major-версии (`1.270 → 1.271`). Обычно требуют rolling restart узлов — кластер… |
| `explanations/day-1/architecture.md:462` | `1.260` | **Major upgrades.** Большие обновления (`1.260 → 1.270`). Раз в полгода. Требуют полного просмот… |
| `explanations/day-1/architecture.md:462` | `1.270` | **Major upgrades.** Большие обновления (`1.260 → 1.270`). Раз в полгода. Требуют полного просмотра relea… |
| `explanations/day-1/smartscape.md:43` | `1.336.55` | …ификатор окружения `guu84124` и версия платформы `1.336.55.20260417-205630`. |
| `explanations/day-2/os-monitoring.md:53` | `1.336.55` | …e old and no longer available`. Версия платформы `1.336.55.20260417-205630`. Универсальный entity list замен… |

## [LATENCY]  — 147 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:26` | `5 минут` | …еский пример: правило «если CPU больше 80% дольше 5 минут — алерт». |
| `explanations/day-1/architecture.md:216` | `5 минут` | …твий пользователя по расписанию. Например, каждые 5 минут проверять, что страница логина в интернет-банке о… |
| `explanations/day-1/architecture.md:216` | `2 секунды` | …о страница логина в интернет-банке открывается за 2 секунды. Эти проверки запускаются с ActiveGate, потому чт… |
| `explanations/day-1/architecture.md:306` | `15 секунд` | …т события до отображения в интерфейсе:** обычно 5–15 секунд. OneAgent отправляет данные не каждое событие отд… |
| `explanations/day-1/architecture.md:306` | `10 секунд` | …нные не каждое событие отдельно, а пакетами раз в 10 секунд (это называется **batch-передача** — от англ. *ba… |
| `explanations/day-1/architecture.md:506` | `10 ms` | …х дата-центрах с low-latency связью между ними (< 10 ms ping). |
| `explanations/day-1/architecture.md:574` | `10 мс` | - **Сетевая задержка между узлами — максимум 10 мс** (не только пропускная способность). |
| `explanations/day-1/architecture.md:706` | `10 мс` | …ть между узлами по 10 Гбит/с (сеть между узлами: ≤10 мс задержка, см. `docs.dynatrace.com/managed/managed… |
| `explanations/day-1/architecture.md:788` | `60 минут` | …sandra и Elasticsearch с первым узлом. Время — 30-60 минут на первичную репликацию данных. |
| `explanations/day-1/architecture.md:917` | `3 минут` | …tatus** — новый хост должен появиться в течение 2-3 минут после установки. |
| `explanations/day-1/architecture.md:1032` | `1 минута` | \| Davis compute lag \| < 1 минута \| Davis отстаёт от реального времени \| |
| `explanations/day-1/baselines.md:62` | `100 мс` | …ute threshold / абсолютный порог** — по умолчанию 100 мс. |
| `explanations/day-1/baselines.md:64` | `1000 мс` | …лучаи — крупные отчёты, большие выборки. Absolute 1000 мс, Relative 50% по умолчанию. |
| `explanations/day-1/baselines.md:104` | `5 минут` | …PU saturation**. Порог по умолчанию 95% в течение 5 минут. Срабатывает, когда процессор забит почти полност… |
| `explanations/day-1/baselines.md:139` | `15 минут` | …ре есть проблемы-шумы: каждую ночь cron-скрипт на 15 минут забивает диск и проходит. Если каждое такое событ… |
| `explanations/day-1/baselines.md:160` | `500 мс` | …оринга с общим порогом «алерт, если отклик больше 500 мс». Такой порог не имеет смысла для сервиса со сред… |
| `explanations/day-1/baselines.md:160` | `50 мс` | …г не имеет смысла для сервиса со средним откликом 50 мс (всегда норма) и одновременно не имеет смысла для… |
| `explanations/day-1/baselines.md:160` | `2000 мс` | …о не имеет смысла для сервиса со средним откликом 2000 мс (всегда аномалия). |
| `explanations/day-1/baselines.md:162` | `50 мс` | …чью почти нулевая. Если сервис обычно отвечает за 50 мс утром и 120 мс в пик-часы, для Davis это два разн… |
| `explanations/day-1/baselines.md:162` | `120 мс` | …вая. Если сервис обычно отвечает за 50 мс утром и 120 мс в пик-часы, для Davis это два разных эталона — ве… |
| `explanations/day-1/baselines.md:168` | `100 мс` | …tive для конкретной сборки кластера. Цифры выше («100 мс / 50% / 0.1% / 10 rpm / 1 минута») приведены как… |
| `explanations/day-1/baselines.md:168` | `1 минута` | …тера. Цифры выше («100 мс / 50% / 0.1% / 10 rpm / 1 минута») приведены как ориентир для типичной свежей инст… |
| `explanations/day-1/components.md:16` | `30 минут` | …c updates at earliest convenience, проверка раз в 30 минут, статусы (Up to date / Update available / Update… |
| `explanations/day-1/components.md:267` | `30 секунд` | …ssandra, Elasticsearch). UI может «мигнуть» на 10–30 секунд, данные не теряются — они буферизуются в ActiveGa… |
| `explanations/day-1/data-explorer.md:86` | `1 минута` | - **Resolution / разрешение по времени** — Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:86` | `5 минут` | …ion / разрешение по времени** — Auto / 1 минута / 5 минут / 1 час. |
| `explanations/day-1/data-explorer.md:100` | `5 минут` | - За 24 часа — шаг в 5 минут. |
| `explanations/day-1/key-objects.md:87` | `120 мс` | …ько отвечает сервис платежей» — медиана, например 120 мс. «Как у самых медленных клиентов» — 90-й перценти… |
| `explanations/day-1/key-objects.md:87` | `450 мс` | …х медленных клиентов» — 90-й перцентиль, например 450 мс. |
| `explanations/day-1/problems-feature.md:135` | `120 мс` | …диана времени отклика `payment-service` растёт со 120 мс до 800 мс. [Davis AI](https://docs.dynatrace.com/… |
| `explanations/day-1/problems-feature.md:135` | `800 мс` | …ени отклика `payment-service` растёт со 120 мс до 800 мс. [Davis AI](https://docs.dynatrace.com/docs/disco… |
| `explanations/day-1/problems-feature.md:147` | `5 минут` | **Фаза 6. Закрытие.** Davis через 5 минут стабильной работы помечает проблему Closed. Jira-… |
| `explanations/day-1/smartscape.md:71` | `30 минут` | …ение появляется на карте сразу, исчезнувшее через 30 минут без активности помечается устаревшим. |
| `explanations/day-1/ui-overview.md:213` | `10 минут` | …к должен уметь без подсказки пройти по тенанту за 10 минут: |
| `explanations/day-2/containers.md:104` | `5 минут` | …build-контейнеры Jenkins / GitLab-Runner живут по 5 минут, но забивают списки. Правило: `image matches jenk… |
| `explanations/day-2/databases.md:74` | `2.09 ms` | …ые показатели `TradeManagement` на демо: медиана `2.09 ms`, Slowest 10% `10.1 ms`, 0% ошибок, 248 запросов… |
| `explanations/day-2/databases.md:74` | `10.1 ms` | …agement` на демо: медиана `2.09 ms`, Slowest 10% `10.1 ms`, 0% ошибок, 248 запросов в минуту. |
| `explanations/day-2/databases.md:112` | `1000 мс` | …жет быть десятки миллисекунд даже в норме. Дефолт 1000 мс будет срабатывать слишком часто. |
| `explanations/day-2/databases.md:128` | `1000 мс` | …орог Slowest 10% часто нужно поднять выше дефолта 1000 мс. Oracle под нагрузкой может естественно давать де… |
| `explanations/day-2/databases.md:153` | `1 мс` | …ть — микросекунды, обычные запросы укладываются в 1 мс. |
| `explanations/day-2/databases.md:176` | `60 секунд` | …апрос вызывается раз в час, занимает минуту — это 60 секунд в час. Сто запросов вызываются раз в секунду, зан… |
| `explanations/day-2/databases.md:176` | `100 мс` | …. Сто запросов вызываются раз в секунду, занимают 100 мс — тоже 60 секунд в час. Оба одинаково нагружают Б… |
| `explanations/day-2/hosts-processes.md:181` | `60 секунд` | …ило: не создавать Problem, если отсутствие меньше 60 секунд. |
| `explanations/day-2/hosts-processes.md:199` | `5 минут` | - **Frequency** — каждую минуту / каждые 5 минут / каждые 10 минут. Чаще — больше данных для диагн… |
| `explanations/day-2/hosts-processes.md:199` | `10 минут` | …uency** — каждую минуту / каждые 5 минут / каждые 10 минут. Чаще — больше данных для диагностики и больше на… |
| `explanations/day-2/hosts-processes.md:229` | `15 минут` | …Процесс прогрева кэша стартует в 02:00, работает 15 минут, корректно завершается. Dynatrace каждую ночь соз… |
| `explanations/day-2/hosts-processes.md:231` | `20 минут` | …on — не создавать Problem, если отсутствие меньше 20 минут. Ложный алерт исчезает. |
| `explanations/day-2/kubernetes.md:210` | `15 минут` | 6. Через 10-15 минут кластер появляется в интерфейсе со всеми ресурсам… |
| `explanations/day-2/oneagent-infra.md:92` | `5 минут` | - RAID-массив в состоянии degraded более 5 минут → Problem. |
| `explanations/day-2/oneagent-infra.md:112` | `10 секунд` | …выполняться чаще (для отдельных метрик хоста — до 10 секунд), но в Data Explorer и в metric events точки с ин… |
| `explanations/day-2/oneagent-infra.md:154` | `10 секунд` | …35 дней**. Гранулярность зависит от timeframe (от 10 секунд для < 20 минут до 1 минуты для > 1 часа). |
| `explanations/day-2/oneagent-infra.md:154` | `20 минут` | …лярность зависит от timeframe (от 10 секунд для < 20 минут до 1 минуты для > 1 часа). |
| `explanations/day-2/oneagent-infra.md:154` | `1 минуты` | …исит от timeframe (от 10 секунд для < 20 минут до 1 минуты для > 1 часа). |
| `explanations/day-2/oneagent-infra.md:157` | `1 минута` | …*5 лет**. Гранулярность по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 д… |
| `explanations/day-2/oneagent-infra.md:157` | `5 минут` | …по timeframe: 0–14 дней → 1 минута, 14–28 дней → 5 минут, 28–400 дней → 1 час, 400 дней–5 лет → 1 день. |
| `explanations/day-2/os-monitoring.md:116` | `10 секунд` | …я для целей anomaly detection может идти чаще (до 10 секунд для отдельных метрик), но это не меняет интервал… |
| `explanations/day-2/problems-navigation.md:53` | `10 минут` | …ravelService`. Началась 21 апреля в 11:11, длится 10 минут. Вторая — `Postgres Availability P-26049003`, Aff… |
| `explanations/day-2/problems-navigation.md:53` | `16 минут` | …wsqmnv8.us-east-1.rds.amazonaws.com:5432`, длится 16 минут. Каждая запись — потенциальная точка входа в расс… |
| `explanations/day-2/service-cards.md:79` | `800 мс` | …я поиска bottleneck. *Пример вывода:* общее время 800 мс, из них 620 мс — один SQL-запрос в БД X. Дальше —… |
| `explanations/day-2/service-cards.md:79` | `620 мс` | …neck. *Пример вывода:* общее время 800 мс, из них 620 мс — один SQL-запрос в БД X. Дальше — SQL оптимизиро… |
| `explanations/day-2/service-cards.md:134` | `120 мс` | 1. Overview → Response time вырос с 120 мс до 450 мс за последний час. |
| `explanations/day-2/service-cards.md:134` | `450 мс` | 1. Overview → Response time вырос с 120 мс до 450 мс за последний час. |
| `explanations/day-2/service-cards.md:136` | `150 мс` | …амедлился больше всех. `/api/payment/process` — с 150 мс до 600 мс. |
| `explanations/day-2/service-cards.md:136` | `600 мс` | …больше всех. `/api/payment/process` — с 150 мс до 600 мс. |
| `explanations/day-2/service-cards.md:137` | `500 мс` | 4. Открываем endpoint → PurePath waterfall → 500 мс — это один SQL-запрос к БД `account-db`. |
| `explanations/day-2/service-cards.md:149` | `45 мс` | 3. Response time — медиана выросла с 30 до 45 мс. Приемлемо. |
| `explanations/day-2/service-cards.md:160` | `10 минут` | …ilure rate за последний час — пик 5% в конкретные 10 минут. |
| `explanations/day-2/service-cards.md:173` | `10 секунд` | …с гранулярностью, зависящей от timeframe запроса (10 секунд для timeframe < 20 минут, до 1 минуты для timefra… |
| `explanations/day-2/service-cards.md:173` | `20 минут` | …й от timeframe запроса (10 секунд для timeframe < 20 минут, до 1 минуты для timeframe > 1 часа), и хранится… |
| `explanations/day-2/service-cards.md:173` | `1 минуты` | …e запроса (10 секунд для timeframe < 20 минут, до 1 минуты для timeframe > 1 часа), и хранится 35 дней. Долг… |
| `explanations/day-2/service-cards.md:203` | `5 минут` | …–14 дней — 1-минутная гранулярность, 14–28 дней — 5 минут, 28–400 дней — 1 час, 400 дней–5 лет — 1 день). Д… |
| `explanations/day-2/services-overview.md:171` | `100 мс` | …нде — «все Database service со временем отклика > 100 мс». Kafka-команде — «все Messaging service с отстав… |
| `explanations/day-3-4/app-cards.md:83` | `2 секунды` | 1. **Performance** (page load, LCP) — 2 секунды. Не супер медленно. |
| `explanations/day-3-4/incident-lifecycle.md:119` | `5 минут` | …op → немедленное уведомление. Slowdown → задержка 5 минут, чтобы отделить шум. |
| `explanations/day-3-4/mlt-concepts.md:78` | `5 секунд` | …пользования.* Жалоба «оформление платежа занимает 5 секунд». Без трейсов инженер видит только «клиент ждал 5… |
| `explanations/day-3-4/mlt-concepts.md:78` | `500 мс` | …нер видит только «клиент ждал 5 сек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (о… |
| `explanations/day-3-4/mlt-concepts.md:78` | `200 мс` | …«клиент ждал 5 сек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (ожидание LDAP), 13… |
| `explanations/day-3-4/mlt-concepts.md:78` | `3000 мс` | …ек». С PurePath: 500 мс frontend, 200 мс gateway, 3000 мс auth-service (ожидание LDAP), 1300 мс payment-ser… |
| `explanations/day-3-4/mlt-concepts.md:78` | `1300 мс` | …мс gateway, 3000 мс auth-service (ожидание LDAP), 1300 мс payment-service. Корень — медленный LDAP. Без руч… |
| `explanations/day-3-4/mlt-concepts.md:89` | `500 мс` | …ime растёт. В Data Explorer — одна общая линия до 500 мс. Вопрос: равномерно по всем клиентам или только у… |
| `explanations/day-3-4/reliability-config.md:69` | `10 минут` | …нул 15 downstream сервисов, был triggered деплоем 10 минут назад». |
| `explanations/day-3-4/response-analysis.md:91` | `15 минут` | 3. Через 10-15 минут Failure rate падает до реального уровня (0.1-0.5%… |
| `explanations/day-3-4/response-analysis.md:103` | `5000 мс` | …го карточке — поднять порог Slowest 10% с 1000 до 5000 мс. Для dev допустимо. |
| `explanations/day-3-4/response-analysis.md:111` | `100 мс` | …seline (history-based). Если Response time обычно 100 мс, а сейчас 400 мс — аномалия, даже если все 400 мс… |
| `explanations/day-3-4/response-analysis.md:111` | `400 мс` | …ased). Если Response time обычно 100 мс, а сейчас 400 мс — аномалия, даже если все 400 мс запросов успешны… |
| `explanations/day-3-4/service-flow.md:54` | `2000 мс` | …бро от сервиса к БД `accounts-db`. Медиана вызова 2000 мс. Остальные рёбра зелёные. Корень — БД, а не сам с… |
| `explanations/day-3-4/sli-slo-sla.md:80` | `3 секунд` | \| Платёжный сервис \| % успешных платежей < 3 секунд \| |
| `explanations/day-3-4/sli-slo-sla.md:82` | `500 мс` | \| Карточный процессинг \| Доля транзакций < 500 мс \| |
| `explanations/day-3-4/sli-slo-sla.md:94` | `43.2 минуты` | …% за 30 дней → допустимо 30 × 24 × 60 × 0.001 = **43.2 минуты** даунтайма в месяц. |
| `explanations/day-3-4/sli-slo-sla.md:96` | `40 минут` | *Как используется.* Если в начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки… |
| `explanations/day-3-4/sli-slo-sla.md:96` | `3.2 минуты` | …начале месяца уже было 40 минут даунтайма (budget 3.2 минуты), команда разработки **замораживает выкатки** рис… |
| `explanations/day-3-4/thresholds.md:50` | `3 секунды` | …жения = потеря клиента. Типовые пороги строгие: 2-3 секунды медиана, 5-7 секунд P95. |
| `explanations/day-3-4/thresholds.md:50` | `7 секунд` | …а. Типовые пороги строгие: 2-3 секунды медиана, 5-7 секунд P95. |
| `explanations/day-3-4/thresholds.md:82` | `15 минут` | *Типовой порог.* Crash rate > 1% за 15 минут → Problem. Для сравнения: Google Play считает пло… |
| `explanations/day-3-4/thresholds.md:106` | `200 мс` | Медиана времени загрузки может быть хорошей (200 мс), но **хвост распределения** (P99) — ужасным (5 с… |
| `explanations/day-3-4/thresholds.md:106` | `5 секунд` | …мс), но **хвост распределения** (P99) — ужасным (5 секунд). Это реальные пользователи с плохой сетью или ст… |
| `explanations/day-5/alerting-logic.md:158` | `10 минут` | …елать escalation («если никто не взял в работу за 10 минут — эскалировать уровень выше»). Это делают специал… |
| `explanations/day-5/alerting-logic.md:192` | `30 секунд` | …**pull-model** — внутренний сервис-poller каждые 30 секунд спрашивает Dynatrace API «есть ли новые проблемы»… |
| `explanations/day-5/alerting-profiles.md:59` | `10 минут` | …. Полезно для plan-release, когда в ходе деплоя 5-10 минут «хаоса» — норма. |
| `explanations/day-5/alerting-profiles.md:95` | `3 минуты` | …олько времени должно держаться условие (например, 3 минуты). |
| `explanations/day-5/alerting-profiles.md:166` | `5 минут` | - **Delay.** 3-5 минут перед первым уведомлением. Проблема «мигнула и уш… |
| `explanations/day-5/alerting-profiles.md:166` | `90 секунд` | …первым уведомлением. Проблема «мигнула и ушла» за 90 секунд — не тревожить дежурного. |
| `explanations/day-5/api.md:173` | `5 минут` | …о меняющиеся результаты (список сущностей — раз в 5 минут, не на каждый запрос). |
| `explanations/day-5/app-segments.md:92` | `500 мс` | …загрузки — норма, для торговой платформы критично 500 мс. Одним Apdex не мониторить. |
| `explanations/day-5/app-segments.md:124` | `800 мс` | …ом регионе».** По региону: медиана 1.2 сек против 800 мс в других. По провайдерам: 80% трафика через один… |
| `explanations/day-5/app-segments.md:124` | `250 мс` | …через один мелкий ISP, у него пинг до дата-центра 250 мс против 60 мс у крупного. Решение — переговоры с I… |
| `explanations/day-5/app-segments.md:124` | `60 мс` | …кий ISP, у него пинг до дата-центра 250 мс против 60 мс у крупного. Решение — переговоры с ISP или CDN. |
| `explanations/day-5/app-segments.md:128` | `300 мс` | …делают deep packet inspection для SSL — добавляет 300 мс. Решение — мониторить SSL handshake time отдельно… |
| `explanations/day-5/journeys.md:118` | `2 минуты` | …Dynatrace помогает отличить ожидаемое поведение (2 минуты листания условий) от проблемы (2 минуты тапов по… |
| `explanations/day-5/rum.md:117` | `15 мс` | …аемость. Серверный агент видит: «запрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользовате… |
| `explanations/day-5/rum.md:117` | `20 мс` | …ент видит: «запрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, п… |
| `explanations/day-5/rum.md:117` | `35 мс` | …апрос пришёл за 15 мс, ответ ушёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, потому что: |
| `explanations/day-5/rum.md:117` | `730 мс` | …ёл за 20 мс, итого 35 мс». Но пользователь ждёт **730 мс**, потому что: |
| `explanations/day-5/rum.md:119` | `200 мс` | - 200 мс запрос шёл до дата-центра (мобильный интернет, пл… |
| `explanations/day-5/rum.md:120` | `35 мс` | - 35 мс обрабатывал сервер. |
| `explanations/day-5/rum.md:121` | `250 мс` | - 250 мс ответ шёл обратно. |
| `explanations/day-5/rum.md:122` | `245 мс` | - 245 мс браузер парсил HTML, исполнял JavaScript, рендери… |
| `explanations/day-5/rum.md:124` | `35 мс` | Без RUM видно только 35 мс. С RUM — все 730 с разбивкой на каждый этап. |
| `explanations/day-5/rum.md:143` | `30 минут` | …умолчанию session завершается, если пользователь 30 минут неактивен (inactivity timeout). Новая session с т… |
| `explanations/day-5/rum.md:150` | `3 секунды` | - **Satisfied** — время < T (например, 3 секунды для веб-страницы). |
| `explanations/day-5/session-replay.md:108` | `250 мс` | 2. **Incremental diff** каждые 250 мс — что изменилось в DOM. |
| `explanations/day-5/synthetic.md:30` | `2 секунды` | …ать 200 OK с текстом `"status":"ok"`, за максимум 2 секунды». Метрики монитора: |
| `explanations/day-5/synthetic.md:116` | `1 минуты` | - Частота: от 1 минуты до 60 минут. |
| `explanations/day-5/synthetic.md:116` | `60 минут` | - Частота: от 1 минуты до 60 минут. |
| `explanations/day-5/synthetic.md:124` | `5 минут` | - Частота: от 5 минут до 60 минут (дороже HTTP, ресурсы браузера). |
| `explanations/day-5/synthetic.md:124` | `60 минут` | - Частота: от 5 минут до 60 минут (дороже HTTP, ресурсы браузера). |
| `explanations/day-5/synthetic.md:174` | `5 минут` | - DNS resolution (каждые 5 минут). |
| `explanations/day-5/synthetic.md:178` | `5 минут` | - Authentication flow (каждые 5 минут). |
| `explanations/day-5/synthetic.md:183` | `15 минут` | - Login + главная (каждые 15 минут). |
| `explanations/day-5/synthetic.md:184` | `30 минут` | - Критичный end-to-end сценарий (каждые 30 минут). |
| `explanations/day-5/synthetic.md:185` | `30 минут` | - Проверка мобильного веб-интерфейса (каждые 30 минут). |
| `explanations/day-5/usql.md:181` | `5 минут` | …аивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversion… |
| `explanations/day-5/ux-metrics.md:50` | `3 секунды` | …**Page load** — загрузка полной страницы. Дефолт 3 секунды. |
| `explanations/day-5/ux-metrics.md:51` | `1 секунда` | - **XHR action** — AJAX-запрос. Дефолт 1 секунда. |
| `explanations/day-5/ux-metrics.md:52` | `1 секунда` | …e** — SPA-переход без полной перезагрузки. Дефолт 1 секунда. |
| `explanations/day-5/ux-metrics.md:56` | `2 секунды` | …*App start** — холодный запуск приложения. Дефолт 2 секунды. |
| `explanations/day-5/ux-metrics.md:57` | `1 секунда` | …разметка через Mobile SDK (`enterAction`). Дефолт 1 секунда. |
| `explanations/day-5/ux-metrics.md:58` | `1 секунда` | …** — HTTP-запрос из мобильного приложения. Дефолт 1 секунда. |
| `explanations/day-5/ux-metrics.md:60` | `3 секунды` | *Когда менять дефолты.* 3 секунды для page load — мировой стандарт для публичных са… |
| `explanations/day-5/ux-metrics.md:60` | `1.5 секунды` | …сеть без задержек интернета. Можно ужесточить до 1.5 секунды — Apdex станет ниже, но точнее отразит проблемы,… |
| `explanations/day-5/ux-metrics.md:83` | `5 секунд` | …ель заполняет форму перевода, жмёт «Подтвердить», 5 секунд ничего не происходит. Кнопка не задизейблилась, о… |
| `explanations/day-5/ux-metrics.md:95` | `200 мс` | …общем языке. Фраза разработчика «API отвечает за 200 мс» бизнесу ничего не говорит. Фраза «Apdex упал с 0… |
| `explanations/day-5/ux-metrics.md:113` | `5 секунд` | …висят от типа приложения.** Для системы аналитики 5 секунд на загрузку — норма, для платёжного виджета на ка… |
| `explanations/day-5/ux-metrics.md:120` | `100 мс` | …отклика на первый или самый долгий клик. Хорошо: <100 мс. Плохо: >300 мс. |
| `explanations/day-5/ux-metrics.md:120` | `300 мс` | …й или самый долгий клик. Хорошо: <100 мс. Плохо: >300 мс. |
| `explanations/day-5/ux-metrics.md:136` | `200 мс` | …т не про производительность (страница грузится за 200 мс), а про **недостаток обратной связи в UI**. Польз… |
| `explanations/day-5/ux-metrics.md:161` | `5 минут` | …*Performance.** Apdex ≥ 0.85 на 95% интервалов по 5 минут. |

## [LIMIT_COUNT]  — 14 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:567` | `600 HU` | …блица для геораспределённого кластера: Large = до 600 HU (32 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU… |
| `explanations/day-1/architecture.md:567` | `250 HU` | …rge = до 600 HU (32 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU / 512 ГБ). В этом режиме суммарная ёмкос… |
| `explanations/day-1/architecture.md:1103` | `500 HU` | - Например: купили 500 HU → дали Production 400, Dev 50, Staging 50 <!-- qc… |
| `explanations/day-1/data-explorer.md:111` | `3000 метрик` | …енанте — **3.1k Metrics, showing 500** — примерно 3000 метрик, в отображаемой странице первые 500. На боевой ин… |
| `explanations/day-2/containers.md:172` | `25 микросервисов` | *Задача.* 25 микросервисов retail-команды, все в namespace `retail-*`. На да… |
| `explanations/day-2/hosts-processes.md:64` | `50 хоста` | …мер, 200 копий `java -jar payment-service.jar` на 50 хостах) и свернуть в **одну Process Group**. В интерфей… |
| `explanations/day-2/hosts-processes.md:255` | `50 хоста` | …вная ценность: 200 копий `payment-service.jar` на 50 хостах превращаются в одну сущность в интерфейсе. Метри… |
| `explanations/day-2/oneagent-infra.md:128` | `200 хостов` | **Первое развёртывание на 100-200 хостов.** Администратор не трогает OneAgent features — п… |
| `explanations/day-5/alerting-profiles.md:195` | `100 микросервисов` | - 100 микросервисов × 10 метрик = уже 1000. |
| `explanations/day-5/alerting-profiles.md:195` | `10 метрик` | - 100 микросервисов × 10 метрик = уже 1000. |
| `explanations/day-5/api.md:172` | `1000 метрик` | - **Батчинг.** Если можно получить 1000 метрик в одном запросе — не слать 1000 отдельных. |
| `explanations/day-5/rum.md:145` | `14 сессий` | …сессий. Если на одном устройстве дважды в день — 14 сессий. Это важно для биллинга (цена в лицензии за user… |
| `explanations/day-5/session-replay.md:87` | `000 сессий` | …сит от сложности страницы и длительности. При 500 000 сессий в день это около 1 TB в день только на Session Re… |
| `explanations/day-5/usql.md:104` | `000 сессий` | …по времени (обычно 30 сек) и по объёму (обычно 10 000 сессий). |

## [MEMORY]  — 28 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:241` | `2 ГБ RAM` | - **2 ГБ RAM** (рекомендуется 4 ГБ) |
| `explanations/day-1/architecture.md:241` | `4 ГБ` | - **2 ГБ RAM** (рекомендуется 4 ГБ) |
| `explanations/day-1/architecture.md:243` | `4 ГБ` | - **4 ГБ** свободного диска под установку, конфигурации и… |
| `explanations/day-1/architecture.md:243` | `2 ГБ` | …Б** под кэш установщиков и контейнер-образов + **~2 ГБ** под логи Extension Controller |
| `explanations/day-1/architecture.md:249` | `4 ГБ` | \| Малый (~c6i.large) \| 2 \| ~4 ГБ \| ~800 \| |
| `explanations/day-1/architecture.md:250` | `8 ГБ` | \| Средний (~c6i.xlarge) \| 4 \| ~8 ГБ \| ~1 800 \| |
| `explanations/day-1/architecture.md:251` | `15 ГБ` | \| Большой (~c6i.2xlarge) \| 8 \| ~15 ГБ \| ~2 500 \| |
| `explanations/day-1/architecture.md:561` | `32 ГБ` | \| Micro \| 50 \| 1 000 \| 4 \| 32 ГБ \| 500 \| |
| `explanations/day-1/architecture.md:562` | `64 ГБ` | \| Small \| 300 \| 10 000 \| 8 \| 64 ГБ \| 3 000 \| |
| `explanations/day-1/architecture.md:563` | `128 ГБ` | \| Medium \| 600 \| 25 000 \| 16 \| 128 ГБ \| 5 000 \| |
| `explanations/day-1/architecture.md:564` | `256 ГБ` | \| Large \| 1 250 \| 50 000 \| 32 \| 256 ГБ \| 7 500 \| |
| `explanations/day-1/architecture.md:565` | `512 ГБ` | \| XLarge \| 2 500 \| 100 000 \| 64 \| 512 ГБ \| 10 000 \| |
| `explanations/day-1/architecture.md:567` | `256 ГБ` | …еделённого кластера: Large = до 600 HU (32 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU / 512 ГБ). В этом… |
| `explanations/day-1/architecture.md:567` | `512 ГБ` | …2 vCPU / 256 ГБ), XLarge = до 1 250 HU (64 vCPU / 512 ГБ). В этом режиме суммарная ёмкость кластера ниже,… |
| `explanations/day-1/architecture.md:573` | `64 ГБ RAM` | - **Log Monitoring включён** → минимум 64 ГБ RAM на всех узлах (даже если HU-лимит попадает в Micr… |
| `explanations/day-1/architecture.md:575` | `1 Гб` | - **Пропускная способность сети между узлами:** 1 Гбит/с минимум, 10 Гбит/с рекомендуется. |
| `explanations/day-1/architecture.md:575` | `10 Гб` | …пособность сети между узлами:** 1 Гбит/с минимум, 10 Гбит/с рекомендуется. |
| `explanations/day-1/architecture.md:706` | `10 Гб` | - Сетевая связность между узлами по 10 Гбит/с (сеть между узлами: ≤10 мс задержка, см. `doc… |
| `explanations/day-1/architecture.md:723` | `50 ГБ` | - `/` (корень) — 50 ГБ (для ОС и Dynatrace бинарников) |
| `explanations/day-1/architecture.md:724` | `500 ГБ` | …opt/dynatrace-managed` — основные данные. Минимум 500 ГБ NVMe для малых, 4 ТБ для больших |
| `explanations/day-1/architecture.md:725` | `500 ГБ` | …d/elasticsearch` — индексы, отдельный том минимум 500 ГБ |
| `explanations/day-1/architecture.md:735` | `2 ГБ` | …файл вида `dynatrace-managed-installer.sh` (около 2 ГБ) |
| `explanations/day-1/architecture.md:928` | `4 ГБ RAM` | - Минимум 4 ГБ RAM, 2 ядра, 32 ГБ диска (для боевой нагрузки подбира… |
| `explanations/day-1/architecture.md:928` | `32 ГБ` | - Минимум 4 ГБ RAM, 2 ядра, 32 ГБ диска (для боевой нагрузки подбирается по sizing g… |
| `explanations/day-1/data-explorer.md:13` | `1 MB` | …t-metrics) — `POST /api/v2/metrics/ingest`, лимит 1 MB на запрос |
| `explanations/day-2/kubernetes.md:214` | `160 GB` | …`retail-prod` с CPU quota 40 cores, Memory quota 160 GB. Нужен алерт при приближении к лимиту. |
| `explanations/day-5/session-replay.md:84` | `5 MB` | …ze** — лимит размера одного ресурса (по умолчанию 5 MB). Выше — не сохраняется. |
| `explanations/day-5/session-replay.md:87` | `2-20 MB` | *Trade-off объёма.* Одна сессия с full replay — 2-20 MB, зависит от сложности страницы и длительности. Пр… |

## [PORT]  — 52 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:26` | `80` | …т». Классический пример: правило «если CPU больше 80% дольше 5 минут — алерт». |
| `explanations/day-1/architecture.md:273` | `порту 8021` | …ерфейсом мониторинга. По умолчанию открывается на порту 8021 (адрес вида `https://<кластер>:8021/cmc`). В CMC… |
| `explanations/day-1/architecture.md:273` | `8021` | …ом мониторинга. По умолчанию открывается на порту 8021 (адрес вида `https://<кластер>:8021/cmc`). В CMC… |
| `explanations/day-1/architecture.md:314` | `9999` | \| OneAgent \| Environment ActiveGate \| 9999 (по умолчанию) или 443 \| HTTPS \| Отправка данных… |
| `explanations/day-1/architecture.md:314` | `443` | …Environment ActiveGate \| 9999 (по умолчанию) или 443 \| HTTPS \| Отправка данных мониторинга \| |
| `explanations/day-1/architecture.md:315` | `443` | \| OneAgent \| Cluster (если без AG) \| 443 \| HTTPS \| Прямое подключение к кластеру \| |
| `explanations/day-1/architecture.md:316` | `443` | \| Environment ActiveGate \| Cluster ActiveGate \| 443 или 8443 \| HTTPS \| Передача данных и метаданных \| |
| `explanations/day-1/architecture.md:316` | `8443` | …ronment ActiveGate \| Cluster ActiveGate \| 443 или 8443 \| HTTPS \| Передача данных и метаданных \| |
| `explanations/day-1/architecture.md:317` | `443` | \| Браузер пользователя \| Cluster (UI) \| 443 \| HTTPS \| Веб-интерфейс \| |
| `explanations/day-1/architecture.md:318` | `8021` | \| Администратор \| CMC \| 8021 \| HTTPS \| Cluster Management Console \| |
| `explanations/day-1/architecture.md:319` | `9091` | \| Cluster ⇆ Cluster (multi-node) \| Внутри \| 9091, 9100, 9300, 7001 и др. \| TCP \| Внутрикластерная… |
| `explanations/day-1/architecture.md:319` | `9300` | …ter ⇆ Cluster (multi-node) \| Внутри \| 9091, 9100, 9300, 7001 и др. \| TCP \| Внутрикластерная синхронизаци… |
| `explanations/day-1/architecture.md:319` | `7001` | …Cluster (multi-node) \| Внутри \| 9091, 9100, 9300, 7001 и др. \| TCP \| Внутрикластерная синхронизация Cass… |
| `explanations/day-1/architecture.md:321` | `порт 443` | …ия администратора и пользователей Dynatrace UI на порт 443. Телеметрия всегда идёт исходящими соединениями:… |
| `explanations/day-1/architecture.md:321` | `443` | …министратора и пользователей Dynatrace UI на порт 443. Телеметрия всегда идёт исходящими соединениями:… |
| `explanations/day-1/architecture.md:433` | `8021` | …в Cluster Management Console (`https://<кластер>:8021/cmc`), раздел **Cluster updates** или **Maintenan… |
| `explanations/day-1/architecture.md:717` | `7000` | - Открыты внутренние порты Cassandra: 7000, 7001, 9042 |
| `explanations/day-1/architecture.md:717` | `7001` | - Открыты внутренние порты Cassandra: 7000, 7001, 9042 |
| `explanations/day-1/architecture.md:717` | `9042` | - Открыты внутренние порты Cassandra: 7000, 7001, 9042 |
| `explanations/day-1/architecture.md:718` | `9200` | - Порты Elasticsearch: 9200, 9300 |
| `explanations/day-1/architecture.md:718` | `9300` | - Порты Elasticsearch: 9200, 9300 |
| `explanations/day-1/architecture.md:719` | `8021` | - Порты Server: 8021, 8443, 9091 |
| `explanations/day-1/architecture.md:719` | `8443` | - Порты Server: 8021, 8443, 9091 |
| `explanations/day-1/architecture.md:719` | `9091` | - Порты Server: 8021, 8443, 9091 |
| `explanations/day-1/architecture.md:720` | `443` | - Порт NGINX: 443 |
| `explanations/day-1/architecture.md:771` | `8021` | Открой в браузере: `https://<DNS-имя-кластера>:8021/cmc` |
| `explanations/day-1/architecture.md:929` | `порт 443` | - Сетевая связность до Cluster (порт 443) и до мониторируемых систем |
| `explanations/day-1/architecture.md:929` | `443` | - Сетевая связность до Cluster (порт 443) и до мониторируемых систем |
| `explanations/day-1/architecture.md:1002` | `8021` | `https://<кластер>:8021/cmc` → **Cluster overview** → **Health**. |
| `explanations/day-1/architecture.md:1021` | `8021` | …environment под cluster admin: `https://<кластер>:8021/me/clusterhealth/`. |
| `explanations/day-1/architecture.md:1030` | `80` | \| Disk usage \| < 80% \| Срочно добавить диск или сократить retention \| |
| `explanations/day-1/baselines.md:40` | `80` | …министратор задаёт фиксированное число. «CPU выше 80% = аномалия». \| Требования compliance, SLA с фикс… |
| `explanations/day-1/baselines.md:170` | `80` | …й baseline — основной инструмент, его хватает для 80% задач. Static thresholds применяются поверх адап… |
| `explanations/day-1/components.md:33` | `8021` | …Cluster Management Console** \| `https://<кластер>:8021/cmc` \| |
| `explanations/day-1/components.md:39` | `порту 8021` | …ster Management Console / CMC** — отдельный UI на порту 8021 для администрирования самого кластера. |
| `explanations/day-1/components.md:39` | `8021` | …anagement Console / CMC** — отдельный UI на порту 8021 для администрирования самого кластера. |
| `explanations/day-1/components.md:259` | `8021` | 1. Открыть CMC (`https://<кластер>:8021/cmc`). |
| `explanations/day-1/components.md:300` | `443` | …верить исходящую связность с хоста до кластера на 443: `curl -vk https://<кластер>/api/v1/deployment`. |
| `explanations/day-1/components.md:306` | `порт 9999` | - Проверить, что порт 9999 открыт от хоста до шлюза. |
| `explanations/day-1/components.md:306` | `9999` | - Проверить, что порт 9999 открыт от хоста до шлюза. |
| `explanations/day-1/key-objects.md:77` | `80` | …ах видны характерные признаки: `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 ng… |
| `explanations/day-1/key-objects.md:77` | `443` | …видны характерные признаки: `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 nginx… |
| `explanations/day-1/ui-overview.md:98` | `53` | …g, Kafka, ActiveMQ Artemis, ActiveMQ Client и ещё 53 опции. |
| `explanations/day-2/kubernetes.md:216` | `80` | …etection → правило `Resource quota usage exceeded 80%`. Alerting profile `retail-ops` шлёт команде. Пр… |
| `explanations/day-2/service-cards.md:161` | `80` | …int даёт больше всего ошибок. `/api/auth/login` — 80% ошибок. |
| `explanations/day-2/services-overview.md:61` | `80` | …анте** (из body_preview выше): `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 ng… |
| `explanations/day-2/services-overview.md:61` | `443` | …е** (из body_preview выше): `_:9024 nginx`, `_:80,443 nginx ingress-nginx-controller-*`, `:10246 nginx… |
| `explanations/day-2/services-overview.md:63` | `80` | …-controller deployment'а на разных портах (9024 и 80,443), Dynatrace создаёт два Service, по одному на… |
| `explanations/day-2/services-overview.md:63` | `443` | …ntroller deployment'а на разных портах (9024 и 80,443), Dynatrace создаёт два Service, по одному на каж… |
| `explanations/day-5/app-segments.md:124` | `80` | …а 1.2 сек против 800 мс в других. По провайдерам: 80% трафика через один мелкий ISP, у него пинг до да… |
| `explanations/day-5/journeys.md:96` | `80` | …й, прошедших от шага 1 до шага 6. Типовая норма — 80-90%. Значительно ниже → сломан auth-pipeline. |
| `explanations/day-5/journeys.md:107` | `80` | …с шагом 1, дошедших до шага 6. Типовая норма — 70-80%. Падение ниже 50% — инцидент. |

## [SAMPLING_INTERVAL]  — 14 claims

| file:line | claim | context |
|---|---|---|
| `explanations/day-1/architecture.md:216` | `каждые 5 мин` | …ия действий пользователя по расписанию. Например, каждые 5 минут проверять, что страница логина в интернет-банке… |
| `explanations/day-1/architecture.md:306` | `раз в 10 сек` | …яет данные не каждое событие отдельно, а пакетами раз в 10 секунд (это называется **batch-передача** — от англ.… |
| `explanations/day-1/components.md:16` | `раз в 30 мин` | …tomatic updates at earliest convenience, проверка раз в 30 минут, статусы (Up to date / Update available / Updat… |
| `explanations/day-2/hosts-processes.md:199` | `каждые 5 мин` | - **Frequency** — каждую минуту / каждые 5 минут / каждые 10 минут. Чаще — больше данных для диа… |
| `explanations/day-2/hosts-processes.md:199` | `каждые 10 мин` | …**Frequency** — каждую минуту / каждые 5 минут / каждые 10 минут. Чаще — больше данных для диагностики и больше… |
| `explanations/day-5/alerting-logic.md:192` | `каждые 30 сек` | …ейти на **pull-model** — внутренний сервис-poller каждые 30 секунд спрашивает Dynatrace API «есть ли новые пробле… |
| `explanations/day-5/api.md:137` | `каждые 30 сек` | **Pull-модель для алертов.** Скрипт каждые 30 сек: `GET /api/v2/problems?from=now-1m&status=OPEN`,… |
| `explanations/day-5/api.md:173` | `раз в 5 мин` | …ь редко меняющиеся результаты (список сущностей — раз в 5 минут, не на каждый запрос). |
| `explanations/day-5/synthetic.md:174` | `каждые 5 мин` | - DNS resolution (каждые 5 минут). |
| `explanations/day-5/synthetic.md:178` | `каждые 5 мин` | - Authentication flow (каждые 5 минут). |
| `explanations/day-5/synthetic.md:183` | `каждые 15 мин` | - Login + главная (каждые 15 минут). |
| `explanations/day-5/synthetic.md:184` | `каждые 30 мин` | - Критичный end-to-end сценарий (каждые 30 минут). |
| `explanations/day-5/synthetic.md:185` | `каждые 30 мин` | - Проверка мобильного веб-интерфейса (каждые 30 минут). |
| `explanations/day-5/usql.md:181` | `каждые 5 мин` | …ос встраивается в dashboard как tile. Обновляется каждые 5 минут, показывает custom-значение (например, conversi… |
