"""
😱 Fear & Greed Index — Scutua-MCP
"""
import httpx
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_fear_index_tools(app):

    @app.tool()
    @mcp_safe_executor("get_fear_index")
    async def get_fear_index() -> dict:
        """Get Crypto Fear & Greed Index history"""
        cache_key = "fear_index"
        cached = cache.get(cache_key)
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.alternative.me/fng/",
                params={"limit": 30},
                timeout=10
            )
            data = r.json()
            cache.set(cache_key, data, ttl=3600)
            return data

