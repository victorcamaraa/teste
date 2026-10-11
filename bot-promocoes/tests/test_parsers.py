"""Testes dos parsers com amostras no formato que cada loja usa.

As amostras são reduzidas à mão (só os campos que o parser lê); se uma loja mudar
o formato, atualize a amostra junto com o parser.
"""

import json

import pytest

from promobot.categories import matches_category
from promobot.http import parse_brl
from promobot.scrapers.kabum import parse_kabum
from promobot.scrapers.mercadolivre import parse_mercadolivre
from promobot.scrapers.pichau import parse_pichau
from promobot.scrapers.terabyte import parse_terabyte


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("R$ 1.299,90", 1299.90),
        ("R$\xa0899,00", 899.0),
        ("de: R$ 12.499,99 por", 12499.99),
        ("1299.9", 1299.9),
        ("1.299", 1299.0),
        (459, 459.0),
        (0, None),
        ("", None),
        (None, None),
    ],
)
def test_parse_brl(raw, expected):
    assert parse_brl(raw) == expected


@pytest.mark.parametrize(
    "title, category, expected",
    [
        ("Processador AMD Ryzen 7 5700X3D, AM4", "processador", True),
        ("Water Cooler para Processador 240mm", "processador", False),
        ("Notebook Gamer Intel Core i5 RTX 3050", "gpu", False),
        ("Memória RAM Kingston Fury Beast, 16GB, DDR4 3200MHz", "memoria", True),
        ("Cartão de Memória microSD 128GB", "memoria", False),
        ("Placa de Vídeo RTX 4060 Ti Gigabyte", "gpu", True),
        ("SSD Kingston NV2 1TB M.2 NVMe", "armazenamento", True),
        ("SSD Externo Portátil 1TB USB-C", "armazenamento", False),
        ("HD Seagate BarraCuda 2TB, 3.5', SATA - HD Interno", "armazenamento", True),
    ],
)
def test_matches_category(title, category, expected):
    assert matches_category(title, category) is expected


KABUM = {
    "data": [
        {
            "id": 520369,
            "type": "product",
            "attributes": {
                "title": "Processador AMD Ryzen 7 5700X3D",
                "price": 1499.99,
                "old_price": 1999.99,
                "price_with_discount": 1274.99,
                "available": True,
                "images": ["https://images.kabum.com.br/produtos/520369_g.jpg"],
                "offer": None,
            },
        },
        {
            "id": 111,
            "type": "product",
            "attributes": {
                "title": "Processador Intel Core i5-12400F",
                "price": 899.99,
                "old_price": 0,
                "price_with_discount": 764.99,
                "available": True,
                "photos": {"g": ["https://images.kabum.com.br/produtos/111_g.jpg"]},
                "offer": {"price_with_discount": 699.99, "ends_at": 1893456000},
            },
        },
        {"id": 222, "attributes": {"title": "Sem preço"}},
    ]
}


def test_parse_kabum():
    deals = parse_kabum(KABUM, "processador")
    assert len(deals) == 2
    ryzen, intel = deals
    assert ryzen.price == 1274.99
    assert ryzen.original_price == 1999.99
    assert ryzen.discount == 36.3
    assert ryzen.url == "https://www.kabum.com.br/produto/520369"
    assert intel.price == 699.99
    assert intel.original_price is None
    assert intel.offer_ends_at.startswith("2030-01-01")
    assert intel.image.endswith("111_g.jpg")
    assert intel.is_promo


PICHAU_NEXT = {
    "props": {
        "pageProps": {
            "apolloState": {
                "products": {
                    "items": [
                        {
                            "name": "Placa de Video Gigabyte GeForce RTX 4060 Eagle OC 8GB",
                            "url_key": "placa-de-video-gigabyte-rtx-4060",
                            "stock_status": "IN_STOCK",
                            "image": {"url": "https://media.pichau.com.br/rtx4060.jpg"},
                            "price_range": {
                                "minimum_price": {
                                    "regular_price": {"value": 2599.99},
                                    "final_price": {"value": 2199.99},
                                }
                            },
                            "pichau_prices": {"avista": 1869.99, "final_price": 2199.99},
                        },
                        {
                            "name": "Suporte para Placa de Video",
                            "url_key": "suporte-gpu",
                            "pichau_prices": {"avista": 49.9},
                        },
                    ]
                }
            }
        }
    }
}


