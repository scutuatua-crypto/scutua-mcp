import httpx
from mcp.server.fastmcp import FastMCP

def register_alert_tools(app: FastMCP):
    @app.tool()
    async def get_price_alert(token: str, threshold: float) -> str:
        """Check if token price is above or below threshold"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={token.lower()}&vs_currencies=usd"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            price = data.get(token.lower(), {}).get("usd", 0)
            if price == 0:
                return f"Token {token} not found"
            status = "🔴 BELOW" if price < threshold else "🟢 ABOVE"
            return f"{token.upper()} Price Alert:\nCurrent: ${price:,.2f}\nThreshold: ${threshold:,.2f}\nStatus: {status} threshold"
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_whale_alert(min_usd: float = 100000) -> str:
        """Get recent large crypto transactions"""
        try:
            return f"🐋 Whale Alert Monitor\nTracking transactions > ${min_usd:,.0f}\nConnect WHALE_API_KEY for live data"
        except Exception as e:
            return f"Error: {e}"
