# Scrapers package
from .bioicons import scrape_bioicons
from .scidraw import scrape_scidraw
 
from .bioart import scrape_bioart
from .flaticon import scrape_flaticon
from .nounproject import scrape_nounproject
from .freepik import scrape_freepik
from .vecteezy import scrape_vecteezy
from .pixabay import scrape_pixabay
from .svgrepo import scrape_svgrepo
from .openclipart import scrape_openclipart

__all__ = [
    'scrape_bioicons',
    'scrape_scidraw',
    'scrape_bioart',
    'scrape_flaticon',
    'scrape_nounproject',
    'scrape_freepik',
    'scrape_vecteezy',
    'scrape_pixabay',
    'scrape_svgrepo',
    'scrape_openclipart',
]
