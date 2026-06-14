"""
Avalanche Chain Tools — Scutua-MCP
"""

import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Snowtrace ใช้ Etherscan API V2 (chainid=43114) — ใช้ key เดียวกัน
SNOWTRACE_API_KEY = (
    os.getenv("SNOWTRACE_API_KEY") or
    os.getenv("ETHERSCAN_API_KEY") or
    ""
)

# Etherscan V2 endpoint (รองรับ Avalanche C-Chain chainid=43114)
BASE_URL_V2 = "https://api.etherscan.io/v2/api"
CHAIN_ID = 43114  # Avalanche C-Chain


async def _snowtrace_get(params: dict) -> dict:
    cache_key = f"snowtrace:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        v2_params = {"chainid": CHAIN_ID, **params}
        async with httpx.AsyncClient() as client:
            r = await client.get(BASE_URL_V2, params=v2_params, timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"Snowtrace error: {e}")
        return {"error": str(e)}


def register_avalanche_tools(app):

    @app.tool()
    async def get_avax_balance(address: str) -> dict:
        """Get AVAX balance on Avalanche C-Chain"""
        data = await _snowtrace_get({
            "module": "account", "action": "balance",
            "address": address, "tag": "latest",
            "apikey": SNOWTRACE_API_KEY
        })
        if data.get("status") == "0" or "error" in data:
            return {"error": data.get("result") or data.get("error") or "Failed to get balance"}
        return {"address": address, "balance_wei": data.get("result"), "chain": "avalanche"}

    @app.tool()
    async def get_avax_gas_price() -> dict:
        """Get current Avalanche C-Chain gas price"""
        data = await _snowtrace_get({
            "module": "gastracker", "action": "gasoracle",
            "apikey": SNOWTRACE_API_KEY
        })
        if "error" in data:
            return data
        result = data.get("result", {})
        return {"gas_price": result.get("ProposeGasPrice"), "chain": "avalanche"}

    @app.tool()
    async def get_avax_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on Avalanche C-Chain"""
        data = await _snowtrace_get({
            "module": "account", "action": "txlist",
            "address": address, "page": 1,
            "offset": limit, "sort": "desc",
            "apikey": SNOWTRACE_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "transactions": data.get("result", [])[:limit], "chain": "avalanche"}