def test_parse_pichau_next_data():
    html = (
        '<html><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(PICHAU_NEXT)
        + "</script></html>"
    )
    deals = parse_pichau(html, "gpu")
    assert [d.title for d in deals] == ["Placa de Video Gigabyte GeForce RTX 4060 Eagle OC 8GB"]
    gpu = deals[0]
    assert gpu.price == 1869.99
    assert gpu.original_price == 2599.99
    assert gpu.url == "https://www.pichau.com.br/placa-de-video-gigabyte-rtx-4060"


def test_parse_pichau_falls_back_to_json_ld():
    ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "item": {
                    "@type": "Product",
                    "name": "Memoria Kingston Fury Beast 16GB DDR5 5600MHz",
                    "url": "/memoria-kingston-fury-16gb-ddr5",
                    "image": ["https://media.pichau.com.br/fury.jpg"],
                    "offers": {
                        "@type": "AggregateOffer",
                        "lowPrice": "329.90",
                        "highPrice": "429.90",
                        "availability": "https://schema.org/InStock",
                    },
                },
            }
        ],
    }
    html = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    [deal] = parse_pichau(html, "memoria")
    assert deal.url == "https://www.pichau.com.br/memoria-kingston-fury-16gb-ddr5"
    assert deal.price == 329.90
    assert deal.original_price == 429.90


TERABYTE_HTML = """
<div class="product-item">
  <a href="/produto/12345/ssd-kingston-nv2-1tb" class="product-item__image">
    <img data-src="https://img.terabyteshop.com.br/produto/m/ssd.jpg" src="/loading.gif">
  </a>
  <a href="/produto/12345/ssd-kingston-nv2-1tb" class="product-item__name"
     title="SSD Kingston NV2 1TB, M.2 2280 NVMe PCIe 4.0"><h2>SSD Kingston NV2 1TB</h2></a>
  <div class="product-item__old-price"><del>de: R$ 649,90</del></div>
  <div class="product-item__new-price"><span>R$ 429,90</span> à vista</div>
</div>
<div class="product-item">
  <a href="/produto/999/hd-seagate-2tb" class="product-item__name" title="HD Seagate BarraCuda 2TB SATA">x</a>
  <div class="product-item__new-price"><span>R$ 389,90</span></div>
  <div class="tbt_esgotado">Esgotado</div>
</div>
<div class="product-item">
  <a href="/produto/555/gaveta-ssd" class="product-item__name" title="Gaveta Case para SSD M.2">x</a>
  <div class="product-item__new-price"><span>R$ 59,90</span></div>
</div>
"""


def test_parse_terabyte():
    deals = parse_terabyte(TERABYTE_HTML, "armazenamento")
    assert len(deals) == 2
    ssd, hd = deals
    assert ssd.title.startswith("SSD Kingston NV2")
    assert ssd.price == 429.90
    assert ssd.original_price == 649.90
    assert ssd.url == "https://www.terabyteshop.com.br/produto/12345/ssd-kingston-nv2-1tb"
    assert ssd.image == "https://img.terabyteshop.com.br/produto/m/ssd.jpg"
    assert ssd.available
    assert not hd.available


def test_parse_mercadolivre():
    payload = {
        "results": [
            {
                "title": "Memória Ram Corsair Vengeance 32gb (2x16) Ddr5 6000mhz",
                "price": 699,
                "original_price": 899,
                "permalink": "https://produto.mercadolivre.com.br/MLB-1",
                "thumbnail": "http://http2.mlstatic.com/D_1.jpg",
                "available_quantity": 5,
            },
            {
                "title": "Notebook Dell 16gb Ram Ddr4",
                "price": 3500,
                "permalink": "https://produto.mercadolivre.com.br/MLB-2",
            },
        ]
    }
    [deal] = parse_mercadolivre(payload, "memoria")
    assert deal.price == 699
    assert deal.discount == 22.2
    assert deal.image.startswith("https://")
