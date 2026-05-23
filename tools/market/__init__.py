"""
Market Intelligence Universe Initialization — Scutua-MCP (Dimension 5)
Fixes absolute sub-module routing paths for cloud runtime environments.
"""
from mcp.server.fastmcp import FastMCP

# Dimension 5 Absolute Node Imports
from src.tools.market.coingecko import register_coingecko_tools
from src.tools.market.cmc import register_cmc_tools
from src.tools.market.trending import register_trending_tools
from src.tools.market.sentiment import register_sentiment_tools
from src.tools.market.fear_index import register_fear_index_tools

def register_market_tools(app: FastMCP) -> None:
    """
    Sequentially registers all core market metrics under the standard fastmcp application context.
    """
    register_coingecko_tools(app)
    register_cmc_tools(app)
    register_trending_tools(app)
    register_sentiment_tools(app)
    register_fear_index_tools(app)
