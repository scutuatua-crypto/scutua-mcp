"""
Ethereum Chain Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
BASE_URL = "https://api.etherscan.io/api"

async def _etherscan_get(params: dict) -> dict:
    cache_key = f"etherscan:{str(params)}"
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
        logger.error(f"Etherscan error: {e}")
        return {"error": str(e)}

def register_ethereum_tools(app):

    @app.tool()
    async def get_eth_balance(address: str) -> dict:
        """Get ETH balance for an address"""
        data = await _etherscan_get({
            "module": "account", "action": "balance",
            "address": address, "tag": "latest",
            "apikey": ETHERSCAN_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "balance_wei": data.get("result"), "chain": "ethereum"}

    @app.tool()
    async def get_eth_gas_price() -> dict:
        """Get current Ethereum gas prices (slow/standard/fast)"""
        data = await _etherscan_get({
            "module": "gastracker", "action": "gasoracle",
            "apikey": ETHERSCAN_API_KEY
        })
        if "error" in data:
            return data
        result = data.get("result", {})
        return {
            "slow": result.get("SafeGasPrice"),
            "standard": result.get("ProposeGasPrice"),
            "fast": result.get("FastGasPrice"),
            "chain": "ethereum"
        }

    @app.tool()
    async def get_eth_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transaction history for an Ethereum address"""
        data = await _etherscan_get({
            "module": "account", "action": "txlist",
            "address": address, "page": 1,
            "offset": limit, "sort": "desc",
            "apikey": ETHERSCAN_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "transactions": data.get("result", [])[:limit], "chain": "ethereum"}
