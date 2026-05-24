import httpx
from mcp.server.fastmcp import FastMCP

def register_arbitrage_tools(app: FastMCP):
    @app.tool()
    async def get_arbitrage_opportunities(token: str) -> str:
        """Find price differences across exchanges"""
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{token.lower()}/tickers"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            tickers = data.get("tickers", [])[:10]
            prices = [(t.get("market", {}).get("name", "?"), t.get("last", 0)) for t in tickers if t.get("last", 0) > 0]
            if not prices:
                return f"No data for {token}"
            prices.sort(key=lambda x: x[1])
            low_ex, low_price = prices[0]
            high_ex, high_price = prices[-1]
            diff = ((high_price - low_price) / low_price) * 100
            return f"""⚡ Arbitrage: {token.upper()}
Lowest: {low_ex} @ ${low_price:,.4f}
Highest: {high_ex} @ ${high_price:,.4f}
Spread: {diff:.2f}%"""
        except Exception as e:
            return f"Error: {e}"
