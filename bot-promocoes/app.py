"""Interface web do bot de promoções.

    python app.py            -> http://localhost:5000
"""

from __future__ import annotations

import logging
import os

from flask import Flask, jsonify, render_template, request

from promobot.categories import CATEGORIES
from promobot.collector import Scheduler
from promobot.scrapers import SCRAPERS
from promobot.storage import SORTS, Storage


def _float(value):
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None


def create_app(storage: Storage | None = None, scheduler: Scheduler | None = None) -> Flask:
    app = Flask(__name__)
    storage = storage or Storage(os.environ.get("PROMOBOT_DB", "promocoes.db"))
    if scheduler is None:
        scheduler = Scheduler(storage, float(os.environ.get("INTERVALO_MINUTOS", "30")))
        scheduler.start()

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            categories=CATEGORIES,
            stores=[s.label for s in SCRAPERS],
        )

    @app.get("/api/deals")
    def deals():
        args = request.args
        rows = storage.query(
            categories=args.getlist("categoria") or None,
            stores=args.getlist("loja") or None,
            text=args.get("q") or None,
            min_price=_float(args.get("preco_min")),
            max_price=_float(args.get("preco_max")),
            min_discount=_float(args.get("desconto_min")) or 0,
            only_promo=args.get("so_promocoes", "1") == "1",
            only_available=args.get("so_disponiveis", "1") == "1",
            sort=args.get("ordem") if args.get("ordem") in SORTS else "desconto",
        )
        return jsonify(deals=rows)

    @app.get("/api/deals/<deal_id>/historico")
    def history(deal_id):
        return jsonify(historico=storage.history(deal_id))

    @app.get("/api/status")
    def status():
        return jsonify(
            coletando=scheduler.busy, ultima_coleta=scheduler.last_run, lojas=storage.status()
        )

    @app.post("/api/atualizar")
    def refresh():
        return jsonify(iniciado=scheduler.trigger())

    return app


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    create_app().run(
        host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "5000"))
    )
