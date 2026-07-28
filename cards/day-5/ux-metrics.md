---
topic_id: ux-metrics
day_id: day-5
timing_min: 25
verified: 2026-07-12
---
## ГДЕ
Три живых экрана.
Список приложений с UX-метриками: Application Observability → Frontend → Applications, route `/ui/applications`.
Пороги Apdex и session-score: Settings → Web and mobile monitoring → User experience score, route `/ui/settings/builtin:rum.user-experience-score`.
Раздражители (rage clicks) и conversions: Settings → Web and mobile monitoring → Usability analytics, route `/ui/settings/builtin:usability-analytics`.

## ЗАЧЕМ
UX-метрики это мост между техникой (response time, error rate) и бизнесом (retention, conversion): дают общий язык с бизнесом.
Фраза «Apdex упал с 0.92 до 0.71, 30% пользователей во frustration» действеннее, чем «API отвечает за 200 мс».
Три экрана: готовые UX-метрики в списке приложений, настройка порогов Apdex и score сессии, включение метрик раздражения.

## ЦИФРЫ
- Apdex: одно число 0.0-1.0, шкала из 5 уровней (Excellent 0.94-1.0 / Good 0.85-0.94 / Fair 0.7-0.85 / Poor 0.5-0.7 / Unacceptable <0.5).
- Формула на уровне действия: `Apdex = (Satisfied + 0.5 × Tolerating) / Total`; действия с JS-ошибкой сразу во Frustrated.
- Зоны по времени: ≤ T это Satisfied, от T до 4T это Tolerating, больше 4T это Frustrated. Порог T задаёте вы: T = 1 сек значит Frustrated дольше 4 сек, T = 0.5 сек значит дольше 2 сек.
- User experience score сессии считается из весов: User action 3, Error 1, Rage event 2, Crash 5000.
- Rage click: серия быстрых кликов по одному элементу (точные пороги детекции в доке не зафиксированы); conversions настраиваются в приложении (Behavior analytics → Conversion goals).
- Web Vitals это LCP / INP / CLS (FID устарел, заменён INP); типовой таргет ДБО: Apdex > 0.85, LCP < 2.5 сек на 75-м перцентиле.

## ЕСЛИ→ТО
- ЕСЛИ время действия ≤ T → Satisfied; ЕСЛИ от T до 4T → Tolerating; ЕСЛИ больше 4T → Frustrated (граница терпимого всегда 4T).
- ЕСЛИ у user action есть JS-ошибка → действие уходит во Frustrated независимо от времени отклика.
- ЕСЛИ в сессии есть Frustrating-элемент с большим весом (crash, вес 5000) → сессия уже не может стать Satisfying.
- ЕСЛИ кнопка не даёт обратной связи и пользователь жмёт снова и снова → Dynatrace ловит rage click; чинится UX-паттерном (задизейблить кнопку, спиннер на кнопке), не оптимизацией бэкенда.

## ЗАПАСНОЙ ПЛАН
На демо-тенанте список приложений может отдавать плашку «Connection issues: trying to reconnect» с кнопками Try to restore connection now и Try again: это ожидаемо для статичного дампа (SPA не достучалась до WebSocket backend), показываю снимок из курса и проговариваю колонки Name, Apdex, User actions per minute, Response time median, JS errors, Problems.
Страницы порогов User experience score и Usability analytics открываю в Settings → Web and mobile monitoring; если они серые без write-прав, конкретные пороги по памяти не называю, проговариваю логику (action-пороги Apdex, session-пороги, rage clicks) и отсылаю к значениям на самой странице тенанта.
Лекторский сценарий: workshop/day-3.md, блок 3. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Чем Apdex отличается от Web Vitals?» Ответ: Apdex это агрегированная метрика для бизнеса и SLA (дашборд руководству), Web Vitals это технические метрики для инженеров (LCP / INP / CLS для оптимизации фронта).
- «Действие быстрое, почему помечено Frustrated?» Ответ: user action с JavaScript-ошибкой автоматически попадает во Frustrated независимо от времени отклика.
- «Rage click это про скорость?» Ответ: нет, это про недостаток обратной связи в UI (пользователь не видит, что клик принят, и жмёт ещё), лечится loading state, а не ускорением бэкенда.
