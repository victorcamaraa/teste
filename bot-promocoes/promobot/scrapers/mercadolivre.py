from __future__ import annotations

import os

from ..categories import CATEGORIES, matches_category
from ..http import TIMEOUT, parse_brl
from ..models import Deal
from .base import Scraper

API = "https://api.mercadolibre.com/sites/MLB/search"


class MercadoLivreScraper(Scraper):
    """API pública de busca do Mercado Livre.

    O ML passou a exigir token em parte das requisições; se a busca anônima
    falhar, defina ML_ACCESS_TOKEN (gerado em developers.mercadolivre.com.br).
    """

    name = "mercadolivre"
    label = "Mercado Livre"

    def fetch(self, category: str) -> list[Deal]:
        headers = {}
        token = os.environ.get("ML_ACCESS_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        resp = self.session.get(
            API,
            params={
                "q": CATEGORIES[category]["search"],
                "condition": "new",
                "limit": 50,
            },
            headers=headers,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return parse_mercadolivre(resp.json(), category)


def parse_mercadolivre(payload: dict, category: str) -> list[Deal]:
    deals = []
    for item in payload.get("results", []):
        title = item.get("title") or ""
        price = parse_brl(item.get("price"))
        if not (price and item.get("permalink")) or not matches_category(title, category):
            continue
        original = parse_brl(item.get("original_price"))
        thumb = item.get("thumbnail")
        deals.append(
            Deal(
                store=MercadoLivreScraper.label,
                category=category,
                title=title.strip(),
                url=item["permalink"],
                price=price,
                original_price=original if original and original > price else None,
                image=thumb.replace("http://", "https://") if thumb else None,
                available=(item.get("available_quantity") or 1) > 0,
            )
        )
    return deals
