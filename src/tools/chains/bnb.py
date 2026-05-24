"""
🌐 BNB Chain Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_bnb_tools(app: FastMCP):

    @app.tool()
    async def get_bnb_balance(address: str) -> dict:
        """Get BNB balance on BNB Chain"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.bscscan.com/api",
                params={"module": "account", "action": "balance", "address": address, "tag": "latest"}
            )
        data = r.json()
        return {"address": address, "balance_wei": data.get("result"), "chain": "bnb"}

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get current BNB Chain gas price"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.bscscan.com/api?module=gastracker&action=gasoracle")
        data = r.json().get("result", {})
        return {"gas_price": data.get("ProposeGasPrice"), "chain": "bnb"}

    @app.tool()
    async def get_bnb_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on BNB Chain"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.bscscan.com/api",
                params={"module": "account", "action": "txlist", "address": address, "page": 1, "offset": limit, "sort": "desc"}
            )
        txs = r.json().get("result", [])
        return {"address": address, "transactions": txs[:limit], "chain": "bnb"}

