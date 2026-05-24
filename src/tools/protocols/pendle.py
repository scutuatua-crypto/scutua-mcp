"""
⚡ Pendle Finance Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_pendle_tools(app: FastMCP):

    @app.tool()
    async def get_pendle_markets() -> dict:
        """Get active Pendle yield markets with fixed APY"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api-v2.pendle.finance/core/v1/1/markets?order_by=volume%3A-1&limit=10")
        markets = r.json().get("results", [])
        return {"markets": markets, "protocol": "pendle"}

    @app.tool()
    async def get_pendle_assets() -> dict:
        """Get all Pendle supported yield-bearing assets"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api-v2.pendle.finance/core/v1/1/assets/all")
        return {"assets": r.json(), "protocol": "pendle"}

    @app.tool()
    async def get_pendle_pt_price(market_address: str) -> dict:
        """Get Principal Token price for a Pendle market"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api-v2.pendle.finance/core/v1/1/markets/{market_address}")
        return r.json()

