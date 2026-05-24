"""
GMX Protocol Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def _gmx_get(url: str, cache_ttl: int = 60) -> dict:
    cache_key = f"gmx:{url}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=cache_ttl)
            return data
    except Exception as e:
        logger.error(f"GMX error: {e}")
        return {"error": str(e)}

def register_gmx_tools(app):

    @app.tool()
    async def get_gmx_stats() -> dict:
        """Get GMX protocol stats — volume, fees, open interest"""
        data = await _gmx_get("https://stats.gmx.io/api/gmx-supply")
        if "error" in data:
            return data
        return {"stats": data, "protocol": "gmx"}

    @app.tool()
    async def get_gmx_prices() -> dict:
        """Get GMX token prices for supported assets"""
        data = await _gmx_get("https://arbitrum-api.gmxinfra.io/prices/tickers")
        if "error" in data:
            return data
        return {"prices": data, "protocol": "gmx"}

    @app.tool()
    async def get_gmx_pools() -> dict:
        """Get GMX V2 liquidity pools (GM pools)"""
        data = await _gmx_get("https://arbitrum-api.gmxinfra.io/markets")
        if "error" in data:
            return data
        return {"pools": data, "protocol": "gmx"}
