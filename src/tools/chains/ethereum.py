"""
🌐 Ethereum Chain Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
from src.utils.cache import get_cached, set_cached
import httpx

def register_ethereum_tools(app: FastMCP):

    @app.tool()
    async def get_eth_balance(address: str) -> dict:
        """Get ETH balance and token holdings for an address"""
        cache_key = f"eth_balance:{address}"
        cached = await get_cached(cache_key)
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.etherscan.io/api",
                params={"module": "account", "action": "balance", "address": address, "tag": "latest"}
            )
            data = r.json()
        result = {"address": address, "balance_wei": data.get("result"), "chain": "ethereum"}
        await set_cached(cache_key, result, ttl=60)
        return result

    @app.tool()
    async def get_eth_gas_price() -> dict:
        """Get current Ethereum gas prices (slow/standard/fast)"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle")
        data = r.json().get("result", {})
        return {
            "slow": data.get("SafeGasPrice"),
            "standard": data.get("ProposeGasPrice"),
            "fast": data.get("FastGasPrice"),
            "chain": "ethereum"
        }

    @app.tool()
    async def get_eth_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transaction history for an Ethereum address"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.etherscan.io/api",
                params={"module": "account", "action": "txlist", "address": address, "page": 1, "offset": limit, "sort": "desc"}
            )
        txs = r.json().get("result", [])
        return {"address": address, "transactions": txs[:limit], "chain": "ethereum"}

