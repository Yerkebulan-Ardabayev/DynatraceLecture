> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 6 из 14: «Детектирование приложений: правила, группы, лучшие практики»

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

**Правила матчатся по:**

- **URL / host name** — основное условие (хост в домене → приложение).
- **URL path prefix** — `/api/*` в одно приложение, `/admin/*` в другое.
- **Query parameter** — по значению специального параметра.
- **HTTP header** — по кастомному заголовку от reverse-proxy.

*Типовое применение.* 3-10 правил App detection по количеству разных публичных и внутренних веб-приложений. Каждое правило даёт отдельный Application в интерфейсе с собственными метриками и SLI.

### Шаг 2 — Beacon origins for CORS

![Beacon origins for CORS — список доменов, откуда принимаются RUM-beacons](screenshots/day-3-4/app-detection/settings/builtinrum.web.beacon-domain-origins/Beacon-origins-for-CORS-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.web.beacon-domain-origins`.

*Что это.* RUM-сниппет в браузере отправляет данные (beacons) на специальный endpoint ActiveGate. Если пользователь открыл страницу на `www.example.com`, а beacons идут на `collector.example.com`, браузер считает это cross-origin запросом и может заблокировать (CORS policy).

Страница настраивает список доменов, от которых ActiveGate **принимает** beacons. Явно разрешает cross-origin от доменов организации.

*Типовое содержание.* Все публичные домены и их CDN: `www.example.com`, `portal.example.com`, `mobile-api.example.com`, `cdn.example.com` и аналогичные.

### Шаг 3 — Identify host names

![Identify host names — правила идентификации имён хостов](screenshots/day-3-4/app-detection/settings/builtinrum.host-headers/Identify-host-names-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.host-headers`.

*Что настраивает.* HTTP-заголовок для определения host name страницы. По умолчанию — `Host`. Но если приложение за reverse-proxy, реальный домен пользователя приходит в `X-Forwarded-Host` или `X-Original-Host`.

*Риск без настройки.* Все страницы кажутся идущими с одного внутреннего домена прокси (`nginx-internal.local`), App detection не работает правильно.

*Типовая настройка за reverse-proxy.* Обязательно добавить `X-Forwarded-Host` в список идентифицирующих заголовков.

### Шаг 4 — IP determination

![IP determination — настройка определения IP-адреса клиента](screenshots/day-3-4/app-detection/settings/builtinrum.ip-determination/IP-determination-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.ip-determination`.

*Что настраивает.* HTTP-заголовок для определения IP клиента. Та же проблема, что и с host name: за reverse-proxy реальный IP клиента в `X-Forwarded-For` или `X-Real-IP`.

*Риск без настройки.* Все клиенты кажутся с IP прокси. Геолокация не работает, анализ по странам невозможен.

### Шаг 5 — Map IP addresses to locations

![Map IP addresses to locations — база для геолокации клиентов](screenshots/day-3-4/app-detection/settings/builtinrum.ip-mappings/Map-IP-addresses-to-locations-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.ip-mappings`.

*Что настраивает.* Правила преобразования IP в геолокацию. По умолчанию Dynatrace использует встроенную GeoIP-базу, обновляется с поставками.

*Для внутренних IP* (10.x, 192.168.x) автоматической геолокации нет — этих диапазонов нет во встроенной базе. Добавляют кастомные mapping: `10.10.0.0/16 → офис 1`, `10.20.0.0/16 → офис 2`. Это помогает анализу «в каком офисе медленно открывается корпоративный портал».

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

**GeoIP база** поставляется в сборке Dynatrace. Обновляется при ручной загрузке новых сборок через CMC. Для кастомных IP-mappings всё локально.

**Cross-origin** в закрытом контуре сложнее, потому что домен ActiveGate обычно публикуется на внутреннем DMZ с specific CORS-настройкой. Список разрешённых origins должен включать все внутренние домены банка.
