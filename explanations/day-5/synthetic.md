> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 6 из 10: «Synthetic Monitoring: HTTP, Browser, браузерные шаги»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/synthetic -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Synthetic Monitoring (shortlink)](https://docs.dynatrace.com/managed/shortlink/synthetic-monitoring)
> - [Create a private Synthetic location](https://docs.dynatrace.com/managed/observe/digital-experience/synthetic-monitoring/private-synthetic-locations/create-a-private-synthetic-location)
> - [Manage private Synthetic locations](https://docs.dynatrace.com/managed/observe/digital-experience/synthetic-monitoring/private-synthetic-locations/manage-private-synthetic-locations)
> - [Synthetic monitoring overview](https://docs.dynatrace.com/managed/observe/digital-experience/synthetic-monitoring)

## 📍 КАРТА — четыре страницы про Synthetic Monitoring

Термины темы: `Synthetic / синтетический мониторинг / проверки роботами по расписанию`, `HTTP monitor / простая проверка URL`, `Browser monitor / сценарий с headless-браузером`, `Multi-step HTTP / цепочка API-запросов`, `Outage / падение монитора`, `Location / локация запуска мониторов`.

⚠️ **На captured-тенанте `guu84124` страница `/ui/synthetic` возвращает 403.** Учебный gap: у реального клиента Managed доступ будет. Разбор по общему знанию платформы плюс доступные captured-настройки.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Synthetic Monitor (list) | **Application Observability → Frontend → Synthetic** | `https://guu84124.live.dynatrace.com/ui/synthetic` ⚠️ **403 на этом тенанте** |
| Synthetic availability settings | **Settings → Web and mobile monitoring → Synthetic availability settings** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:synthetic.synthetic-availability-settings` |
| Browser monitor outage handling | **Settings → Web and mobile monitoring → Synthetic → Browser outage handling** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:synthetic.browser.outage-handling` |
| HTTP monitor outage handling | **Settings → Web and mobile monitoring → Synthetic → HTTP outage handling** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:synthetic.http.outage-handling` |

---

## 🎬 Работа с Synthetic на четырёх экранах

### Шаг 1 — Synthetic Monitor list (ОГРАНИЧЕНИЕ ДОСТУПА)

![403 — нет прав для просмотра synthetic](screenshots/day-5/synthetic/synthetic/403-You-dont-have-permission-to-view-this-page-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/synthetic`.

**Что видно на скриншоте.** Страница 403 — You don't have permission to view this page. Error details - 403 forbidden.

На живом Managed-тенанте здесь список всех настроенных synthetic-мониторов. По официальной документации Dynatrace Synthetic Monitoring в Managed предлагает **четыре типа** мониторов:

- **Single-URL Browser monitors** — эквивалент симулированного посещения приложения современным браузером. Запускаются c публичных или **private** локаций; периодичность — раз в 5 минут или реже.
- **Browser clickpaths** — сценарии с заданной последовательностью кликов и пользовательского ввода для бизнес-критичных процессов.
- **HTTP monitors** — простые HTTP(S)-запросы для проверки доступности API endpoint'ов и одиночных ресурсов. Поддерживаются Multi-step HTTP-сценарии (например, `GET /auth` → `POST /login` с извлечённым токеном → `GET /user/profile`). High-resource HTTP-варианты с OAuth2 / Kerberos выполняются только на private locations.
- **Network Availability Monitoring (NAM)** — мониторы remote hosts, когда HTTP-endpoint'ы недостаточны: ICMP-ping, TCP-connection check, DNS-resolution. NAM работает **только на private locations**.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/synthetic-monitoring -->

Метрики любого монитора:
- **Availability** — процент успешных проверок за период.
- **Response time** — медиана, перцентили.
- **Location** — с какой локации проверялось (для географического анализа).

### Шаг 2 — Synthetic availability settings

![Synthetic availability settings — настройки доступности](screenshots/day-5/synthetic/settings/builtinsynthetic.synthetic-availability-settings/Synthetic-availability-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:synthetic.synthetic-availability-settings`.

*Что настраивает.* Общие параметры availability для всех synthetic-мониторов:

- **Global availability calculation** — как считается общий availability: среднее по всем локациям, worst-case (худший из локаций), медиана.
- **Maintenance windows awareness** — игнорировать падения во время maintenance window. Иначе плановая работа ломает availability-статистику.
- **Retry policy** — сколько раз повторить проверку перед засчитыванием fail. По умолчанию 2 retry с паузой 30 сек. Отсекает случайные сетевые сбои.
- **Location health** — если отдельная локация умерла (ActiveGate упал), её fail-ы не засчитывать как проблему приложения.

### Шаг 3 — Browser monitor outage handling

![Browser monitor outage handling — обработка падений браузерных мониторов](screenshots/day-5/synthetic/settings/builtinsynthetic.browser.outage-handling/Outage-handling-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:synthetic.browser.outage-handling`.

*Что настраивает.* Правила превращения сбоя browser-монитора в Problem у Davis.

**Два типа outage:**

- **Global outage** — монитор упал во всех локациях. Реальное падение приложения.
- **Local outage** — монитор упал в одной-двух локациях, в остальных работает. Региональная проблема (например CDN).

**Параметры:**

- **Consecutive failures before outage** — сколько подряд fail-ов считать падением. По умолчанию 3-5, отсекает случайные сбои.
- **Failure threshold** — процент локаций в fail state для global outage. По умолчанию 100% (все локации).
- **Recovery threshold** — сколько успешных проверок подряд для восстановления. Обычно 2-3.

### Шаг 4 — HTTP monitor outage handling

![HTTP monitor outage handling — обработка падений HTTP-мониторов](screenshots/day-5/synthetic/settings/builtinsynthetic.http.outage-handling/Outage-handling-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:synthetic.http.outage-handling`.

Аналогично Шагу 3, но для HTTP-мониторов:

- **Consecutive failures before outage** — сколько fail-ов подряд.
- **Global vs local outage detection** — количество локаций в fail state.
- **Expected HTTP codes override** — какие коды считать успехом. По умолчанию 2xx. Можно настроить 401 как успех для защищённого endpoint — это доказательство, что сервис жив, просто требует auth.

---

## 🎓 ТЕОРИЯ — Synthetic Monitoring как инструмент

### RUM vs Synthetic — разница и комбинация

**RUM** — реальные пользователи, естественный трафик, реальная нагрузка. Минусы:

- Ночью пользователей нет, проблему не увидим до утра.
- На редко используемых страницах мало данных, статистики нет.
- Ограничен путями, по которым реально ходят.

**Synthetic** — искусственный трафик от роботов по расписанию. Плюсы:

- 24/7, независимо от реальной нагрузки.
- Предсказуемые метрики — одни и те же шаги и данные.
- Проактивное обнаружение — катастрофу увидим до жалоб клиентов.

Нужны **оба**:

- RUM — для аналитики пользовательского опыта.
- Synthetic — для SLO, на который вы отчитываетесь.

### Типы synthetic monitors детально

**HTTP monitor** — простые HTTP-проверки:
- Один или цепочка HTTP-запросов (GET, POST, PUT, …) — Multi-step реализуется как несколько шагов внутри одного HTTP-монитора с возможностью извлечь значение из ответа предыдущего шага и подставить в следующий.
- Запускается с Synthetic-enabled ActiveGate в private location.
- Проверки: HTTP code, response time, content matching.
- High-resource варианты с OAuth2 / Kerberos — только на private locations.
- **Use case**: health check endpoint-ов, API availability, end-to-end API-цепочки (authenticate → fetch → update → logout).

**Single-URL Browser monitor** — посещение одной страницы реальным браузером:
- Запускается современный браузер (на Linux ActiveGate с 1.331 — Chrome for Testing с авто-обновлением, можно отключить для air-gapped).
- Проверяет все ресурсы страницы, метрики Visually Complete, Speed Index, Page Load Time.
- Минимальная частота — 5 минут или реже.

**Browser clickpath** — сценарий с последовательностью кликов:
- Записывается через Recorder-расширение или собирается вручную из шагов.
- Робот выполняет клики, ввод, ассерты состояния — end-to-end бизнес-сценарии (login, поиск, корзина, оплата).
- Дороже Single-URL по ресурсам и времени, ниже частота.

**Network Availability Monitoring (NAM)** — сетевая доступность хостов:
- Поддерживает ICMP (ping), TCP connect, DNS lookup.
- Применяется, когда HTTP-endpoint'а нет или важна сетевая связность.
- **Только private locations.**

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/shortlink/synthetic-monitoring -->

### Где запускаются synthetic мониторы

В Dynatrace Managed используются **private locations** — synthetic-мониторы выполняются с ваших же ActiveGate'ов внутри корпоративной сети. Public Synthetic locations Dynatrace формально существуют как отдельная фича, но в **air-gapped Managed** (без outbound в интернет к Dynatrace public synthetic-инфраструктуре) использоваться не могут — это ровно тот случай, ради которого нужны private locations.

**Synthetic-enabled ActiveGate**:
- **Clean installation:** при установке роли Synthetic другие модули ActiveGate отключаются, чтобы посторонние процессы не искажали performance-метрики.
- **Версии:** Environment ActiveGate **1.169+** или Cluster ActiveGate (с Managed **1.176+**).
- Поддерживает **и browser, и HTTP** мониторы.
- Один или несколько Synthetic-enabled ActiveGate'ов формируют private location.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/synthetic-monitoring/private-synthetic-locations/create-a-private-synthetic-location -->

**Capacity-индикация private location** в UI:
- Зелёный — загрузка <80%.
- Жёлтый — >80% или нет failover-резерва.
- Красный — >90% или часть мониторов уже не запускается.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/synthetic-monitoring/private-synthetic-locations/manage-private-synthetic-locations -->

*Ограничение.* Если только один ActiveGate (например, в одном ЦОД), synthetic видит доступность приложения только оттуда. Падение сети между ЦОД-1 и ЦОД-2 не обнаружится — synthetic «не пробивает» между ними.

*Рекомендация.* Минимум 2 Synthetic-enabled ActiveGate в разных зонах (основной + резервный ЦОД). Мониторы настраиваются «с обеих локаций» — видна и доступность приложения, и межсайтовая связность.

### Алертинг через Alerting profiles

Synthetic-проблемы — это обычные Davis Problems, подчиняются общим правилам alerting profiles (Тема 7). Типовая настройка:

- Profile `synthetic-critical-uptime`.
- Filter: monitor type = synthetic AND monitor name IN (`prod-auth-monitor`, `prod-payment-monitor`, `prod-login-monitor`).
- Severity: Critical.
- Routing: PagerDuty → on-call team.

Это независимый алерт-канал «сайт упал с точки зрения робота», не зависит от наличия реального трафика.

### SLI / SLO через Synthetic

Synthetic — идеальный источник данных для SLO:

- **Availability SLO.** HTTP monitor `prod-login` имеет availability ≥ 99.9% за месяц.
- **Latency SLO.** Browser monitor `prod-checkout-flow` выполняется за ≤ 5 сек на 95-м перцентиле.

Настройка SLO разобрана в Дне 3-4, Тема 11. Synthetic-метрики как SLI — преимущество: данные стабильные и воспроизводимые, в отличие от RUM, где среднее зависит от состава пользователей.

### Ограничения Synthetic

- **Не заменяет функциональные тесты.** Synthetic проверяет «страница открывается, кнопка кликается», не «логика бизнес-процесса корректна». Для последнего — QA-автотесты.
- **Не масштабируется.** Нельзя заменить нагрузочное тестирование — каждый монитор максимум 1 запуск в минуту.
- **Зависит от тестовых кредов.** Browser monitor для логина требует хранения пароля в credential vault. Управление — отдельная операционная задача.
- **Ложные срабатывания.** Маркетологи поменяли CSS-селектор кнопки — robot не нашёл, считает fail. Browser monitors требуют поддержки, как обычный QA-код.

### Типичный набор synthetic

**HTTP monitors** (высокая частота, низкая цена):

- Health endpoints каждого сервиса (каждую минуту).
- TLS-сертификаты (каждый час, проверка срока истечения).
- DNS resolution (каждые 5 минут).

**Multi-step HTTP monitors** (средняя частота):

- Authentication flow (каждые 5 минут).
- Ключевые API-сценарии: получение данных, создание записи, отмена.

**Browser monitors** (низкая частота, высокая цена):

- Login + главная (каждые 15 минут).
- Критичный end-to-end сценарий (каждые 30 минут).
- Проверка мобильного веб-интерфейса (каждые 30 минут).

Общая нагрузка: ~200-300 monitor executions в час, 1 ActiveGate справляется.

### Почему 403 на captured-тенанте

Тенант `guu84124` для учебных целей, на этом окружении доступ к Synthetic закрыт (страница `/ui/synthetic` отдаёт 403). В Managed Dynatrace функциональность Synthetic — отдельный лицензируемый модуль; если модуль на тенанте не активирован или роль пользователя не имеет прав на Synthetic-зону, страница UI возвращает 403.

На боевом Managed-тенанте, где модуль активирован, доступ настраивается через IAM на уровне Management zones и Permissions. Скриншот этой страницы для учебника снимается **в empty_screens_todo.md** как известный gap captured-тенанта (см. ниже).

### Ключевые термины

- **Synthetic Monitoring** — проактивное тестирование роботами по расписанию.
- **HTTP monitor** — простая проверка одного URL.
- **Browser monitor** — сценарий с headless-браузером.
- **Multi-step HTTP monitor** — цепочка HTTP-запросов.
- **ActiveGate Synthetic role** — роль ActiveGate'а для запуска мониторов.
- **Outage** — падение монитора (global / local).
- **Consecutive failures** — количество fail'ов для срабатывания alert.
- **Retry policy** — сколько раз повторить перед finaл fail.
