from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Deal:
    """Um produto encontrado em uma loja."""

    store: str
    category: str
    title: str
    url: str
    price: float
    original_price: float | None = None
    image: str | None = None
    available: bool = True
    offer_ends_at: str | None = None
    found_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="microseconds")
    )

    @property
    def id(self) -> str:
        return hashlib.sha1(f"{self.store}|{self.url}".encode()).hexdigest()[:16]

    @property
    def discount(self) -> float:
        """Desconto percentual em relação ao preço original (0 se não houver)."""
        if not self.original_price or self.original_price <= self.price:
            return 0.0
        return round((1 - self.price / self.original_price) * 100, 1)

    @property
    def is_promo(self) -> bool:
        return self.discount > 0 or self.offer_ends_at is not None
