"""Tipos de peça suportados e classificação de títulos por palavra-chave."""

from __future__ import annotations

import re
import unicodedata

CATEGORIES = {
    "processador": {
        "label": "Processadores",
        "search": "processador",
        "include": ["processador", "cpu", "ryzen", "core i3", "core i5", "core i7",
                    "core i9", "core ultra", "intel core", "athlon", "pentium", "celeron"],
    },
    "memoria": {
        "label": "Memória RAM",
        "search": "memoria ram ddr",
        "include": ["memoria ram", "memoria", "ddr3", "ddr4", "ddr5", "sodimm", "udimm"],
    },
    "gpu": {
        "label": "Placas de Vídeo",
        "search": "placa de video",
        "include": ["placa de video", "geforce", "radeon", "rtx", "gtx", "arc a", "arc b",
                    "rx 5", "rx 6", "rx 7", "rx 9"],
    },
    "armazenamento": {
        "label": "Armazenamento",
        "search": "ssd",
        "include": ["ssd", "nvme", "m.2", "hd ", "disco rigido", "hard disk", "hdd"],
    },
}

# Produtos que costumam aparecer em buscas por texto mas não são a peça em si.
EXCLUDE = ["notebook", "computador", "pc gamer", "desktop", "celular", "smartphone",
           "cooler", "water cooler", "gabinete", "case para", "suporte", "cabo",
           "adaptador", "dissipador", "pasta termica", "kit upgrade", "console",
           "case externo", "gaveta", "hd externo", "ssd externo", "pen drive", "cartao de memoria",
           "monitor", "smart tv"]


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", text.lower()).strip()


def matches_category(title: str, category: str) -> bool:
    """True se o título parece ser uma peça da categoria pedida."""
    t = normalize(title) + " "
    if any(_has(t, word) for word in EXCLUDE):
        return False
    return any(_has(t, word) for word in CATEGORIES[category]["include"])


def _has(text: str, word: str) -> bool:
    # \b só no início: "rx 6" casa com "rx 6600", mas "hd " não casa com "ssd ".
    return re.search(r"\b" + re.escape(word), text) is not None
