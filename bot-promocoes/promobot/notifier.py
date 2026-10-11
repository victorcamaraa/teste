"""Alertas opcionais no Telegram (defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID)."""

from __future__ import annotations

import logging
import os

import requests

log = logging.getLogger(__name__)


def telegram_enabled() -> bool:
    return bool(os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID"))


def format_deal(deal: dict) -> str:
    lines = [f"🔥 {deal['title']}", f"🏬 {deal['store']}"]
    price = f"💰 R$ {deal['price']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if deal.get("effective_discount"):
        price += f"  (-{deal['effective_discount']:.0f}%)"
    lines += [price, deal["url"]]
    return "\n".join(lines)


def notify(deals: list[dict]) -> int:
    if not telegram_enabled() or not deals:
        return 0
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    sent = 0
    for deal in deals:
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": format_deal(deal)},
                timeout=15,
            )
            resp.raise_for_status()
            sent += 1
        except requests.RequestException as exc:
            log.warning("Falha ao enviar alerta no Telegram: %s", exc)
    return sent
