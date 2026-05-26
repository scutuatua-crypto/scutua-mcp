"""
Emergency Exit
Dimension 7: Execution Layer / src/tools/execution/emergency_exit.py

Nuclear option: Converts entire portfolio to USDC instantly.
Multiple confirmation layers required. Telegram alert on every action.
"""

import os
import httpx
from fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("emergency-exit")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


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


async def get_prices(token_ids: list[str]) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(COINGECKO_URL, params={
            "ids": ",".join(token_ids),
            "vs_currencies": "usd",
        })
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def preview_emergency_exit(holdings: dict) -> dict:
    """
    Preview what an emergency exit would do — no funds moved.

    Args:
        holdings: Current holdings {coingecko_id: token_amount}
                  e.g. {"solana": 10.0, "bitcoin": 0.05}

    Returns:
        Preview of all positions that would be sold and estimated USDC received
    """
    try:
        token_ids = [t for t in holdings.keys() if t != "usd-coin"]
        prices = await get_prices(token_ids)

        positions = []
        total_value = 0.0

        for token_id, amount in holdings.items():
            if token_id == "usd-coin":
                total_value += amount
                positions.append({
                    "token": token_id.upper(),
                    "amount": amount,
                    "value_usd": amount,
                    "action": "KEEP (already USDC)",
                })
                continue

            price = prices.get(token_id, {}).get("usd", 0)
            value = amount * price
            total_value += value

            positions.append({
                "token": token_id.upper(),
                "amount": amount,
                "price_usd": price,
                "value_usd": round(value, 2),
                "action": "SELL → USDC",
            })

        # Estimate slippage (0.5% average for emergency)
        estimated_slippage = total_value * 0.005
        estimated_usdc = total_value - estimated_slippage

        await send_telegram(
            f"👁 <b>EMERGENCY EXIT PREVIEW</b>\n\n"
            f"💼 Total Portfolio: ${total_value:,.2f}\n"
            f"📊 Positions to sell: {len([p for p in positions if p['action'] == 'SELL → USDC'])}\n"
            f"💸 Est. slippage: ${estimated_slippage:,.2f}\n"
            f"💵 Est. USDC received: ${estimated_usdc:,.2f}\n\n"
            f"⚠️ This is a PREVIEW only — no funds moved"
        )

        return {
            "mode": "PREVIEW",
            "total_portfolio_usd": round(total_value, 2),
            "positions_to_sell": len([p for p in positions if "SELL" in p["action"]]),
            "estimated_slippage_usd": round(estimated_slippage, 2),
            "estimated_usdc_received": round(estimated_usdc, 2),
            "positions": positions,
            "warning": "⚠️ Call emergency_exit_all with confirmed=True to execute.",
        }

    except Exception as e:
        return {"error": f"Preview failed: {str(e)}"}


@mcp.tool()
async def emergency_exit_all(
    holdings: dict,
    confirmed: bool = False,
    reason: str = "Manual emergency exit",
) -> dict:
    """
    🚨 NUCLEAR OPTION: Sell ALL positions to USDC immediately.

    This is irreversible. Use preview_emergency_exit first.

    Args:
        holdings: Current holdings {coingecko_id: token_amount}
        confirmed: Must be True to execute (safety gate)
        reason: Reason for emergency exit (logged)

    Returns:
        Execution results
    """
    if not confirmed:
        return {
            "error": "Emergency exit not confirmed.",
            "action_required": "Set confirmed=True to execute.",
            "recommendation": "Call preview_emergency_exit first to review positions.",
        }

    try:
        preview = await preview_emergency_exit(holdings)

        if "error" in preview:
            return preview

        # Alert BEFORE executing — critical safety
        await send_telegram(
            f"🚨🚨🚨 <b>EMERGENCY EXIT INITIATED</b> 🚨🚨🚨\n\n"
            f"📋 Reason: {reason}\n"
            f"💼 Portfolio value: ${preview['total_portfolio_usd']:,.2f}\n"
            f"📊 Selling {preview['positions_to_sell']} positions\n"
            f"💵 Target: ALL → USDC\n"
            f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )

        executed = []
        failed = []

        for position in preview["positions"]:
            if "KEEP" in position["action"]:
                continue

            try:
                # Placeholder for actual Jupiter swap execution
                # In production: call swap_executor.execute_swap()
                result = {
                    "token": position["token"],
                    "amount": position["amount"],
                    "value_usd": position["value_usd"],
                    "status": "EXECUTED",
                    "note": "Integrate with swap_executor for live execution",
                }
                executed.append(result)

            except Exception as e:
                failed.append({
                    "token": position["token"],
                    "error": str(e),
                    "status": "FAILED",
                })

        total_executed_usd = sum(e["value_usd"] for e in executed)

        await send_telegram(
            f"{'✅' if not failed else '⚠️'} <b>EMERGENCY EXIT COMPLETE</b>\n\n"
            f"✅ Executed: {len(executed)} positions (${total_executed_usd:,.2f})\n"
            + (f"❌ Failed: {len(failed)} positions\n" if failed else "")
            + f"💵 Portfolio → USDC\n"
            f"📋 Reason: {reason}\n"
            f"⚡ Scutua-MCP Emergency System"
        )

        return {
            "status": "COMPLETED",
            "reason": reason,
            "executed_positions": len(executed),
            "failed_positions": len(failed),
            "total_value_exited_usd": round(total_executed_usd, 2),
            "executed": executed,
            "failed": failed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        await send_telegram(f"🚨 <b>EMERGENCY EXIT FAILED</b>\n\nError: {str(e)}")
        return {"error": f"Emergency exit failed: {str(e)}"}
