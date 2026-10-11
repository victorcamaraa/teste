"""Roda todos os scrapers e grava o resultado. Pode ser usado pela linha de comando:

    python -m promobot.collector
"""

from __future__ import annotations

import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from .categories import CATEGORIES
from .notifier import notify
from .scrapers import SCRAPERS
from .storage import Storage, now

log = logging.getLogger(__name__)

NOTIFY_MIN_DISCOUNT = float(os.environ.get("NOTIFY_MIN_DISCOUNT", "15"))


def collect_one(storage: Storage, scraper, category: str) -> list[str]:
    started = now()
    try:
        deals = scraper.fetch(category)
    except Exception as exc:  # noqa: BLE001 - uma loja fora do ar não pode parar as outras
        log.warning("%s/%s falhou: %s", scraper.label, category, exc)
        storage.record_status(scraper.label, category, False, str(exc)[:300], 0, started)
        return []
    for deal in deals:
        deal.found_at = started
    changed = storage.save_deals(deals)
    storage.record_status(scraper.label, category, True, "", len(deals), started)
    log.info("%s/%s: %d produtos", scraper.label, category, len(deals))
    return changed


def collect_all(storage: Storage, categories=None, scrapers=None) -> dict:
    categories = categories or list(CATEGORIES)
    instances = [cls() for cls in (scrapers or SCRAPERS)]
    jobs = [(s, c) for s in instances for c in categories]
    # Uma thread por loja evita martelar o mesmo site em paralelo.
    by_store: dict[str, list] = {}
    for scraper, category in jobs:
        by_store.setdefault(scraper.name, []).append((scraper, category))

    def run_store(store_jobs):
        changed = []
        for scraper, category in store_jobs:
            changed += collect_one(storage, scraper, category)
            time.sleep(1)
        return changed

    with ThreadPoolExecutor(max_workers=len(by_store) or 1) as pool:
        changed = [cid for result in pool.map(run_store, by_store.values()) for cid in result]

    alerts = notify(storage.pending_notifications(changed, NOTIFY_MIN_DISCOUNT))
    return {"changed": len(changed), "alerts": alerts}


class Scheduler:
    """Coleta em segundo plano a cada `interval_min` minutos."""

    def __init__(self, storage: Storage, interval_min: float):
        self.storage = storage
        self.interval = interval_min * 60
        self.running = threading.Lock()
        self.last_run: str | None = None
        self._wake = threading.Event()

    def start(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def trigger(self) -> bool:
        """Pede uma coleta imediata. False se já houver uma em andamento."""
        if self.running.locked():
            return False
        self._wake.set()
        return True

    @property
    def busy(self) -> bool:
        return self.running.locked()

    def _loop(self):
        while True:
            with self.running:
                try:
                    collect_all(self.storage)
                except Exception:  # noqa: BLE001
                    log.exception("Erro na coleta")
                self.last_run = now()
            self._wake.wait(self.interval)
            self._wake.clear()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    db = Storage(os.environ.get("PROMOBOT_DB", "promocoes.db"))
    print(collect_all(db))
