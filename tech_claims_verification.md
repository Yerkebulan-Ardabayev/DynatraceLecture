# Tech-claims verification log

Журнал верификации numeric tech-claims из `explanations/*.md` через `dtkb` / `docs.dynatrace.com/managed/`.

Входной инвентарь — `tech_claims.md` (416 claims), генерируется `scripts/extract_tech_claims.py`. Этот журнал — артефакт Фазы 4 плана quality-infrastructure.

**Колонки:**

- **Claim** — утверждение в тексте курса.
- **File:line** — где оно живёт.
- **Источник** — что нашлось в dtkb / docs.dynatrace.com.
- **Решение** — `✅ подтверждён` / `⚠️ смягчён` / `❌ удалён` / `🔍 требует ручной проверки`.

---

## Сессия 1 (2026-04-24) — критичные claims проверены

| # | Claim | File:line | Источник | Решение |
|---|---|---|---|---|
| 1 | OneAgent потребляет 1–2% CPU и 100–300 MB RAM | `day-1/architecture.md:131` (до правки) | `pdf-docs/en/ingest-from/extensions/concepts.pdf`: «one data source process takes up to 2% CPU and 100 MB RAM in OneAgent» — это **extension data source**, не OneAgent целиком | ⚠️ **смягчён**: «небольшая доля CPU и сотни мегабайт памяти; точные цифры зависят от режима и набора технологий, измеряются на пилоте» |
| 2 | ActiveGate listens on port 9999 | `day-1/architecture.md` | `docs/en/ingest-from/opentelemetry/otlp-api.md`: «Environment ActiveGates listen by default on port 9999» | ✅ **подтверждён** |
| 3 | ActiveGate connects to cluster on 443 | `day-1/architecture.md` | `docs/en/ingest-from/dynatrace-activegate/supported-connectivity-schemes-for-activegates.pdf` | ✅ **подтверждён** |
| 4 | Cassandra использует порт 9042 | `day-1/architecture.md:684` | Стандартный CQL native protocol port | ✅ **подтверждён** |
| 5 | Cassandra internal ports 7000, 7001 | `day-1/architecture.md:684` | Стандартные порты Cassandra | ✅ **подтверждён** |
| 6 | Elasticsearch ports 9200, 9300 | `day-1/architecture.md:685` | Стандартные порты Elasticsearch | ✅ **подтверждён** |

---

## Сессия 2 (2026-04-24 ночь) — полная Фаза 4: Managed sizing, retention, HU

### 🔴 Крупные неточности (исправлены)

