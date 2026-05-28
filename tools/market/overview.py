"""
Market Overview Tools — Scutua-MCP
Combines CoinGecko global + Alternative.me Fear & Greed
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
CG_BASE = "https://api.coingecko.com/api/v3"


async def _cg_get(endpoint: str) -> dict:
    """CoinGecko GET with API key + cache"""
    cache_key = f"cg_market:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        headers = {}
        if COINGECKO_API_KEY:
            headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{CG_BASE}{endpoint}",
                headers=headers,
                timeout=10
            )
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"CoinGecko market_overview error: {e}")
        return {"error": str(e)}


def register_market_overview_tools(app):

    @app.tool()
    async def get_market_overview() -> str:
        """Get global crypto market overview — total market cap, volume, dominance"""
        data = await _cg_get("/global")
        if "error" in data:
            return f"❌ Market overview error: {data['error']}"

        m = data.get("data", {})
        if not m:
            return "❌ No market data returned"

        total_mcap = m.get("total_market_cap", {}).get("usd", 0) or 0
        total_vol   = m.get("total_volume", {}).get("usd", 0) or 0
        change_24h  = m.get("market_cap_change_percentage_24h_usd", 0) or 0
        btc_dom     = m.get("market_cap_percentage", {}).get("btc", 0) or 0
        eth_dom     = m.get("market_cap_percentage", {}).get("eth", 0) or 0
        active_coins = m.get("active_cryptocurrencies", 0)
        markets      = m.get("markets", 0)

        arrow = "📈" if change_24h >= 0 else "📉"
        sign  = "+" if change_24h >= 0 else ""

        return (
            f"🌍 Crypto Market Overview\n"
            f"{'─'*32}\n"
            f"💰 Total Market Cap:  ${total_mcap/1e12:.2f}T\n"
            f"📊 24h Volume:        ${total_vol/1e9:.1f}B\n"
            f"{arrow} 24h Change:        {sign}{change_24h:.2f}%\n"
            f"₿  BTC Dominance:     {btc_dom:.1f}%\n"
            f"Ξ  ETH Dominance:     {eth_dom:.1f}%\n"
            f"🪙 Active Coins:      {active_coins:,}\n"
            f"🏦 Exchanges:         {markets:,}"
        )

    @app.tool()
    async def get_market_sentiment() -> str:
        """Get overall crypto market sentiment — combines Fear & Greed + market cap change"""
        # CoinGecko global
        cg_data = await _cg_get("/global")
        change_24h = 0.0
        if "error" not in cg_data:
            change_24h = cg_data.get("data", {}).get(
                "market_cap_change_percentage_24h_usd", 0
            ) or 0

        # Alternative.me Fear & Greed
        fg_value = None
        fg_label = "Unknown"
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.alternative.me/fng/?limit=1", timeout=10
                )
                fg = r.json()
                item = fg.get("data", [{}])[0]
                fg_value = int(item.get("value", 0))
                fg_label = item.get("value_classification", "Unknown")
        except Exception as e:
            logger.warning(f"Fear & Greed fetch failed: {e}")

        # Sentiment score
        if fg_value is not None:
            if fg_value >= 75:
                mood = "🟢 Extreme Greed"
            elif fg_value >= 55:
                mood = "🟡 Greed"
            elif fg_value >= 45:
                mood = "⚪ Neutral"
            elif fg_value >= 25:
                mood = "🟠 Fear"
            else:
                mood = "🔴 Extreme Fear"
        else:
            mood = "❓ Unknown"

        arrow = "📈" if change_24h >= 0 else "📉"
        sign  = "+" if change_24h >= 0 else ""

        return (
            f"🧠 Market Sentiment\n"
            f"{'─'*28}\n"
            f"😱 Fear & Greed:   {fg_value}/100 — {fg_label}\n"
            f"   Mood:           {mood}\n"
            f"{arrow} Market Cap 24h:  {sign}{change_24h:.2f}%\n"
        )
