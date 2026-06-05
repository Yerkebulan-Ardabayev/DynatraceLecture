> 📅 **День 5: Мониторинг фронтенда и пользовательского опыта** → Тема 4 из 10: «Воспроизведение сессий (Session Replay)»
<!-- live-ui: https://guu84124.live.dynatrace.com/ui/user-sessions/replay-landing -->
<!-- revision: 2026-04-27 -->

🔖 **Редакция от 2026-04-27.**

> 📚 **Источники (только Dynatrace Managed):**
>
> - [Session Replay (shortlink)](https://docs.dynatrace.com/managed/shortlink/session-replay)
> - [Configure Session Replay for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/configure-session-replay-web)
> - [Enable Session Replay for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/enable-session-replay-web)
> - [Technical restrictions for Session Replay for web applications](https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/session-replay-restrictions-web)

## 📍 КАРТА: три страницы про Session Replay

Термины темы: `Session Replay / воспроизведение сессии`, `DOM snapshot / слепок структуры страницы`, `DOM diff / инкрементальные изменения`, `Masking / маскирование sensitive-полей`, `Consent cookie / cookie согласия`, `Resource capturing / захват ресурсов`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| User sessions / Session Replay landing | **Application Observability → Frontend → User sessions** | `https://guu84124.live.dynatrace.com/ui/user-sessions/replay-landing` |
| Session Replay state cookie | **Settings → Web and mobile monitoring → Session Replay → Cookie** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.cookie` |
| Session Replay resource capturing | **Settings → Web and mobile monitoring → Session Replay → Resource capturing** | `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.web.resource-capturing` |

---

## 🎬 Работа с Session Replay на трёх экранах

### Шаг 1: Вход в Session Replay через список сессий

![Список сессий со значком Session Replay](screenshots/day-5/session-replay/user-sessions/Session-List-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/user-sessions/replay-landing`. На этом тенанте URL с префиксом `replay-landing` редиректит на обычный список сессий. Session Replay не имеет отдельной landing-страницы, это функциональность внутри карточки конкретной сессии.

**Что видно на скриншоте.** Всё та же страница User sessions из Темы 1. Кнопка `Session replayYes` в фильтре говорит о том, что мы можем отфильтровать только те сессии, для которых доступна запись Session Replay. По умолчанию Session Replay пишется не для всех сессий: только для выборки, настраиваемой в application settings.

**Как клиенту показать.** Выбираем фильтр → получаем список сессий с доступным Replay → кликаем на конкретную сессию → в карточке появляется вкладка Session Replay → нажимаем Play → смотрим, что делал пользователь: в виде видео.

### Шаг 2: Session Replay state cookie (управление согласием пользователя)

![Session Replay state cookie: настройка cookie согласия](screenshots/day-5/session-replay/settings/builtinsessionreplay.cookie/Session-Replay-state-cookie-Environment-Settings-Demo-live-Demo-Live-Dynatrace.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.cookie`.

**Что здесь настраивается.** Имя и параметры cookie, в которой хранится состояние согласия пользователя на запись Session Replay. Это compliance-механизм.

*Типичная схема согласия.* Пользователь открывает сайт → видит cookie consent banner:

> Мы собираем аналитические данные о вашем взаимодействии с сайтом для улучшения сервиса. Включает запись ваших действий на странице. [Разрешить] [Отклонить]

Если нажал «Разрешить»: сайт через JavaScript устанавливает cookie (имя задаётся на этой странице, например `dtReplay=true`). RUM-агент видит cookie и начинает писать Session Replay.

**Ключевые настройки cookie:**

- **Cookie name**: имя (по умолчанию `dtCookie`).
- **Domain**: для какого домена действует (пусто = текущий, `.example.com` = все поддомены).
- **Path**: для какого пути URL (`/` = весь сайт).
- **Secure, HttpOnly, SameSite**: стандартные флаги защиты.

*Почему важно.* Session Replay может захватить:

- Поля форм (пароли, CVV, номер карты, PIN).
- Промо-коды, купоны.
- Паспортные данные при регистрации.

Даже с настроенным маскированием (кружочки вместо пароля) **риск остаётся**: неправильная маска, новое поле формы, ошибка в CSS-селекторе. Запись без явного согласия: юридический риск.

**Типовые требования compliance:**

- Баннер согласия в соответствии с законом о персональных данных.
- Маскирование всех полей с sensitive-данными.
- Возможность пользователю отозвать согласие в настройках аккаунта.
- Автоматическая очистка Session Replay для отозвавших согласие.

### Шаг 3: Resource capture for Session Replay (захват ресурсов)

![Resource capture for Session Replay: настройка захвата ресурсов](screenshots/day-5/session-replay/settings/builtinsessionreplay.web.resource-capturing/Resource-capture-for-Session-Replay-Environment-Settings-Demo-live-Demo-Live-Dyn.png)

Путь: `https://guu84124.live.dynatrace.com/ui/settings/builtin:sessionreplay.web.resource-capturing`.

*Что настраивает.* Какие внешние ресурсы (CSS, шрифты, картинки, иконки) Dynatrace сохраняет вместе с записью сессии.

*Зачем.* Session Replay: не видеозапись экрана, а **реконструкция DOM во времени**. Dynatrace сохраняет:

1. Начальный HTML страницы (snapshot DOM).
2. DOM-изменения во времени (добавлены / удалены / изменены узлы).
3. Координаты курсора, клики, клавишные события.

При воспроизведении через неделю Dynatrace не «включает запись», а **повторно рендерит страницу** в браузере администратора, прогоняя DOM-изменения в ускоренном режиме. Чтобы страница выглядела как тогда, нужны те же CSS, шрифты, картинки: иначе кнопки окажутся не на месте, шрифт другой, иконок нет.

**Настройки:**

- **Resource capture (захват ресурсов)**: по умолчанию включён и сохраняет только **CSS-ресурсы** (стили). Без них страница при воспроизведении развалится.
- **Картинки и шрифты не захватываются** даже при включённом resource capture: при playback они подгружаются с исходного сервера. Если ресурс недоступен, защищён авторизацией или персонализирован (один URL отдаёт разное разным пользователям), в replay его не будет.
- **Max resource size**: лимит размера одного ресурса; выше: ресурс не сохраняется (точное значение задаётся в settings приложения).
- **Ignore patterns**: URL-паттерны ресурсов, которые не сохранять (`*/ads/*` для маркетинговых баннеров).

*Что нельзя восстановить.* Resources, защищённые персональной авторизацией (один URL: разное содержимое разным пользователям), и blob/object URLs не воспроизводятся; они должны быть доступны браузеру администратора при playback.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/session-replay-restrictions-web -->

*Trade-off объёма.* По данным Dynatrace, в среднем минута записи и replay занимает порядка 100 кБ хранилища; для приложений с активными DOM-изменениями и iFrame'ами цифра выше. Storage-оценка для cluster-инсталляции: `sessions/day × avg session size (500 kB) × % recorded × retention (35 days) × buffer (1.5)`. Поэтому Session Replay включают не для всех, а для выборки: типовые стратегии: записывать только часть общего трафика, плюс 100% сессий с ошибками, плюс приоритетные сегменты (VIP-клиенты, критичные функции).

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/enable-session-replay-web -->

Cost control: фактическая доля записываемых сессий = % из настройки RUM × % из настройки Session Replay (например, RUM 50% × SR 20% = 10% от всех сессий). Настраивается в Application settings → Cost and traffic control.

---

## 🎓 ТЕОРИЯ: как устроен Session Replay

### Технология: DOM snapshots + diff

Session Replay не записывает пиксели экрана (это были бы терабайты трафика на одну сессию и нарушение privacy). Вместо этого:

1. **Full DOM snapshot** при старте сессии: HTML-структура, атрибуты, inline-styles.
2. **Incremental diff** во времени: что изменилось в DOM.
3. **Events**: клики, touch-ы, прокрутки, ввод в поля. Только таймстемпы и координаты, значения полей маскируются.
4. **Resources snapshot**: CSS-файлы, шрифты, картинки по настройкам из Шага 3.

Всё сжимается собственным бинарным протоколом Dynatrace и отправляется beacon-ом в кластер. Beacon Session Replay использует `application/octet-stream`: firewall между браузером и тенантом обязан его пропускать, иначе записи не дойдут до кластера.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/enable-session-replay-web -->

### Воспроизведение

При открытии сессии в UI:
1. Браузер инженера загружает snapshot + все diff'ы + ресурсы.
2. Строит виртуальный iframe с начальным DOM.
3. Прогоняет diff'ы во времени, синхронно с записанным курсором и событиями.
4. Показывает это как плеер с таймлайном (play, pause, rewind, скорость 0.5× / 1× / 2× / 4×).

В сайдбаре параллельно плеера: хронология user actions, console logs пользователя (если включено), сетевые запросы.

### Маскирование sensitive-данных

В Dynatrace Session Replay для web доступны **четыре режима маскирования**:

- **Mask all**: маскируется всё (только структура страницы и заглушки текстов; используется в т.ч. для тестирования).
- **Mask user input**: маскируются только поля ввода (текст, числа), всё остальное (статические тексты, заголовки) видно.
- **Allow list**: записывается всё, кроме явно перечисленных селекторов; рекомендованный режим для большинства приложений.
- **Block list**: записываются только явно разрешённые селекторы; всё остальное замаскировано.

Маскирование закрывает только алфавитно-цифровые символы: формат-разделители (точки, запятые, двоеточия) остаются видны, что помогает воспроизвести «форму» данных без раскрытия содержимого.

URL-исключения настраиваются регулярными выражениями: при первом совпадении остальные правила игнорируются.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/configure-session-replay-web -->

**Recording vs Playback.** Маскирование может применяться как при записи, так и при воспроизведении. ЕСЛИ маска на записи → ТО sensitive-данные физически не попадают в beacon и в кластере их нет вообще. ЕСЛИ маска только на воспроизведении → ТО данные в кластере хранятся, но скрыты при playback; увидеть их сможет лишь пользователь с permission «Replay sessions without masking».

**Opt-in mode.** Чтобы соблюсти явное согласие пользователя, Session Replay можно перевести в режим opt-in. ЕСЛИ opt-in включён → ТО запись стартует только после вызова `dtrum.enableSessionReplay()` из JS приложения; ЕСЛИ opt-in выключен → ТО пишутся все сессии, попавшие в выборку, без отдельного подтверждения. Типовая схема: показать consent-баннер, при «Согласен»: установить cookie + дёрнуть `dtrum.enableSessionReplay()`.

*Рекомендация для sensitive-сценариев.* Использовать **Mask all** или **Block list** по умолчанию и явно разрешать только заголовки, навигацию и статические тексты. Инверсия модели риска: по умолчанию ничего не видно, в whitelist попадает только согласованное с compliance.

### Юридические требования

Типовой закон о персональных данных требует:

1. **Согласие субъекта** на сбор, обработку, хранение.
2. **Ограничение трансграничной передачи.** Для регулируемых отраслей: данные должны оставаться в юрисдикции, в собственной инфраструктуре. Это одна из причин выбора Managed вместо SaaS.
3. **Право на отзыв согласия.** Cookie consent banner должен позволять отзыв.
4. **Право на уничтожение.** Если пользователь запросил удалить данные: Session Replay-записи тоже должны быть уничтожены.

Dynatrace Session Replay технически позволяет соблюсти эти требования, но настройка: задача админа и compliance-команды, не автоматическая.

### Когда НЕ нужен Session Replay

- **Zero-trust системы**: даже маскированная запись непозволительна.
- **Транзакционные backend-сервисы без UI.** Session Replay про фронтенд, бэкенду не нужен.
- **Когда данных достаточно.** Если Dynatrace показывает «кнопка Confirm тормозит 2.5 сек»: Session Replay не добавит ценности.

Session Replay полезен, когда стандартная аналитика не объясняет поведения пользователя. Типовые случаи:

- «Пользователь жалуется, а по метрикам всё норм»: в replay видно, что он не находит нужную кнопку на мобильном.
- «В funnel падение на шаге 3»: 10 replay-ев со шага 3 показывают UX-проблему.
- «Ошибка появилась вчера на определённой версии Android»: смотрим replay именно на этой версии.

### Connection issues на странице Applications

На скриншоте Темы 2 страница `/ui/applications` показывает плашку «Connection issues». Это не бага Session Replay, это свойство захваченных в crawler'е HTML-дампов. Классические SPA-страницы Dynatrace ожидают WebSocket-соединения с бэкендом для подгрузки данных. В offline-дампе соединения нет, страница показывает восстановление.

**На живом тенанте** эта страница грузится нормально: там есть соединение с кластером.

### Ограничения

Согласно официальным technical restrictions:

- **Не поддерживаются** для записи: Frames (старые HTML-фреймы), Canvas, WebGL, Web Animations API, плагины (Adobe Flash Player, Java applets) и иные не-HTML технологии.
- **iFrame**: нужен RUM JavaScript отдельно в каждый iFrame; одно и то же приложение должно мониторить и parent-страницу, и iFrame, иначе iframe в replay будет некорректно отображаться. Inserting RUM JS только в parent: content iframe в replay не появится.
- **Resources, защищённые личной авторизацией** или blob/object URLs: не воспроизводятся.
- **Form values, обновлённые через `.value`-property напрямую**, могут не попадать в diff; для корректного захвата: обновлять атрибут или `.textContent`.
- **Browser extensions** (блокировщики, privacy-плагины) могут мешать инъекции и записи.
- **OneAgent 1.193+** требуется на хостах: эта версия поддерживает высокий объём передачи beacon'ов, нужный для Session Replay.

<!-- last-verified: 2026-04-27 source: https://docs.dynatrace.com/managed/observe/digital-experience/session-replay/session-replay-restrictions-web -->

### Ключевые термины

- **Session Replay**: функциональность воспроизведения сессий.
- **DOM snapshot**: полный слепок структуры страницы.
- **DOM diff**: инкрементальные изменения структуры.
- **Masking**: маскирование sensitive-полей в записи.
- **Consent cookie**: cookie согласия пользователя.
- **Resource capturing**: захват CSS/шрифтов/картинок для воспроизведения.
