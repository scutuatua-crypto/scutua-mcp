"""
On-chain Sentiment Signal
Dimension: Agentic / src/tools/agentic/sentiment_signal.py
"""
import os
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

FEAR_GREED_URL = "https://api.alternative.me/fng/"
COINGECKO_URL = "https://api.coingecko.com/api/v3"

_cache: dict = {}
CACHE_TTL = 300


def _get_cache(key: str):
    import time
    if key in _cache:
        value, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return value
    return None


def _set_cache(key: str, value):
    import time
    _cache[key] = (value, time.time())


async def fetch_fear_greed() -> dict:
    cached = _get_cache("fear_greed")
    if cached:
        return cached
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{FEAR_GREED_URL}?limit=1")
        resp.raise_for_status()
        entry = resp.json()["data"][0]
        result = {"value": int(entry["value"]), "classification": entry["value_classification"]}
        _set_cache("fear_greed", result)
        return result


async def fetch_market_data(token_ids: list[str]) -> dict:
    cache_key = f"market_{'_'.join(sorted(token_ids))}"
    cached = _get_cache(cache_key)
    if cached:
        return cached
    params = {"ids": ",".join(token_ids), "vs_currencies": "usd",
               "include_24hr_change": "true", "include_24hr_vol": "true",
               "include_market_cap": "true"}
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY} if COINGECKO_API_KEY else {}
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{COINGECKO_URL}/simple/price", params=params, headers=headers)
        if resp.status_code == 429:
            stale = _cache.get(cache_key)
            return stale[0] if stale else {"error": "CoinGecko rate limit — retry later"}
        resp.raise_for_status()
        data = resp.json()
        _set_cache(cache_key, data)
        return data


def calculate_signal(fear_greed_value: int, price_change_24h: float, volume_change_pct: float = 0) -> dict:
    fg_score = fear_greed_value
    price_score = max(0, min(100, 50 + (price_change_24h * 3)))
    vol_score = max(0, min(100, 50 + (volume_change_pct * 2)))
    composite = (fg_score * 0.4) + (price_score * 0.4) + (vol_score * 0.2)
    if composite >= 65:
        signal, emoji = "BUY", "🟢"
        confidence = "HIGH" if composite >= 75 else "MEDIUM"
    elif composite <= 35:
        signal, emoji = "SELL", "🔴"
        confidence = "HIGH" if composite <= 25 else "MEDIUM"
    else:
        signal, confidence, emoji = "HOLD", "MEDIUM", "🟡"
    return {"signal": signal, "confidence": confidence, "emoji": emoji,
            "composite_score": round(composite, 1),
            "components": {"fear_greed_score": fg_score,
                           "price_momentum_score": round(price_score, 1),
                           "volume_score": round(vol_score, 1)}}


async def _send_telegram(message: str) -> dict:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        return {"sent": False, "reason": "Telegram not configured"}
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(url, json={"chat_id": TELEGRAM_CHANNEL_ID,
                                             "text": message, "parse_mode": "HTML"})
        resp.raise_for_status()
        return {"sent": True}


def register_sentiment_tools(app: FastMCP):
    @app.tool()
    async def get_sentiment_signal(
        tokens: list[str] = None,
        notify_telegram: bool = True,
    ) -> dict:
        """Generate unified BUY/SELL/HOLD signal from on-chain sentiment data."""
        if tokens is None:
            tokens = ["bitcoin", "ethereum", "solana"]
        try:
            fg_data, market_data = await asyncio.gather(
                fetch_fear_greed(), fetch_market_data(tokens))
            if "error" in market_data:
                return {"error": market_data["error"]}

            signals = {}
            for token_id in tokens:
                if token_id not in market_data:
                    continue
                td = market_data[token_id]
                price_change = td.get("usd_24h_change", 0)
                sig = calculate_signal(fear_greed_value=fg_data["value"], price_change_24h=price_change)
                signals[token_id] = {"price_usd": td.get("usd", 0),
                                     "change_24h_pct": round(price_change, 2), **sig}

            if not signals:
                return {"error": "No signal data available"}

            avg_composite = sum(s["composite_score"] for s in signals.values()) / len(signals)
            market_signal = ("🟢 BULLISH" if avg_composite >= 65
                             else "🔴 BEARISH" if avg_composite <= 35 else "🟡 NEUTRAL")

            result = {"fear_greed": fg_data, "market_signal": market_signal,
                      "market_composite_score": round(avg_composite, 1), "signals": signals}

            if notify_telegram:
                lines = [f"{s['emoji']} <b>{tid.upper()}</b>: {s['signal']} ({s['confidence']}) "
                         f"| ${s['price_usd']:,.2f} ({s['change_24h_pct']:+.2f}%)"
                         for tid, s in signals.items()]
                message = (f"📡 <b>Sentiment Signal Report</b>\n\n"
                           f"😨 Fear & Greed: <b>{fg_data['value']} — {fg_data['classification']}</b>\n"
                           f"🌍 Market: <b>{market_signal}</b>\n\n" + "\n".join(lines)
                           + "\n\n🤖 Scutua-MCP Agentic Layer")
                result["telegram"] = await _send_telegram(message)

            return result
        except Exception as e:
            return {"error": f"Signal generation failed: {str(e)}"}
