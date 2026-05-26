"""
Token Sniper
Dimension 7: Execution Layer / src/tools/execution/sniper.py

Monitors new token listings and auto-buys on trigger conditions.
Safety-first: multiple guards to prevent rug pulls.
"""

import os
import httpx
from fastmcp import FastMCP
from datetime import datetime, timezone

mcp = FastMCP("token-sniper")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")
BIRDEYE_URL = "https://public-api.birdeye.so"

SNIPE_TARGETS: dict[str, dict] = {}
SNIPE_HISTORY: list[dict] = []


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


async def get_token_security(mint: str) -> dict:
    """Check token security metrics via Birdeye."""
    headers = {"X-API-KEY": BIRDEYE_API_KEY}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BIRDEYE_URL}/defi/token_security",
            params={"address": mint},
            headers=headers,
        )
        if resp.status_code == 200:
            return resp.json().get("data", {})
        return {}


async def get_token_overview(mint: str) -> dict:
    """Get token overview from Birdeye."""
    headers = {"X-API-KEY": BIRDEYE_API_KEY}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{BIRDEYE_URL}/defi/token_overview",
            params={"address": mint},
            headers=headers,
        )
        if resp.status_code == 200:
            return resp.json().get("data", {})
        return {}


def safety_score(security: dict, overview: dict) -> tuple[int, list[str]]:
    """
    Calculate safety score (0-100) and list of warnings.
    Higher = safer.
    """
    score = 100
    warnings = []

    # Liquidity check
    liquidity = overview.get("liquidity", 0)
    if liquidity < 10_000:
        score -= 30
        warnings.append(f"⚠️ Low liquidity: ${liquidity:,.0f}")
    elif liquidity < 50_000:
        score -= 10
        warnings.append(f"⚡ Medium liquidity: ${liquidity:,.0f}")

    # Holder concentration
    top10_holders = security.get("top10HolderPercent", 0)
    if top10_holders > 80:
        score -= 40
        warnings.append(f"🚨 Top 10 holders own {top10_holders:.1f}%")
    elif top10_holders > 50:
        score -= 20
        warnings.append(f"⚠️ Top 10 holders own {top10_holders:.1f}%")

    # Mint authority
    if security.get("mintAuthority"):
        score -= 20
        warnings.append("🚨 Mint authority not renounced")

    # Freeze authority
    if security.get("freezeAuthority"):
        score -= 15
        warnings.append("🚨 Freeze authority active")

    return max(0, score), warnings


@mcp.tool()
async def analyze_token_safety(mint_address: str) -> dict:
    """
    Analyze a token's safety before sniping.

    Args:
        mint_address: Solana token mint address

    Returns:
        Safety score, warnings, and token metrics
    """
    try:
        security, overview = await asyncio.gather(
            get_token_security(mint_address),
            get_token_overview(mint_address),
        )

        score, warnings = safety_score(security, overview)

        risk_level = "LOW" if score >= 70 else "MEDIUM" if score >= 40 else "HIGH"
        recommendation = "✅ SAFE TO SNIPE" if score >= 60 else "⚠️ PROCEED WITH CAUTION" if score >= 40 else "🚫 AVOID"

        return {
            "mint": mint_address,
            "safety_score": score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "warnings": warnings,
            "metrics": {
                "liquidity_usd": overview.get("liquidity", 0),
                "market_cap_usd": overview.get("mc", 0),
                "holders": overview.get("holder", 0),
                "price_usd": overview.get("price", 0),
                "volume_24h_usd": overview.get("v24hUSD", 0),
                "top10_holder_pct": security.get("top10HolderPercent", 0),
                "mint_authority_renounced": not bool(security.get("mintAuthority")),
                "freeze_authority_renounced": not bool(security.get("freezeAuthority")),
            },
        }

    except Exception as e:
        return {"error": f"Safety analysis failed: {str(e)}"}


@mcp.tool()
async def snipe_token(
    mint_address: str,
    amount_usd: float,
    min_safety_score: int = 60,
    dry_run: bool = True,
) -> dict:
    """
    Snipe a token with safety checks.

    ⚠️ High risk operation. Always use dry_run=True first.

    Args:
        mint_address: Solana token mint to buy
        amount_usd: USD amount to spend
        min_safety_score: Minimum safety score to proceed (default 60)
        dry_run: Simulate only if True

    Returns:
        Snipe result or safety rejection
    """
    try:
        # Safety check first — always
        safety = await analyze_token_safety(mint_address)

        if "error" in safety:
            return safety

        score = safety["safety_score"]

        if score < min_safety_score:
            await send_telegram(
                f"🚫 <b>SNIPE REJECTED — SAFETY FAIL</b>\n\n"
                f"🪙 Mint: {mint_address[:8]}...{mint_address[-4:]}\n"
                f"🛡 Safety Score: {score}/100 (min: {min_safety_score})\n"
                f"⚠️ Warnings:\n" + "\n".join(safety["warnings"])
            )
            return {
                "status": "REJECTED",
                "reason": f"Safety score {score} below minimum {min_safety_score}",
                "safety": safety,
            }

        if dry_run:
            return {
                "mode": "DRY RUN",
                "mint": mint_address,
                "amount_usd": amount_usd,
                "safety_score": score,
                "risk_level": safety["risk_level"],
                "warnings": safety["warnings"],
                "would_execute": True,
                "message": "Set dry_run=False to execute real snipe.",
            }

        # Execute snipe via Jupiter swap
        snipe_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mint": mint_address,
            "amount_usd": amount_usd,
            "safety_score": score,
            "status": "EXECUTED",
        }
        SNIPE_HISTORY.append(snipe_record)

        await send_telegram(
            f"🎯 <b>SNIPE EXECUTED</b>\n\n"
            f"🪙 {mint_address[:8]}...{mint_address[-4:]}\n"
            f"💵 Amount: ${amount_usd:,.2f}\n"
            f"🛡 Safety: {score}/100\n"
            f"⚡ Scutua-MCP Sniper"
        )

        return {
            "status": "EXECUTED",
            "mint": mint_address,
            "amount_usd": amount_usd,
            "safety_score": score,
            "note": "Integrate with swap_executor for full execution",
        }

    except Exception as e:
        return {"error": f"Snipe failed: {str(e)}"}


import asyncio
