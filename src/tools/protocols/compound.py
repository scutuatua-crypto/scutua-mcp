"""
Compound Finance Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.compound.finance/api/v2"

async def _compound_get(endpoint: str) -> dict:
    cache_key = f"compound:{endpoint}"
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
        logger.error(f"Compound error: {e}")
        return {"error": str(e)}

def register_compound_tools(app):

    @app.tool()
    async def get_compound_markets() -> dict:
        """Get all Compound V3 markets with supply/borrow APY"""
        data = await _compound_get("/ctoken")
        if "error" in data:
            return data
        tokens = data.get("cToken", [])
        markets = [{"symbol": t.get("symbol"), "supply_apy": t.get("supply_rate", {}).get("value"), "borrow_apy": t.get("borrow_rate", {}).get("value"), "tvl": t.get("total_supply", {}).get("value")} for t in tokens[:10]]
        return {"markets": markets, "protocol": "compound"}

    @app.tool()
    async def get_compound_account(address: str) -> dict:
        """Get Compound account health and positions"""
        data = await _compound_get(f"/account?addresses[]={address}")
        return data
