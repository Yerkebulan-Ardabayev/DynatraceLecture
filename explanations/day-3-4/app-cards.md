> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 7 из 14: «Инфографика приложений: показатели UX и производительности»

## 📍 КАРТА — три страницы про метрики UX

Термины темы: `Apdex / Application Performance Index` (0-1), `UX score / индекс пользовательского опыта`, `Core Web Vitals / LCP / FID / CLS`, `Rage click / злой клик / многократный клик в frustration`, `Dead click / клик по неинтерактивному элементу`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Список Applications | **Application Observability → Frontend** | `https://guu84124.live.dynatrace.com/ui/applications` |
| User experience score | **Settings → Web and mobile monitoring → User experience score** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.user-experience-score` |
| Usability analytics | **Settings → Web and mobile monitoring → Usability analytics** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:usability-analytics` |

---

## 🎬 Работа с метриками приложений на трёх экранах

### Шаг 1 — Applications (список приложений)

![Applications — список веб-приложений под RUM-мониторингом](screenshots/day-3-4/app-cards/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/applications`. Разбирался в Дне 1 (DEM, UI overview). На captured-тенанте центральная область часто пустая или показывает Connection issues — демо без активных RUM-приложений.

**В карточке приложения (в боевом окружении):**

- **Apdex score** — индекс удовлетворённости пользователей (0-1, >0.94 = Excellent).
- **User actions per session** — сколько действий пользователь делает за сессию в среднем.
- **JavaScript errors** — число JS-ошибок и частота.
- **Response time** — медиана и перцентили времени загрузки страницы.
- **Core Web Vitals** — LCP (Largest Contentful Paint), FID (First Input Delay), CLS (Cumulative Layout Shift).
- **Distribution** — по браузерам, странам, устройствам, версиям приложения.

### Шаг 2 — User experience score

![User experience score — настройка расчёта UX-индекса](screenshots/day-3-4/app-cards/settings/builtinrum.user-experience-score/User-experience-score-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:rum.user-experience-score`.

*User experience score* — агрегированная метрика из нескольких факторов пользовательского опыта. Отличие от Apdex: учитывает не только скорость, но и ошибки, rage clicks, другие поведенческие сигналы.

**Что настраивается:**

- Какие факторы учитывать (скорость, ошибки, поведение).
- Веса факторов.
- Пороги для классификации Satisfied / Tolerating / Frustrated.

### Шаг 3 — Usability analytics

![Usability analytics — анализ юзабилити](screenshots/day-3-4/app-cards/settings/builtinusability-analytics/Usability-analytics-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `/ui/settings/builtin:usability-analytics`.

*Usability analytics* — продвинутые сигналы UX:

- **Rage clicks** — пользователь многократно кликает в одно место, признак frustration.
- **Dead clicks** — клики по не-интерактивным элементам.
- **Error clicks** — клики по элементам, после которых возникла ошибка.
- **Session length anomalies** — сессии заметно короче или длиннее обычных.

**На странице:** пороги классификации (сколько кликов за сколько секунд считать rage), включение / выключение каждого сигнала.

*Типовое применение.* Включают для критичных клиентских путей (оформление кредита, перевод, оплата). Сигналы помогают поймать UX-проблемы, невидимые через метрики скорости.

---

## 🎓 ТЕОРИЯ — три слоя метрик приложений

### Слой 1 — Performance metrics

Чисто технические показатели. Page load time, First Contentful Paint, Time to Interactive. Измеряются RUM-сниппетом через Web Performance API браузера. Не зависят от пользовательского поведения.

### Слой 2 — User behaviour metrics

Что делает пользователь на странице. User actions (клики, переходы), bounce rate, conversion rate, session duration. Требуют корректной настройки User Actions (тема key-actions).

### Слой 3 — UX quality metrics

Качественные сигналы. Apdex, User Experience Score, Rage/Dead/Error clicks. Вычисляются на основе первых двух слоёв плюс дополнительных эвристик.

### Как слои работают вместе

*Пример инцидента.* Жалоба «страница платежа тормозит». Инженер смотрит:

1. **Performance** (page load, LCP) — 2 секунды. Не супер медленно.
2. **User behaviour** (успешные payments per hour) — упали в 2 раза.
3. **UX quality** (rage clicks on payment button) — выросли в 10 раз.

*Вывод.* Дело не в скорости. Кнопка payment не срабатывает (JS-ошибка), пользователи кликают много раз, уходят без оплаты. Нужен анализ JS-ошибок и, возможно, Session Replay.

### Air-gapped specifics

Расчёт всех метрик происходит в кластере, на данных от RUM-сниппетов в браузерах. Внешних вызовов нет. Единственное — нужно, чтобы браузеры пользователей могли достучаться до ActiveGate (обычно через опубликованный DMZ).
