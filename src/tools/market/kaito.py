"""
📊 Kaito AI Market Intelligence — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

KAITO_API_KEY = os.getenv("KAITO_API_KEY", "")

def register_kaito_tools(app: FastMCP):

    @app.tool()
    async def get_kaito_mindshare(token: str) -> dict:
        """Get crypto mindshare score from Kaito AI"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://api.kaito.ai/api/v1/mindshare?ticker={token}",
                headers={"Authorization": f"Bearer {KAITO_API_KEY}"}
            )
        return r.json()

    @app.tool()
    async def get_kaito_trending() -> dict:
        """Get trending crypto topics from Kaito AI"""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.kaito.ai/api/v1/trending",
                headers={"Authorization": f"Bearer {KAITO_API_KEY}"}
            )
        return r.json()

