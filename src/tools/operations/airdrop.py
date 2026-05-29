import os
import httpx
import asyncio
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")


def register_airdrop_tools(app: FastMCP):
    @app.tool()
    async def get_airdrop_info(query: str = "latest") -> str:
        """Get crypto airdrop info — trending and new token launches"""
        try:
            headers = {"accept": "application/json"}
            if COINGECKO_API_KEY:
                headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

            async with httpx.AsyncClient() as client:
                # ดึง trending coins — มักเป็น new launch / airdrop hype
                r = await client.get(
                    "https://api.coingecko.com/api/v3/search/trending",
                    headers=headers,
                    timeout=10,
                )
                if r.status_code == 429:
                    return "Rate limit — retry later"
                r.raise_for_status()
                data = r.json()

            coins = data.get("coins", [])
            if not coins:
                return "No trending data available"

            lines = ["🪂 Trending Coins — Potential Airdrops & New Launches\n"]

            for item in coins[:10]:
                coin   = item.get("item", {})
                name   = coin.get("name", "?")
                symbol = coin.get("symbol", "?").upper()
                rank   = coin.get("market_cap_rank", "N/A")
                score  = coin.get("score", 0)
                price  = coin.get("data", {}).get("price", "N/A")
                change = coin.get("data", {}).get("price_change_percentage_24h", {}).get("usd", 0) or 0

                emoji = "🟢" if change >= 0 else "🔴"
                lines.append(
                    f"{emoji} {name} ({symbol}) | Rank: {rank} | "
                    f"Price: {price} | 24h: {change:+.2f}%"
                )

            lines.append("\n💡 Check each project for official airdrop announcements")
            return "\n".join(lines)

        except Exception as e:
            return f"Error: {str(e)}"
