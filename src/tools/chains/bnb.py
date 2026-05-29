"""
BNB Chain Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# BSC ใช้ Etherscan API V2 (chainid=56) — key เดียวกับ ETHERSCAN_API_KEY
BSCSCAN_API_KEY = (
    os.getenv("BSC_API_KEY") or
    os.getenv("BSCSCAN_API_KEY") or
    os.getenv("ETHERSCAN_API_KEY") or
    ""
)

BASE_URL = "https://api.etherscan.io/v2/api"
CHAIN_ID = 56  # BNB Smart Chain

async def _bscscan_get(params: dict) -> dict:
    cache_key = f"bscscan:{str(params)}"
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
        logger.error(f"BscScan error: {e}")
        return {"error": str(e)}

def register_bnb_tools(app):

    @app.tool()
    async def get_bnb_balance(address: str) -> dict:
        """Get BNB balance on BNB Chain"""
        data = await _bscscan_get({
            "module": "account", "action": "balance",
            "address": address, "tag": "latest",
            "apikey": BSCSCAN_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "balance_wei": data.get("result"), "chain": "bnb"}

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get current BNB Chain gas price"""
        data = await _bscscan_get({
            "module": "gastracker", "action": "gasoracle",
            "apikey": BSCSCAN_API_KEY
        })
        if "error" in data:
            return data
        result = data.get("result", {})
        return {"gas_price": result.get("ProposeGasPrice"), "chain": "bnb"}

    @app.tool()
    async def get_bnb_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on BNB Chain"""
        data = await _bscscan_get({
            "module": "account", "action": "txlist",
            "address": address, "page": 1,
            "offset": limit, "sort": "desc",
            "apikey": BSCSCAN_API_KEY
        })
        if "error" in data:
            return data
        return {"address": address, "transactions": data.get("result", [])[:limit], "chain": "bnb"}
