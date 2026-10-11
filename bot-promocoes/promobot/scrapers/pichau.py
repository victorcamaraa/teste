from __future__ import annotations

import json
import re

from ..categories import matches_category
from ..http import TIMEOUT, parse_brl
from ..models import Deal
from .base import Scraper, deal_from_ld, json_ld_products

BASE = "https://www.pichau.com.br"

CATEGORY_PATHS = {
    "processador": ["/hardware/processadores"],
    "memoria": ["/hardware/memorias"],
    "gpu": ["/hardware/placa-de-video"],
    "armazenamento": ["/hardware/ssd", "/hardware/hard-disk-e-ssd"],
}

NEXT_DATA = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)


class PichauScraper(Scraper):
    """Pichau é um site Next.js: os produtos vêm no JSON __NEXT_DATA__ da página."""

    name = "pichau"
    label = "Pichau"

    def fetch(self, category: str) -> list[Deal]:
        deals, last_error = [], None
        for path in CATEGORY_PATHS[category]:
            resp = self.session.get(BASE + path, timeout=TIMEOUT)
            if resp.status_code == 404:
                last_error = f"404 em {path}"
                continue
            resp.raise_for_status()
            deals.extend(parse_pichau(resp.text, category))
        if not deals and last_error:
            raise RuntimeError(last_error)
        return deals


def parse_pichau(html: str, category: str) -> list[Deal]:
    deals = {}
    match = NEXT_DATA.search(html)
    if match:
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            data = None
        for product in _walk_products(data):
            deal = _deal_from_magento(product, category)
            if deal:
                deals[deal.url] = deal
    if not deals:
        for product in json_ld_products(html):
            deal = deal_from_ld(product, PichauScraper.label, category, BASE)
            if deal:
                deals[deal.url] = deal
    return [d for d in deals.values() if matches_category(d.title, category)]


def _walk_products(node):
    """Encontra objetos com cara de produto Magento (name + url_key + preço)."""
    if isinstance(node, dict):
        if "name" in node and "url_key" in node and (
            "price_range" in node or "pichau_prices" in node
        ):
            yield node
            return
        for value in node.values():
            yield from _walk_products(value)
    elif isinstance(node, list):
        for value in node:
            yield from _walk_products(value)


def _deal_from_magento(p: dict, category: str) -> Deal | None:
    prices = p.get("pichau_prices") or {}
    minimum = (p.get("price_range") or {}).get("minimum_price") or {}
    price = (
        parse_brl(prices.get("avista"))
        or parse_brl((minimum.get("final_price") or {}).get("value"))
        or parse_brl(prices.get("final_price"))
    )
    if not price:
        return None
    original = parse_brl((minimum.get("regular_price") or {}).get("value")) or parse_brl(
        prices.get("base_price")
    )
    image = p.get("image")
    if isinstance(image, dict):
        image = image.get("url")
    return Deal(
        store=PichauScraper.label,
        category=category,
        title=str(p["name"]).strip(),
        url=f"{BASE}/{p['url_key']}",
        price=price,
        original_price=original if original and original > price else None,
        image=image,
        available=p.get("stock_status", "IN_STOCK") == "IN_STOCK",
    )
