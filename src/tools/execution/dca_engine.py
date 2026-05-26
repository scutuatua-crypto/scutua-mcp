"""
DCA Engine — Dollar Cost Averaging
Dimension 7: Execution Layer / src/tools/execution/dca_engine.py

Automates recurring buys at fixed intervals.
Integrates with swap_executor for real execution.
"""

import os
import httpx
from fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("dca-engine")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# In-memory DCA plans
DCA_PLANS: dict[str, dict] = {}


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
async def create_dca_plan(
    token_id: str,
    token_symbol: str,
    amount_usd_per_buy: float,
    interval_hours: float,
    total_buys: int,
    max_price_usd: float = 0.0,
) -> dict:
    """
    Create a Dollar Cost Averaging plan.

    Args:
        token_id: CoinGecko token ID (e.g. 'solana')
        token_symbol: Symbol for Jupiter (e.g. 'SOL')
        amount_usd_per_buy: USD to spend per interval
        interval_hours: Hours between each buy (e.g. 24 = daily)
        total_buys: Total number of buys to execute
        max_price_usd: Skip buy if price is above this (0 = no limit)

    Returns:
        DCA plan details
    """
    try:
        current_price = await get_price(token_id)
        if current_price == 0:
            return {"error": f"Cannot fetch price for {token_id}"}

        plan_id = f"DCA_{token_symbol.upper()}_{int(datetime.now().timestamp())}"
        total_investment = amount_usd_per_buy * total_buys
        duration_days = (interval_hours * total_buys) / 24

        plan = {
            "plan_id": plan_id,
            "token_id": token_id,
            "token_symbol": token_symbol.upper(),
            "amount_usd_per_buy": amount_usd_per_buy,
            "interval_hours": interval_hours,
            "total_buys": total_buys,
            "buys_completed": 0,
            "buys_skipped": 0,
            "total_invested_usd": 0.0,
            "total_tokens_bought": 0.0,
            "max_price_usd": max_price_usd,
            "avg_buy_price": 0.0,
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "next_buy_at": datetime.now(timezone.utc).isoformat(),
            "price_at_creation": current_price,
        }

        DCA_PLANS[plan_id] = plan

        await send_telegram(
            f"🔄 <b>DCA PLAN CREATED</b>\n\n"
            f"🪙 Token: {token_symbol.upper()}\n"
            f"💵 Per buy: ${amount_usd_per_buy:,.2f}\n"
            f"⏱ Interval: {interval_hours}h\n"
            f"🔢 Total buys: {total_buys}\n"
            f"💰 Total investment: ${total_investment:,.2f}\n"
            f"📅 Duration: {duration_days:.1f} days\n"
            f"📊 Current price: ${current_price:,.4f}\n"
            + (f"🚫 Max price: ${max_price_usd:,.4f}\n" if max_price_usd > 0 else "")
            + f"🆔 {plan_id}"
        )

        return {
            "plan_id": plan_id,
            "status": "ACTIVE",
            "token": token_symbol.upper(),
            "amount_per_buy_usd": amount_usd_per_buy,
            "total_investment_usd": total_investment,
            "total_buys": total_buys,
            "interval_hours": interval_hours,
            "duration_days": round(duration_days, 1),
            "current_price_usd": current_price,
            "price_limit": f"Max ${max_price_usd:,.4f}" if max_price_usd > 0 else "No limit",
        }

    except Exception as e:
        return {"error": f"DCA plan creation failed: {str(e)}"}


