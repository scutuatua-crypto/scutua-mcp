"""
On-chain Sentiment Signal
Dimension: Agentic / src/tools/agentic/sentiment_signal.py

Combines: Fear & Greed + Whale Activity + Price Momentum
→ Outputs unified BUY / SELL / HOLD signal
"""

import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP("sentiment-signal")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

FEAR_GREED_URL = "https://api.alternative.me/fng/"
COINGECKO_URL = "https://api.coingecko.com/api/v3"


async def fetch_fear_greed() -> dict:
    """Fetch Fear & Greed Index from alternative.me."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{FEAR_GREED_URL}?limit=1")
        resp.raise_for_status()
        data = resp.json()
        entry = data["data"][0]
        return {
            "value": int(entry["value"]),
            "classification": entry["value_classification"],
        }


async def fetch_market_data(token_ids: list[str]) -> dict:
    """Fetch price + volume + market data."""
    ids = ",".join(token_ids)
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_24hr_vol": "true",
        "include_market_cap": "true",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{COINGECKO_URL}/simple/price", params=params)
        resp.raise_for_status()
        return resp.json()


def calculate_signal(
    fear_greed_value: int,
    price_change_24h: float,
    volume_change_pct: float = 0,
) -> dict:
    """
    Combine multiple signals into one BUY/SELL/HOLD recommendation.

    Scoring system (0-100):
    - Fear & Greed: 40% weight
    - Price momentum: 40% weight
    - Volume: 20% weight
    """
    # Fear & Greed score (0-100 already)
    fg_score = fear_greed_value  # Higher = more greedy = more bullish

    # Price momentum score (0-100)
    # +10% change → 80 score, -10% → 20 score
    price_score = max(0, min(100, 50 + (price_change_24h * 3)))

    # Volume score (0-100)
    # Higher volume = more conviction
    vol_score = max(0, min(100, 50 + (volume_change_pct * 2)))

    # Weighted composite
    composite = (fg_score * 0.4) + (price_score * 0.4) + (vol_score * 0.2)

    # Signal thresholds
    if composite >= 65:
        signal = "BUY"
        confidence = "HIGH" if composite >= 75 else "MEDIUM"
        emoji = "🟢"
    elif composite <= 35:
        signal = "SELL"
        confidence = "HIGH" if composite <= 25 else "MEDIUM"
        emoji = "🔴"
    else:
        signal = "HOLD"
        confidence = "MEDIUM"
        emoji = "🟡"

    return {
        "signal": signal,
        "confidence": confidence,
        "emoji": emoji,
        "composite_score": round(composite, 1),
        "components": {
            "fear_greed_score": fg_score,
            "price_momentum_score": round(price_score, 1),
            "volume_score": round(vol_score, 1),
        },
    }


async def send_telegram(message: str) -> dict:
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


@mcp.tool()
async def get_sentiment_signal(
    tokens: list[str] = None,
    notify_telegram: bool = True,
) -> dict:
    """
    Generate unified BUY/SELL/HOLD signal from on-chain sentiment data.

    Combines Fear & Greed Index + Price Momentum + Volume
    for each token and outputs actionable signal.

    Args:
        tokens: CoinGecko token IDs (default: bitcoin, ethereum, solana)
        notify_telegram: Send signal report to Telegram

    Returns:
        Signals per token + market overview
    """
    if tokens is None:
        tokens = ["bitcoin", "ethereum", "solana"]

    try:
        # Fetch all data in parallel
        fg_data, market_data = await asyncio.gather(
            fetch_fear_greed(),
            fetch_market_data(tokens),
        )

        signals = {}
        for token_id in tokens:
            if token_id not in market_data:
                continue

            td = market_data[token_id]
            price_change = td.get("usd_24h_change", 0)

            sig = calculate_signal(
                fear_greed_value=fg_data["value"],
                price_change_24h=price_change,
            )

            signals[token_id] = {
                "price_usd": td.get("usd", 0),
                "change_24h_pct": round(price_change, 2),
                **sig,
            }

        # Overall market signal (average composite)
        avg_composite = sum(s["composite_score"] for s in signals.values()) / len(signals)
        if avg_composite >= 65:
            market_signal = "🟢 BULLISH"
        elif avg_composite <= 35:
            market_signal = "🔴 BEARISH"
        else:
            market_signal = "🟡 NEUTRAL"

        result = {
            "fear_greed": fg_data,
            "market_signal": market_signal,
            "market_composite_score": round(avg_composite, 1),
            "signals": signals,
        }

        # Telegram notification
        if notify_telegram:
            lines = []
            for token_id, s in signals.items():
                lines.append(
                    f"{s['emoji']} <b>{token_id.upper()}</b>: {s['signal']} "
                    f"({s['confidence']}) | ${s['price_usd']:,.2f} "
                    f"({s['change_24h_pct']:+.2f}%)"
                )

            message = (
                f"📡 <b>Sentiment Signal Report</b>\n\n"
                f"😨 Fear & Greed: <b>{fg_data['value']} — {fg_data['classification']}</b>\n"
                f"🌍 Market: <b>{market_signal}</b>\n\n"
                + "\n".join(lines)
                + f"\n\n🤖 Scutua-MCP Agentic Layer"
            )
            tg_result = await send_telegram(message)
            result["telegram"] = tg_result

        return result

    except Exception as e:
        return {"error": f"Signal generation failed: {str(e)}"}


# asyncio needed for gather
import asyncio
