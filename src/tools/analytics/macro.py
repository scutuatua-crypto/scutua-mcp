import os
import httpx
import asyncio
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")


async def _fetch_global() -> dict:
    headers = {"accept": "application/json"}
    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.coingecko.com/api/v3/global",
            headers=headers,
            timeout=10,
        )
        if r.status_code == 429:
            return {}
        r.raise_for_status()
        return r.json().get("data", {})


async def _fetch_fear_greed() -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.alternative.me/fng/?limit=2",
            timeout=10,
        )
        r.raise_for_status()
        return r.json().get("data", [])


def register_macro_tools(app: FastMCP):
    @app.tool()
    async def get_macro_info(query: str = "overview") -> str:
        """Get crypto macro overview — market cap, dominance, fear & greed, volume"""
        try:
            global_data, fg_data = await asyncio.gather(
                _fetch_global(),
                _fetch_fear_greed(),
            )

            if not global_data:
                return "Rate limit — retry later"

            mcap        = global_data.get("total_market_cap", {}).get("usd", 0)
            vol         = global_data.get("total_volume", {}).get("usd", 0)
            mcap_change = global_data.get("market_cap_change_percentage_24h_usd", 0) or 0
            btc_dom     = global_data.get("market_cap_percentage", {}).get("btc", 0)
            eth_dom     = global_data.get("market_cap_percentage", {}).get("eth", 0)
            active      = global_data.get("active_cryptocurrencies", 0)

            # Fear & Greed
            fg_now  = fg_data[0] if fg_data else {}
            fg_prev = fg_data[1] if len(fg_data) > 1 else {}
            fg_val  = fg_now.get("value", "N/A")
            fg_cls  = fg_now.get("value_classification", "N/A")
            fg_prev_val = fg_prev.get("value", "N/A")

            mcap_emoji = "🟢" if mcap_change >= 0 else "🔴"

            return f"""🌍 Crypto Macro Overview

💰 Total Market Cap:  ${mcap:,.0f}
{mcap_emoji} 24h Change:       {mcap_change:+.2f}%
📦 24h Volume:        ${vol:,.0f}

📊 Dominance:
  ₿  BTC: {btc_dom:.1f}%
  Ξ  ETH: {eth_dom:.1f}%
  🔵 Others: {100 - btc_dom - eth_dom:.1f}%

😨 Fear & Greed:
  Now:      {fg_val}/100 — {fg_cls}
  Yesterday: {fg_prev_val}/100

🪙 Active Coins: {active:,}"""

        except Exception as e:
            return f"Error: {str(e)}"
