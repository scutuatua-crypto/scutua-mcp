import os
import httpx
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")


def register_exchange_rates_tools(app: FastMCP):
    @app.tool()
    async def get_exchange_rates(base: str = "usd") -> str:
        """Get crypto exchange rates vs fiat"""
        try:
            headers = {"accept": "application/json"}
            if COINGECKO_API_KEY:
                headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    headers=headers,
                    params={
                        "ids": "bitcoin,ethereum,solana,ripple,binancecoin",
                        "vs_currencies": "usd,eur,gbp,jpy,thb",
                        "include_24hr_change": "true",
                    },
                    timeout=10,
                )
                if r.status_code == 429:
                    return "Rate limit — retry later"
                r.raise_for_status()
                data = r.json()

            lines = ["💹 Crypto Exchange Rates\n"]
            name_map = {
                "bitcoin":     "BTC",
                "ethereum":    "ETH",
                "solana":      "SOL",
                "ripple":      "XRP",
                "binancecoin": "BNB",
            }

            for coin_id, symbol in name_map.items():
                if coin_id not in data:
                    continue
                d = data[coin_id]
                usd    = d.get("usd", 0)
                eur    = d.get("eur", 0)
                gbp    = d.get("gbp", 0)
                jpy    = d.get("jpy", 0)
                thb    = d.get("thb", 0)
                change = d.get("usd_24h_change", 0) or 0
                emoji  = "🟢" if change >= 0 else "🔴"

                lines.append(
                    f"{emoji} {symbol}: ${usd:,.2f} | €{eur:,.2f} | £{gbp:,.2f} | ¥{jpy:,.0f} | ฿{thb:,.2f} ({change:+.2f}%)"
                )

            return "\n".join(lines)

        except Exception as e:
            return f"Error: {str(e)}"
