"""
Market Intelligence Universe Initialization — Scutua-MCP (Dimension 5)
Aggregates and registers all market intelligence feeds under a centralized registry.
"""
from mcp.server.fastmcp import FastMCP
from src.tools.market.coingecko import register_coingecko_tools

# Future dimension components to be activated sequentially
# from src.tools.market.cmc import register_cmc_tools
# from src.tools.market.trending import register_trending_tools
# from src.tools.market.sentiment import register_sentiment_tools
# from src.tools.market.fear_index import register_fear_index_tools

def register_market_tools(app: FastMCP) -> None:
    """
    Bootstrap and register all sub-modules belonging to Dimension 5: Market Intelligence.
    """
    # Initialize CoinGecko feeds
    register_coingecko_tools(app)
    
    # Placeholder for future multi-feed extensions
    # register_cmc_tools(app)
    # register_trending_tools(app)
    # register_sentiment_tools(app)
    # register_fear_index_tools(app)

@mcp_safe_executor("get_market_init_info")  # Keeping consistent structure if needed
async def get_market_init_info(query: str) -> str:
    """
    Provides fallback discovery telemetry for the Market Intelligence dimension.
    """
    try:
        return f"Dimension 5 (Market Intelligence) initialization status: Active. Metadata for query '{query}' is currently routing."
    except Exception as e:
        return f"Error executing market intelligence initialization telemetry: {str(e)}"
