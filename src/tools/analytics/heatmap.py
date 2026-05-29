import os
import httpx
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

CATEGORY_MAP = {
    "defi":   "decentralized-finance-defi",
    "layer1": "layer-1",
    "layer2": "layer-2",
    "nft":    "non-fungible-tokens-nft",
    "gaming": "gaming",
    "ai":     "artificial-intelligence",
    "meme":   "meme-token",
    "top":    None,  # top = no category filter
}


async def _fetch_heatmap(category: str = None) -> list:
    headers = {"accept": "application/json"}
    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "price_change_percentage": "24h",
        "sparkline": "false",
    }
    if category:
        params["category"] = category

    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            headers=headers,
            params=params,
            timeout=10,
        )
        if r.status_code == 429:
            return []
        r.raise_for_status()
        return r.json()


def register_heatmap_tools(app: FastMCP):
    @app.tool()
    async def get_heatmap_info(query: str = "top") -> str:
        """Get crypto market heatmap — top movers by category (defi/layer1/layer2/nft/gaming/ai/meme/top)"""
        try:
            category_id = CATEGORY_MAP.get(query.lower(), None)
            coins = await _fetch_heatmap(category_id)

            if not coins:
                return f"No heatmap data available for '{query}'"

            lines = [f"🌡️ Heatmap — {query.upper()} (24h change)\n"]
            for coin in coins[:15]:
                change = coin.get("price_change_percentage_24h") or 0
                price  = coin.get("current_price", 0)
                symbol = coin.get("symbol", "").upper()
                name   = coin.get("name", "")

                if change >= 5:
                    emoji = "🟢🟢"
                elif change >= 2:
                    emoji = "🟢"
                elif change >= 0:
                    emoji = "🟡"
                elif change >= -2:
                    emoji = "🟠"
                elif change >= -5:
                    emoji = "🔴"
                else:
                    emoji = "🔴🔴"

                lines.append(f"{emoji} {symbol} ({name}): {change:+.2f}% | ${price:,.4f}")

            return "\n".join(lines)

        except Exception as e:
            return f"Error: {str(e)}"
