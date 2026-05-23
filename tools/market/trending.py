"""
🔥 Trending Tokens — Scutua-MCP
"""
import httpx
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_trending_tools(app):

    @app.tool()
    @mcp_safe_executor("get_trending_tokens")
    async def get_trending_tokens() -> dict:
        """Get trending tokens across DEXes"""
        cache_key = "trending_tokens"
        cached = cache.get(cache_key)
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.coingecko.com/api/v3/search/trending",
                timeout=10
            )
            data = r.json()
            cache.set(cache_key, data, ttl=300)
            return data

