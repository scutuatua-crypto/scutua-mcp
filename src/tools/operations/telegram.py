"""
🛠️ Telegram Notification Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def register_telegram_tools(app: FastMCP):

    @app.tool()
    async def send_telegram_alert(message: str) -> dict:
        """Send a whale alert or notification via Telegram bot"""
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
            )
        return r.json()

    @app.tool()
    async def send_telegram_price_alert(token: str, price: float, threshold: float) -> dict:
        """Send price alert when token crosses threshold"""
        if price >= threshold:
            msg = f"🚨 *Price Alert*\n{token}: ${price} crossed ${threshold}"
            return await send_telegram_alert(msg)
        return {"status": "threshold not crossed", "token": token, "price": price}

