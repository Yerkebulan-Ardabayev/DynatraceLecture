---
topic_id: session-replay
day_id: day-5
timing_min: 22
verified: 2026-07-12
---
## ГДЕ
Три экрана.
Вход в запись через список сессий: Application Observability → Frontend → User sessions, route `/ui/user-sessions/replay-landing` (префикс replay-landing редиректит на обычный список сессий, отдельной landing-страницы у Session Replay нет, сама запись живёт внутри карточки конкретной сессии).
Cookie согласия: Settings → Web and mobile monitoring → Session Replay → Cookie, route `/ui/settings/builtin:sessionreplay.cookie`.
Захват ресурсов: Settings → Web and mobile monitoring → Session Replay → Resource capturing, route `/ui/settings/builtin:sessionreplay.web.resource-capturing`.

## ЗАЧЕМ
Session Replay это не видеозапись экрана, а реконструкция DOM во времени: snapshot структуры страницы плюс инкрементальные изменения плюс события (клики, ввод, прокрутки), браузер инженера повторно рендерит сессию как плеер.
Нужен, когда стандартная аналитика не объясняет поведение: пользователь жалуется, а метрики в норме; воронка падает на конкретном шаге; ошибка воспроизводится только на определённой версии клиента.

## ЦИФРЫ
- Четыре режима маскирования: Mask all (скрыто всё), Mask user input (только поля ввода), Allow list (маскируется всё, кроме перечисленных селекторов: они пишутся открыто; рекомендован докой), Block list (записывается всё, маскируется только перечисленное).
- Плеер воспроизведения: скорости 0.5× / 1× / 2× / 4×, рядом хронология user actions, console logs пользователя, сетевые запросы.
- Storage: около 100 кБ на минуту записи; оценка для кластера sessions/day × avg session size 500 kB × % recorded × retention 35 days × buffer 1.5.
- Cost control: реальная доля записи = % из настройки RUM × % из настройки Session Replay (пример 50% × 20% = 10% всех сессий), задаётся в Application settings → Cost and traffic control.
- OneAgent 1.193+ на хостах обязателен для Session Replay: эта версия держит высокий объём передачи beacon'ов.

## ЕСЛИ→ТО
- ЕСЛИ маска применяется на записи → sensitive-данные физически не попадают в beacon и в кластере их нет вообще; ЕСЛИ маска только на воспроизведении → данные в кластере хранятся, скрыты при playback, снять маску сможет лишь пользователь с permission «Replay sessions without masking».
- ЕСЛИ opt-in включён → запись стартует только после вызова `dtrum.enableSessionReplay()` из JS приложения; ЕСЛИ opt-in выключен → пишутся все попавшие в выборку сессии без отдельного подтверждения.
- ЕСЛИ ресурс защищён личной авторизацией, персонализирован (один URL отдаёт разное разным пользователям) или это blob/object URL → в replay он не появится.
- ЕСЛИ RUM JavaScript вставлен только в parent-страницу, а не в каждый iFrame → content iFrame в replay не отобразится.

## ЗАПАСНОЙ ПЛАН
Отдельной landing-страницы у Session Replay нет: URL с replay-landing редиректит на обычный список сессий, поэтому вход показываю через карточку конкретной сессии и вкладку Session Replay внутри неё, дальше Play.
Если на демо нет доступной записи или прав, разбираю на снимках из курса три экрана: список сессий с фильтром Session replay = Yes, cookie согласия, resource capturing.
Если по пути показа список приложений (это экран смежной темы UX-метрик) встречает плашкой Connection issues в оффлайн-дампе: проговариваю честно, что это свойство захваченного HTML-дампа без соединения с кластером, а не бага Session Replay; на живом тенанте страница грузится нормально, и в сессию захожу через Session Segmentation.
Лекторский сценарий: workshop/day-3.md, блок 4 и workshop/day-4.md, блок 4. <!-- qc:ignore=CARD_UNSOURCED_NUMBER -->

## ВОПРОСЫ АУДИТОРИИ
- «Это видеозапись экрана?» Ответ: нет, это реконструкция DOM (snapshot плюс инкрементальные diff'ы плюс события), браузер инженера повторно рендерит страницу, поэтому при playback нужны те же CSS, шрифты и картинки.
- «Как соблюсти согласие пользователя?» Ответ: consent-баннер плюс cookie согласия плюс режим opt-in (`dtrum.enableSessionReplay()` по нажатию «Согласен»), а маскирование на записи гарантирует, что sensitive-данные вообще не уйдут в кластер.
- «Что Session Replay не пишет вообще?» Ответ: не поддерживаются для записи Frames, Canvas, WebGL, Web Animations API и плагины (Adobe Flash Player, Java applets); картинки и шрифты не захватываются в resource capture и подтягиваются с исходного сервера при playback.
