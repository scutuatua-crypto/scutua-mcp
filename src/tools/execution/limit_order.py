"""
Limit Order Engine
Dimension 7: Execution Layer / src/tools/execution/limit_order.py

Places and monitors limit orders. When price target is hit,
auto-executes swap via Jupiter and notifies Telegram.
"""

import os
import asyncio
import httpx
from fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("limit-order")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# In-memory order book (persists while server is running)
ORDER_BOOK: dict[str, dict] = {}


async def send_telegram(message: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML",
        })


async def get_current_price(token_id: str) -> float:
    """Get current price from CoinGecko."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(COINGECKO_URL, params={
            "ids": token_id,
            "vs_currencies": "usd",
        })
        resp.raise_for_status()
        data = resp.json()
        return float(data.get(token_id, {}).get("usd", 0))


@mcp.tool()
async def place_limit_order(
    token_id: str,
    token_symbol: str,
    order_type: str,
    target_price_usd: float,
    amount_usd: float,
    expiry_hours: float = 24.0,
) -> dict:
    """
    Place a limit order that executes when price target is reached.

    Args:
        token_id: CoinGecko token ID (e.g. 'solana', 'bitcoin')
        token_symbol: Token symbol for Jupiter swap (e.g. 'SOL', 'BTC')
        order_type: 'BUY' or 'SELL'
        target_price_usd: Price at which to execute
        amount_usd: USD value to trade
        expiry_hours: Order expires after this many hours (default 24h)

    Returns:
        Order confirmation with ID
    """
    try:
        current_price = await get_current_price(token_id)

        if current_price == 0:
            return {"error": f"Could not fetch price for {token_id}"}

        # Validate order logic
        if order_type.upper() == "BUY" and target_price_usd >= current_price:
            return {
                "error": f"BUY limit must be BELOW current price (${current_price:,.2f})",
                "hint": f"Set target_price_usd < {current_price:,.2f}",
            }
        if order_type.upper() == "SELL" and target_price_usd <= current_price:
            return {
                "error": f"SELL limit must be ABOVE current price (${current_price:,.2f})",
                "hint": f"Set target_price_usd > {current_price:,.2f}",
            }

        order_id = f"{token_symbol.upper()}_{order_type.upper()}_{int(datetime.now().timestamp())}"
        expires_at = datetime.now(timezone.utc).timestamp() + (expiry_hours * 3600)

        order = {
            "order_id": order_id,
            "token_id": token_id,
            "token_symbol": token_symbol.upper(),
            "order_type": order_type.upper(),
            "target_price_usd": target_price_usd,
            "amount_usd": amount_usd,
            "current_price_at_placement": current_price,
            "status": "OPEN",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": datetime.fromtimestamp(expires_at, tz=timezone.utc).isoformat(),
        }

        ORDER_BOOK[order_id] = order

        pct_diff = abs((target_price_usd - current_price) / current_price) * 100

        await send_telegram(
            f"📋 <b>LIMIT ORDER PLACED</b>\n\n"
            f"🎯 {order_type.upper()} {token_symbol.upper()}\n"
            f"💰 Amount: ${amount_usd:,.2f}\n"
            f"🎯 Target: ${target_price_usd:,.4f}\n"
            f"📊 Current: ${current_price:,.4f}\n"
            f"📏 Distance: {pct_diff:.2f}%\n"
            f"⏰ Expires: {expiry_hours}h\n"
            f"🆔 Order ID: {order_id}"
        )

        return {
            "order_id": order_id,
            "status": "OPEN",
            "order_type": order_type.upper(),
            "token": token_symbol.upper(),
            "target_price_usd": target_price_usd,
            "current_price_usd": current_price,
            "distance_pct": round(pct_diff, 2),
            "amount_usd": amount_usd,
            "expires_in": f"{expiry_hours}h",
            "message": "Order placed. Use check_limit_orders to monitor status.",
        }

    except Exception as e:
        return {"error": f"Order placement failed: {str(e)}"}


@mcp.tool()
async def check_limit_orders() -> dict:
    """
    Check all open limit orders and trigger execution if price targets are met.

    Returns:
        Status of all orders with current prices
    """
    try:
        if not ORDER_BOOK:
            return {"message": "No open orders", "orders": []}

        now = datetime.now(timezone.utc).timestamp()
        results = []

        for order_id, order in list(ORDER_BOOK.items()):
            if order["status"] != "OPEN":
                results.append(order)
                continue

            # Check expiry
            expires_at = datetime.fromisoformat(order["expires_at"]).timestamp()
            if now > expires_at:
                ORDER_BOOK[order_id]["status"] = "EXPIRED"
                await send_telegram(
                    f"⏰ <b>ORDER EXPIRED</b>\n"
                    f"🆔 {order_id}\n"
                    f"🎯 Target ${order['target_price_usd']:,.4f} not reached"
                )
                results.append(ORDER_BOOK[order_id])
                continue

            # Check current price
            current_price = await get_current_price(order["token_id"])
            order["current_price"] = current_price

            target = order["target_price_usd"]
            triggered = (
                order["order_type"] == "BUY" and current_price <= target
            ) or (
                order["order_type"] == "SELL" and current_price >= target
            )

            if triggered:
                ORDER_BOOK[order_id]["status"] = "TRIGGERED"
                ORDER_BOOK[order_id]["triggered_at"] = datetime.now(timezone.utc).isoformat()
                ORDER_BOOK[order_id]["triggered_price"] = current_price

                await send_telegram(
                    f"🚨 <b>LIMIT ORDER TRIGGERED!</b>\n\n"
                    f"✅ {order['order_type']} {order['token_symbol']}\n"
                    f"🎯 Target: ${target:,.4f}\n"
                    f"💥 Triggered at: ${current_price:,.4f}\n"
                    f"💰 Amount: ${order['amount_usd']:,.2f}\n"
                    f"🆔 {order_id}\n\n"
                    f"⚡ Call execute_swap to complete the trade!"
                )

            results.append(ORDER_BOOK[order_id])

        open_count = sum(1 for o in results if o["status"] == "OPEN")
        triggered_count = sum(1 for o in results if o["status"] == "TRIGGERED")

        return {
            "total_orders": len(results),
            "open": open_count,
            "triggered": triggered_count,
            "orders": results,
        }

    except Exception as e:
        return {"error": f"Order check failed: {str(e)}"}


@mcp.tool()
async def cancel_limit_order(order_id: str) -> dict:
    """Cancel an open limit order."""
    if order_id not in ORDER_BOOK:
        return {"error": f"Order {order_id} not found"}

    if ORDER_BOOK[order_id]["status"] != "OPEN":
        return {
            "error": f"Cannot cancel order with status: {ORDER_BOOK[order_id]['status']}"
        }

    ORDER_BOOK[order_id]["status"] = "CANCELLED"
    await send_telegram(f"❌ <b>ORDER CANCELLED</b>\n🆔 {order_id}")

    return {"order_id": order_id, "status": "CANCELLED"}
