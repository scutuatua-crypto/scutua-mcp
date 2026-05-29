"""
Arbitrum Chain Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Arbiscan ตอนนี้ใช้ Etherscan API V2 (chainid=42161) — ใช้ key เดียวกัน
ARBISCAN_API_KEY = (
    os.getenv("ARBISCAN_API_KEY") or
    os.getenv("ETHERSCAN_API_KEY") or
    ""
)

# Etherscan V2 endpoint (รองรับ Arbitrum chainid=42161)
BASE_URL_V2 = "https://api.etherscan.io/v2/api"
CHAIN_ID = 42161  # Arbitrum One

async def _arbiscan_get(params: dict) -> dict:
    cache_key = f"arbiscan:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        # ใช้ Etherscan V2 + chainid=42161
        v2_params = {"chainid": CHAIN_ID, **params}
        async with httpx.AsyncClient() as client:
            r = await client.get(BASE_URL_V2, params=v2_params, timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"Arbiscan error: {e}")
        return {"error": str(e)}

def register_arbitrum_tools(app):

    @app.tool()
    async def get_arbitrum_balance(address: str) -> dict:
        """Get ETH balance on Arbitrum L2"""
        data = await _arbiscan_get({
            "module": "account", "action": "balance",
            "address": address, "tag": "latest",
            "apikey": ARBISCAN_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "balance_wei": data.get("result"), "chain": "arbitrum"}

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get current Arbitrum gas price"""
        data = await _arbiscan_get({
            "module": "gastracker", "action": "gasoracle",
            "apikey": ARBISCAN_API_KEY
        })
        if "error" in data:
            return data
        result = data.get("result", {})
        return {"gas_price": result.get("ProposeGasPrice"), "chain": "arbitrum"}

    @app.tool()
    async def get_arbitrum_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on Arbitrum"""
        data = await _arbiscan_get({
            "module": "account", "action": "txlist",
            "address": address, "page": 1,
            "offset": limit, "sort": "desc",
            "apikey": ARBISCAN_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "transactions": data.get("result", [])[:limit], "chain": "arbitrum"}