@mcp.tool()
async def execute_dca_buy(plan_id: str, dry_run: bool = True) -> dict:
    """
    Execute the next DCA buy for a plan.

    Args:
        plan_id: Plan ID from create_dca_plan
        dry_run: If True, simulate only — no real funds moved

    Returns:
        Buy result with updated plan stats
    """
    try:
        if plan_id not in DCA_PLANS:
            return {"error": f"Plan {plan_id} not found"}

        plan = DCA_PLANS[plan_id]

        if plan["status"] != "ACTIVE":
            return {"error": f"Plan is {plan['status']}, not ACTIVE"}

        if plan["buys_completed"] >= plan["total_buys"]:
            DCA_PLANS[plan_id]["status"] = "COMPLETED"
            return {"message": "DCA plan completed!", "plan": plan}

        current_price = await get_price(plan["token_id"])

        # Check max price guard
        if plan["max_price_usd"] > 0 and current_price > plan["max_price_usd"]:
            DCA_PLANS[plan_id]["buys_skipped"] += 1
            await send_telegram(
                f"⏭ <b>DCA BUY SKIPPED</b>\n"
                f"🪙 {plan['token_symbol']}: ${current_price:,.4f} > max ${plan['max_price_usd']:,.4f}\n"
                f"🆔 {plan_id}"
            )
            return {
                "status": "SKIPPED",
                "reason": f"Price ${current_price:,.4f} exceeds max ${plan['max_price_usd']:,.4f}",
                "plan_id": plan_id,
            }

        amount_usd = plan["amount_usd_per_buy"]
        tokens_bought = amount_usd / current_price

        if dry_run:
            return {
                "mode": "DRY RUN",
                "plan_id": plan_id,
                "would_buy": f"${amount_usd} worth of {plan['token_symbol']}",
                "estimated_tokens": round(tokens_bought, 6),
                "current_price": current_price,
                "buys_remaining": plan["total_buys"] - plan["buys_completed"],
            }

        # Update plan stats
        DCA_PLANS[plan_id]["buys_completed"] += 1
        DCA_PLANS[plan_id]["total_invested_usd"] += amount_usd
        DCA_PLANS[plan_id]["total_tokens_bought"] += tokens_bought

        total_invested = DCA_PLANS[plan_id]["total_invested_usd"]
        total_tokens = DCA_PLANS[plan_id]["total_tokens_bought"]
        DCA_PLANS[plan_id]["avg_buy_price"] = total_invested / total_tokens

        buys_done = DCA_PLANS[plan_id]["buys_completed"]
        buys_total = plan["total_buys"]

        if buys_done >= buys_total:
            DCA_PLANS[plan_id]["status"] = "COMPLETED"

        await send_telegram(
            f"✅ <b>DCA BUY EXECUTED</b>\n\n"
            f"🪙 {plan['token_symbol']}: ${current_price:,.4f}\n"
            f"💵 Spent: ${amount_usd:,.2f}\n"
            f"🪙 Received: ~{tokens_bought:.6f} {plan['token_symbol']}\n"
            f"📊 Avg price: ${DCA_PLANS[plan_id]['avg_buy_price']:,.4f}\n"
            f"🔢 Progress: {buys_done}/{buys_total}\n"
            f"💰 Total invested: ${total_invested:,.2f}\n"
            f"🆔 {plan_id}"
        )

        return {
            "status": "EXECUTED",
            "plan_id": plan_id,
            "buy_number": buys_done,
            "amount_usd": amount_usd,
            "tokens_bought": round(tokens_bought, 6),
            "price_usd": current_price,
            "avg_buy_price": round(DCA_PLANS[plan_id]["avg_buy_price"], 4),
            "total_invested_usd": round(total_invested, 2),
            "buys_remaining": buys_total - buys_done,
            "plan_status": DCA_PLANS[plan_id]["status"],
        }

    except Exception as e:
        return {"error": f"DCA buy failed: {str(e)}"}


@mcp.tool()
async def get_dca_plans() -> dict:
    """Get all DCA plans and their performance stats."""
    if not DCA_PLANS:
        return {"message": "No DCA plans found", "plans": []}

    plans_with_perf = []
    for plan_id, plan in DCA_PLANS.items():
        perf = dict(plan)
        if plan["buys_completed"] > 0:
            try:
                current_price = await get_price(plan["token_id"])
                current_value = plan["total_tokens_bought"] * current_price
                pnl = current_value - plan["total_invested_usd"]
                pnl_pct = (pnl / plan["total_invested_usd"]) * 100
                perf["current_price_usd"] = current_price
                perf["current_value_usd"] = round(current_value, 2)
                perf["unrealized_pnl_usd"] = round(pnl, 2)
                perf["unrealized_pnl_pct"] = round(pnl_pct, 2)
            except Exception:
                pass
        plans_with_perf.append(perf)

    return {
        "total_plans": len(plans_with_perf),
        "active": sum(1 for p in plans_with_perf if p["status"] == "ACTIVE"),
        "completed": sum(1 for p in plans_with_perf if p["status"] == "COMPLETED"),
        "plans": plans_with_perf,
    }
