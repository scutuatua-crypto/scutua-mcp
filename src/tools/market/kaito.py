"""
Kaito AI Market Intelligence — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

KAITO_API_KEY = os.getenv("KAITO_API_KEY", "")
BASE_URL = "https://api.kaito.ai/api/v1"

async def _kaito_get(endpoint: str, params: dict = {}) -> dict:
    if not KAITO_API_KEY:
        return {"error": "KAITO_API_KEY not configured"}
    cache_key = f"kaito:{endpoint}:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}{endpoint}",
                headers={"Authorization": f"Bearer {KAITO_API_KEY}"},
                params=params,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"Kaito error: {e}")
        return {"error": str(e)}

def register_kaito_tools(app):

    @app.tool()
    async def get_kaito_mindshare(token: str) -> dict:
        """Get crypto mindshare score from Kaito AI"""
        return await _kaito_get("/mindshare", {"ticker": token})

    @app.tool()
    async def get_kaito_trending() -> dict:
        """Get trending crypto topics from Kaito AI"""
        return await _kaito_get("/trending")
