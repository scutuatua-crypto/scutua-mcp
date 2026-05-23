from .coingecko import register_coingecko_tools
from .cmc import register_cmc_tools
from .trending import register_trending_tools
from .sentiment import register_sentiment_tools
from .fear_index import register_fear_index_tools

__all__ = [
    "register_coingecko_tools",
    "register_cmc_tools",
    "register_trending_tools",
    "register_sentiment_tools",
    "register_fear_index_tools",
]

