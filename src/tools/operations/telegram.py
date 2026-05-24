"""
Telegram Notification Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.logger import get_logger

logger = get_logger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def register_telegram_tools(app):

    @app.tool()
    async def send_telegram_alert(message: str) -> dict:
        """Send a whale alert or notification via Telegram bot"""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            return {"error": "Telegram credentials not configured"}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    f"{BASE_URL}/sendMessage",
                    json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"},
                    timeout=10
                )
                r.raise_for_status()
                return r.json()
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            return {"error": str(e)}

    @app.tool()
    async def send_telegram_price_alert(token: str, price: float, threshold: float) -> dict:
        """Send price alert when token crosses threshold"""
        if price >= threshold:
            msg = f"*Price Alert*\n{token}: ${price} crossed ${threshold}"
            if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
                return {"error": "Telegram credentials not configured"}
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.post(
                        f"{BASE_URL}/sendMessage",
                        json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"},
                        timeout=10
                    )
                    r.raise_for_status()
                    return r.json()
            except Exception as e:
                logger.error(f"Telegram price alert error: {e}")
                return {"error": str(e)}
        return {"status": "threshold not crossed", "token": token, "price": price}
