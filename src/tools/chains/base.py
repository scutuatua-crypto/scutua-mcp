import httpx
from mcp.server.fastmcp import FastMCP

def register_base_tools(app: FastMCP):
    @app.tool()
    async def get_base_balance(address: str) -> str:
        """Get Base chain ETH balance"""
        try:
            url = "https://mainnet.base.org"
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [address, "latest"],
                "id": 1
            }
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload, timeout=10)
                data = r.json()
            wei = int(data["result"], 16)
            eth = wei / 1e18
            return f"Base Balance: {eth:.6f} ETH"
        except Exception as e:
            return f"Error: {e}"
