from .kabum import KabumScraper
from .mercadolivre import MercadoLivreScraper
from .pichau import PichauScraper
from .terabyte import TerabyteScraper

SCRAPERS = [KabumScraper, PichauScraper, TerabyteScraper, MercadoLivreScraper]

__all__ = ["SCRAPERS"]
