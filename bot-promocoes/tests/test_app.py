import pytest

from app import create_app
from promobot.collector import collect_all
from promobot.models import Deal
from promobot.storage import Storage


class FakeScraper:
    """Loja de teste: devolve os preços configurados em `catalog`."""

    name = "fake"
    label = "Loja Teste"
    catalog: dict[str, list[tuple]] = {}
    fail = False

    def fetch(self, category):
        if self.fail:
            raise RuntimeError("site fora do ar")
        return [
            Deal(store=self.label, category=category, title=title, url=url,
                 price=price, original_price=original)
            for title, url, price, original in self.catalog.get(category, [])
        ]


class IdleScheduler:
    busy = False
    last_run = None

    def trigger(self):
        return True


@pytest.fixture
def storage(tmp_path):
    return Storage(str(tmp_path / "test.db"))


@pytest.fixture(autouse=True)
def reset_fake():
    FakeScraper.catalog = {}
    FakeScraper.fail = False


def run(storage, monkeypatch):
    monkeypatch.setattr("promobot.collector.time.sleep", lambda _: None)
    return collect_all(storage, categories=["gpu", "memoria"], scrapers=[FakeScraper])


def test_promotions_and_price_drops(storage, monkeypatch):
    FakeScraper.catalog = {
        "gpu": [
            ("RTX 4060", "https://x/rtx4060", 1800.0, 2400.0),
            ("RX 7600", "https://x/rx7600", 1500.0, None),
        ],
        "memoria": [("DDR5 16GB", "https://x/ddr5", 350.0, None)],
    }
    run(storage, monkeypatch)
    promos = storage.query()
    assert [d["title"] for d in promos] == ["RTX 4060"]
    assert promos[0]["effective_discount"] == 25.0
    assert len(storage.query(only_promo=False)) == 3

    # RX 7600 baixou de preço desde a última coleta -> vira promoção.
    FakeScraper.catalog["gpu"][1] = ("RX 7600", "https://x/rx7600", 1350.0, None)
    run(storage, monkeypatch)
    promos = {d["title"]: d for d in storage.query(categories=["gpu"])}
    assert promos["RX 7600"]["effective_discount"] == 10.0
    assert promos["RX 7600"]["previous_price"] == 1500.0
    assert promos["RX 7600"]["lowest_price"] == 1350.0
    assert len(storage.history(promos["RX 7600"]["id"])) == 2


def test_products_gone_from_listing_are_hidden(storage, monkeypatch):
    FakeScraper.catalog = {"gpu": [("RTX 4060", "https://x/a", 1800.0, 2400.0)]}
    run(storage, monkeypatch)
    assert len(storage.query()) == 1

    FakeScraper.catalog = {"gpu": []}
    run(storage, monkeypatch)
    assert storage.query() == []


def test_failed_store_keeps_last_results(storage, monkeypatch):
    FakeScraper.catalog = {"gpu": [("RTX 4060", "https://x/a", 1800.0, 2400.0)]}
    run(storage, monkeypatch)
    FakeScraper.fail = True
    run(storage, monkeypatch)
    assert len(storage.query()) == 1
    status = {s["category"]: s for s in storage.status()}
    assert status["gpu"]["ok"] == 0
    assert "fora do ar" in status["gpu"]["message"]


def test_api_filters(storage, monkeypatch):
    FakeScraper.catalog = {
        "gpu": [
            ("Placa RTX 4060", "https://x/a", 1800.0, 2400.0),
            ("Placa RTX 4070", "https://x/b", 3500.0, 3900.0),
        ],
        "memoria": [("Memória DDR5 16GB", "https://x/c", 300.0, 400.0)],
    }
    run(storage, monkeypatch)
    client = create_app(storage, IdleScheduler()).test_client()

    def titles(query):
        return sorted(d["title"] for d in client.get(f"/api/deals?{query}").json["deals"])

    assert len(titles("")) == 3
    assert titles("categoria=memoria") == ["Memória DDR5 16GB"]
    assert titles("categoria=gpu&preco_max=2000") == ["Placa RTX 4060"]
    assert titles("desconto_min=20") == ["Memória DDR5 16GB", "Placa RTX 4060"]
    assert titles("q=rtx 4070") == ["Placa RTX 4070"]
    assert titles("loja=Outra") == []

    page = client.get("/")
    assert page.status_code == 200
    assert "Placas de Vídeo" in page.get_data(as_text=True)
    assert client.get("/api/status").json["lojas"]
    assert client.post("/api/atualizar").json == {"iniciado": True}
