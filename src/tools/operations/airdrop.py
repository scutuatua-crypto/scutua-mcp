import os
import httpx
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")


def register_airdrop_tools(app: FastMCP):
    @app.tool()
    async def get_airdrop_info(query: str = "latest") -> str:
        """Get crypto airdrop info — trending new coins and recently listed tokens"""
        try:
            headers = {"accept": "application/json"}
            if COINGECKO_API_KEY:
                headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

            async with httpx.AsyncClient() as client:
                # ดึง recently added coins — มักเป็น airdrop/new launch
                r = await client.get(
                    "https://api.coingecko.com/api/v3/coins/list/new",
                    headers=headers,
                    timeout=10,
                )
                if r.status_code == 429:
                    return "Rate limit — retry later"
                r.raise_for_status()
                coins = r.json()

            if not coins:
                return "No new listings found"

            lines = [f"🪂 Recently Listed Coins (potential airdrops)\n"]
            for coin in coins[:15]:
                name      = coin.get("name", "?")
                symbol    = coin.get("symbol", "?").upper()
                activated = coin.get("activated_at", "")

                # format date
                if activated:
                    from datetime import datetime, timezone
                    dt = datetime.fromtimestamp(activated, tz=timezone.utc)
                    date_str = dt.strftime("%Y-%m-%d")
                else:
                    date_str = "N/A"

                lines.append(f"🆕 {name} ({symbol}) — Listed: {date_str}")

            lines.append(f"\n💡 Tip: Check each project on CoinGecko or DeFiLlama for airdrop eligibility")
            return "\n".join(lines)

        except Exception as e:
            return f"Error: {str(e)}"
