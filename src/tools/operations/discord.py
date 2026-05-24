"""
Discord Notification Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.logger import get_logger

logger = get_logger(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

def register_discord_tools(app):

    @app.tool()
    async def send_discord_alert(message: str, title: str = "Scutua-MCP Alert") -> dict:
        """Send whale alert or notification to Discord webhook"""
        if not DISCORD_WEBHOOK_URL:
            return {"error": "DISCORD_WEBHOOK_URL not configured"}
        try:
            payload = {
                "embeds": [{
                    "title": title,
                    "description": message,
                    "color": 3447003
                }]
            }
            async with httpx.AsyncClient() as client:
                r = await client.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
                r.raise_for_status()
                return {"status": r.status_code, "message": "sent"}
        except Exception as e:
            logger.error(f"Discord error: {e}")
            return {"error": str(e)}

    @app.tool()
    async def send_discord_whale_alert(wallet: str, amount: float, token: str, chain: str) -> dict:
        """Send formatted whale movement alert to Discord"""
        if not DISCORD_WEBHOOK_URL:
            return {"error": "DISCORD_WEBHOOK_URL not configured"}
        msg = f"Whale moved **{amount:,.2f} {token}** on {chain}\nWallet: `{wallet}`"
        try:
            payload = {
                "embeds": [{
                    "title": "Whale Alert",
                    "description": msg,
                    "color": 3447003
                }]
            }
            async with httpx.AsyncClient() as client:
                r = await client.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
                r.raise_for_status()
                return {"status": r.status_code, "message": "sent"}
        except Exception as e:
            logger.error(f"Discord whale alert error: {e}")
            return {"error": str(e)}
