"""
🧠 Nansen Analytics Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

NANSEN_API_KEY = os.getenv("NANSEN_API_KEY", "")

def register_nansen_tools(app: FastMCP):

    @app.tool()
    async def get_smart_money_flows() -> dict:
        """Get smart money wallet flows from Nansen"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.nansen.ai/v1/smart-money/flows",
                headers={"apiKey": NANSEN_API_KEY}
            )
        return r.json()

    @app.tool()
    async def get_nansen_token_god_mode(token_address: str) -> dict:
        """Get token analytics in God Mode from Nansen"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.nansen.ai/v1/token/{token_address}",
                headers={"apiKey": NANSEN_API_KEY}
            )
        return r.json()

    @app.tool()
    async def get_wallet_label(address: str) -> dict:
        """Get Nansen wallet label (whale, smart money, etc.)"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.nansen.ai/v1/wallet/{address}/label",
                headers={"apiKey": NANSEN_API_KEY}
            )
        return r.json()

