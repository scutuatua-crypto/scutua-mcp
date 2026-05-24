"""
Alternative.me Market Data — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.alternative.me"

async def _alt_get(endpoint: str) -> dict:
    cache_key = f"alternative:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE_URL}{endpoint}", timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=300)
            return data
    except Exception as e:
        logger.error(f"Alternative.me error: {e}")
        return {"error": str(e)}

def register_alternative_tools(app):

    @app.tool()
    async def get_fear_greed_index() -> dict:
        """Get current Crypto Fear & Greed Index from Alternative.me"""
        data = await _alt_get("/fng/?limit=1")
        if "error" in data:
            return data
        item = data.get("data", [{}])[0]
        return {
            "value": item.get("value"),
            "classification": item.get("value_classification"),
            "timestamp": item.get("timestamp")
        }

    @app.tool()
    async def get_fear_greed_history(limit: int = 30) -> dict:
        """Get Fear & Greed Index history"""
        return await _alt_get(f"/fng/?limit={limit}")

    @app.tool()
    async def get_global_crypto_stats() -> dict:
        """Get global cryptocurrency market statistics"""
        return await _alt_get("/v2/global/")
