"""
💭 Market Sentiment — Scutua-MCP
"""
import httpx
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_sentiment_tools(app):

    @app.tool()
    @mcp_safe_executor("get_market_sentiment")
    async def get_market_sentiment() -> dict:
        """Get overall crypto market sentiment"""
        cache_key = "market_sentiment"
        cached = cache.get(cache_key)
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.alternative.me/fng/",
                params={"limit": 7},
                timeout=10
            )
            data = r.json()
            cache.set(cache_key, data, ttl=3600)
            return data

