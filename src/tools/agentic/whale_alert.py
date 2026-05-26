"""
Whale Alert → Telegram Auto
Dimension: Agentic / src/tools/agentic/whale_alert.py
"""

import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP("whale-alert")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

WHALE_API_URL = "https://api.whale-alert.io/v1/transactions"
WHALE_API_KEY = os.getenv("WHALE_ALERT_API_KEY", "")

# Threshold: only alert if USD value exceeds this
DEFAULT_MIN_USD = 500_000


async def send_telegram(message: str) -> dict:
    """Send message to Telegram channel."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        return {"sent": False, "reason": "Telegram credentials not configured"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return {"sent": True, "message_id": resp.json().get("result", {}).get("message_id")}


def format_whale_alert(tx: dict) -> str:
    """Format whale transaction into readable Telegram message."""
    symbol = tx.get("symbol", "???").upper()
    amount = tx.get("amount", 0)
    amount_usd = tx.get("amount_usd", 0)
    tx_type = tx.get("transaction_type", "transfer").upper()
    from_owner = tx.get("from", {}).get("owner_type", "unknown")
    to_owner = tx.get("to", {}).get("owner_type", "unknown")
    blockchain = tx.get("blockchain", "unknown").upper()
    hash_ = tx.get("hash", "")

    emoji = "🐋"
    if amount_usd >= 10_000_000:
        emoji = "🚨🐋🚨"
    elif amount_usd >= 1_000_000:
        emoji = "⚠️🐋"

    return (
        f"{emoji} <b>WHALE ALERT</b>\n\n"
        f"💰 <b>{amount:,.0f} {symbol}</b> (${amount_usd:,.0f})\n"
        f"🔗 Chain: {blockchain}\n"
        f"📤 From: {from_owner}\n"
        f"📥 To: {to_owner}\n"
        f"⚡ Type: {tx_type}\n"
        f"🔎 <a href='https://etherscan.io/tx/{hash_}'>View TX</a>"
    )


@mcp.tool()
async def monitor_whales(
    min_usd: float = DEFAULT_MIN_USD,
    notify_telegram: bool = True,
    limit: int = 10,
) -> dict:
    """
    Fetch recent whale transactions and optionally alert via Telegram.

    Args:
        min_usd: Minimum transaction value in USD to include
        notify_telegram: Send alerts to Telegram channel
        limit: Max number of transactions to fetch

    Returns:
        Whale transactions with alert status
    """
    try:
        params = {
            "api_key": WHALE_API_KEY,
            "min_value": int(min_usd),
            "limit": limit,
            "currency": "usd",
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(WHALE_API_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        transactions = data.get("transactions", [])
        alerts_sent = []

        for tx in transactions:
            amount_usd = tx.get("amount_usd", 0)
            if amount_usd < min_usd:
                continue

            alert_result = {"tx_hash": tx.get("hash", ""), "amount_usd": amount_usd}

            if notify_telegram:
                message = format_whale_alert(tx)
                tg_result = await send_telegram(message)
                alert_result["telegram"] = tg_result

            alerts_sent.append(alert_result)

        return {
            "transactions_fetched": len(transactions),
            "alerts_triggered": len(alerts_sent),
            "min_usd_threshold": min_usd,
            "telegram_enabled": notify_telegram,
            "alerts": alerts_sent,
        }

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return {"error": "Invalid WHALE_ALERT_API_KEY — get one at whale-alert.io"}
        return {"error": f"HTTP {e.response.status_code}: {str(e)}"}
    except Exception as e:
        return {"error": f"Monitor failed: {str(e)}"}


@mcp.tool()
async def test_telegram_alert() -> dict:
    """
    Send a test message to verify Telegram integration is working.
    """
    message = (
        "✅ <b>WhaleTrucker Alert System</b>\n\n"
        "🔗 Telegram integration is <b>active</b>\n"
        "🐋 Whale monitoring ready\n"
        "⚡ Powered by Scutua-MCP"
    )
    result = await send_telegram(message)
    return result
