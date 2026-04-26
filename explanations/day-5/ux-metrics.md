> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 2 из 10: «Метрики UX: Apdex и другие показатели качества»

## 📍 КАРТА — три страницы про метрики пользовательского опыта

Термины темы: `Apdex / индекс удовлетворённости` (0.0-1.0), `Satisfied / Tolerating / Frustrated` — три зоны классификации, `Core Web Vitals / LCP / FID / INP / CLS`, `Rage click / раздражённый клик`, `Dead click / клик без реакции`, `Conversion / достижение бизнес-цели`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Applications (список с UX-метриками) | **Application Observability → Frontend → Applications** | `https://guu84124.live.dynatrace.com/ui/applications` |
| User experience score (настройка порогов Apdex) | **Settings → Web and mobile monitoring → User experience score** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.user-experience-score` |
| Usability analytics (фильтры раздражителей) | **Settings → Web and mobile monitoring → Usability analytics** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:usability-analytics` |

---

## 🎬 Работа с UX-метриками на трёх экранах

### Шаг 1 — Applications (список приложений с UX-метриками)

![Applications — список приложений с UX-метриками](screenshots/day-5/ux-metrics/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/applications`.

*На captured-экране* видна плашка «Connection issues — trying to reconnect» с кнопками `Try to restore connection now` и `Try again`. Стандартное поведение захваченной страницы: SPA-UI пытается подключиться к WebSocket backend для подгрузки данных, в статическом дампе соединения нет.

**На живом тенанте** — список RUM-приложений, строка на каждое:

- **Name** — имя приложения (auto-detected или заданное через rules — разбирается в Теме 5).
- **Apdex** — индекс удовлетворённости (0.0-1.0), динамика за период.
- **User actions per minute** — скорость действий.
- **Response time median** — медианное время отклика user actions.
- **JS errors** — процент user actions с JavaScript-ошибками.
- **Problems** — сколько проблем Davis зарегистрировал против приложения.

Сверху **Global Filter panel** — фильтры по management zone, application type, времени.

Клик по строке открывает карточку приложения: графики, список user actions по типам, топ проблем, география пользователей.

### Шаг 2 — User experience score (настройка порогов Apdex)

![User experience score — настройка порогов Apdex](screenshots/day-5/ux-metrics/settings/builtinrum.user-experience-score/User-experience-score-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.user-experience-score`.

*Что настраивает.* Пороги, по которым user action классифицируется как Satisfied / Tolerating / Frustrated.

*Формула.* Если время ≤ T → Satisfied, T < время ≤ 4T → Tolerating, время > 4T → Frustrated.

**Web actions:**

- **Page load** — загрузка полной страницы. Дефолт 3 секунды.
- **XHR action** — AJAX-запрос. Дефолт 1 секунда.
- **Route change** — SPA-переход без полной перезагрузки. Дефолт 1 секунда.

**Mobile actions:**

- **App start** — холодный запуск приложения. Дефолт 2 секунды.
- **Custom action** — ручная разметка через Mobile SDK (`enterAction`). Дефолт 1 секунда.
- **Web request** — HTTP-запрос из мобильного приложения. Дефолт 1 секунда.

*Когда менять дефолты.* 3 секунды для page load — мировой стандарт для публичных сайтов. Для внутренних приложений (корпоративный портал, ДБО внутри офиса) это слишком мягко — локальная сеть без задержек интернета. Можно ужесточить до 1.5 секунды — Apdex станет ниже, но точнее отразит проблемы, видимые реальным пользователям.

### Шаг 3 — Usability analytics (аналитика раздражителей)

![Usability analytics — аналитика пользовательских раздражителей](screenshots/day-5/ux-metrics/settings/builtinusability-analytics/Usability-analytics-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:usability-analytics`.

*Что настраивает.* Дополнительные метрики оценки качества взаимодействия. Классические «раздражающие паттерны» из UX-исследований:

- **Rage clicks** — серия кликов по одному элементу с интервалом меньше 1 сек. Означает «жму, ничего не происходит». Типично на «зависшей» кнопке.
- **Dead clicks** — клик по элементу, не зарегистрировавшему действия. Кнопка задизейблена, обработчик сломан.
- **Error clicks** — клик, за которым сразу появилось сообщение об ошибке.
- **Slow activity** — user action со временем в 4+ раза больше среднего на приложении.
- **Conversions** — достижение бизнес-цели (покупка, регистрация, отправка заявки). Настраивается через user action rules.

**Где эти метрики появляются:**

- Фильтр `Errors and annoyances` в user sessions list (видели в Теме 1).
- Графики карточки приложения.

Они отвечают не на «быстро ли грузится», а на «удобно ли пользоваться».

*Пример.* Пользователь заполняет форму перевода, жмёт «Подтвердить», 5 секунд ничего не происходит. Кнопка не задизейблилась, он жмёт ещё раз, и ещё. Dynatrace регистрирует **rage click**. Сигнал UX-команде: кнопка работает, логика работает, пользователь страдает из-за отсутствия индикации загрузки.

---

## 🎓 ТЕОРИЯ — количественная UX-аналитика

> 📚 **Источники (официальная документация Dynatrace):**
>
> - [Real User Monitoring — метрики UX](https://docs.dynatrace.com/docs/shortlink/rum)

### Зачем нужны UX-метрики

Чтобы разговор с бизнесом на общем языке. Фраза разработчика «API отвечает за 200 мс» бизнесу ничего не говорит. Фраза «Apdex упал с 0.92 до 0.71, 30% пользователей теперь испытывают frustration» — конкретная и действенная.

UX-метрики — это мост между техническими показателями (response time, error rate) и бизнес-результатами (retention, conversion, NPS).

### Apdex — индустриальный стандарт

Apdex разработан в 2004 году консорциумом Apdex Alliance (Compuware, HP, Mercury, и др.), стал стандартом в мире APM. Формула:

```
Apdex = (Satisfied + 0.5 × Tolerating) / Total
```

- 1.0 — идеально, все пользователи в зоне Satisfied.
- 0.85+ — «Excellent» (индустриальный порог для критичных приложений).
- 0.70–0.85 — «Good».
- 0.50–0.70 — «Fair».
- < 0.50 — «Poor».

**Пороги зависят от типа приложения.** Для системы аналитики 5 секунд на загрузку — норма, для платёжного виджета на кассе магазина — катастрофа. Поэтому Dynatrace позволяет задавать пороги индивидуально для каждого приложения через override на уровне application settings.

### Core Web Vitals — Google-стандарт

Параллельно с Apdex есть метрики Google, встроенные в браузерный API и обязательные для ранжирования в поиске:

- **LCP (Largest Contentful Paint)** — время до появления самого крупного элемента на экране. Хорошо: <2.5 сек. Плохо: >4 сек.
- **FID (First Input Delay) / INP (Interaction to Next Paint)** — время отклика на первый или самый долгий клик. Хорошо: <100 мс. Плохо: >300 мс.
- **CLS (Cumulative Layout Shift)** — насколько «дёргается» вёрстка при загрузке. Хорошо: <0.1. Плохо: >0.25.

**Dynatrace собирает их автоматически**, они видны в разделе Performance карточки приложения и в Data Explorer как `dt.rum.web.vitals.*` метрики.

### Apdex vs Web Vitals — что выбирать

- **Apdex** — агрегированная метрика для бизнеса и SLA. Удобна для дашбордов «как в целом себя чувствует приложение».
- **Web Vitals** — технические метрики для инженеров. Удобны для оптимизации («надо ускорить LCP с 3.8 до 2.5»).

В банке принято мониторить оба:
- Apdex — на дашборде для руководства, таргет >0.85 для ДБО.
- Web Vitals — для frontend-команды, таргет LCP <2.5 сек на 75-м перцентиле.

### Rage clicks — психология пользователя

Rage click — самый «эмоциональный» сигнал. Он говорит не про производительность (страница грузится за 200 мс), а про **недостаток обратной связи в UI**. Пользователь не видит, что его клик принят, поэтому жмёт ещё и ещё.

Лечится не оптимизацией бэкенда, а UX-паттерном:
- Задизейблить кнопку сразу после клика.
- Показать спиннер на самой кнопке.
- Воспроизвести лёгкий haptic feedback (на мобилке).

Dynatrace rage clicks не делают приложение быстрее, но заставляют команду фронта серьёзно относиться к loading states. Это один из инструментов, который из RUM превращает Dynatrace в UX-платформу.

### Conversions — связь с бизнесом

Conversion — самый важный показатель из этого набора. Настраивается через user action rules: какое конкретное действие считается «успехом» (клик по кнопке «Оплатить» с последующим HTTP 200, переход на страницу «Спасибо», факт успешного логина).

Далее Dynatrace показывает:
- **Conversion rate** — процент сессий, в которых была конверсия.
- **Drop-off points** — на каком шаге funnel пользователи уходят (разберём в Теме 3).
- **Correlation with errors** — сколько конверсий сорвано из-за JS-ошибок и slow actions.

Это связывает технические проблемы с бизнес-потерями: «из-за одного слабого звена в backend мы потеряли 800 потенциальных оплат за сутки».

### Типичный SLO по UX

Формулировка SLO для фронтенда критичного приложения:

- **Availability.** >99.9% user actions завершаются без JS-errors и network failures.
- **Performance.** Apdex ≥ 0.85 на 95% интервалов по 5 минут.
- **Web Vitals.** LCP < 2.5 сек на 75-м перцентиле.
- **Business.** Conversion rate по ключевой операции ≥ 98% (2% допустимых fail — технические ретраи).

При нарушении любого SLO создаётся инцидент, анализируется причина, планируется исправление.

### Ключевые термины

- **Apdex (Application Performance Index)** — индекс удовлетворённости, 0.0–1.0.
- **Satisfied / Tolerating / Frustrated** — три зоны по времени отклика.
- **Core Web Vitals** — метрики Google: LCP, FID/INP, CLS.
- **Rage click** — серия раздражённых кликов по одному элементу.
- **Dead click** — клик без реакции.
- **Conversion** — достижение бизнес-цели в сессии.
- **SLO (Service Level Objective)** — формальный таргет по показателю, который команда обязуется держать.
