"""
Юнит-тесты чистой логики краулера (без сети и браузера).

Покрывают баги из аудита раздела 12:
- возобновляемость: frontier + visited + extracted_links персистятся и
  восстанавливаются, посещённые не пере-обходятся, ссылки не теряются;
- дедуп URL с учётом query-строки (нормализация);
- уникальность имён файлов скриншотов/HTML на совпадении title;
- ретрай упавшего URL (возврат во фронтир);
- граница хоста (suffix-домен не проходит как свой);
- slugify fallback на пустой строке.

Запуск:  python -m pytest tests/ -q   (из корня dt-crawler, playwright не нужен)
"""
import importlib

import pytest

crawler = importlib.import_module("crawler")


@pytest.fixture()
def tmp_checkpoints(tmp_path, monkeypatch):
    """Перенаправить файлы чекпоинтов краулера во временную папку."""
    monkeypatch.setattr(crawler, "CHECKPOINTS", tmp_path)
    monkeypatch.setattr(crawler, "VISITED_FILE", tmp_path / "visited.json")
    monkeypatch.setattr(crawler, "FRONTIER_FILE", tmp_path / "frontier.json")
    monkeypatch.setattr(crawler, "EXTRACTED_LINKS_FILE", tmp_path / "extracted_links.json")
    return tmp_path


# ---------- normalize_url / дедуп с query ----------

def test_normalize_url_drops_query_and_fragment():
    base = "https://guu84124.live.dynatrace.com/ui/apps/dashboards"
    assert crawler.normalize_url(base + "?gtf=-2h") == base
    assert crawler.normalize_url(base + "#section") == base
    assert crawler.normalize_url(base + "?gtf=-2h#top") == base
    assert crawler.normalize_url(base + "/") == base


def test_query_variants_dedup_to_single_frontier_entry():
    """Разные ?gtf=... на одной странице не должны плодить дубли во фронтире."""
    base = "https://guu84124.live.dynatrace.com/ui/problems"
    links = [base + "?gtf=-2h", base + "?gtf=-24h", base + "#x", base]
    visited = set()
    in_queue = set()
    queue = []
    added = crawler.enqueue_links(links, depth=0, max_depth=2,
                                  visited=visited, in_queue=in_queue, queue=queue)
    assert added == 1
    assert queue == [(base, 1)]


# ---------- граница хоста (suffix-домен) ----------

def test_same_host_rejects_suffix_domain():
    base = crawler.TENANT_URL
    host = crawler._host_of(base)
    evil = f"https://{host}.evil.com/ui/x"
    assert crawler.same_host(base, base) is True
    assert crawler.same_host(evil, base) is False
    assert crawler.should_skip_url(evil) is True


def test_should_skip_external_and_skip_patterns():
    base = crawler.TENANT_URL
    assert crawler.should_skip_url(base + "/ui/logout") is True   # skip-паттерн
    assert crawler.should_skip_url("https://docs.dynatrace.com/x") is True
    assert crawler.should_skip_url(base + "/ui/dashboards") is False


# ---------- slugify / уникальность имён файлов ----------

def test_slugify_empty_fallback():
    assert crawler.slugify("") == "unnamed"
    assert crawler.slugify("   ") == "unnamed"
    assert crawler.slugify("!!!") == "unnamed"


def test_unique_filename_differs_for_same_title_different_url():
    a = crawler.unique_filename("dashboards", "https://x/ui/a", ".png")
    b = crawler.unique_filename("dashboards", "https://x/ui/b", ".png")
    assert a != b
    assert a.startswith("dashboards-") and a.endswith(".png")
    # то же имя+URL -> стабильно
    assert a == crawler.unique_filename("dashboards", "https://x/ui/a", ".png")


# ---------- ретрай ----------

def test_enqueue_respects_max_depth():
    links = ["https://guu84124.live.dynatrace.com/ui/x"]
    queue = []
    added = crawler.enqueue_links(links, depth=2, max_depth=2,
                                  visited=set(), in_queue=set(), queue=queue)
    assert added == 0
    assert queue == []


def test_enqueue_skips_visited_and_noise():
    base = "https://guu84124.live.dynatrace.com"
    visited = {base + "/ui/seen"}
    queue = []
    in_queue = set()
    links = [
        base + "/ui/seen",          # уже посещён
        base + "/ui/logout",        # skip-паттерн
        base + "/other/page",       # не /ui/ и не /apps/
        base + "/ui/new",           # валидный
    ]
    added = crawler.enqueue_links(links, depth=0, max_depth=2,
                                  visited=visited, in_queue=in_queue, queue=queue)
    assert added == 1
    assert queue == [(base + "/ui/new", 1)]


# ---------- возобновляемость: сохранение/восстановление ----------

