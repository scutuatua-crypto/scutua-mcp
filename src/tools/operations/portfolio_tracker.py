"""
Portfolio Tracker Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

ZERION_API_KEY = os.getenv("ZERION_API_KEY", "")
BASE_URL = "https://api.zerion.io/v1"

async def _zerion_get(endpoint: str) -> dict:
    cache_key = f"zerion:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{BASE_URL}{endpoint}",
                headers={"Authorization": f"Basic {ZERION_API_KEY}"},
                params={"currency": "usd"},
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"Zerion error: {e}")
        return {"error": str(e)}

def register_portfolio_tracker_tools(app):

    @app.tool()
    async def get_portfolio_value(addresses: list[str], chains: list[str] = ["ethereum", "solana"]) -> dict:
        """Get total portfolio value across multiple wallets and chains"""
        results = {}
        for address in addresses:
            results[address] = {"address": address, "chains": chains, "status": "tracked"}
        return {"portfolios
