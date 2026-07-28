---
topic_id: rum
day_id: day-5
timing_min: 30
verified: 2026-07-12
---
## ГДЕ
Четыре живых экрана.
User sessions (список): Application Observability → Frontend → User sessions, route `/ui/user-sessions`.
User session query: Frontend → User sessions query, route `/ui/user-sessions/query`.
RUM Web enablement: Settings → Web and mobile monitoring → Web enablement and cost control, route `/ui/settings/builtin:rum.web.enablement`.
RUM Mobile enablement: Settings → Web and mobile monitoring → Mobile enablement and cost control, route `/ui/settings/builtin:rum.mobile.enablement`.

## ЗАЧЕМ
RUM это вторая точка наблюдения в дополнение к серверному OneAgent: агент прямо в браузере или мобильном приложении.
Отвечает на «медленно на бэкенде, в сети или в браузере» и показывает весь путь от клика до картинки, а не только время сервера.

## ЦИФРЫ
- Серверный агент видит только обработку на бэкенде (например 35 мс), а пользователь ждёт 730 мс: 200 мс сеть до дата-центра · 35 мс сервер · 250 мс ответ обратно · 245 мс браузер (парсинг, JavaScript, рендеринг).
- Apdex: одно число от 0.0 до 1.0, шкала из пяти уровней (Excellent 0.94-1.0 / Good 0.85-0.94 / Fair 0.7-0.85 / Poor 0.5-0.7 / Unacceptable <0.5); action с JavaScript-ошибкой автоматически Frustrated.
- Таймаут бездействия сессии: Web 30 минут, Mobile и Custom 10 минут.
- RUM-приложений на демо-тенанте: 17, три видны сразу плюс «+ 14 more» (у вашего тенанта цифры могут быть другими).
- Cost control: доля захватываемых сессий для RUM и Session Replay; держать ниже 100% на пиковые периоды.
- iOS: static builds и Carthage не поддерживаются с версии 8.323; поддержка IE 11 в Web-RUM прекращена с RUM JavaScript 1.293.

## ЕСЛИ→ТО
- ЕСЛИ собирать данные только серверным агентом → видно лишь время обработки на сервере (например 35 мс), а реальное ожидание пользователя (например 730 мс) и его причина (медленная сеть, тяжёлый JavaScript) остаются невидимы.
- ЕСЛИ пользователь сделал паузу дольше таймаута бездействия (Web 30 минут, Mobile 10 минут) и вернулся → Dynatrace закрывает прежнюю сессию и заводит новую с новым session-id, а не продолжает старую.
- ЕСЛИ доля захвата ниже 100% → при всплеске трафика пишется только заданная доля сессий, квота не сгорает за сутки.
- ЕСЛИ ограничение не настроить → один пиковый день рискует выбрать заметную часть месячной квоты.

## ЗАПАСНОЙ ПЛАН
Если список User sessions пуст, показываю снимок из курса: слева панель фильтров (Application type Web/Custom/Mobile, Applications, User experience score, Errors and annoyances), справа таблица сессий с колонками User session, Replay, User, User experience score, Duration, User action count, Total conversions, Errors and annoyances.
Новый Apps-интерфейс Users & Sessions в изолированном Managed не активирован, поэтому вся работа идёт в классическом list-view, это не устаревшая функциональность, а параллельный стабильный интерфейс.
На экране User session query по умолчанию пусто (заголовок Run a query to view results): запрос на USQL пишу сам и сразу проговариваю, что DQL и Grail в air-gapped Managed не работают, USQL в Classic UI остаётся рабочим.
На страницах enablement без write-прав разбираю логику cost control (доля захватываемых сессий) по снимку, настройки не меняю.
Лекторский сценарий: workshop/day-3.md, блок 4. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Зачем RUM, если бэкенд уже под OneAgent?» Ответ: серверный агент видит только время на бэкенде (например 35 мс), а пользователь ждёт 730 мс из-за сети и браузера, RUM меряет весь путь от клика до картинки с разбивкой по этапам.
- «Как в закрытом контуре собирать RUM с внешних клиентов?» Ответ: beacon нельзя пускать напрямую в кластер, ставят ActiveGate в DMZ (смотрит наружу, принимает beacon'ы и пересылает внутрь по защищённому каналу) либо web-сервер с OneAgent.
- «USQL или DQL в изолированном Managed?» Ответ: только USQL в классическом UI, DQL поверх Grail доступен лишь в SaaS и в air-gapped Managed не работает.
