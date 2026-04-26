> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 5 из 10: «Разделение фронтенд-приложений на части, фильтры, сегменты»

## 📍 КАРТА — три страницы про сегментацию приложений

Термины темы: `Application / приложение / логическая RUM-единица`, `Detection rule / правило детекции`, `CORS / Cross-Origin Resource Sharing` (браузерная политика), `Beacon origin / разрешённый источник beacon-ов`, `Provider breakdown / разбивка по ISP`, `Management zone / сквозной разрез`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Application detection rules | **Settings → Web and mobile monitoring → Application detection → Detection rules** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.app-detection` |
| Beacon origins for CORS | **Settings → Web and mobile monitoring → Application detection → Beacon CORS origins** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.beacon-domain-origins` |
| Provider breakdown | **Settings → Web and mobile monitoring → Provider breakdown** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.provider-breakdown` |

---

## 🎬 Работа с сегментацией приложений на трёх экранах

### Шаг 1 — Application detection rules

![Application detection rules — правила определения приложений](screenshots/day-5/app-segments/settings/builtinrum.web.app-detection/Application-detection-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.app-detection`.

*Что на странице.* Заголовок `Define application detection rules` и таблица правил. Каждое правило — условие «если URL страницы соответствует паттерну X, то она принадлежит приложению Y».

*Зачем.* Пример: на домене `example.com` крутятся:

- `example.com` — публичный сайт (маркетинговый).
- `example.com/retail/*` — ДБО для физлиц.
- `example.com/corporate/*` — ДБО для юрлиц.
- `example.com/blog/*` — новости и статьи.

Без детекции Dynatrace видел бы **одно гигантское приложение** с общим Apdex. Падение производительности ДБО-для-юрлиц растворилось бы в объёме публичного сайта. Детекция разделяет трафик на четыре отдельных приложения, каждое со своим Apdex, SLO, командой ответственных.

**Типы правил:**

- **Domain-based** — по полному домену (`corporate.example.com` → `Corporate Banking`).
- **Path-based** — по URL-пути (`example.com/retail/*` → `Retail Banking`).
- **Query param** — по параметрам URL.
- **Default fallback** — если ничего не подошло, назначается приложение по умолчанию.

*Порядок правил важен.* Применяются сверху вниз, первое совпавшее «выигрывает». Более специфичные правила должны быть выше общих.

### Шаг 2 — Beacon origins for CORS

