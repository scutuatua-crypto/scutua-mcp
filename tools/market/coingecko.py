"""
🦎 CoinGecko Market Feed — Scutua-MCP
"""
import httpx
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_coingecko_tools(app):

    @app.tool()
    @mcp_safe_executor("get_coingecko_price")
    async def get_coingecko_price(coin_id: str) -> dict:
        """Get token price from CoinGecko"""
        cache_key = f"coingecko_price_{coin_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd,thb"},
                timeout=10
            )
            data = r.json()
            cache.set(cache_key, data, ttl=60)
            return data

    @app.tool()
    @mcp_safe_executor("get_coingecko_trending")
    async def get_coingecko_trending() -> dict:
        """Get trending coins from CoinGecko"""
        cache_key = "coingecko_trending"
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

