"""
Fantom Chain Tools — Scutua-MCP
"""

import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Fantom ใช้ Etherscan API V2 (chainid=250)
FTMSCAN_API_KEY = (
    os.getenv("FTMSCAN_API_KEY") or
    os.getenv("ETHERSCAN_API_KEY") or
    ""
)

# Etherscan V2 endpoint (รองรับ Fantom Opera chainid=250)
BASE_URL_V2 = "https://api.etherscan.io/v2/api"
CHAIN_ID = 250  # Fantom Opera


async def _ftmscan_get(params: dict) -> dict:
    cache_params = {k: v for k, v in params.items() if k != "apikey"}
    cache_key = f"ftmscan:{str(cache_params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        v2_params = {"chainid": CHAIN_ID, **params}
        async with httpx.AsyncClient() as client:
            r = await client.get(BASE_URL_V2, params=v2_params, timeout=10)
            r.raise_for_status()
            data = r.json()
            if data.get("status") == "1":
                set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"FtmScan error: {e}")
        return {"error": str(e)}


def register_fantom_tools(app):

    @app.tool()
    async def get_ftm_balance(
        address: str,  # Fantom Opera wallet address (0x...)
    ) -> dict:
        """
        Get FTM balance on Fantom Opera chain.
        Returns balance in wei for the specified wallet address.
        """
        data = await _ftmscan_get({
            "module": "account", "action": "balance",
            "address": address, "tag": "latest",
            "apikey": FTMSCAN_API_KEY
        })
        if data.get("status") == "0" or "error" in data:
            return {"error": data.get("result") or data.get("error") or "Failed to get balance"}
        return {"address": address, "balance_wei": data.get("result"), "chain": "fantom"}

    @app.tool()
    async def get_ftm_gas_price() -> dict:
        """
        Get current Fantom Opera gas price.
        Returns the proposed gas price in Gwei from the FtmScan gas oracle.
        """
        data = await _ftmscan_get({
            "module": "gastracker", "action": "gasoracle",
            "apikey": FTMSCAN_API_KEY
        })
        if data.get("status") == "0" or "error" in data:
            return {"error": data.get("result") or data.get("error") or "Failed to get gas price"}
        result = data.get("result")
        if not isinstance(result, dict):
            return {"error": "Unexpected response format"}
        return {"gas_price": result.get("ProposeGasPrice"), "chain": "fantom"}

    @app.tool()
    async def get_ftm_tx_history(
        address: str,    # Fantom Opera wallet address (0x...)
        limit: int = 10, # Number of recent transactions to return (default: 10, max: 100)
    ) -> dict:
        """
        Get recent transactions on Fantom Opera chain.
        Returns a list of the most recent transactions for the specified wallet address,
        sorted by block number descending.
        """
        data = await _ftmscan_get({
            "module": "account", "action": "txlist",
            "address": address, "page": 1,
            "offset": limit, "sort": "desc",
            "apikey": FTMSCAN_API_KEY
        })
        if data.get("status") == "0" or "error" in data:
            if data.get("message") == "No transactions found":
                return {"address": address, "transactions": [], "chain": "fantom"}
            return {"error": data.get("result") or data.get("error") or "Failed to get transaction history"}
        result = data.get("result")
        if not isinstance(result, list):
            return {"error": "Unexpected response format"}
        return {"address": address, "transactions": result[:limit], "chain": "fantom"}
