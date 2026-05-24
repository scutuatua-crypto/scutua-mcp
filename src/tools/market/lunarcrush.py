"""
📊 LunarCrush Social Intelligence — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

LUNARCRUSH_API_KEY = os.getenv("LUNARCRUSH_API_KEY", "")

def register_lunarcrush_tools(app: FastMCP):

    @app.tool()
    async def get_social_dominance(token: str) -> dict:
        """Get social dominance score for a token from LunarCrush"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://lunarcrush.com/api4/public/coins/{token}/v1",
                headers={"Authorization": f"Bearer {LUNARCRUSH_API_KEY}"}
            )
        return r.json()

    @app.tool()
    async def get_galaxy_score(token: str) -> dict:
        """Get LunarCrush Galaxy Score for a token"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://lunarcrush.com/api4/public/coins/{token}/v1",
                headers={"Authorization": f"Bearer {LUNARCRUSH_API_KEY}"}
            )
        data = r.json().get("data", {})
        return {"token": token, "galaxy_score": data.get("galaxy_score"), "alt_rank": data.get("alt_rank")}

    @app.tool()
    async def get_trending_social() -> dict:
        """Get trending crypto assets by social activity"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://lunarcrush.com/api4/public/coins/list/v2?sort=galaxy_score&limit=20",
                headers={"Authorization": f"Bearer {LUNARCRUSH_API_KEY}"}
            )
        return r.json()

