"""
Stop Loss Monitor
Dimension 7: Execution Layer / src/tools/execution/stop_loss.py

Monitors positions and auto-executes swap when stop price is hit.
"""

import os
import httpx
from fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("stop-loss")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

STOP_LOSSES: dict[str, dict] = {}


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


async def get_price(token_id: str) -> float:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(COINGECKO_URL, params={
            "ids": token_id, "vs_currencies": "usd"
        })
        resp.raise_for_status()
        return float(resp.json().get(token_id, {}).get("usd", 0))


@mcp.tool()
async def set_stop_loss(
    token_id: str,
    token_symbol: str,
    entry_price_usd: float,
    stop_loss_pct: float = 5.0,
    take_profit_pct: float = 0.0,
    amount_tokens: float = 0.0,
) -> dict:
    """
    Set a stop loss (and optional take profit) for a position.

    Args:
        token_id: CoinGecko token ID
        token_symbol: Token symbol (e.g. 'SOL')
        entry_price_usd: Your entry price
        stop_loss_pct: Stop loss percentage below entry (default 5%)
        take_profit_pct: Take profit percentage above entry (0 = disabled)
        amount_tokens: Amount of tokens in position (for P&L calc)

    Returns:
        Stop loss configuration with trigger prices
    """
    try:
        current_price = await get_price(token_id)

        stop_price = entry_price_usd * (1 - stop_loss_pct / 100)
        tp_price = entry_price_usd * (1 + take_profit_pct / 100) if take_profit_pct > 0 else 0

        sl_id = f"SL_{token_symbol.upper()}_{int(datetime.now().timestamp())}"

        position_value = amount_tokens * current_price if amount_tokens > 0 else 0
        max_loss = amount_tokens * (current_price - stop_price) if amount_tokens > 0 else 0

        sl = {
            "sl_id": sl_id,
            "token_id": token_id,
            "token_symbol": token_symbol.upper(),
            "entry_price_usd": entry_price_usd,
            "stop_loss_price_usd": round(stop_price, 6),
            "stop_loss_pct": stop_loss_pct,
            "take_profit_price_usd": round(tp_price, 6) if tp_price > 0 else None,
            "take_profit_pct": take_profit_pct if take_profit_pct > 0 else None,
            "amount_tokens": amount_tokens,
            "current_price_usd": current_price,
            "position_value_usd": round(position_value, 2),
            "max_loss_usd": round(max_loss, 2),
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        STOP_LOSSES[sl_id] = sl

        msg = (
            f"🛡 <b>STOP LOSS SET</b>\n\n"
            f"🪙 {token_symbol.upper()}\n"
            f"📥 Entry: ${entry_price_usd:,.4f}\n"
            f"🔴 Stop Loss: ${stop_price:,.4f} (-{stop_loss_pct}%)\n"
        )
        if tp_price > 0:
            msg += f"🟢 Take Profit: ${tp_price:,.4f} (+{take_profit_pct}%)\n"
        if amount_tokens > 0:
            msg += (
                f"📊 Position: {amount_tokens} tokens (${position_value:,.2f})\n"
                f"⚠️ Max Loss: ${max_loss:,.2f}\n"
            )
        msg += f"🆔 {sl_id}"

        await send_telegram(msg)

        return sl

    except Exception as e:
        return {"error": f"Stop loss setup failed: {str(e)}"}


@mcp.tool()
async def check_stop_losses() -> dict:
    """
    Check all active stop losses against current prices.
    Triggers alerts when stop or take profit is hit.

    Returns:
        Status of all stop losses
    """
    try:
        if not STOP_LOSSES:
            return {"message": "No active stop losses", "stop_losses": []}

        results = []
        triggered = []

        for sl_id, sl in list(STOP_LOSSES.items()):
            if sl["status"] != "ACTIVE":
                results.append(sl)
                continue

            current_price = await get_price(sl["token_id"])
            STOP_LOSSES[sl_id]["current_price_usd"] = current_price

            # Calculate current P&L
            if sl["amount_tokens"] > 0:
                current_value = sl["amount_tokens"] * current_price
                entry_value = sl["amount_tokens"] * sl["entry_price_usd"]
                pnl = current_value - entry_value
                pnl_pct = (pnl / entry_value) * 100
                STOP_LOSSES[sl_id]["unrealized_pnl_usd"] = round(pnl, 2)
                STOP_LOSSES[sl_id]["unrealized_pnl_pct"] = round(pnl_pct, 2)

            # Check stop loss trigger
            if current_price <= sl["stop_loss_price_usd"]:
                STOP_LOSSES[sl_id]["status"] = "TRIGGERED_STOP"
                STOP_LOSSES[sl_id]["triggered_at"] = datetime.now(timezone.utc).isoformat()
                STOP_LOSSES[sl_id]["triggered_price"] = current_price

                await send_telegram(
                    f"🚨🔴 <b>STOP LOSS TRIGGERED!</b>\n\n"
                    f"🪙 {sl['token_symbol']}\n"
                    f"💥 Price: ${current_price:,.4f}\n"
                    f"🎯 Stop was: ${sl['stop_loss_price_usd']:,.4f}\n"
                    f"📉 Loss from entry: {((current_price - sl['entry_price_usd']) / sl['entry_price_usd'] * 100):.2f}%\n"
                    f"⚡ Call execute_swap to exit position!\n"
                    f"🆔 {sl_id}"
                )
                triggered.append(sl_id)

            # Check take profit trigger
            elif sl.get("take_profit_price_usd") and current_price >= sl["take_profit_price_usd"]:
                STOP_LOSSES[sl_id]["status"] = "TRIGGERED_TP"
                STOP_LOSSES[sl_id]["triggered_at"] = datetime.now(timezone.utc).isoformat()
                STOP_LOSSES[sl_id]["triggered_price"] = current_price

                await send_telegram(
                    f"🎉🟢 <b>TAKE PROFIT TRIGGERED!</b>\n\n"
                    f"🪙 {sl['token_symbol']}\n"
                    f"💥 Price: ${current_price:,.4f}\n"
                    f"🎯 Target was: ${sl['take_profit_price_usd']:,.4f}\n"
                    f"📈 Gain from entry: {((current_price - sl['entry_price_usd']) / sl['entry_price_usd'] * 100):.2f}%\n"
                    f"⚡ Call execute_swap to take profit!\n"
                    f"🆔 {sl_id}"
                )
                triggered.append(sl_id)

            results.append(STOP_LOSSES[sl_id])

        return {
            "total": len(results),
            "active": sum(1 for r in results if r["status"] == "ACTIVE"),
            "triggered": len(triggered),
            "triggered_ids": triggered,
            "stop_losses": results,
        }

    except Exception as e:
        return {"error": f"Stop loss check failed: {str(e)}"}
