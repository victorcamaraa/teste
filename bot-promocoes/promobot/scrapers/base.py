from __future__ import annotations

import json
from typing import Iterator

from bs4 import BeautifulSoup

from ..http import make_session, parse_brl
from ..models import Deal


class Scraper:
    """Base para os coletores de cada loja."""

    name = "base"
    label = "Base"

    def __init__(self, session=None):
        self.session = session or make_session()

    def fetch(self, category: str) -> list[Deal]:
        raise NotImplementedError


def json_ld_products(html: str) -> Iterator[dict]:
    """Percorre os blocos JSON-LD da página e devolve objetos schema.org Product."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        yield from _walk_ld(data)


def _walk_ld(node) -> Iterator[dict]:
    if isinstance(node, list):
        for item in node:
            yield from _walk_ld(item)
    elif isinstance(node, dict):
        kind = node.get("@type")
        if kind == "Product" or (isinstance(kind, list) and "Product" in kind):
            yield node
            return
        for key in ("@graph", "itemListElement", "item"):
            if key in node:
                yield from _walk_ld(node[key])


def deal_from_ld(product: dict, store: str, category: str, base_url: str) -> Deal | None:
    offers = product.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    price = parse_brl(offers.get("price") or offers.get("lowPrice"))
    url = product.get("url") or offers.get("url")
    title = product.get("name")
    if not (price and url and title):
        return None
    if url.startswith("/"):
        url = base_url.rstrip("/") + url
    image = product.get("image")
    if isinstance(image, list):
        image = image[0] if image else None
    if isinstance(image, dict):
        image = image.get("url")
    original = parse_brl(offers.get("highPrice"))
    availability = str(offers.get("availability", "InStock"))
    return Deal(
        store=store,
        category=category,
        title=title.strip(),
        url=url,
        price=price,
        original_price=original if original and original > price else None,
        image=image,
        available="OutOfStock" not in availability,
    )
