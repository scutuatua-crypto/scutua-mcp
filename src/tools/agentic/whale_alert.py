"""
Whale Alert → Bitquery GraphQL (Free tier)
Dimension: Agentic / src/tools/agentic/whale_alert.py
"""

import os
import httpx

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

BITQUERY_TOKEN = os.getenv("BITQUERY_TOKEN", "")
BITQUERY_URL = "https://streaming.bitquery.io/eap"

DEFAULT_MIN_USD = 500_000

WHALE_QUERY = """
{
  EVM(network: eth) {
    Transfers(
      where: {
        Transfer: {
          AmountInUSD: {ge: "%s"}
        }
      }
      limit: {count: %d}
      orderBy: {descending: Block_Time}
    ) {
      Block { Time }
      Transfer {
        Amount
        AmountInUSD
        Currency { Symbol Name }
        Sender
        Receiver
      }
      Transaction { Hash }
    }
  }
}
"""


async def send_telegram(message: str) -> dict:
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
    transfer = tx.get("Transfer", {})
    symbol = transfer.get("Currency", {}).get("Symbol", "???").upper()
    amount = float(transfer.get("Amount", 0))
    amount_usd = float(transfer.get("AmountInUSD", 0))
    sender = transfer.get("Sender", "unknown")[:10] + "..."
    receiver = transfer.get("Receiver", "unknown")[:10] + "..."
    hash_ = tx.get("Transaction", {}).get("Hash", "")
    block_time = tx.get("Block", {}).get("Time", "")
    emoji = "🚨🐋🚨" if amount_usd >= 10_000_000 else "⚠️🐋" if amount_usd >= 1_000_000 else "🐋"
    return (
        f"{emoji} <b>WHALE ALERT</b>\n\n"
        f"💰 <b>{amount:,.2f} {symbol}</b> (${amount_usd:,.0f})\n"
        f"🔗 Chain: ETHEREUM\n"
        f"📤 From: <code>{sender}</code>\n"
        f"📥 To: <code>{receiver}</code>\n"
        f"🕐 Time: {block_time}\n"
        f"🔎 <a href='https://etherscan.io/tx/{hash_}'>View TX</a>"
    )


async def monitor_whales(
    min_usd: float = DEFAULT_MIN_USD,
    notify_telegram: bool = True,
    limit: int = 10,
) -> dict:
    """Fetch recent whale transactions via Bitquery and optionally alert via Telegram."""
    if not BITQUERY_TOKEN:
        return {"error": "BITQUERY_TOKEN not configured"}
    try:
        query = WHALE_QUERY % (int(min_usd), limit)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BITQUERY_TOKEN}",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(BITQUERY_URL, json={"query": query}, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        transfers = data.get("data", {}).get("EVM", {}).get("Transfers", [])
        alerts_sent = []
        for tx in transfers:
            transfer = tx.get("Transfer", {})
            amount_usd = float(transfer.get("AmountInUSD", 0))
            alert_result = {
                "tx_hash": tx.get("Transaction", {}).get("Hash", ""),
                "amount_usd": amount_usd,
                "symbol": transfer.get("Currency", {}).get("Symbol", "???"),
            }
            if notify_telegram:
                message = format_whale_alert(tx)
                tg_result = await send_telegram(message)
                alert_result["telegram"] = tg_result
            alerts_sent.append(alert_result)

        return {
            "transactions_fetched": len(transfers),
            "alerts_triggered": len(alerts_sent),
            "min_usd_threshold": min_usd,
            "source": "Bitquery EVM (Ethereum)",
            "alerts": alerts_sent,
        }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return {"error": "Invalid BITQUERY_TOKEN"}
        return {"error": f"HTTP {e.response.status_code}: {str(e)}"}
    except Exception as e:
        return {"error": f"Monitor failed: {str(e)}"}


async def get_whale_alert(min_usd: float = 100_000) -> dict:
    """Get recent large crypto transactions via Bitquery."""
    if not BITQUERY_TOKEN:
        return {"error": "BITQUERY_TOKEN not configured"}
    try:
        query = WHALE_QUERY % (int(min_usd), 20)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BITQUERY_TOKEN}",
        }
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(BITQUERY_URL, json={"query": query}, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        transfers = data.get("data", {}).get("EVM", {}).get("Transfers", [])
        if not transfers:
            return f"🐋 Whale Alert Monitor\nNo transactions above ${min_usd:,.0f} found recently"

        lines = [f"🐋 Whale Alert Monitor\nTracking transactions > ${min_usd:,.0f}\n"]
        for tx in transfers[:10]:
            transfer = tx.get("Transfer", {})
            amount = float(transfer.get("Amount", 0))
            amount_usd = float(transfer.get("AmountInUSD", 0))
            symbol = transfer.get("Currency", {}).get("Symbol", "???")
            time_ = tx.get("Block", {}).get("Time", "")
            emoji = "🚨" if amount_usd >= 10_000_000 else "⚠️" if amount_usd >= 1_000_000 else "🐋"
            lines.append(f"{emoji} {amount:,.2f} {symbol} (${amount_usd:,.0f})\n   {time_}")

        return "\n".join(lines)
    except Exception as e:
        return {"error": f"get_whale_alert failed: {str(e)}"}


async def test_telegram_alert() -> dict:
    """Send a test message to verify Telegram integration is working."""
    message = (
        "✅ <b>WhaleTrucker Alert System</b>\n\n"
        "🔗 Telegram integration is <b>active</b>\n"
        "🐋 Whale monitoring ready (via Bitquery)\n"
        "⚡ Powered by Scutua-MCP"
    )
    return await send_telegram(message)
