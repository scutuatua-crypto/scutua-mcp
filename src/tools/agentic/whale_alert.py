"""
Whale Alert → Bitquery GraphQL (Free tier)
Dimension: Agentic / src/tools/agentic/whale_alert.py
"""

import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP("whale-alert")

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
      Block {
        Time
      }
      Transfer {
        Amount
        AmountInUSD
        Currency {
          Symbol
          Name
        }
        Sender
        Receiver
      }
      Transaction {
        Hash
      }
    }
  }
}
"""


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
    """Format Bitquery transfer into readable Telegram message."""
    transfer = tx.get("Transfer", {})
    symbol = transfer.get("Currency", {}).get("Symbol", "???").upper()
    amount = float(transfer.get("Amount", 0))
    amount_usd = float(transfer.get("AmountInUSD", 0))
    sender = transfer.get("Sender", "unknown")[:10] + "..."
    receiver = transfer.get("Receiver", "unknown")[:10] + "..."
    hash_ = tx.get("Transaction", {}).get("Hash", "")
    block_time = tx.get("Block", {}).get("Time", "")

    emoji = "🐋"
    if amount_usd >= 10_000_000:
        emoji = "🚨🐋🚨"
    elif amount_usd >= 1_000_000:
        emoji = "⚠️🐋"

    return (
        f"{emoji} <b>WHALE ALERT</b>\n\n"
        f"💰 <b>{amount:,.2f} {symbol}</b> (${amount_usd:,.0f})\n"
        f"🔗 Chain: ETHEREUM\n"
        f"📤 From: <code>{sender}</code>\n"
        f"📥 To: <code>{receiver}</code>\n"
        f"🕐 Time: {block_time}\n"
        f"🔎 <a href='https://etherscan.io/tx/{hash_}'>View TX</a>"
    )


@mcp.tool()
async def monitor_whales(
    min_usd: float = DEFAULT_MIN_USD,
    notify_telegram: bool = True,
    limit: int = 10,
) -> dict:
    """
    Fetch recent whale transactions via Bitquery and optionally alert via Telegram.

    Args:
        min_usd: Minimum transaction value in USD to include
        notify_telegram: Send alerts to Telegram channel
        limit: Max number of transactions to fetch

    Returns:
        Whale transactions with alert status
    """
    if not BITQUERY_TOKEN:
        return {"error": "BITQUERY_TOKEN not configured — add it to environment variables"}

    try:
        query = WHALE_QUERY % (int(min_usd), limit)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BITQUERY_TOKEN}",
        }

        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                BITQUERY_URL,
                json={"query": query},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()

        transfers = (
            data.get("data", {})
            .get("EVM", {})
            .get("Transfers", [])
        )

        alerts_sent = []

        for tx in transfers:
            transfer = tx.get("Transfer", {})
            amount_usd = float(transfer.get("AmountInUSD", 0))

            alert_result = {
                "tx_hash": tx.get("Transaction", {}).get("Hash", ""),
                "amount_usd": amount_usd,
                "symbol": transfer.get("Currency", {}).get("Symbol", "???"),
                "amount": float(transfer.get("Amount", 0)),
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
            "telegram_enabled": notify_telegram,
            "source": "Bitquery EVM (Ethereum)",
            "alerts": alerts_sent,
        }

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return {"error": "Invalid BITQUERY_TOKEN — check Authorization tab on account.bitquery.io"}
        return {"error": f"HTTP {e.response.status_code}: {str(e)}"}
    except Exception as e:
        return {"error": f"Monitor failed: {str(e)}"}


@mcp.tool()
async def get_whale_alert(min_usd: float = 100_000) -> dict:
    """
    Get recent large crypto transactions (whale alert) via Bitquery.

    Args:
        min_usd: Minimum USD value to filter transactions

    Returns:
        List of recent large transactions
    """
    if not BITQUERY_TOKEN:
        return {"error": "BITQUERY_TOKEN not configured"}

    try:
        query = WHALE_QUERY % (int(min_usd), 20)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BITQUERY_TOKEN}",
        }

        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                BITQUERY_URL,
                json={"query": query},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()

        transfers = (
            data.get("data", {})
            .get("EVM", {})
            .get("Transfers", [])
        )

        results = []
        for tx in transfers:
            transfer = tx.get("Transfer", {})
            results.append({
                "symbol": transfer.get("Currency", {}).get("Symbol", "???"),
                "amount": float(transfer.get("Amount", 0)),
                "amount_usd": float(transfer.get("AmountInUSD", 0)),
                "sender": transfer.get("Sender", ""),
                "receiver": transfer.get("Receiver", ""),
                "hash": tx.get("Transaction", {}).get("Hash", ""),
                "time": tx.get("Block", {}).get("Time", ""),
            })

        if not results:
            return f"🐋 Whale Alert Monitor\nNo transactions above ${min_usd:,.0f} found recently"

        lines = [f"🐋 Whale Alert Monitor\nTracking transactions > ${min_usd:,.0f}\n"]
        for r in results[:10]:
            emoji = "🚨" if r["amount_usd"] >= 10_000_000 else "⚠️" if r["amount_usd"] >= 1_000_000 else "🐋"
            lines.append(
                f"{emoji} {r['amount']:,.2f} {r['symbol']} (${r['amount_usd']:,.0f})\n"
                f"   {r['time']}"
            )

        return "\n".join(lines)

    except Exception as e:
        return {"error": f"get_whale_alert failed: {str(e)}"}


@mcp.tool()
async def test_telegram_alert() -> dict:
    """
    Send a test message to verify Telegram integration is working.
    """
    message = (
        "✅ <b>WhaleTrucker Alert System</b>\n\n"
        "🔗 Telegram integration is <b>active</b>\n"
        "🐋 Whale monitoring ready (via Bitquery)\n"
        "⚡ Powered by Scutua-MCP"
    )
    result = await send_telegram(message)
    return result
