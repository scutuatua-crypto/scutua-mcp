import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_analytics_tools(app: FastMCP):
    @app.tool()
    async def get_market_overview() -> str:
        """Get crypto market overview"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get("https://api.coingecko.com/api/v3/global")
                r.raise_for_status()
                data = r.json().get("data", {})
            if not data:
                return "❌ No market data available"
            mcap   = data.get("total_market_cap", {}).get("usd", 0) or 0
            volume = data.get("total_volume", {}).get("usd", 0) or 0
            btc_dom = data.get("market_cap_percentage", {}).get("btc", 0) or 0
            eth_dom = data.get("market_cap_percentage", {}).get("eth", 0) or 0
            change  = data.get("market_cap_change_percentage_24h_usd", 0) or 0
            return (f"🌍 Crypto Market Overview:\n"
                    f"Total Market Cap: ${mcap/1e12:.2f}T\n"
                    f"24h Volume: ${volume/1e9:.1f}B\n"
                    f"24h Change: {change:+.2f}%\n"
                    f"BTC Dominance: {btc_dom:.1f}%\n"
                    f"ETH Dominance: {eth_dom:.1f}%")
        except Exception as e:
            logger.error(f"market_overview error: {e}")
            return f"❌ Error: {e}"

    @app.tool()
    async def get_trending_coins() -> str:
        """Get trending coins on CoinGecko"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get("https://api.coingecko.com/api/v3/search/trending")
                r.raise_for_status()
                data = r.json()

            # 🔧 FIX: defensive parse — CoinGecko response format อาจเปลี่ยน
            raw_coins = data.get("coins", [])
            if not isinstance(raw_coins, list) or not raw_coins:
                return "❌ No trending data available"

            result = ["🔥 Trending Coins:"]
            for i, c in enumerate(raw_coins[:5], 1):
                # รองรับทั้ง format เก่า {"item": {...}} และ format ใหม่
                item = c.get("item", c) if isinstance(c, dict) else {}
                name   = item.get("name") or item.get("id") or "Unknown"
                symbol = item.get("symbol", "?")
                rank   = item.get("market_cap_rank") or item.get("rank", "N/A")
                score  = item.get("score", "")
                score_str = f" · Score #{int(score)+1}" if isinstance(score, (int, float)) else ""
                result.append(f"{i}. {name} ({symbol}) — Rank #{rank}{score_str}")

            return "\n".join(result)
        except Exception as e:
            logger.error(f"trending_coins error: {e}")
            return f"❌ Error: {e}"
