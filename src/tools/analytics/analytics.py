import httpx
from mcp.server.fastmcp import FastMCP

def register_analytics_tools(app: FastMCP):
    @app.tool()
    async def get_market_overview() -> str:
        """Get crypto market overview"""
        try:
            url = "https://api.coingecko.com/api/v3/global"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json().get("data", {})
            mcap = data.get("total_market_cap", {}).get("usd", 0)
            volume = data.get("total_volume", {}).get("usd", 0)
            btc_dom = data.get("market_cap_percentage", {}).get("btc", 0)
            eth_dom = data.get("market_cap_percentage", {}).get("eth", 0)
            change = data.get("market_cap_change_percentage_24h_usd", 0)
            return f"""🌍 Crypto Market Overview:
Total Market Cap: ${mcap/1e12:.2f}T
24h Volume: ${volume/1e9:.1f}B
24h Change: {change:+.2f}%
BTC Dominance: {btc_dom:.1f}%
ETH Dominance: {eth_dom:.1f}%"""
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_trending_coins() -> str:
        """Get trending coins on CoinGecko"""
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            coins = data.get("coins", [])[:5]
            result = ["🔥 Trending Coins:"]
            for i, c in enumerate(coins, 1):
                item = c.get("item", {})
                result.append(f"{i}. {item.get('name')} ({item.get('symbol')}) - Rank #{item.get('market_cap_rank', 'N/A')}")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
