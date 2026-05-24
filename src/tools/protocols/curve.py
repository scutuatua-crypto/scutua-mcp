"""
⚡ Curve Finance Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_curve_tools(app: FastMCP):

    @app.tool()
    async def get_curve_pools() -> dict:
        """Get top Curve Finance liquidity pools with APY"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.curve.fi/api/getPools/ethereum/main")
        pools = r.json().get("data", {}).get("poolData", [])
        top = [{"name": p.get("name"), "tvl": p.get("usdTotal"), "apy": p.get("latestDailyApy")} for p in pools[:10]]
        return {"pools": top, "protocol": "curve"}

    @app.tool()
    async def get_curve_pool_detail(pool_address: str) -> dict:
        """Get detailed info for a specific Curve pool"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.curve.fi/api/getPools/ethereum/main")
        pools = r.json().get("data", {}).get("poolData", [])
        pool = next((p for p in pools if p.get("address", "").lower() == pool_address.lower()), None)
        return pool or {"error": "Pool not found"}

    @app.tool()
    async def get_curve_tvl() -> dict:
        """Get total TVL across all Curve pools"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.curve.fi/api/getTVL")
        return r.json()

