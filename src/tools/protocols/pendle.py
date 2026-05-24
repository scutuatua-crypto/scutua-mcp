"""
Pendle Finance Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api-v2.pendle.finance/core/v1/1"

async def _pendle_get(endpoint: str) -> dict:
    cache_key = f"pendle:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE_URL}{endpoint}", timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"Pendle error: {e}")
        return {"error": str(e)}

def register_pendle_tools(app):

    @app.tool()
    async def get_pendle_markets() -> dict:
        """Get active Pendle yield markets with fixed APY"""
        data = await _pendle_get("/markets?order_by=volume%3A-1&limit=10")
        if "error" in data:
            return data
        return {"markets": data.get("results", []), "protocol": "pendle"}

    @app.tool()
    async def get_pendle_assets() -> dict:
        """Get all Pendle supported yield-bearing assets"""
        data = await _pendle_get("/assets/all")
        if "error" in data:
            return data
        return {"assets": data, "protocol": "pendle"}

    @app.tool()
    async def get_pendle_pt_price(market_address: str) -> dict:
        """Get Principal Token price for a Pendle market"""
        return await _pendle_get(f"/markets/{market_address}")
