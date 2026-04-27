> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 6 из 14: «Детектирование приложений: правила, группы, лучшие практики»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.app-detection -->
<!-- revision: 2026-04-27 -->

🔖 Редакция от 2026-04-27.

Путь в UI: **Settings → Web and mobile monitoring → Web → Application detection / Beacon origins for CORS / Identify host names / IP determination / Geographic regions → Map IP addresses to locations**.

## 📚 Источники

- [Application detection rules (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/application-detection-rules)
- [Beacon origin allowlist (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/configure-beacon-domain-allowlist)
- [Detection of IP addresses, locations and user agents (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/detection-of-ip-addresses-locations-and-user-agents)
- [Web Applications RUM (Managed)](https://docs.dynatrace.com/managed/observe/digital-experience/web-applications)

## 📍 КАРТА — пять страниц про детекцию и группировку приложений

Термины темы: `Application / приложение / логическая web-единица в RUM`, `Beacon / бикон / пакет RUM-данных`, `CORS / Cross-Origin Resource Sharing`, `Host name / имя хоста`, `GeoIP / гео-IP-база`, `Reverse proxy / обратный прокси`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Application detection | **Settings → Web and mobile monitoring → Web → Application detection** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.app-detection` |
| Beacon origins for CORS | **Settings → Web and mobile monitoring → Web → Beacon origins for CORS** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.beacon-domain-origins` |
| Identify host names | **Settings → Web and mobile monitoring → Web → Identify host names** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.host-headers` |
| IP determination | **Settings → Web and mobile monitoring → Web → IP determination** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.ip-determination` |
| Map IP addresses to locations | **Settings → Web and mobile monitoring → Web → Geographic regions → Map IP addresses** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.ip-mappings` |

---

## 🎬 Работа с детекцией приложений на пяти экранах

### Шаг 1 — Application detection

![Application detection — главная страница правил обнаружения приложений](screenshots/day-3-4/app-detection/settings/builtinrum.web.app-detection/Application-detection-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.app-detection`.

*Что такое App detection.* RUM-сниппет собирает данные со всех страниц веб-сервера. Чтобы разделить их между Applications (например, `www.example.com` → `Public Site`, `portal.example.com` → `Client Portal`), нужны правила детекции.

**Правила матчатся по URL** в формате `scheme://host:port/path?query` (порты 80 и 443 опускаются по умолчанию). Доступные операторы матчинга: **contains / ends with / equals**. Правила оцениваются **сверху вниз, срабатывает первое совпавшее**, дальнейшая обработка останавливается. Лимит — **до 1000 правил на окружение**.

Можно сопоставлять:

- **URL / host name** — основное условие (хост в домене → приложение).
- **URL path prefix** — `/api/*` в одно приложение, `/admin/*` в другое.
- **Query parameter** — по значению специального параметра.
- **HTTP header** — по кастомному заголовку от reverse-proxy.

Изменения правил доезжают до OneAgent обычно в течение минуты.

На той же странице есть инструмент **Check your existing detection rules** — ввести URL и увидеть, какое правило сработает и включён ли RUM.

*Типовое применение.* 3-10 правил App detection по количеству разных публичных и внутренних веб-приложений. Каждое правило даёт отдельный Application в интерфейсе с собственными метриками и SLI.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/application-detection-rules -->

### Шаг 2 — Beacon origins for CORS

![Beacon origins for CORS — список доменов, откуда принимаются RUM-beacons](screenshots/day-3-4/app-detection/settings/builtinrum.web.beacon-domain-origins/Beacon-origins-for-CORS-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.beacon-domain-origins`.

*Что это.* RUM-сниппет в браузере отправляет данные (beacons) на специальный endpoint. Если страница на `www.example.com`, а beacons идут на `collector.example.com`, браузер считает это cross-origin запросом и применяет CORS-политику.

Страница настраивает список origins, от которых endpoint **принимает** cross-origin RUM-beacons. До 20 правил на окружение. Same-origin beacons (одинаковые protocol/host/port) под allowlist не попадают и не нуждаются в правилах.

*Поведение allowlist:*
- Список пустой → принимаются beacons с любого origin (дефолтное поведение).
- Добавлено хотя бы одно правило → отклоняется всё, что не подходит, ответ `403 Forbidden`.

*Когда нужен.* CORS обязателен только для двух сценариев: agentless-приложения (beacons идут на Cluster ActiveGate на другом домене) и auto-injected приложения с переключённым beacon endpoint.

*Типовое содержание.* Все публичные домены и их CDN: `www.example.com`, `portal.example.com`, `mobile-api.example.com`, `cdn.example.com`.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/web-applications/additional-configuration/configure-beacon-domain-allowlist -->

### Шаг 3 — Identify host names

![Identify host names — правила идентификации имён хостов](screenshots/day-3-4/app-detection/settings/builtinrum.host-headers/Identify-host-names-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.host-headers`.

*Что настраивает.* HTTP-заголовок для определения host name страницы. По умолчанию — `Host`. Но если приложение за reverse-proxy, реальный домен пользователя приходит в `X-Forwarded-Host` или `X-Original-Host`.

*Риск без настройки.* Все страницы кажутся идущими с одного внутреннего домена прокси (`nginx-internal.local`), App detection не работает правильно.

*Типовая настройка за reverse-proxy.* Обязательно добавить `X-Forwarded-Host` в список идентифицирующих заголовков.

### Шаг 4 — IP determination

![IP determination — настройка определения IP-адреса клиента](screenshots/day-3-4/app-detection/settings/builtinrum.ip-determination/IP-determination-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.ip-determination`.

*Что настраивает.* Список HTTP-заголовков для определения IP клиента. Когда запрос приходит напрямую в инструментированный сервер, IP берётся из socket. За reverse-proxy / CDN / load balancer Dynatrace разбирает заголовки в **заданном порядке** (его можно менять, можно добавить свои). Стандартный набор включает `X-Forwarded-For`, `X-Real-IP` и аналоги.

По умолчанию **последний октет IP маскируется** для соблюдения приватности.

*Риск без настройки.* Все клиенты кажутся с IP прокси. Геолокация не работает, анализ по странам невозможен.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/detection-of-ip-addresses-locations-and-user-agents -->

### Шаг 5 — Map IP addresses to locations

![Map IP addresses to locations — база для геолокации клиентов](screenshots/day-3-4/app-detection/settings/builtinrum.ip-mappings/Map-IP-addresses-to-locations-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.ip-mappings`.

*Что настраивает.* Кастомные правила преобразования IP в геолокацию. Для веб-приложений Dynatrace по умолчанию использует **MaxMind Geo2 database**, которая обновляется с каждой поставкой Managed-релиза. Для мобильных при наличии разрешения предпочтение отдаётся GPS, иначе fallback на IP-геолокацию.

*Для внутренних IP* (10.x, 192.168.x) автоматической геолокации нет — этих диапазонов в MaxMind нет. Добавляют кастомные mapping: `10.10.0.0/16 → офис 1`, `10.20.0.0/16 → офис 2`. Это помогает анализу «в каком офисе медленно открывается корпоративный портал».
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/detection-of-ip-addresses-locations-and-user-agents -->

---

## 🎓 ТЕОРИЯ — детекция приложений в RUM

### Почему App detection важна

**Один RUM-сниппет может служить нескольким приложениям.** OneAgent на веб-сервере вставляет один и тот же сниппет во все HTML-ответы. Если на сервере хостятся три разных приложения (публичный сайт, клиентский портал, внутренняя админка), все они получат сниппет, и данные пойдут в ActiveGate с одного источника.

**App detection разбирает эти данные** на отдельные Applications в интерфейсе. Без правил — одно огромное приложение со смешанными метриками. С правилами — три отдельных с собственной статистикой.

### Последствия неправильной детекции

- **Метрики смешиваются.** Проблема в админке влияет на метрики публичного сайта и наоборот.
- **SLO невозможны.** Нельзя задать «Availability клиентского портала ≥ 99.9%» — нет отдельной сущности.
- **Alerting profiles некорректны.** Алерты на одно приложение срабатывают по проблемам другого.

### Связь с остальными настройками темы

Правильная детекция приложений требует всех пяти страниц в комплекте:
- **App detection** — основные правила (по какому URL/host какое приложение).
- **Identify host names** — чтобы правила могли корректно работать за reverse-proxy.
- **IP determination** — чтобы геолокация работала.
- **Beacon origins CORS** — чтобы браузеры не блокировали отправку данных.
- **IP mappings** — чтобы внутренние IP имели понятную локацию.

Без хотя бы одного пункта — картина неполная.

### Air-gapped specifics

**MaxMind Geo2 database** входит в сборку Managed и обновляется при ручной загрузке новых сборок через CMC. Кастомные IP-mappings полностью локальны.

**Cross-origin** в закрытом контуре сложнее, потому что домен ActiveGate обычно публикуется на внутреннем DMZ со специфичной CORS-настройкой. Список разрешённых origins должен включать все внутренние домены банка.
<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/detection-of-ip-addresses-locations-and-user-agents -->
