import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

CATEGORIES = {
    "defi":    "decentralized-finance-defi",
    "layer1":  "layer-1",
    "layer2":  "layer-2",
    "nft":     "non-fungible-tokens-nft",
    "gaming":  "gaming",
    "ai":      "artificial-intelligence",
    "meme":    "meme-token",
}


def register_heatmap_tools(app: FastMCP):
    @app.tool()
    async def get_heatmap_info(query: str = "top") -> str:
        """Get crypto market heatmap — top movers by category (defi/layer1/layer2/nft/gaming/ai/meme/top)"""
        try:
            query = query.lower().strip()
            category_id = CATEGORIES.get(query)

            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
                "price_change_percentage": "24h",
                "sparkline": "false",
            }
            if category_id:
                params["category"] = category_id

            async with httpx.AsyncClient(timeout=12) as client:
                r = await client.get(
                    "https://api.coingecko.com/api/v3/coins/markets",
                    params=params,
                )
                r.raise_for_status()
                coins = r.json()

            if not coins or not isinstance(coins, list):
                return f"❌ No heatmap data for '{query}'"

            label = query.upper() if query != "top" else "TOP 10"
            lines = [f"🌡️ Market Heatmap — {label}\n"]
            lines.append(f"{'#':<3} {'Symbol':<8} {'Price':>12} {'24h':>8} {'MCap':>12}")
            lines.append("─" * 46)

            for i, coin in enumerate(coins, 1):
                symbol = (coin.get("symbol") or "?").upper()
                price  = coin.get("current_price") or 0
                change = coin.get("price_change_percentage_24h") or 0
                mcap   = coin.get("market_cap") or 0
                emoji  = "🟢" if change >= 0 else "🔴"
                price_str = f"${price:,.4f}" if price < 1 else f"${price:,.2f}"
                mcap_str  = f"${mcap/1e9:.1f}B" if mcap >= 1e9 else f"${mcap/1e6:.0f}M"
                lines.append(f"{i:<3} {symbol:<8} {price_str:>12} {emoji}{change:>+6.1f}% {mcap_str:>10}")

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"heatmap error: {e}")
            return f"❌ Error: {e}"
