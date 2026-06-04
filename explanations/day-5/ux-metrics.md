> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 2 из 10: «Метрики UX: Apdex и другие показатели качества»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/applications -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Apdex ratings](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings)
> - [User experience score](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/user-experience-score)
> - [Scores and ratings (overview)](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings)
> - [User actions](https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/user-actions)
> - [Real User Monitoring (RUM)](https://docs.dynatrace.com/managed/shortlink/rum)

## 📍 КАРТА: три страницы про метрики пользовательского опыта

Термины темы: `Apdex / индекс удовлетворённости` (0.0-1.0), `Satisfied / Tolerating / Frustrated`: три зоны классификации, `Core Web Vitals / LCP / FID / INP / CLS`, `Rage click / раздражённый клик`, `Dead click / клик без реакции`, `Conversion / достижение бизнес-цели`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Applications (список с UX-метриками) | **Application Observability → Frontend → Applications** | `https://guu84124.live.dynatrace.com/ui/applications` |
| User experience score (настройка порогов Apdex) | **Settings → Web and mobile monitoring → User experience score** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.user-experience-score` |
| Usability analytics (фильтры раздражителей) | **Settings → Web and mobile monitoring → Usability analytics** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:usability-analytics` |

---

## 🎬 Работа с UX-метриками на трёх экранах

### Шаг 1: Applications (список приложений с UX-метриками)

![Applications: список приложений с UX-метриками](screenshots/day-5/ux-metrics/applications/Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/applications`.

*На captured-экране* видна плашка «Connection issues: trying to reconnect» с кнопками `Try to restore connection now` и `Try again`. Стандартное поведение захваченной страницы: SPA-UI пытается подключиться к WebSocket backend для подгрузки данных, в статическом дампе соединения нет.

**На живом тенанте**: список RUM-приложений, строка на каждое:

- **Name**: имя приложения (auto-detected или заданное через rules: разбирается в Теме 5).
- **Apdex**: индекс удовлетворённости (0.0-1.0), динамика за период.
- **User actions per minute**: скорость действий.
- **Response time median**: медианное время отклика user actions.
- **JS errors**: процент user actions с JavaScript-ошибками.
- **Problems**: сколько проблем Davis зарегистрировал против приложения.

Сверху **Global Filter panel**: фильтры по management zone, application type, времени.

Клик по строке открывает карточку приложения: графики, список user actions по типам, топ проблем, география пользователей.

### Шаг 2: User experience score (настройка порогов Apdex и UX-score)

![User experience score: настройка порогов Apdex](screenshots/day-5/ux-metrics/settings/builtinrum.user-experience-score/User-experience-score-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:rum.user-experience-score`.

*Что настраивает.* На этой странице задаются:
1. **Action-level пороги Apdex**: по ним каждое действие классифицируется как Satisfied / Tolerating / Frustrated.
2. **Session-level пороги User experience score**: по ним сессия целиком классифицируется как Satisfying / Tolerable / Frustrating (детали в ТЕОРИИ).

*Формула Apdex.* Порог T задаёте вы. ЕСЛИ время действия ≤ T → ТО действие Satisfied; ЕСЛИ T < время ≤ 4T → ТО Tolerating; ЕСЛИ время > 4T → ТО Frustrated. То есть граница «терпимого», это всегда 4T: поставите T = 1 сек → действия дольше 4 сек считаются Frustrated, поставите T = 0.5 сек → уже всё дольше 2 сек. Стандарт Apdex Alliance.

**Типы action, для которых задаются пороги (по captured-странице):**

- **Web**: Page load (загрузка полной страницы), XHR action (AJAX-вызов), Route change (SPA-переход без полной перезагрузки).
- **Mobile**: App start (холодный запуск приложения), Custom action (через Mobile SDK), Web request (HTTP-запрос из мобильного приложения).

Конкретные значения по умолчанию настраиваются на самой странице и могут отличаться от тенанта к тенанту; типично page load измеряется в секундах, XHR / route change / web request: в десятых долях секунды.

*Когда менять дефолты.* Для публичных сайтов с пользователями в открытом интернете обычно используют более мягкие пороги. Для внутренних приложений (корпоративный портал, ДБО внутри офиса) часто ужесточают: локальная сеть без задержек интернета означает, что задержка в 2 секунды у внутреннего пользователя, это уже плохо. Apdex станет ниже, но точнее отразит проблемы, видимые реальным пользователям.

### Шаг 3: Usability analytics (аналитика раздражителей)

![Usability analytics: аналитика пользовательских раздражителей](screenshots/day-5/ux-metrics/settings/builtinusability-analytics/Usability-analytics-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:usability-analytics`.

*Что настраивает.* Дополнительные метрики оценки качества взаимодействия. Классические «раздражающие паттерны» из UX-исследований:

- **Rage clicks**: серия кликов по одному элементу с интервалом меньше 1 сек. Означает «жму, ничего не происходит». Типично на «зависшей» кнопке.
- **Dead clicks**: клик по элементу, не зарегистрировавшему действия. Кнопка задизейблена, обработчик сломан.
- **Error clicks**: клик, за которым сразу появилось сообщение об ошибке.
- **Slow activity**: user action со временем в 4+ раза больше среднего на приложении.
- **Conversions**: достижение бизнес-цели (покупка, регистрация, отправка заявки). Настраивается через user action rules.

**Где эти метрики появляются:**

- Фильтр `Errors and annoyances` в user sessions list (видели в Теме 1).
- Графики карточки приложения.

Они отвечают не на «быстро ли грузится», а на «удобно ли пользоваться».

*Пример.* Пользователь заполняет форму перевода, жмёт «Подтвердить», 5 секунд ничего не происходит. Кнопка не задизейблилась, он жмёт ещё раз, и ещё. Dynatrace регистрирует **rage click**. Сигнал UX-команде: кнопка работает, логика работает, пользователь страдает из-за отсутствия индикации загрузки.

---

## 🎓 ТЕОРИЯ: количественная UX-аналитика

### Зачем нужны UX-метрики

Чтобы разговор с бизнесом на общем языке. Фраза разработчика «API отвечает за 200 мс» бизнесу ничего не говорит. Фраза «Apdex упал с 0.92 до 0.71, 30% пользователей теперь испытывают frustration»: конкретная и действенная.

UX-метрики, это мост между техническими показателями (response time, error rate) и бизнес-результатами (retention, conversion, NPS).

### Apdex: индустриальный стандарт

Apdex (Application Performance Index): индустриальный стандарт, ставший общеупотребимым в мире APM. Формула на user-action уровне:

```
Apdex = (Satisfied + 0.5 × Tolerating) / Total
```

User actions с JavaScript-ошибками автоматически попадают в **Frustrated** независимо от времени отклика. Итоговый Apdex score, это число от 0.0 до 1.0; в Dynatrace для него используется пятиуровневая шкала качества:

- **Excellent**: 0.94–1.0
- **Good**: 0.85–0.94
- **Fair**: 0.7–0.85
- **Poor**: 0.5–0.7
- **Unacceptable**: < 0.5

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/apdex-ratings -->

**Пороги зависят от типа приложения.** Для системы аналитики 5 секунд на загрузку: норма, для платёжного виджета на кассе магазина: катастрофа. Поэтому Dynatrace позволяет задавать пороги индивидуально для каждого приложения через override на уровне application settings.

### User experience score: на уровне сессии

Параллельно action-уровневому Apdex существует **session-level User Experience Score**, который классифицирует сессию целиком как **Satisfying / Tolerable / Frustrating**. Формирование score устроено через веса элементов сессии:

| Элемент сессии | Вес |
|---|---|
| User action | 3 |
| Error | 1 (Frustrating) |
| Rage event | 2 (Frustrating) |
| Crash | 5000 (Frustrating) |

Каждый элемент классифицируется как Satisfying / Tolerable / Frustrating, дальше Dynatrace сравнивает суммарный вес frustrating-элементов с настраиваемым порогом frustration. Жёсткое правило: если в сессии есть хотя бы один Frustrating-элемент с большим весом (например, crash), сессия не может быть Satisfying. Пороги настраиваются отдельно для web, mobile и custom приложений.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/rum-concepts/scores-and-ratings/user-experience-score -->

### Core Web Vitals: Google-стандарт

Параллельно с Apdex есть метрики Google, встроенные в браузерный API:

- **LCP (Largest Contentful Paint)**: время до появления самого крупного элемента на экране. Доступен в Chromium-браузерах через Google-предоставленный API; для других браузеров Dynatrace использует собственную метрику Visually complete.
- **Метрика отзывчивости на ввод**: FID (First Input Delay) в более старых версиях Web Vitals и INP (Interaction to Next Paint) в актуальных, заменивший FID в стандарте Google.
- **CLS (Cumulative Layout Shift)**: насколько «дёргается» вёрстка при загрузке.

Конкретные «хорошо/плохо» пороги устанавливаются Google и регулярно меняются: их следует уточнять в актуальной редакции Web Vitals. **Dynatrace собирает эти метрики автоматически** в составе RUM JavaScript, они видны в карточке приложения и в Data Explorer.

### Apdex vs Web Vitals: что выбирать

- **Apdex**: агрегированная метрика для бизнеса и SLA. Удобна для дашбордов «как в целом себя чувствует приложение».
- **Web Vitals**: технические метрики для инженеров. Удобны для оптимизации («надо ускорить LCP с 3.8 до 2.5»).

В банке принято мониторить оба:
- Apdex: на дашборде для руководства, таргет >0.85 для ДБО.
- Web Vitals: для frontend-команды, таргет LCP <2.5 сек на 75-м перцентиле.

### Rage clicks: психология пользователя

Rage click: самый «эмоциональный» сигнал. Он говорит не про производительность (страница грузится за 200 мс), а про **недостаток обратной связи в UI**. Пользователь не видит, что его клик принят, поэтому жмёт ещё и ещё.

Лечится не оптимизацией бэкенда, а UX-паттерном:
- Задизейблить кнопку сразу после клика.
- Показать спиннер на самой кнопке.
- Воспроизвести лёгкий haptic feedback (на мобилке).

Dynatrace rage clicks не делают приложение быстрее, но заставляют команду фронта серьёзно относиться к loading states. Это один из инструментов, который из RUM превращает Dynatrace в UX-платформу.

### Conversions: связь с бизнесом

Conversion: самый важный показатель из этого набора. Настраивается через user action rules: какое конкретное действие считается «успехом» (клик по кнопке «Оплатить» с последующим HTTP 200, переход на страницу «Спасибо», факт успешного логина).

Далее Dynatrace показывает:
- **Conversion rate**: процент сессий, в которых была конверсия.
- **Drop-off points**: на каком шаге funnel пользователи уходят (разберём в Теме 3).
- **Correlation with errors**: сколько конверсий сорвано из-за JS-ошибок и slow actions.

Это связывает технические проблемы с бизнес-потерями: «из-за одного слабого звена в backend мы потеряли 800 потенциальных оплат за сутки».

### Типичный SLO по UX

Пример формулировки SLO для фронтенда критичного приложения (значения подбираются под бизнес-задачу, ниже: иллюстрация):

- **Availability.** Доля user actions без JS-errors и network failures выше целевого уровня (для ДБО обычно ставят строгий target, разбор в Теме про SLI/SLO/SLA).
- **Performance.** Apdex score > 0.85 на основной массе временных интервалов.
- **Web Vitals.** LCP < 2.5 сек, CLS и INP в пределах рекомендованных Google значений, всё на 75-м перцентиле.
- **Business.** Conversion rate по ключевой операции выше целевого уровня (часть fail-ов: технические ретраи).

SLO-плитка на дашборде показывает три поля: **Status**, **Error budget** (остаток допустимых сбоев) и **Target**. Если включён burn rate и он выше 1, перед значением Error budget появляется цветной индикатор статуса. Burn rate > 1 означает, что бюджет ошибок тратится быстрее запланированного и до конца окна оценки его не хватит.

Пример с числами (иллюстрация, значения произвольные): target 99.5%, текущий статус 99.7%. При включённой нормализации остаток бюджета считается той же формулой, что в Теме про SLI/SLO/SLA: `(статус − target) ÷ (100 − target) × 100` = `(99.7 − 99.5) ÷ (100 − 99.5) × 100` = **40%**. То есть до срыва SLO ещё 40% допустимых сбоев. ЕСЛИ статус опустится до 99.6% → ТО остаток упадёт до 20%, и плитка перейдёт в Warning раньше фактического нарушения. <!-- last-verified: 2026-06-04 source: https://docs.dynatrace.com/managed/deliver/service-level-objectives-classic/slo-basics -->

ЕСЛИ Availability опустится ниже target (бюджет ошибок исчерпан) → ТО SLO переходит в нарушение, заводится инцидент, анализируется причина, планируется исправление. ЕСЛИ бюджет ещё есть, но burn rate высокий → ТО это ранний сигнал риска до фактического нарушения.

### Ключевые термины

- **Apdex (Application Performance Index)**: индекс удовлетворённости, 0.0–1.0.
- **Satisfied / Tolerating / Frustrated**: три зоны по времени отклика.
- **Core Web Vitals**: метрики Google: LCP, FID/INP, CLS.
- **Rage click**: серия раздражённых кликов по одному элементу.
- **Dead click**: клик без реакции.
- **Conversion**: достижение бизнес-цели в сессии.
- **SLO (Service Level Objective)**: формальный таргет по показателю, который команда обязуется держать.
