"""
📊 Alternative.me Market Data — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_alternative_tools(app: FastMCP):

    @app.tool()
    async def get_fear_greed_index() -> dict:
        """Get current Crypto Fear & Greed Index from Alternative.me"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.alternative.me/fng/?limit=1")
        data = r.json().get("data", [{}])[0]
        return {
            "value": data.get("value"),
            "classification": data.get("value_classification"),
            "timestamp": data.get("timestamp")
        }

    @app.tool()
    async def get_fear_greed_history(limit: int = 30) -> dict:
        """Get Fear & Greed Index history"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.alternative.me/fng/?limit={limit}")
        return r.json()

    @app.tool()
    async def get_global_crypto_stats() -> dict:
        """Get global cryptocurrency market statistics"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.alternative.me/v2/global/")
        return r.json()

