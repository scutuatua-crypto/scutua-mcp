"""
Market Intelligence Universe Initialization — Scutua-MCP (Dimension 5)
Uses absolute clean relative pathing to bypass environment routing bugs.
"""
from mcp.server.fastmcp import FastMCP

# Force relative import to strict local files to avoid src/src mismatch
from .coingecko import register_coingecko_tools
from .cmc import register_cmc_tools
from .trending import register_trending_tools
from .sentiment import register_sentiment_tools
from .fear_index import register_fear_index_tools

def register_market_tools(app: FastMCP) -> None:
    """
    Registers Dimension 5 modules cleanly without global path dependency.
    """
    register_coingecko_tools(app)
    register_cmc_tools(app)
    register_trending_tools(app)
    register_sentiment_tools(app)
    register_fear_index_tools(app)
