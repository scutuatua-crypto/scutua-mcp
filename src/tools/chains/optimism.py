"""
Optimism Chain Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Optimism ใช้ Etherscan API V2 (chainid=10) — key เดียวกัน
OPTIMISM_API_KEY = (
    os.getenv("OPTIMISM_API_KEY") or
    os.getenv("ETHERSCAN_API_KEY") or
    ""
)

BASE_URL = "https://api.etherscan.io/v2/api"
CHAIN_ID = 10  # Optimism Mainnet

async def _optimism_get(params: dict) -> dict:
    cache_key = f"optimism:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        v2_params = {"chainid": CHAIN_ID, **params}
        async with httpx.AsyncClient() as client:
            r = await client.get(BASE_URL, params=v2_params, timeout=10)
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
        balance_wei = data.get("result", "0")
        try:
            balance_eth = int(balance_wei) / 1e18
        except:
            balance_eth = 0
        return {
            "address": address,
            "balance_wei": balance_wei,
            "balance_eth": f"{balance_eth:.6f}",
            "chain": "optimism"
        }

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
