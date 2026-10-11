from __future__ import annotations

from datetime import datetime, timezone

from ..http import TIMEOUT, parse_brl
from ..models import Deal
from .base import Scraper

API = "https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/{path}"

CATEGORY_PATHS = {
    "processador": ["hardware/processadores"],
    "memoria": ["hardware/memoria-ram"],
    "gpu": ["hardware/placa-de-video-vga"],
    "armazenamento": ["hardware/ssd-2-5", "hardware/disco-rigido-hd"],
}


class KabumScraper(Scraper):
    """KaBuM! expõe o catálogo numa API JSON pública usada pelo próprio site."""

    name = "kabum"
    label = "KaBuM!"

    def fetch(self, category: str) -> list[Deal]:
        deals = []
        for path in CATEGORY_PATHS[category]:
            resp = self.session.get(
                API.format(path=path),
                params={
                    "page_number": 1,
                    "page_size": 100,
                    "facet_filters": "",
                    "sort": "most_searched",
                    "include": "gift",
                },
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
            deals.extend(parse_kabum(resp.json(), category))
        return deals


def parse_kabum(payload: dict, category: str) -> list[Deal]:
    deals = []
    for item in payload.get("data", []):
        attrs = item.get("attributes", {})
        offer = attrs.get("offer") or {}
        price = (
            parse_brl(offer.get("price_with_discount"))
            or parse_brl(attrs.get("price_with_discount"))
            or parse_brl(attrs.get("price"))
        )
        title = attrs.get("title")
        if not (price and title):
            continue
        original = parse_brl(attrs.get("old_price"))
        images = attrs.get("images") or (attrs.get("photos") or {}).get("g") or []
        deals.append(
            Deal(
                store=KabumScraper.label,
                category=category,
                title=title.strip(),
                url=f"https://www.kabum.com.br/produto/{item.get('id')}",
                price=price,
                original_price=original if original and original > price else None,
                image=images[0] if images else None,
                available=bool(attrs.get("available", True)),
                offer_ends_at=_offer_end(offer),
            )
        )
    return deals


def _offer_end(offer: dict) -> str | None:
    ends = offer.get("ends_at")
    if not ends:
        return None
    if isinstance(ends, (int, float)):
        return datetime.fromtimestamp(ends, tz=timezone.utc).isoformat(timespec="seconds")
    return str(ends)
