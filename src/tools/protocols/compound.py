"""
⚡ Compound Finance Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_compound_tools(app: FastMCP):

    @app.tool()
    async def get_compound_markets() -> dict:
        """Get all Compound V3 markets with supply/borrow APY"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.compound.finance/api/v2/ctoken")
        tokens = r.json().get("cToken", [])
        markets = [{"symbol": t.get("symbol"), "supply_apy": t.get("supply_rate", {}).get("value"), "borrow_apy": t.get("borrow_rate", {}).get("value"), "tvl": t.get("total_supply", {}).get("value")} for t in tokens[:10]]
        return {"markets": markets, "protocol": "compound"}

    @app.tool()
    async def get_compound_account(address: str) -> dict:
        """Get Compound account health and positions"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.compound.finance/api/v2/account?addresses[]={address}")
        return r.json()

