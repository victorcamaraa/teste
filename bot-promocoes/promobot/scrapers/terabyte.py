from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..categories import matches_category
from ..http import TIMEOUT, parse_brl
from ..models import Deal
from .base import Scraper, deal_from_ld, json_ld_products

BASE = "https://www.terabyteshop.com.br"

CATEGORY_PATHS = {
    "processador": ["/hardware/processadores"],
    "memoria": ["/hardware/memorias"],
    "gpu": ["/hardware/placas-de-video"],
    "armazenamento": ["/hardware/hard-disk"],
}

# Os nomes de classe já mudaram algumas vezes; tentamos cada seletor em ordem.
CARD_SELECTORS = [".product-item", ".pbox", "[class*=product-item]"]
NAME_SELECTORS = ["a.product-item__name", "a.prod-name", "h2 a", "a[title]"]
PRICE_SELECTORS = [".product-item__new-price", ".prod-new-price", "[class*=new-price]"]
OLD_PRICE_SELECTORS = [".product-item__old-price", ".prod-old-price", "[class*=old-price]"]


class TerabyteScraper(Scraper):
    name = "terabyte"
    label = "Terabyte"

    def fetch(self, category: str) -> list[Deal]:
        deals = []
        for path in CATEGORY_PATHS[category]:
            resp = self.session.get(BASE + path, timeout=TIMEOUT)
            resp.raise_for_status()
            deals.extend(parse_terabyte(resp.text, category))
        return deals


def _first(node, selectors):
    for selector in selectors:
        found = node.select_one(selector)
        if found:
            return found
    return None


def parse_terabyte(html: str, category: str) -> list[Deal]:
    soup = BeautifulSoup(html, "html.parser")
    deals = {}
    cards = []
    for selector in CARD_SELECTORS:
        cards = soup.select(selector)
        if cards:
            break
    for card in cards:
        link = _first(card, NAME_SELECTORS)
        price_el = _first(card, PRICE_SELECTORS)
        if not (link and price_el and link.get("href")):
            continue
        price = parse_brl(price_el.get_text())
        title = (link.get("title") or link.get_text()).strip()
        if not (price and title):
            continue
        old_el = _first(card, OLD_PRICE_SELECTORS)
        original = parse_brl(old_el.get_text()) if old_el else None
        img = card.select_one("img")
        image = img and (img.get("data-src") or img.get("src"))
        url = urljoin(BASE, link["href"])
        deals[url] = Deal(
            store=TerabyteScraper.label,
            category=category,
            title=title,
            url=url,
            price=price,
            original_price=original if original and original > price else None,
            image=urljoin(BASE, image) if image else None,
            available=not card.select_one(".tbt_esgotado, [class*=esgotado]"),
        )
    if not deals:
        for product in json_ld_products(html):
            deal = deal_from_ld(product, TerabyteScraper.label, category, BASE)
            if deal:
                deals[deal.url] = deal
    return [d for d in deals.values() if matches_category(d.title, category)]
