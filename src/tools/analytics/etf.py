import os
import httpx
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")


def register_etf_tools(app: FastMCP):
    @app.tool()
    async def get_etf_info(query: str = "bitcoin") -> str:
        """Get Bitcoin/Ethereum ETF price and market data"""
        try:
            headers = {"accept": "application/json"}
            if COINGECKO_API_KEY:
                headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

            # Map query to coin id
            coin_map = {
                "bitcoin": "bitcoin",
                "btc":     "bitcoin",
                "ethereum": "ethereum",
                "eth":     "ethereum",
            }
            coin_id = coin_map.get(query.lower(), "bitcoin")

            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"https://api.coingecko.com/api/v3/coins/{coin_id}",
                    headers=headers,
                    params={
                        "localization": "false",
                        "tickers": "false",
                        "community_data": "false",
                        "developer_data": "false",
                    },
                    timeout=10,
                )
                if r.status_code == 429:
                    return "Rate limit — retry later"
                r.raise_for_status()
                data = r.json()

            market = data.get("market_data", {})
            price       = market.get("current_price", {}).get("usd", 0)
            change_24h  = market.get("price_change_percentage_24h", 0) or 0
            change_7d   = market.get("price_change_percentage_7d", 0) or 0
            change_30d  = market.get("price_change_percentage_30d", 0) or 0
            mcap        = market.get("market_cap", {}).get("usd", 0)
            vol         = market.get("total_volume", {}).get("usd", 0)
            ath         = market.get("ath", {}).get("usd", 0)
            ath_change  = market.get("ath_change_percentage", {}).get("usd", 0) or 0

            emoji = "🟢" if change_24h >= 0 else "🔴"

            return f"""📊 ETF Tracker — {coin_id.upper()}

{emoji} Price:      ${price:,.2f}
📈 24h:        {change_24h:+.2f}%
📅 7d:         {change_7d:+.2f}%
🗓️ 30d:        {change_30d:+.2f}%
💰 Market Cap: ${mcap:,.0f}
📦 Volume 24h: ${vol:,.0f}
🏆 ATH:        ${ath:,.2f} ({ath_change:+.2f}% from ATH)"""

        except Exception as e:
            return f"Error: {str(e)}"