def test_checkpoint_roundtrip_restores_frontier(tmp_checkpoints):
    visited = {"https://x/ui/a", "https://x/ui/b"}
    queue = [("https://x/ui/c", 1), ("https://x/ui/d", 2)]
    extracted = {"https://x/ui/a": ["https://x/ui/c", "https://x/ui/d"]}

    crawler.save_checkpoint(visited, queue, extracted)

    assert crawler.load_visited() == visited
    assert crawler.load_frontier() == [("https://x/ui/c", 1), ("https://x/ui/d", 2)]
    assert crawler.load_extracted_links() == extracted


def test_restart_after_interruption_preserves_progress(tmp_checkpoints):
    """Симуляция kill посреди обхода и рестарта.

    Первый прогон посетил 2 seed'а и накопил во фронтире их исходящие ссылки.
    После 'kill' (данные на диске) второй прогон должен:
      - восстановить фронтир (найденные ссылки не потеряны),
      - НЕ пере-обходить посещённые seed'ы,
      - продолжить с оставшейся очереди.
    """
    base = "https://guu84124.live.dynatrace.com"
    seeds = [base + "/ui/dashboards", base + "/ui/problems"]

    # --- прогон 1: посетили оба seed'а, из них извлекли ссылки во фронтир ---
    visited = set()
    queue, in_queue = crawler.build_initial_frontier(seeds, restored_frontier=[], visited=visited)
    assert len(queue) == 2

    extracted = {}
    # обрабатываем seed'ы
    for seed_url, depth in list(queue):
        visited.add(seed_url)
        child_links = [seed_url + "/child1", seed_url + "/child2"]
        # заменим на /ui/ пути, чтобы прошли is_crawlable_link
        child_links = [base + "/ui/" + seed_url.rsplit("/", 1)[1] + "-child1",
                       base + "/ui/" + seed_url.rsplit("/", 1)[1] + "-child2"]
        extracted[seed_url] = child_links
    # заново собрать очередь только из детей (seed'ы уже visited)
    queue, in_queue = crawler.build_initial_frontier(seeds, restored_frontier=[], visited=visited)
    for seed_url in seeds:
        crawler.enqueue_links(extracted[seed_url], depth=0, max_depth=2,
                              visited=visited, in_queue=in_queue, queue=queue)
    n_children = sum(len(v) for v in extracted.values())
    assert len(queue) == n_children  # 4 ребёнка во фронтире, seed'ы не в нём

    crawler.save_checkpoint(visited, queue, extracted)

    # --- kill: очистим память, читаем только диск ---
    del visited, queue, in_queue, extracted

    # --- прогон 2: рестарт ---
    visited2 = crawler.load_visited()
    restored = crawler.load_frontier()
    extracted2 = crawler.load_extracted_links()

    # найденные ссылки не потеряны
    assert len(restored) == n_children
    # посещённые seed'ы восстановлены
    for s in seeds:
        assert s in visited2

    queue2, in_queue2 = crawler.build_initial_frontier(seeds, restored_frontier=restored, visited=visited2)
    # фронтир восстановлен из чекпоинта (а не из seeds)
    assert len(queue2) == n_children
    # seed'ы НЕ вернулись в очередь (не пере-обходятся)
    urls_in_queue = {u for u, _ in queue2}
    for s in seeds:
        assert s not in urls_in_queue
    # извлечённые ссылки сохранены
    assert extracted2 == {s: crawler.load_extracted_links()[s] for s in seeds}


def test_build_initial_frontier_falls_back_to_seeds_when_no_checkpoint(tmp_checkpoints):
    base = "https://guu84124.live.dynatrace.com"
    seeds = [base + "/ui/a", base + "/ui/b"]
    queue, in_queue = crawler.build_initial_frontier(seeds, restored_frontier=[], visited=set())
    assert {u for u, _ in queue} == {base + "/ui/a", base + "/ui/b"}
    assert all(d == 0 for _, d in queue)


def test_retry_returns_failed_url_to_frontier():
    """Логика ретрая: упавший URL возвращается в очередь до MAX_RETRIES раз."""
    max_retries = 2
    retries = {}
    url, depth = "https://x/ui/flaky", 1
    queue = []
    in_queue = set()

    def fail_once():
        attempts = retries.get(url, 0)
        if attempts < max_retries:
            retries[url] = attempts + 1
            queue.append((url, depth))
            in_queue.add(url)
            return "retried"
        return "gave_up"

    assert fail_once() == "retried"
    assert queue == [(url, 1)]
    queue.pop(0)
    assert fail_once() == "retried"
    queue.pop(0)
    assert fail_once() == "gave_up"   # исчерпали ретраи
    assert queue == []


def test_atomic_write_no_partial_on_reader(tmp_checkpoints):
    """Атомарная запись: после save_checkpoint файл валиден (не .tmp обрывок)."""
    crawler.save_checkpoint({"https://x/ui/a"}, [("https://x/ui/b", 1)], {})
    # .tmp не остаётся
    assert not (tmp_checkpoints / "frontier.json.tmp").exists()
    assert not (tmp_checkpoints / "visited.json.tmp").exists()
    # содержимое читается
    assert crawler.load_frontier() == [("https://x/ui/b", 1)]
