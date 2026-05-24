"""
LunarCrush Social Intelligence — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

LUNARCRUSH_API_KEY = os.getenv("LUNARCRUSH_API_KEY", "")
BASE_URL = "https://lunarcrush.com/api4/public"

async def _lunarcrush_get(endpoint: str, params: dict = {}) -> dict:
    if not LUNARCRUSH_API_KEY:
        return {"error": "LUNARCRUSH_API_KEY not configured"}
    cache_key = f"lunarcrush:{endpoint}:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}{endpoint}",
                headers={"Authorization": f"Bearer {LUNARCRUSH_API_KEY}"},
                params=params,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"LunarCrush error: {e}")
        return {"error": str(e)}

def register_lunarcrush_tools(app):

    @app.tool()
    async def get_social_dominance(token: str) -> dict:
        """Get social dominance score for a token from LunarCrush"""
        return await _lunarcrush_get(f"/coins/{token}/v1")

    @app.tool()
    async def get_galaxy_score(token: str) -> dict:
        """Get LunarCrush Galaxy Score for a token"""
        data = await _lunarcrush_get(f"/coins/{token}/v1")
        if "error" in data:
            return data
        coin = data.get("data", {})
        return {"token": token, "galaxy_score": coin.get("galaxy_score"), "alt_rank": coin.get("alt_rank")}

    @app.tool()
    async def get_trending_social() -> dict:
        """Get trending crypto assets by social activity"""
        return await _lunarcrush_get("/coins/list/v2", {"sort": "galaxy_score", "limit": 20})
