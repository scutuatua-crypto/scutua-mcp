"""
🧠 Birdeye Analytics Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")

def register_birdeye_tools(app: FastMCP):

    @app.tool()
    async def get_token_price_birdeye(token_address: str) -> dict:
        """Get real-time token price from Birdeye"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://public-api.birdeye.so/defi/price?address={token_address}",
                headers={"X-API-KEY": BIRDEYE_API_KEY}
            )
        return r.json()

    @app.tool()
    async def get_token_trending_birdeye() -> dict:
        """Get trending tokens on Solana from Birdeye"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://public-api.birdeye.so/defi/trending_tokens",
                headers={"X-API-KEY": BIRDEYE_API_KEY}
            )
        return r.json()

    @app.tool()
    async def get_wallet_portfolio_birdeye(wallet_address: str) -> dict:
        """Get full wallet portfolio from Birdeye"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://public-api.birdeye.so/v1/wallet/token_list?wallet={wallet_address}",
                headers={"X-API-KEY": BIRDEYE_API_KEY}
            )
        return r.json()

