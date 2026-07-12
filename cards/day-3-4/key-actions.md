---
topic_id: key-actions
day_id: day-3-4
timing_min: 24
verified: 2026-07-12
---
## ГДЕ
Четыре экрана Settings → Web and mobile monitoring.
User action custom metrics, route `/ui/settings/builtin:user-action-custom-metrics`.
Custom app → Enablement (главный тумблер Custom RUM), route `/ui/settings/builtin:rum.custom.enablement`.
Web → Resource types, route `/ui/settings/builtin:rum.web.resource-types`.
Web → Resource URL cleanup rules, route `/ui/settings/builtin:rum.web.resource-cleanup-rules`.

## ЗАЧЕМ
User actions это базовый слой RUM: клики, переходы, timing каждого действия, из него считаются User experience score, conversions, bounce rate.
Custom metrics это бизнес-слой поверх user actions: вытащить из действия сумму платежа или способ логина и строить бизнес-срезы, доступны в Data Explorer и могут служить SLI.
Resource types и cleanup rules приводят в порядок ресурсы страницы (CSS, JS, картинки, XHR), чтобы статистика загрузки была осмысленной.
Custom RUM через OpenKit закрывает точки контакта без браузера: банкоматы, десктоп кассира, IoT, голосовые интерфейсы.

## ЦИФРЫ
- Три типа user actions Dynatrace распознаёт сам: Load actions (переход и загрузка страницы до onload), XHR actions (запрос через XMLHttpRequest или fetch), Custom actions (создаются через RUM JavaScript API).
- Лимит user action custom metrics считается по enabled: до 500 enabled на окружение, до 100 enabled на приложение.
- Четыре настроечных экрана темы: User action custom metrics, Custom RUM Enablement, Resource types, Resource URL cleanup rules.
- Два механизма для бизнес-данных: Custom metrics (метрики поверх user actions RUM) и Business events (отдельный поток атомарных событий через API).

## ЕСЛИ→ТО
- ЕСЛИ метрику создаёте только сейчас → в неё попадут только новые данные, историю задним числом Dynatrace не пересчитывает (нужны платежи за прошлый месяц, метрику надо было завести месяц назад).
- ЕСЛИ упёрлись в лимит (100 enabled на приложение или 500 на окружение) → освобождаете место: disable снимает метрику со счётчика enabled либо удаляете; свойства созданной метрики менять нельзя, для правки её удаляют и создают заново.
- ЕСЛИ Resource URL cleanup rule не настроено → каждый URL с динамическим суффиксом (main.js?v=8f3a1c, main.js?v=2b9d04) Dynatrace считает отдельным ресурсом, среднее время загрузки main.js посчитать не по чему; ЕСЛИ правило есть → все версии сливаются в один канонический main.js.
- ЕСЛИ приложение не Web и не Mobile (банкомат, десктоп кассира, IoT, голосовой интерфейс) → инструментируется как Custom application через OpenKit, включается тумблером на экране Custom RUM Enablement.

## ЗАПАСНОЙ ПЛАН
Экраны Settings серые (нет write-прав на демо): метрику вживую не создаю, показываю снимок и проговариваю путь создания Web → application → Impact of user actions on performance → Analyze performance → Create metric.
Custom metric заводится не из экрана User action custom metrics, а из карточки приложения: если спросят про кнопку, показываю именно этот путь.
Про закрытый контур проговариваю честно: custom metrics лежат в Cassandra как любые метрики Dynatrace, а OpenKit для Custom applications банк держит в своём внутреннем Maven / npm / GitHub-зеркале.

## ВОПРОСЫ АУДИТОРИИ
- «Custom metrics или Business events, что когда?» Ответ: Custom metrics это агрегированные показатели поверх user actions RUM для графиков и SLO, а Business events это поток атомарных событий через API, где каждый платёж отдельная запись с суммой, ID транзакции и признаком фрода.
- «Custom applications работают в закрытом контуре?» Ответ: да, custom metrics хранятся в Cassandra локально, а OpenKit-библиотеки банк держит в своём внутреннем Maven / npm / GitHub-зеркале.
- «Завёл метрику payment_amount сегодня, где данные за прошлый месяц?» Ответ: их нет, Dynatrace не пересчитывает историю задним числом, метрика собирает только с момента создания.
