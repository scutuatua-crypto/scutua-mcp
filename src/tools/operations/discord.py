"""
🛠️ Discord Notification Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

def register_discord_tools(app: FastMCP):

    @app.tool()
    async def send_discord_alert(message: str, title: str = "WhaleTrucker Alert") -> dict:
        """Send whale alert or notification to Discord webhook"""
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": 3447003
            }]
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(DISCORD_WEBHOOK_URL, json=payload)
        return {"status": r.status_code, "message": "sent"}

    @app.tool()
    async def send_discord_whale_alert(wallet: str, amount: float, token: str, chain: str) -> dict:
        """Send formatted whale movement alert to Discord"""
        msg = f"🐋 Whale moved **{amount:,.2f} {token}** on {chain}\nWallet: `{wallet}`"
        return await send_discord_alert(msg, title="🐋 Whale Alert")