![Beacon origins for CORS — настройка CORS-origin для beacon'ов](screenshots/day-5/app-segments/settings/builtinrum.web.beacon-domain-origins/Beacon-origins-for-CORS-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.web.beacon-domain-origins`.

*Что настраивает.* Список доменов, которым разрешено отправлять beacon-ы в Dynatrace. Это безопасность: подделанный beacon с произвольного сайта будет отвергнут.

*Как работает.* RUM-агент `ruxit.js` отправляет beacon — браузер устанавливает HTTP-заголовок `Origin: https://example.com`. Dynatrace Cluster / ActiveGate сравнивает со списком разрешённых origins. Совпадает — принимает. Нет — возвращает CORS error, beacon отбрасывается.

*Зачем важно.* Без ограничения origin-ов любой сайт мог бы «наливать мусорный трафик» и искажать статистику — подделанные fake-сессии портят Apdex. CORS-список — белый список легитимных доменов.

**Типичный набор:**

- `https://example.com` — основной домен.
- `https://www.example.com` — с www.
- `https://mobile.example.com` — мобильная версия.
- `https://test.example.com` — тестовый стенд (если мониторим и его).

Никаких wildcard (`*`), никаких посторонних доменов. Всё конкретно.

### Шаг 3 — Provider breakdown (разбивка по интернет-провайдерам)

![Provider breakdown — разбивка по интернет-провайдерам](screenshots/day-5/app-segments/settings/builtinrum.provider-breakdown/Provider-breakdown-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.provider-breakdown`.

*Что настраивает.* Автоматическое разделение статистики по ISP (Internet Service Provider). Dynatrace по IP-адресу клиента через справочник определяет провайдера и записывает как атрибут сессии.

*Типовая ситуация.* Пользователи жалуются на медленное приложение, но только некоторые. Provider breakdown показывает: все жалобщики из одного провайдера, у него проблемы с маршрутизацией до дата-центра. Решение — переговоры с провайдером или перенос дата-центра в более центральный IX.

**Настройки:**

- **Enable provider detection** — тумблер включения (обычно Да).
- **Known providers overrides** — ручная подмена имён (если справочник даёт одно имя, а нужно другое).
- **Mapping rules** — правила назначения провайдера по IP-диапазонам. Для внутренней сети, чтобы «свой» трафик отображался как `Internal`, а не как внешний провайдер.

*Связка с другими разрезами.* Provider — один из атрибутов сессии. По нему можно фильтровать, группировать, строить дашборды. Пример дашборда «Apdex по провайдерам» — видно: у крупного ISP 0.95 (норма), у мелкого 0.62 (проблема). Дальше — копать: какие user actions тормозят у этого ISP, какие ресурсы долго грузятся.

---

## 🎓 ТЕОРИЯ — сегментация и multi-tenancy на одном домене

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Real User Monitoring — applications](https://docs.dynatrace.com/docs/shortlink/rum)

### Зачем разделять приложения

- **Разные SLO.** Для маркетингового сайта 3 сек загрузки — норма, для торговой платформы критично 500 мс. Одним Apdex не мониторить.
- **Разные команды.** Команда ДБО-retail отвечает за одно, команда ДБО-corporate за другое. Проблемы должны идти к нужной команде.
- **Разные источники биллинга.** Если публичный сайт ведёт маркетинговая команда, а ДБО — внутреннее IT, стоимость мониторинга разнесена.
- **Разные compliance-требования.** Публичный сайт — GDPR baseline. ДБО — банковская тайна + закон о персональных данных.
- **Разные каденции.** Публичный сайт мониторится ежечасно. ДБО — 24/7 сменой.

### Alternative: Management zones

Второй инструмент сегментации — **Management zones** (разбирали в Дне 1, Тема 5). MZ — view на все сущности (apps + services + hosts), принадлежащие одной логической единице.

*Разница:*

- **Application detection** — **создаёт** отдельную Dynatrace-сущность (Application). У неё свой Apdex, свои метрики, свои правила, свой ID.
- **Management zone** — **фильтрует** существующие сущности. У MZ нет своих метрик, это просто способ смотреть на мир глазами конкретной команды.

Обычно используются оба:

- Приложения — `example.com-retail`, `example.com-corporate`, `example.com-marketing`.
- Management zones — `retail-banking` (включает приложение `retail` + все backend-сервисы + все хосты), `corporate-banking`, `marketing`.

Приложение = один уровень (фронт). Management zone = сквозной разрез (фронт + бэк + инфра).

### Автоматический vs ручной режим detection

По умолчанию Dynatrace использует **one application per domain** логику: каждый уникальный домен — отдельное приложение. Это работает для простых случаев (один сайт = один домен). Для сложных (несколько продуктов на одном домене) нужны правила.

**Рекомендация.** Начинать с автоматического режима, смотреть список детектированных приложений через неделю трафика. Если всё на одном домене — создавать path-based rules. Не увлекаться: слишком много приложений тоже плохо (каждое требует отдельной настройки пороговых значений, alerting, команды реагирования).

### Provider breakdown как инструмент root cause

Типовые случаи:

- **«Сайт тормозит в определённом регионе».** По региону: медиана 1.2 сек против 800 мс в других. По провайдерам: 80% трафика через один мелкий ISP, у него пинг до дата-центра 250 мс против 60 мс у крупного. Решение — переговоры с ISP или CDN.

- **«ДБО падает по утрам».** По провайдерам падение только у мобильных операторов, у фиксированных норма. Причина — на утреннем cold start пула соединений операторы делают reroute. Решение — keep-alive и retry на мобильном SDK.

- **«Жалобы только от корпоративных клиентов».** IP-диапазоны жалобщиков соответствуют крупным корпорациям (фиксированные IP). У них in-house firewall-ы делают deep packet inspection для SSL — добавляет 300 мс. Решение — мониторить SSL handshake time отдельно, предупреждать про флаг «корпоративные сети».

### CORS — как работает на уровне браузера

CORS (Cross-Origin Resource Sharing) — механизм браузерной безопасности. По умолчанию скрипт, загруженный с `example.com`, не может делать XHR-запросы к `dynatrace-cluster.local`. Браузер блокирует.

**Обход через CORS preflight + actual request:**

1. Браузер шлёт `OPTIONS` на `dynatrace-cluster.local/beacon` с заголовком `Origin: https://example.com`.
2. ActiveGate отвечает заголовком `Access-Control-Allow-Origin: https://example.com` (если `example.com` есть в Beacon origins) или не отвечает вообще (если нет в списке).
3. Совпало — браузер шлёт реальный POST с beacon. Не совпало — preflight fail, запрос отменён.

Поэтому Beacon origins — не про policy Dynatrace, а про **техническую возможность** RUM-агента отправить beacon. Без корректной настройки RUM-агент молчит, даже если всё остальное настроено.

### Multi-application домен в air-gapped Managed

В Managed важен **Beacon URL** — адрес, куда RUM-агент шлёт beacon-ы. По умолчанию это тот же URL, откуда загрузился `ruxit.js` (обычно Public ActiveGate).

Если приложения в разных сетях (внутренний портал шлёт в internal ActiveGate, публичный сайт — в Public ActiveGate), нужна кастомная настройка Beacon URL в каждой RUM-конфигурации.

Настраивается в Application settings → RUM → Capture settings → Beacon URL. Формат — полный URL до `/beacon` endpoint ActiveGate.

### Сегментация на уровне Mobile

На мобильном правила детекции другие — приложение идентифицируется **bundle ID** (iOS) или **application ID** (Android), а не URL. Поэтому настройка app detection для мобильных делается в отдельной секции Settings → Web and mobile monitoring → Mobile applications, а не в Web detection rules. Каждое мобильное приложение создаётся отдельно при инициализации Mobile SDK.

### Ключевые термины

- **Application detection** — автоматическое или ручное разделение трафика на Dynatrace applications.
- **Detection rule** — условие «URL X → приложение Y».
- **CORS (Cross-Origin Resource Sharing)** — браузерная безопасность для cross-domain запросов.
- **Beacon origin** — origin, разрешённый отправлять beacon'ы.
- **Provider breakdown** — разбивка по интернет-провайдерам по IP.
- **Management zone** — сквозной разрез сущностей, отличается от приложения.
