> 📅 **День 3-4: Архитектура сквозного мониторинга и Observability** → Тема 15 из 15: «Атрибуты запросов (Request attributes)»
<!-- live-ui: https://guu84124.live.dynatrace.com/#settings/server/requestattributes -->
<!-- revision: 2026-07-28 -->

🔖 **Редакция от 2026-07-28.** Тема добавлена по итогам gap-анализа workshop-слоя; экран сверен живой досверкой 2026-07-28.

Путь в UI: **Settings → Server-side service monitoring → Request attributes** (хлебные крошки сверены вживую).

## 📚 Источники

- [Request attributes (Managed)](https://docs.dynatrace.com/managed/shortlink/request-attributes)

## 📍 КАРТА: бизнес-атрибут на техническом запросе

Тема: мост между техникой и бизнесом на server-side. Request attributes уже упоминались в темах response-analysis (custom error rules) и в retention-таблицах («Requests and request attributes до 365 дней»: см. темы Дня 2); здесь их собственный экран и механика.

Термины темы: `Request attribute / атрибут запроса`, `Data source / источник значения`, `Multidimensional analysis / MDA / многомерный анализ`.

| Что показать | Путь в меню | Прямая ссылка |
|---|---|---|
| Настройка атрибутов | **Settings → Server-side service monitoring → Request attributes** | классический маршрут `https://guu84124.live.dynatrace.com/#settings/server/requestattributes` (сверено 2026-07-28) |
| Результат в анализе | **Application Observability → Multidimensional Analysis** | `https://guu84124.live.dynatrace.com/ui/diagnostictools` |

---

## 🎬 Работа с атрибутами на двух экранах

### Шаг 1: Экран Request attributes

Путь: **Settings → Server-side service monitoring → Request attributes** → `/#settings/server/requestattributes`.

**Что на экране (сверено вживую 2026-07-28).** Заголовок **«Request attributes»** и кнопка **«Define a new request attribute»**. На демо-тенанте список пуст: дословно **«No request attributes defined!»**, а прав на создание нет: **«Missing permissions to create or edit request attributes»**. Поэтому на демо показываем экран и форму без сохранения, а результат: готовым видом MDA (Шаг 2).

**Конструкция атрибута.** По [доке](https://docs.dynatrace.com/managed/shortlink/request-attributes) request attribute это пары ключ/значение, привязанные к конкретному сервисному запросу («key/value pairs that are associated with a particular service request»). Источники значения: данные web-запроса (заголовки, параметры), аргументы методов Java / .NET / PHP, данные через OneAgent SDK.

### Шаг 2: Результат в Multidimensional Analysis

Путь: **Application Observability → Multidimensional Analysis** (`/ui/diagnostictools`).

На демо-тенанте живёт готовый вид **«Easy Trave User Request Attribute View1»** (имя с опечаткой: так назвали на демо-стенде, цитируем дословно): пример разреза запросов по значению атрибута. Это и есть выгода темы: обычный график отвечает «сколько в среднем», разрез по атрибуту отвечает «кто именно» (какой клиент, канал, версия).

---

## 🎓 ТЕОРИЯ: зачем и почём

**Мост техника ↔ бизнес.** Типовой запрос бизнеса: «покажи ошибки только по премиум-клиентам» или «время отклика по каналу мобильного банка». Без атрибутов это невозможно: все запросы на один endpoint выглядят одинаково. Атрибут вытаскивает бизнес-ключ (тип клиента, канал, регион) прямо из запроса и делает его измерением анализа.

**Где атрибут работает дальше.** Разрезы и фильтры в Multidimensional Analysis; custom error rules в failure detection (тема response-analysis); фильтры запросов в карточке сервиса.

**Документированные лимиты** (по [доке](https://docs.dynatrace.com/managed/shortlink/request-attributes)): до **100** атрибутов на запрос; до **10** значений одного атрибута; до **1 000** значений в расчётах (avg, sum, count, max); до **1 000** атрибутов в одном распределённом трейсе.

**Конфиденциальность.** Атрибут может захватить чувствительное значение (номер счёта в параметре запроса). Правило контура: согласовывать список атрибутов с безопасностью, захватывать бизнес-ключи, а не персональные данные.

**Хранение.** Метрики «Services: Requests and request attributes» конфигурируются до 365 дней (retention-лестница разобрана в темах Дня 2).

---

## 📝 Практика (2 минуты, выполнимо на demo-тенанте: read-only достаточно)

1. Открыть **Settings → Server-side service monitoring → Request attributes**, прочитать состояние списка и кнопку «Define a new request attribute».
2. Открыть **Multidimensional Analysis** и найти вид «Easy Trave User Request Attribute View1».
3. Прочитать, какой разрез запросов он даёт.

Что должно получиться: устный ответ «какой атрибут вы завели бы первым на своей инсталляции: тип клиента, канал, версия» и почему именно его.
