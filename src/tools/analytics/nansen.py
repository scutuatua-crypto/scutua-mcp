"""
Nansen Analytics Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

NANSEN_API_KEY = os.getenv("NANSEN_API_KEY", "")
BASE_URL = "https://api.nansen.ai/v1"

async def _nansen_get(endpoint: str) -> dict:
    if not NANSEN_API_KEY:
        return {"error": "NANSEN_API_KEY not configured"}
    cache_key = f"nansen:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}{endpoint}",
                headers={"apiKey": NANSEN_API_KEY},
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"Nansen error: {e}")
        return {"error": str(e)}

def register_nansen_tools(app):

    @app.tool()
    async def get_smart_money_flows() -> dict:
        """Get smart money wallet flows from Nansen"""
        return await _nansen_get("/smart-money/flows")

    @app.tool()
    async def get_nansen_token_god_mode(token_address: str) -> dict:
        """Get token analytics in God Mode from Nansen"""
        return await _nansen_get(f"/token/{token_address}")

    @app.tool()
    async def get_wallet_label(address: str) -> dict:
        """Get Nansen wallet label (whale, smart money, etc.)"""
        return await _nansen_get(f"/wallet/{address}/label")
