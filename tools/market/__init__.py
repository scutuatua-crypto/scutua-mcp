"""
Market Intelligence Registry Initialization — Scutua-MCP (Dimension 5)
Handles module exposure using standard absolute imports.
"""
from src.tools.market.coingecko import register_coingecko_tools
from src.tools.market.cmc import register_cmc_tools
from src.tools.market.trending import register_trending_tools
from src.tools.market.sentiment import register_sentiment_tools
from src.tools.market.fear_index import register_fear_index_tools

# Expose definitions to the master tool registry
__all__ = [
    "register_coingecko_tools",
    "register_cmc_tools",
    "register_trending_tools",
    "register_sentiment_tools",
    "register_fear_index_tools"
]
