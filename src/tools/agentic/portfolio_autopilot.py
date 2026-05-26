"""
Portfolio Autopilot
Dimension: Agentic / src/tools/agentic/portfolio_autopilot.py
"""

import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP("portfolio-autopilot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

COINGECKO_URL = "https://api.coingecko.com/api/v3"


async def get_prices(token_ids: list[str]) -> dict:
    """Fetch current prices from CoinGecko."""
    ids = ",".join(token_ids)
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{COINGECKO_URL}/simple/price", params=params)
        resp.raise_for_status()
        return resp.json()


async def send_telegram(message: str) -> dict:
    """Send rebalance report to Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        return {"sent": False, "reason": "Telegram not configured"}

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return {"sent": True}


def calculate_rebalance(
    holdings: dict,
    current_prices: dict,
    target_weights: dict,
) -> dict:
    """
    Calculate rebalancing actions needed.

    holdings: {"bitcoin": 0.5, "ethereum": 2.0, ...}  token_id: amount
    target_weights: {"bitcoin": 0.4, "ethereum": 0.3, ...}  token_id: 0-1
    """
    # Current portfolio value
    portfolio = {}
    total_value = 0.0

    for token_id, amount in holdings.items():
        price = current_prices.get(token_id, {}).get("usd", 0)
        value = amount * price
        change_24h = current_prices.get(token_id, {}).get("usd_24h_change", 0)
        portfolio[token_id] = {
            "amount": amount,
            "price_usd": price,
            "value_usd": value,
            "change_24h_pct": round(change_24h, 2),
        }
        total_value += value

    if total_value == 0:
        return {"error": "Portfolio value is zero — check token IDs and prices"}

    # Current weights
    for token_id in portfolio:
        portfolio[token_id]["current_weight"] = round(
            portfolio[token_id]["value_usd"] / total_value, 4
        )

    # Rebalancing actions
    actions = []
    for token_id, target_w in target_weights.items():
        if token_id not in portfolio:
            continue

        current_w = portfolio[token_id]["current_weight"]
        diff_w = target_w - current_w
        diff_usd = diff_w * total_value
        price = portfolio[token_id]["price_usd"]
        diff_tokens = diff_usd / price if price > 0 else 0

        if abs(diff_usd) < 10:  # Ignore tiny rebalances < $10
            continue

        action = "BUY" if diff_usd > 0 else "SELL"
        actions.append({
            "token": token_id,
            "action": action,
            "current_weight_pct": round(current_w * 100, 2),
            "target_weight_pct": round(target_w * 100, 2),
            "diff_usd": round(abs(diff_usd), 2),
            "diff_tokens": round(abs(diff_tokens), 6),
            "urgency": "HIGH" if abs(diff_w) > 0.1 else "MEDIUM" if abs(diff_w) > 0.05 else "LOW",
        })

    actions.sort(key=lambda x: abs(x["diff_usd"]), reverse=True)

    return {
        "total_value_usd": round(total_value, 2),
        "portfolio": portfolio,
        "rebalance_actions": actions,
        "actions_needed": len(actions),
    }


@mcp.tool()
async def autopilot_analyze(
    holdings: dict,
    target_weights: dict,
    notify_telegram: bool = True,
) -> dict:
    """
    Analyze portfolio and generate rebalancing recommendations.

    Args:
        holdings: Token holdings as {coingecko_id: amount}
                  Example: {"bitcoin": 0.5, "ethereum": 2.0, "solana": 10.0}
        target_weights: Target allocation as {coingecko_id: weight_0_to_1}
                  Example: {"bitcoin": 0.5, "ethereum": 0.3, "solana": 0.2}
        notify_telegram: Send rebalance report to Telegram

    Returns:
        Portfolio analysis with rebalancing actions
    """
    try:
        # Validate weights sum to ~1.0
        weight_sum = sum(target_weights.values())
        if not (0.95 <= weight_sum <= 1.05):
            return {
                "error": f"Target weights must sum to 1.0 (got {weight_sum:.2f})"
            }

        token_ids = list(holdings.keys())
        prices = await get_prices(token_ids)

        result = calculate_rebalance(holdings, prices, target_weights)

        if "error" in result:
            return result

        # Send Telegram report if enabled
        if notify_telegram and result["actions_needed"] > 0:
            actions_text = ""
            for a in result["rebalance_actions"]:
                emoji = "🟢" if a["action"] == "BUY" else "🔴"
                actions_text += (
                    f"{emoji} <b>{a['action']} {a['token'].upper()}</b>\n"
                    f"   ${a['diff_usd']:,.2f} ({a['diff_tokens']} tokens)\n"
                    f"   {a['current_weight_pct']}% → {a['target_weight_pct']}% "
                    f"[{a['urgency']}]\n\n"
                )

            message = (
                f"📊 <b>Portfolio Autopilot Report</b>\n\n"
                f"💼 Total Value: <b>${result['total_value_usd']:,.2f}</b>\n"
                f"⚡ Actions Needed: {result['actions_needed']}\n\n"
                f"{actions_text}"
                f"🤖 Powered by Scutua-MCP"
            )
            tg_result = await send_telegram(message)
            result["telegram"] = tg_result

        return result

    except Exception as e:
        return {"error": f"Autopilot failed: {str(e)}"}
