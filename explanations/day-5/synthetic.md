> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 6 из 10: «Synthetic Monitoring: HTTP, Browser, браузерные шаги»

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

На живом Managed-тенанте здесь список всех настроенных synthetic-мониторов:

- **HTTP monitors** — простые проверки одного URL через HTTP(S) каждые N минут. Пример: «каждую минуту бить в `https://example.com/health`, ожидать 200 OK с текстом `"status":"ok"`, за максимум 2 секунды». Метрики монитора:
  - **Availability** — процент успешных проверок за период.
  - **Response time** — медиана, перцентили.
  - **Location** — с какой точки проверялось (для географического анализа).

- **Browser monitors** — сложные сценарии. Робот-браузер открывает сайт, кликает кнопки, заполняет формы, проверяет результат. Пример: «открой `example.com`, нажми Login, введи тестовые креды, проверь, что попал на главную, выйди». End-to-end сценарии.

- **Multi-step HTTP monitors** — цепочки HTTP-запросов для API: `GET /auth` → `POST /login` с token из предыдущего → `GET /user/profile` с session cookie. Проверяет работу API-цепочки.

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

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Synthetic Monitoring](https://docs.dynatrace.com/docs/shortlink/synthetic-monitoring)

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

**HTTP monitor** — минимальный:
- Один HTTP-запрос (GET, POST, PUT, …).
- Запускается с ActiveGate (любого, где включена роль Synthetic).
- Проверки: HTTP code, time до first byte, content matching.
- Частота: от 1 минуты до 60 минут.
- **Use case**: health check endpoint-ов, API доступность.

**Browser monitor (Classic)** — полная симуляция пользователя:
- Запускается headless-браузер (Chromium).
- Выполняет сценарий: клики, ввод, проверки.
- Проверяет все ресурсы страницы (HTML, CSS, JS, картинки), все XHR-запросы.
- Метрики: Visually Complete, Speed Index, Page Load Time.
- Частота: от 5 минут до 60 минут (дороже HTTP, ресурсы браузера).
- **Use case**: end-to-end функциональные сценарии (login, поиск, корзина, оплата).

**Multi-step HTTP monitor** — цепочка API-запросов:
- Несколько HTTP-шагов, каждый зависит от предыдущего.
- Поддерживает extract variable → use in next step (например, извлечь `accessToken` из ответа login и использовать в следующем запросе).
- **Use case**: end-to-end API-сценарии (authenticate → fetch → update → logout).

### Где запускаются synthetic мониторы

- **В облачной Dynatrace** — на глобальной сети Dynatrace Cluster Synthetic (Frankfurt, Mumbai, Sydney и др.).
- **В Managed air-gapped** — только с ваших ActiveGate с включённой ролью Synthetic.

*Ограничение.* Если только один ActiveGate (например в одном ЦОД), synthetic видит доступность приложения только оттуда. Падение сети между ЦОД-1 и ЦОД-2 не обнаружится — synthetic «не пробивает» между ними.

*Рекомендация.* Минимум 2 ActiveGate в разных зонах (основной + резервный ЦОД), на каждом — роль Synthetic. Мониторы настраиваются «с обеих локаций» — видна и доступность приложения, и межсайтовая связность.

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

Тенант `guu84124` для учебных целей, лицензии на Synthetic Monitoring на нём нет. В Managed Dynatrace лицензия продаётся отдельными модулями: Infrastructure, APM, Frontend (RUM), Synthetic, AppSec, Log Management. Если модуль не куплен — страницы UI недоступны с HTTP 403.

На боевом тенанте модуль Synthetic обычно в лицензии. Доступ настраивается через IAM на уровне Management zones и Permissions.

### Ключевые термины

- **Synthetic Monitoring** — проактивное тестирование роботами по расписанию.
- **HTTP monitor** — простая проверка одного URL.
- **Browser monitor** — сценарий с headless-браузером.
- **Multi-step HTTP monitor** — цепочка HTTP-запросов.
- **ActiveGate Synthetic role** — роль ActiveGate'а для запуска мониторов.
- **Outage** — падение монитора (global / local).
- **Consecutive failures** — количество fail'ов для срабатывания alert.
- **Retry policy** — сколько раз повторить перед finaл fail.
