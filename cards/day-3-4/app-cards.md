---
topic_id: app-cards
day_id: day-3-4
timing_min: 26
verified: 2026-07-12
---
## ГДЕ
Три страницы про метрики UX.
Список приложений: Application Observability → Frontend, route `/ui/applications`.
User experience score: Settings → Web and mobile monitoring → User experience score, route `/ui/settings/builtin:rum.user-experience-score`.
Usability analytics: Settings → Web and mobile monitoring → Usability analytics, route `/ui/settings/builtin:usability-analytics`.

## ЗАЧЕМ
Метрики приложения читаются тремя слоями: Performance (чистая скорость: page load, LCP, INP, CLS), User behaviour (что делает пользователь: клики, конверсия, длительность сессии), UX quality (качественные сигналы: Apdex, User experience score, rage/dead/error clicks).
Один слой обманчив: страница грузится быстро, а пользователь всё равно уходит. Apdex и User experience score сводят опыт в один индекс, Usability analytics ловит то, что через скорость не видно.

## ЦИФРЫ
- Apdex: одно число от 0 до 1, пять уровней (Excellent 0.94-1.0 / Good 0.85-0.94 / Fair 0.7-0.85 / Poor 0.5-0.7 / Unacceptable <0.5), считается на уровне действий.
- User experience score: три категории на уровне сессии (Satisfactory / Tolerable / Frustrating), в отличие от пятиуровневого Apdex на уровне действий; учитывает не только скорость, но и ошибки, rage clicks, поведение.
- Core Web Vitals, три показателя: LCP, INP (заменил FID), CLS.
- Usability analytics, четыре сигнала: rage clicks, dead clicks, error clicks, session length anomalies; у каждого свой порог и тумблер включения.
- Пример разбора платёжного пути: page load 2 секунды (не медленно), успешные оплаты за час упали в 2 раза, rage clicks на кнопке выросли в 10 раз (пример из курса, у вашего тенанта цифры будут другими).

## ЕСЛИ→ТО
- ЕСЛИ page load в норме (в примере 2 секунды), но оплаты упали в 2 раза и rage clicks выросли в 10 раз → проблема не в скорости, а в кнопке (JS-ошибка): иду в анализ JS-ошибок и, если включён, в Session Replay.
- ЕСЛИ у приложения хороший Apdex по скорости, но много rage/dead/error clicks → User experience score всё равно падает: Apdex видит только скорость, UX score добавляет ошибки и поведение.
- ЕСЛИ путь критичный (оформление кредита, перевод, оплата) → включаю Usability analytics и задаю порог rage (сколько кликов за сколько секунд), чтобы поймать UX-проблемы, невидимые через метрики скорости.

## ЗАПАСНОЙ ПЛАН
На демо-тенанте центр списка Applications часто пустой или показывает Connection issues (нет активных RUM-приложений): показываю карточку приложения по снимку из курса, проговариваю Apdex, Response time, Core Web Vitals, Distribution по браузерам и странам.
Страницы User experience score и Usability analytics без write-прав открываю на чтение: показываю, какие факторы, веса и пороги настраиваются, ничего не меняю.
Конкретные пороги классификации по памяти сверх снимка не называю, отсылаю к значениям на самой странице тенанта.

## ВОПРОСЫ АУДИТОРИИ
- «Чем Apdex отличается от User experience score?» Ответ: Apdex меряет только скорость (0-1, пять уровней, на уровне действий), а User experience score добавляет ошибки, rage clicks и поведение и делит сессии на Satisfactory / Tolerable / Frustrating.
- «Работает ли расчёт этих метрик в закрытом контуре?» Ответ: да, всё считается в кластере на данных RUM-сниппетов, внешних вызовов нет, нужно лишь, чтобы браузеры пользователей достучались до ActiveGate (обычно через опубликованный DMZ).
- «Зачем rage/dead/error clicks, если есть метрики скорости?» Ответ: они ловят UX-проблемы, невидимые по скорости, например кнопка оплаты не срабатывает при нормальном page load, и пользователь кликает много раз и уходит без оплаты.
