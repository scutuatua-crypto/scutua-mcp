"""
⚡ GMX Protocol Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_gmx_tools(app: FastMCP):

    @app.tool()
    async def get_gmx_stats() -> dict:
        """Get GMX protocol stats — volume, fees, open interest"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://stats.gmx.io/api/gmx-supply")
        return {"stats": r.json(), "protocol": "gmx"}

    @app.tool()
    async def get_gmx_prices() -> dict:
        """Get GMX token prices for supported assets"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://arbitrum-api.gmxinfra.io/prices/tickers")
        return {"prices": r.json(), "protocol": "gmx"}

    @app.tool()
    async def get_gmx_pools() -> dict:
        """Get GMX V2 liquidity pools (GM pools)"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://arbitrum-api.gmxinfra.io/markets")
        return {"pools": r.json(), "protocol": "gmx"}

