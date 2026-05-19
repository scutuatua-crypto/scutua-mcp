import httpx
from mcp.server.fastmcp import FastMCP

def register_ton_tools(app: FastMCP):
    @app.tool()
    async def get_ton_balance(address: str) -> str:
        """Get TON wallet balance"""
        try:
            url = f"https://toncenter.com/api/v2/getAddressBalance?address={address}"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            if data.get("ok"):
                nano = int(data["result"])
                ton = nano / 1e9
                return f"TON Balance: {ton:.4f} TON"
            return "Error fet