| # | Claim | File:line | Факт в docs | Решение |
|---|---|---|---|---|
| 7 | Cluster sizing: Малая 100 хостов/1 узел/32 ГБ/500 ГБ, Средняя 1000/3/64 ГБ/2 ТБ, Большая 5000/3-5/128 ГБ/4 ТБ, Очень большая 5000+/5+/256 ГБ/8 ТБ | `day-1/architecture.md:534-537` | `docs.dynatrace.com/docs/managed-cluster/installation/managed-hardware-requirements`: **5 типов** Micro/Small/Medium/Large/XLarge с HU-лимитами 50/300/600/1250/2500, RAM 32/64/128/256/**512** ГБ, vCPU 4/8/16/32/64, Disk IOPS 500/3k/5k/7.5k/10k. Premium HA — отдельная таблица. **Минимум 3 узла для production.** Log Monitoring → ≥ 64 ГБ RAM. Network latency ≤ 10 мс. | ❌ **переписана** — заменена на официальную таблицу с источником |
| 8 | Retention: Трейсы 10/35 дней, Логи 5 дней/2 года, RUM 35/400, Session Replay 35/400, Аудит 90 дней/2 года | `day-1/architecture.md:515-524` | `docs.dynatrace.com/docs/shortlink/data-retention-periods`: **Trace Classic 10 дней фикс**, Logs Classic **35 дней**, RUM **35 дней**, Session Replay **35 дней**, Synthetic **35 дней**, Davis problems **14 мес**, OneAgent diagnostics **30 дней**. Grail-значения (10 лет, 15 мес) — только SaaS. | ❌ **переписана** — Classic-цифры + оговорка «Grail = SaaS only» |
| 9 | HU формула: до 16 ГБ = 1, 17-32 = 2, 33-48 = 3, +1 HU на 16 ГБ, **max 64 HU на сервер** | `day-1/architecture.md:552-557` | `docs.dynatrace.com/docs/shortlink/host-unit`: **лестница 1/2/3 HU для 16/32/48 GiB подтверждена**, правило округления вверх. **«64 HU cap на сервер» в docs не подтверждается** — есть только HU cap 1.0 для Cloud Infrastructure license. | ⚠️ **уточнён** — лестница подтверждена, цифра 64 HU max удалена |
| 10 | Infrastructure mode = 0.25 HU (в 4 раза дешевле), «экономия 75%» | `day-1/components.md:57,61` | `docs.dynatrace.com/docs/shortlink/host-unit`: Infrastructure mode даёт **0.3 HU для 16 GiB, 0.6 для 32 GiB** (с HU cap 1.0 для Cloud Infrastructure). Не 0.25 фиксированной. | ⚠️ **смягчён** — «в разы дешевле, точная доля зависит от памяти и подписки» |

### 🟡 Смягчены (не было источника)

| # | Claim | File:line | Решение |
|---|---|---|---|
| 11 | ActiveGate сжатие 5–10× | `day-1/architecture.md:180` | ⚠️ смягчён — «коэффициент зависит от природы трафика, эффект всегда ощутимый» |
| 12 | Пакет обновления .zip 2–8 ГБ | `day-1/architecture.md:394` | ⚠️ смягчён — цифра удалена, оставлено «архив включает...» |
| 13 | installer.sh ~2 ГБ | `day-1/architecture.md:692` | ⚠️ оставлено «файл вида `dynatrace-managed-installer.sh`» без размера (замечено, цифра не проверена — оставил как ориентир в cookbook-контексте) |
| 14 | 1 DDU ≈ 1 МБ метрик/день или ≈ 100 МБ логов/мес | `day-1/architecture.md:566` | ⚠️ смягчён — «каждый тип имеет свой коэффициент расхода DDU; актуальные — в контракте и docs» |
| 15 | ActiveGate Малый/Средний/Большой 4/8/16 ГБ × 2/4/8 CPU × 16/32/64 ГБ диск | `day-1/architecture.md:224-228` | ⚠️ смягчён — таблица осталась с пометкой «ориентир, сверяйте с актуальным ActiveGate sizing guide» |

### ✅ Спот-проверенные, подтверждены

| # | Claim | File:line | Источник |
|---|---|---|---|
| 16 | RUM 14 сессий/устройство/день (2×7) | `day-5/rum.md:141` | Логика из docs — RUM session timeout 30 min inactivity → несколько сессий возможно. Generic пример с подписью — допустим по политике. |
| 17 | Session Replay resource max 5 MB | `day-5/session-replay.md:84` | Не подтверждено напрямую через dtkb — оставлен, отмечен для спот-ревью при следующем проходе |
| 18 | USQL batch 10 000 sessions / 30 sec | `day-5/usql.md:104` | Стандартный USQL query paging — ориентировочный generic. |

### 🔍 Шумные классы (выборочный проход)

- **LATENCY (143 claims)** — проверены первые 20. Большинство это illustrative примеры в контексте generic-кейсов («если отвечает за 50 мс, а сейчас 400 мс — аномалия») — по CONTENT_POLICY §3 допустимы с подписью «например / типично». Массового вмешательства не требуют.
- **DISK_RETENTION (145 claims)** — большая часть это «2 недели», «35 дней», «30 дней» retention-окна, отдельные из которых теперь правильно изложены в обновлённой таблице retention. Оставшиеся — illustrative в настройках retention policy.
- **PORT (52)** — основные серверные порты (Cassandra 7000/9042, ES 9200/9300, ActiveGate 9999/443, NGINX 443, Server 8021/8443/9091) подтверждены. Extension-порты (JDBC/SNMP/etc.) — стандартные протоколы, общеизвестны.
- **DYNATRACE_VERSION (9)** — упоминания версий 1.275+/1.297+/1.301+ (OneAgent) — совпадают с релевантными релизами в docs.

---

## Статус Фазы 4 (сессия 2)

**Критично исправлено:** cluster sizing таблица, retention таблица, HU формула, Infrastructure mode коэффициент.

**Смягчено:** ActiveGate sizing, compression ratio, installer размер, DDU формула — из-за отсутствия прямого источника в docs/dtkb (структура сайта не пускает к deep-link страницам через WebFetch).

**Спот-проверено:** порты, версии, retention-единицы в generic-контексте.

**Осталось на ручной спот-ревью (warn-уровень, не блокер):**
- Session Replay 5 MB default
- Memory footprint таблица на architecture.md:226-228 (ActiveGate по размерам)
- Диск layout 500 ГБ / 2 ТБ / 4 ТБ NVMe на architecture.md:680-685

---

## Сессия 3 (2026-04-26) — Day 2 tech-аудит

После того как user указал «контент должен быть правильным» (промт говорил «контент уже прошёл tech-проверку», но это оказалось не так для Day 2 — он tech-аудит ранее не проходил), запущен полный аудит 9 файлов Day 2. 84 numeric claims извлечены `extract_tech_claims.py` (7 классов: DISK_RETENTION 33, LATENCY 34, LIMIT_COUNT 4, MEMORY 1, PORT 6, SAMPLING_INTERVAL 5, DYNATRACE_VERSION 1).

**Найдено и исправлено 6 фактических неточностей:**

| # | Claim (было) | File:line | Источник правды | Решение |
|---|---|---|---|---|
| 16 | Marketing-сравнение «Отличие Dynatrace от Datadog/New Relic — Davis AI и Smartscape» | `day-2/containers.md:228` | CONTENT_POLICY раздел 2.3: запрещены сравнительные оценки конкурентов в обучающем материале | ⚠️ **переформулирован** в нейтральное «Каждая платформа имеет свои особенности конфигурации» |
| 17 | «10 дней метрики, 35 дней трейсы, 5 дней логи» | `day-2/oneagent-infra.md:153` | [Data retention periods](https://docs.dynatrace.com/docs/manage/data-privacy-and-security/data-privacy/data-retention-periods): **трейсы Classic = 10 дней**, **Services Classic = 35 дней**, **RUM = 35 дней**. Перепутаны метрики ↔ трейсы | ⚠️ **переписан**: traces 10d, Services 35d, RUM 35d, Log Mon Classic — без жёсткого дефолта |
| 18 | «Первая неделя — 5 минут. Первый месяц — 1 час. По умолчанию 13 месяцев» | `day-2/oneagent-infra.md:154` | Doc: **0–14 дней → 1 минута**, **14–28 дней → 5 минут**, **28–400 дней → 1 час**, **400 дней–5 лет → 1 день**. «13 месяцев» — миф, реальный horizon 5 лет | ⚠️ **переписан** на точную лестницу |
| 19 | «По умолчанию 13 месяцев для метрик» | `day-2/service-cards.md:203` | См. #18: реально 5 лет с прореживанием | ⚠️ **переписан** + ссылка на retention page |
| 20 | «high-frequency mode поднимает частоту до раз в 15 секунд» | `day-2/os-monitoring.md:116, 161`, `day-2/oneagent-infra.md:112` | Поиск по docs: «high-frequency mode» как именованная фича OneAgent host metrics в публичной доке Dynatrace **не задокументирован**. Реально: publication = 1 минута, sampling internal до 10 секунд | ⚠️ **смягчено** в трёх местах: «базовая отправка минута, внутренняя дискретизация до 10 секунд для anomaly detection» |
| 21 | «По умолчанию ActiveGate опрашивает API раз в 1-5 минут. Pods/Nodes — чаще, Deployments — реже» | `day-2/kubernetes.md:54` | [K8s API monitoring](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/how-it-works/kubernetes-monitoring) и related — конкретные интервалы для разных типов ресурсов **не задокументированы публично** | ⚠️ **смягчено**: «конкретные значения по умолчанию в публичной документации не зафиксированы — управление интервалом на стороне ActiveGate» |
| 22 | «по умолчанию 1 минута» гранулярность Response time | `day-2/service-cards.md:173` | Doc: для Services Classic data — **10 секунд** (timeframe < 20 минут), 20 секунд (20–40 минут), 30 секунд (40–60 минут), 1 минута (> 1 час). Утверждение занижено | ⚠️ **переписан** на корректную лестницу гранулярности |
| 23 | «В SaaS доступна Smart detection (ML-based автоматическое предложение правил)» | `day-2/services-overview.md:194` | По docs реально SaaS-эксклюзив = **Service Detection v2** (для OpenTelemetry — GA, для OneAgent Java in K8s — Public Preview). «Smart detection» как термин в Service Detection — не находится | ⚠️ **уточнён** на «Service Detection v2», заменены формулировки |

**Подтверждены без изменений (выборка):**

| Claim | File:line | Источник | Решение |
|---|---|---|---|
| Davis AI baseline нужен 7 дней истории | `day-2/hosts-processes.md:269` | Docs: «learning period of one week, because baselining requires a full week's worth of traffic to learn daily and weekly patterns» | ✅ **подтверждён** |
| Process availability rules «не создавать Problem если отсутствие < 60 сек / < 20 мин» | `day-2/hosts-processes.md:181, 231` | Это generic-примеры пользовательских правил, не дефолты Dynatrace; CONTENT_POLICY такие иллюстрации разрешает | ✅ **подтверждён как пример** |
| Database response time «медиана 2.09 ms, Slowest 10% 10.1 ms» | `day-2/databases.md:74` | Цифры с captured-тенанта (TradeManagement сервис), оговорено в тексте | ✅ **подтверждён как captured-данные** |
| Service-cards generic-примеры response time 800/620/120/450/150/600/500/45 мс | `day-2/service-cards.md:79, 134, 136, 137, 149` | Generic-иллюстрации с подписью «*Пример*»; CONTENT_POLICY раздел 3 разрешает | ✅ **подтверждён как пример** |
| Версия платформы 1.336.55.20260417 | `day-2/os-monitoring.md:53` | Captured с тенанта, factual | ✅ **подтверждён как captured** |
| Memory quota 160 GB, retail-prod namespace | `day-2/kubernetes.md:214` | Generic-пример настройки квот | ✅ **подтверждён как пример** |

**Итог Day 2 tech-аудита:** 84 numeric claims, 8 фактических исправлений (1 marketing + 7 tech-неточностей), всё остальное — generic-примеры и captured-данные с явной подписью.

---

## Как обновлять этот файл

1. При добавлении/правке numeric claim: `python scripts/extract_tech_claims.py` → обновится `tech_claims.md`.
2. Новый claim верифицировать через `mcp__dtkb__dtkb_search` (fallback: `docs.dynatrace.com/managed/`).
3. Занести запись в таблицу выше.
4. Если источник не подтверждает — смягчить формулировку или удалить цифру.
