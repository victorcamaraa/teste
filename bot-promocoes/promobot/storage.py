"""Persistência em SQLite: ofertas atuais, histórico de preços e status das lojas."""

from __future__ import annotations

import sqlite3
import threading
from datetime import datetime, timezone

from .models import Deal

SCHEMA = """
CREATE TABLE IF NOT EXISTS deals (
    id TEXT PRIMARY KEY,
    store TEXT NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    image TEXT,
    price REAL NOT NULL,
    original_price REAL,
    discount REAL NOT NULL DEFAULT 0,
    previous_price REAL,
    lowest_price REAL NOT NULL,
    available INTEGER NOT NULL DEFAULT 1,
    offer_ends_at TEXT,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS price_history (
    deal_id TEXT NOT NULL,
    price REAL NOT NULL,
    seen_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_history_deal ON price_history(deal_id);
CREATE TABLE IF NOT EXISTS source_status (
    store TEXT NOT NULL,
    category TEXT NOT NULL,
    ok INTEGER NOT NULL,
    message TEXT,
    count INTEGER NOT NULL DEFAULT 0,
    ran_at TEXT NOT NULL,
    last_ok TEXT,
    PRIMARY KEY (store, category)
);
"""

# Desconto efetivo: o maior entre o "de/por" da loja e a queda desde a última coleta.
EFFECTIVE_DISCOUNT = """
MAX(d.discount,
    CASE WHEN d.previous_price > d.price
         THEN ROUND((1 - d.price / d.previous_price) * 100, 1) ELSE 0 END)
"""

SORTS = {
    "desconto": "effective_discount DESC, d.price ASC",
    "menor_preco": "d.price ASC",
    "maior_preco": "d.price DESC",
    "recentes": "d.first_seen DESC",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


class Storage:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        with self.lock:
            self.conn.executescript(SCHEMA)

    def save_deals(self, deals: list[Deal]) -> list[str]:
        """Grava as ofertas e devolve os ids que são novos ou baixaram de preço."""
        changed = []
        with self.lock, self.conn:
            for deal in deals:
                row = self.conn.execute(
                    "SELECT price, lowest_price, previous_price FROM deals WHERE id = ?",
                    (deal.id,),
                ).fetchone()
                if row is None:
                    self.conn.execute(
                        """INSERT INTO deals (id, store, category, title, url, image, price,
                               original_price, discount, lowest_price, available,
                               offer_ends_at, first_seen, last_seen)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (deal.id, deal.store, deal.category, deal.title, deal.url, deal.image,
                         deal.price, deal.original_price, deal.discount, deal.price,
                         int(deal.available), deal.offer_ends_at, deal.found_at, deal.found_at),
                    )
                    changed.append(deal.id)
                else:
                    previous = row["previous_price"]
                    if deal.price != row["price"]:
                        previous = row["price"]
                        if deal.price < row["price"]:
                            changed.append(deal.id)
                    self.conn.execute(
                        """UPDATE deals SET title = ?, image = ?, price = ?, original_price = ?,
                               discount = ?, previous_price = ?, lowest_price = ?,
                               available = ?, offer_ends_at = ?, last_seen = ?
                           WHERE id = ?""",
                        (deal.title, deal.image, deal.price, deal.original_price, deal.discount,
                         previous, min(row["lowest_price"], deal.price), int(deal.available),
                         deal.offer_ends_at, deal.found_at, deal.id),
                    )
                    if deal.price == row["price"]:
                        continue
                self.conn.execute(
                    "INSERT INTO price_history (deal_id, price, seen_at) VALUES (?, ?, ?)",
                    (deal.id, deal.price, deal.found_at),
                )
        return changed

    def record_status(
        self, store: str, category: str, ok: bool, message: str, count: int, ran_at: str
    ):
        """ran_at deve ser o mesmo found_at usado nas ofertas daquela coleta."""
        with self.lock, self.conn:
            self.conn.execute(
                """INSERT INTO source_status (store, category, ok, message, count, ran_at, last_ok)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(store, category) DO UPDATE SET
                       ok = excluded.ok, message = excluded.message, count = excluded.count,
                       ran_at = excluded.ran_at,
                       last_ok = COALESCE(excluded.last_ok, source_status.last_ok)""",
                (store, category, int(ok), message, count, ran_at, ran_at if ok else None),
            )

    def status(self) -> list[dict]:
        with self.lock:
            rows = self.conn.execute(
                "SELECT * FROM source_status ORDER BY store, category"
            ).fetchall()
        return [dict(r) for r in rows]

    def query(
        self,
        categories: list[str] | None = None,
        stores: list[str] | None = None,
        text: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_discount: float = 0,
        only_promo: bool = True,
        only_available: bool = True,
        sort: str = "desconto",
        limit: int = 200,
    ) -> list[dict]:
        # Só mostra o que apareceu na última coleta bem-sucedida daquela loja/categoria;
        # o que sumiu da listagem provavelmente acabou.
        sql = [f"""
            SELECT d.*, {EFFECTIVE_DISCOUNT} AS effective_discount,
                   (SELECT COUNT(*) FROM price_history h WHERE h.deal_id = d.id) AS history_count
            FROM deals d
            JOIN source_status s ON s.store = d.store AND s.category = d.category
            WHERE d.last_seen >= s.last_ok
        """]
        params: list = []
        if categories:
            sql.append(f"AND d.category IN ({','.join('?' * len(categories))})")
            params += categories
        if stores:
            sql.append(f"AND d.store IN ({','.join('?' * len(stores))})")
            params += stores
        if text:
            for word in text.split():
                sql.append("AND d.title LIKE ?")
                params.append(f"%{word}%")
        if min_price is not None:
            sql.append("AND d.price >= ?")
            params.append(min_price)
        if max_price is not None:
            sql.append("AND d.price <= ?")
            params.append(max_price)
        if only_available:
            sql.append("AND d.available = 1")
        if only_promo:
            sql.append(f"AND ({EFFECTIVE_DISCOUNT} > 0 OR d.offer_ends_at IS NOT NULL)")
        if min_discount:
            sql.append(f"AND {EFFECTIVE_DISCOUNT} >= ?")
            params.append(min_discount)
        sql.append(f"ORDER BY {SORTS.get(sort, SORTS['desconto'])} LIMIT ?")
        params.append(limit)
        with self.lock:
            rows = self.conn.execute("\n".join(sql), params).fetchall()
        return [dict(r) for r in rows]

    def history(self, deal_id: str) -> list[dict]:
        with self.lock:
            rows = self.conn.execute(
                "SELECT price, seen_at FROM price_history WHERE deal_id = ? ORDER BY seen_at",
                (deal_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    def pending_notifications(self, ids: list[str], min_discount: float) -> list[dict]:
        if not ids:
            return []
        with self.lock:
            rows = self.conn.execute(
                f"""SELECT d.*, {EFFECTIVE_DISCOUNT} AS effective_discount FROM deals d
                    WHERE d.id IN ({','.join('?' * len(ids))}) AND d.available = 1
                      AND {EFFECTIVE_DISCOUNT} >= ?""",
                [*ids, min_discount],
            ).fetchall()
        return [dict(r) for r in rows]
