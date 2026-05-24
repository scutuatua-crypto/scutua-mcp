"""
Optimism Chain Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

OPTIMISM_API_KEY = os.getenv("OPTIMISM_API_KEY", "")
BASE_URL = "https://api-optimistic.etherscan.io/api"

async def _optimism_get(params: dict) -> dict:
    cache_key = f"optimism:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(BASE_URL, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"Optimism error: {e}")
        return {"error": str(e)}

def register_optimism_tools(app):

    @app.tool()
    async def get_optimism_balance(address: str) -> dict:
        """Get ETH balance on Optimism L2"""
        data = await _optimism_get({
            "module": "account", "action": "balance",
            "address": address, "tag": "latest",
            "apikey": OPTIMISM_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "balance_wei": data.get("result"), "chain": "optimism"}

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get current Optimism gas price"""
        data = await _optimism_get({
            "module": "gastracker", "action": "gasoracle",
            "apikey": OPTIMISM_API_KEY
        })
        if "error" in data:
            return data
        result = data.get("result", {})
        return {"gas_price": result.get("ProposeGasPrice"), "chain": "optimism"}

    @app.tool()
    async def get_optimism_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on Optimism"""
        data = await _optimism_get({
            "module": "account", "action": "txlist",
            "address": address, "page": 1,
            "offset": limit, "sort": "desc",
            "apikey": OPTIMISM_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "transactions": data.get("result", [])[:limit], "chain": "optimism"}
