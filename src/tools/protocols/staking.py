import httpx
from mcp.server.fastmcp import FastMCP

def register_staking_tools(app: FastMCP):
    @app.tool()
    async def get_staking_info(address: str) -> str:
        """Get TON staking information"""
        try:
            url = f"https://toncenter.com/api/v2/getWalletInformation?address={address}"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            if data.get("ok"):
                return f"Staking info retrieved for {address}"
            return "Error fetching staking info"
        except Exception as e:
            return "Error fetching staking info"
