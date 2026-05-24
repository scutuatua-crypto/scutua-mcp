"""
🌐 Arbitrum Chain Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_arbitrum_tools(app: FastMCP):

    @app.tool()
    async def get_arbitrum_balance(address: str) -> dict:
        """Get ETH balance on Arbitrum L2"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.arbiscan.io/api",
                params={"module": "account", "action": "balance", "address": address, "tag": "latest"}
            )
        data = r.json()
        return {"address": address, "balance_wei": data.get("result"), "chain": "arbitrum"}

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get current Arbitrum gas price"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.arbiscan.io/api?module=gastracker&action=gasoracle")
        data = r.json().get("result", {})
        return {"gas_price": data.get("ProposeGasPrice"), "chain": "arbitrum"}

    @app.tool()
    async def get_arbitrum_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on Arbitrum"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.arbiscan.io/api",
                params={"module": "account", "action": "txlist", "address": address, "page": 1, "offset": limit, "sort": "desc"}
            )
        txs = r.json().get("result", [])
        return {"address": address, "transactions": txs[:limit], "chain": "arbitrum"}

