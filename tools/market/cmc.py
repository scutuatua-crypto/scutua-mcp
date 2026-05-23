"""
📊 CoinMarketCap Feed — Scutua-MCP
"""
import httpx
import os
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)
CMC_API_KEY = os.environ.get("CMC_API_KEY", "")

def register_cmc_tools(app):

    @app.tool()
    @mcp_safe_executor("get_cmc_listings")
    async def get_cmc_listings(limit: int = 10) -> dict:
        """Get top crypto listings from CoinMarketCap"""
        cache_key = f"cmc_listings_{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
                headers={"X-CMC_PRO_API_KEY": CMC_API_KEY},
                params={"limit": limit, "convert": "USD"},
                timeout=10
            )
            data = r.json()
            cache.set(cache_key, data, ttl=120)
            return data

