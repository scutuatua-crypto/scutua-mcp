"""
Birdeye Analytics Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")
BASE_URL = "https://public-api.birdeye.so"

async def _birdeye_get(endpoint: str, params: dict = {}) -> dict:
    cache_key = f"birdeye:{endpoint}:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        headers = {"X-API-KEY": BIRDEYE_API_KEY}
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE_URL}{endpoint}", headers=headers, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"Birdeye error: {e}")
        return {"error": str(e)}

def register_birdeye_tools(app):

    @app.tool()
    async def get_token_price_birdeye(token_address: str) -> dict:
        """Get real-time token price from Birdeye"""
        return await _birdeye_get("/defi/price", {"address": token_address})

    @app.tool()
    async def get_token_trending_birdeye() -> dict:
        """Get trending tokens on Solana from Birdeye"""
        return await _birdeye_get("/defi/trending_tokens")

    @app.tool()
    async def get_wallet_portfolio_birdeye(wallet_address: str) -> dict:
        """Get full wallet portfolio from Birdeye"""
        return await _birdeye_get("/v1/wallet/token_list", {"wallet": wallet_address})

    @app.tool()
    async def get_token_overview_birdeye(token_address: str) -> dict:
        """Get token overview from Birdeye"""
        return await _birdeye_get("/defi/token_overview", {"address": token_address})
