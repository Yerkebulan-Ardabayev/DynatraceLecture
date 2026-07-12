---
topic_id: hosts-processes
day_id: day-2
timing_min: 30
verified: 2026-07-12
---
## ГДЕ
Точка входа, список хостов: Infrastructure Observability → Hosts, рабочий route `/ui/entity/list/HOST` (голый `/ui/entity/list` отдаёт 404, как в первой теме дня).
Шесть страниц настройки в Settings → Processes and containers (префикс `/ui/settings/`): Process grouping rules `builtin:process-grouping-rules`, Simple detection rules `builtin:process-group.simple-detection-rule`, Advanced detection rules `builtin:process-group.advanced-detection-rule`, Custom process monitoring rules `builtin:process.custom-process-monitoring-rule`, Process availability `builtin:processavailability`, Process instance snapshots `builtin:process-visibility`.

## ЗАЧЕМ
Process Group это слой между конкретным процессом с PID и сервисом, который обрабатывает запросы: одинаковые инстансы одного приложения сворачиваются в одну сущность с общими метриками.
Стабильная группировка держит дашборды, baseline Davis и alerting profiles привязанными к одному объекту. Эти страницы отвечают на «как система распознаёт процессы, объединяет их в группы, когда считает процесс упавшим и когда снимает детальный снимок».

## ЦИФРЫ
- Триггер снимка процесса: превышение 1% по CPU, памяти или сети, сбор включается автоматически.
- Один снимок процесса: 20 минут данных, 10 минут до триггера и 10 минут после.
- Ручной запрос «Request process snapshot now»: данные появляются после reload в течение 90 секунд.
- Лимит на хост: до 60 минут таких метрик в сутки, квота исчерпана и новые снимки в этот день не пишутся.
- Один снимок захватывает maximum/default 100 процессов (значение можно понизить).
- Новая Process Group это новая модель Davis: baseline формируется за 7 дней истории.

## ЕСЛИ→ТО
- ЕСЛИ в Process availability выставить Condition «процесс не обнаружен N секунд» с порогом 60 → ТО плановые рестарты короче 60 секунд Problem не создают, а отсутствие дольше 60 секунд заводит Problem.
- ЕСЛИ в Action правила указать Alerting Profile → ТО уведомление уйдёт только адресатам профиля, иначе Problem появится на экране, но никого не оповестит.
- ЕСЛИ за сутки триггеры уже выбрали 60 минут метрик на хосте → ТО следующий триггер снимок не создаст, придётся ждать суток.
- ЕСЛИ в Process grouping rules задать стабильное правило (Merge по имени deployment вместо случайных имён подов) → ТО Process Group живёт дольше недели и Davis копит baseline; ЕСЛИ группа рождается раз в день → ТО baseline не формируется и аномалии не детектируются.

## ЗАПАСНОЙ ПЛАН
Голый `/ui/entity/list` отдаёт 404: сразу открываю типизированный `/ui/entity/list/HOST`, показываю карточку хоста и разбираю Running processes, Technology overview, Smartscape.
Если на демо нет write-прав на страницах Settings → Processes and containers: не создаю правило вживую, показываю форму (Rule name, Property, Action, Scope) и проговариваю на примере из курса, как split по environment variable разводит prod и dev в разные Process Groups.
Если список процессов на хосте пуст: разбираю концепцию на снимке, 200 копий одного .jar на 50 хостах сворачиваются в одну Process Group, метрики агрегируются с возможностью провалиться в конкретный инстанс.

## ВОПРОСЫ АУДИТОРИИ
- «Чем процесс отличается от Process Group?» Ответ: процесс это конкретный бинарник с PID, Process Group это логическое объединение одинаковых процессов одного приложения, одна группа содержит N инстансов.
- «В закрытом контуре появилась новая технология (например, приложение на Rust), почему нет осмысленных Process Groups?» Ответ: встроенных правил для неё нет, пока Dynatrace не выпустит сборку OneAgent с поддержкой этой технологии и админ не загрузит её через CMC; до этого пишем Simple или Advanced detection rule вручную по признакам (имя executable, библиотеки в path).
- «Simple или Advanced detection rule, с чего начать?» Ответ: Simple закрывает большинство случаев и умеет только split, Advanced нужен для логических выражений AND/OR, regex и merge; начинать с Simple, переходить на Advanced когда не хватает.
