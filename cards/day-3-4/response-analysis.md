---
topic_id: response-analysis
day_id: day-3-4
timing_min: 28
verified: 2026-07-12
---
## ГДЕ
Пять экранов. Точка входа Services: Application Observability → Services, route `/ui/services`.
Пороги детекции отклика: Settings → Anomaly detection → Services, route `/ui/settings/builtin:anomaly-detection.services`.
Классификация ошибок: Settings → Server-side service monitoring → Failure detection parameters `/ui/settings/builtin:failure-detection.environment.parameters`, Failure detection rules `/ui/settings/builtin:failure-detection.environment.rules`, общая страница Failure detection (rulesets) `/ui/settings/builtin:failure-detection-rulesets`.

## ЗАЧЕМ
Тема про отклик, деградации и аномалии: два разных механизма.
Failure detection определяет, какой запрос считать упавшим, это основа метрики Failure rate (что идёт в числитель).
Anomaly detection ловит статистическое отклонение метрики от baseline: отклик обычно 100 мс, а стал 400 мс это аномалия, даже если запросы успешные.
Davis заводит Problem, когда отклик аномально высокий либо Failure rate аномально высокий.

## ЦИФРЫ
- Services на снимке темы: 241 (у вашего тенанта цифры могут быть другими).
- Reference period Davis по умолчанию: последние 7 дней; кнопка Reset сбрасывает baseline (нужно после крупного релиза).
- HTTP по умолчанию: 500-599 это server-side ошибка, 400-599 трактуются как client-side.
- HTTP 404 по умолчанию client-side (битая ссылка), в Failure rate не идёт, пока не включён Consider 404 as failures.
- Response time degradation: две категории, All responses (медиана) и Slowest 10% (самые медленные), в каждой порог relative (% от baseline) и absolute (в мс).

## ЕСЛИ→ТО
- ЕСЛИ отклик нарушил и relative, и absolute порог категории одновременно → Davis заводит Problem; ЕСЛИ только один из двух → Davis молчит, это отсекает шум на быстрых сервисах, где +50% это всё равно единицы миллисекунд.
- ЕСЛИ оставить дефолт HTTP-кодов → в Failure rate идут только серверные сбои (5xx, exception, error page), клиентские 4xx не идут; ЕСЛИ добавить 4xx в server-side errors → клиентские 400-е начнут поднимать Failure rate.
- ЕСЛИ включить Consider 404 as failures → 404 считаются отказом сервера и влияют на Failure rate; ЕСЛИ не включать → 404 остаются на стороне вызывающего.
- ЕСЛИ Sensitivity = High → Problem на каждом нарушении порога (шумит на коротких всплесках); ЕСЛИ Sensitivity = Low → нужна высокая статистическая уверенность, кратковременные всплески Problem не создают.

## ЗАПАСНОЙ ПЛАН
Если страницы Failure detection или Anomaly detection на демо серые (нет write-прав): показываю снимки из курса и проговариваю, что на боевом окружении админ правит пороги и rules под реальный профиль трафика.
Конкретные дефолтные пороги по памяти не называю, отсылаю к значениям на самой странице тенанта.
Если список Services пуст: показываю снимок Services из курса, проговариваю заголовок с числом сервисов и захожу в разбор отклика оттуда.

## ВОПРОСЫ АУДИТОРИИ
- «Чем Anomaly detection отличается от Failure detection?» Ответ: Failure detection классифицирует каждый запрос как успех или неудачу (что считать ошибкой), Anomaly detection ловит статистическое отклонение метрики от baseline (когда рост это аномалия).
- «У auth-service Failure rate высокий, это авария?» Ответ: нет, если это ожидаемые 401 от неверных паролей; правилом Failure detection rules 401 помечают как not failure, и Failure rate падает до реального уровня.
- «Работает ли эта детекция в закрытом контуре?» Ответ: да, все настройки локальны, хранятся в кластере, применяются OneAgent без внешних вызовов.
