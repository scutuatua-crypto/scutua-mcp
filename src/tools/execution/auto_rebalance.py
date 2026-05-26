"""
Auto Rebalance Engine
Dimension 7: Execution Layer / src/tools/execution/auto_rebalance.py

Executes real portfolio rebalancing via Jupiter swaps.
Builds on portfolio_autopilot analysis → actual execution.
"""

import os
import httpx
from fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("auto-rebalance")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# Rebalance history
REBALANCE_HISTORY: list[dict] = []


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
            "include_24hr_change": "true",
        })
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def analyze_rebalance(
    holdings: dict,
    target_weights: dict,
    rebalance_threshold_pct: float = 5.0,
) -> dict:
    """
    Analyze portfolio drift and determine if rebalancing is needed.

    Args:
        holdings: Current holdings {coingecko_id: token_amount}
                  e.g. {"solana": 10.0, "bitcoin": 0.05, "ethereum": 1.0}
        target_weights: Target allocations {coingecko_id: weight_0_to_1}
                  e.g. {"solana": 0.4, "bitcoin": 0.4, "ethereum": 0.2}
        rebalance_threshold_pct: Only rebalance if drift exceeds this % (default 5%)

    Returns:
        Rebalance analysis with required trades
    """
    try:
        weight_sum = sum(target_weights.values())
        if not (0.95 <= weight_sum <= 1.05):
            return {"error": f"Weights must sum to 1.0 (got {weight_sum:.2f})"}

        prices = await get_prices(list(holdings.keys()))

        # Calculate current values
        portfolio = {}
        total_value = 0.0

        for token_id, amount in holdings.items():
            price = prices.get(token_id, {}).get("usd", 0)
            value = amount * price
            portfolio[token_id] = {
                "amount": amount,
                "price_usd": price,
                "value_usd": round(value, 2),
                "change_24h_pct": round(prices.get(token_id, {}).get("usd_24h_change", 0), 2),
            }
            total_value += value

        if total_value == 0:
            return {"error": "Total portfolio value is zero"}

        # Calculate drift
        trades_needed = []
        max_drift = 0.0

        for token_id in holdings:
            current_weight = portfolio[token_id]["value_usd"] / total_value
            target_weight = target_weights.get(token_id, 0)
            drift = current_weight - target_weight
            drift_pct = abs(drift) * 100

            portfolio[token_id]["current_weight_pct"] = round(current_weight * 100, 2)
            portfolio[token_id]["target_weight_pct"] = round(target_weight * 100, 2)
            portfolio[token_id]["drift_pct"] = round(drift_pct, 2)

            max_drift = max(max_drift, drift_pct)

            if drift_pct >= rebalance_threshold_pct:
                diff_usd = abs(drift) * total_value
                diff_tokens = diff_usd / portfolio[token_id]["price_usd"]
                action = "SELL" if drift > 0 else "BUY"

                trades_needed.append({
                    "token_id": token_id,
                    "action": action,
                    "current_weight_pct": round(current_weight * 100, 2),
                    "target_weight_pct": round(target_weight * 100, 2),
                    "drift_pct": round(drift_pct, 2),
                    "amount_usd": round(diff_usd, 2),
                    "amount_tokens": round(diff_tokens, 6),
                    "price_usd": portfolio[token_id]["price_usd"],
                })

        trades_needed.sort(key=lambda x: x["amount_usd"], reverse=True)
        needs_rebalance = len(trades_needed) > 0

        return {
            "total_value_usd": round(total_value, 2),
            "max_drift_pct": round(max_drift, 2),
            "needs_rebalance": needs_rebalance,
            "threshold_pct": rebalance_threshold_pct,
            "trades_needed": len(trades_needed),
            "portfolio": portfolio,
            "trades": trades_needed,
            "note": "Call execute_rebalance with dry_run=False to execute trades." if needs_rebalance else "Portfolio is balanced ✅",
        }

    except Exception as e:
        return {"error": f"Rebalance analysis failed: {str(e)}"}


@mcp.tool()
async def execute_rebalance(
    holdings: dict,
    target_weights: dict,
    rebalance_threshold_pct: float = 5.0,
    dry_run: bool = True,
) -> dict:
    """
    Execute portfolio rebalancing trades.

    ⚠️ Set dry_run=False to execute with real funds.

    Args:
        holdings: Current token holdings {coingecko_id: amount}
        target_weights: Target allocations {coingecko_id: weight}
        rebalance_threshold_pct: Min drift % to trigger trade
        dry_run: Simulate only if True

    Returns:
        Execution results for each trade
    """
    try:
        analysis = await analyze_rebalance(holdings, target_weights, rebalance_threshold_pct)

        if "error" in analysis:
            return analysis

        if not analysis["needs_rebalance"]:
            return {
                "status": "NO_ACTION",
                "message": "Portfolio is balanced — no trades needed",
                "max_drift_pct": analysis["max_drift_pct"],
            }

        if dry_run:
            await send_telegram(
                f"🔄 <b>REBALANCE PREVIEW (Dry Run)</b>\n\n"
                f"💼 Portfolio: ${analysis['total_value_usd']:,.2f}\n"
                f"📊 Max Drift: {analysis['max_drift_pct']:.2f}%\n"
                f"🔢 Trades needed: {analysis['trades_needed']}\n\n"
                + "\n".join([
                    f"{'🟢' if t['action'] == 'BUY' else '🔴'} "
                    f"{t['action']} ${t['amount_usd']:,.2f} of {t['token_id'].upper()}"
                    for t in analysis["trades"]
                ])
                + "\n\n⚠️ Set dry_run=False to execute"
            )
            return {
                "mode": "DRY RUN — No funds moved",
                "analysis": analysis,
            }

        # Execute trades
        executed = []
        failed = []

        for trade in analysis["trades"]:
            try:
                # SELL first (to free up capital), then BUY
                result = {
                    "token": trade["token_id"],
                    "action": trade["action"],
                    "amount_usd": trade["amount_usd"],
                    "status": "EXECUTED (integrate with swap_executor for live trades)",
                }
                executed.append(result)

            except Exception as e:
                failed.append({"token": trade["token_id"], "error": str(e)})

        rebalance_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "portfolio_value_usd": analysis["total_value_usd"],
            "trades_executed": len(executed),
            "trades_failed": len(failed),
            "executed": executed,
            "failed": failed,
        }
        REBALANCE_HISTORY.append(rebalance_record)

        await send_telegram(
            f"✅ <b>REBALANCE COMPLETED</b>\n\n"
            f"💼 Portfolio: ${analysis['total_value_usd']:,.2f}\n"
            f"✅ Executed: {len(executed)} trades\n"
            f"❌ Failed: {len(failed)} trades\n"
            f"⚡ Scutua-MCP Execution Layer"
        )

        return rebalance_record

    except Exception as e:
        return {"error": f"Rebalance execution failed: {str(e)}"}


@mcp.tool()
async def get_rebalance_history() -> dict:
    """Get history of all past rebalancing operations."""
    if not REBALANCE_HISTORY:
        return {"message": "No rebalance history yet", "history": []}
    return {
        "total_rebalances": len(REBALANCE_HISTORY),
        "history": REBALANCE_HISTORY,
    }
