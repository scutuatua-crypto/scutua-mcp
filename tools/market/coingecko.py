"""
CoinGecko Market Intelligence Feed — Scutua-MCP (Dimension 5)
"""
import httpx
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_coingecko_tools(app):
    """
    Registers CoinGecko market data intelligence tools into the MCP application context.
    """

    @app.tool()
    @mcp_safe_executor("get_coingecko_price")
    async def get_coingecko_price(coin_id: str) -> dict:
        """
        Fetch the live cryptocurrency price from CoinGecko API.
        Returns valuation in both USD and THB tracking metrics.
        """
        cache_key = f"coingecko_price_{coin_id}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd,thb"},
                timeout=10
            )
            data = response.json()
            cache.set(cache_key, data, ttl=60)
            return data

    @app.tool()
    @mcp_safe_executor("get_coingecko_trending")
    async def get_coingecko_trending() -> dict:
        """
        Fetch globally trending search tokens from the CoinGecko ecosystem.
        Useful for discovering short-term market narratives and velocity tracking.
        """
        cache_key = "coingecko_trending"
        cached = cache.get(cache_key)
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.coingecko.com/api/v3/search/trending",
                timeout=10
            )
            data = response.json()
            cache.set(cache_key, data, ttl=300)
            return data
