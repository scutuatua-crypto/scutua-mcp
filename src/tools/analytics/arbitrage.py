import os
import time
import httpx
from mcp.server.fastmcp import FastMCP

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

_cache: dict = {}
CACHE_TTL = 300


def _get_cache(key: str):
    if key in _cache:
        value, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return value
    return None


def _set_cache(key: str, value):
    _cache[key] = (value, time.time())


def register_arbitrage_tools(app: FastMCP):
    @app.tool()
    async def get_arbitrage_opportunities(token: str) -> str:
        """Find price differences across exchanges"""
        cache_key = f"arb_{token.lower()}"
        cached = _get_cache(cache_key)
        if cached:
            return cached

        try:
            url = f"https://api.coingecko.com/api/v3/coins/{token.lower()}/tickers"
            headers = {}
            if COINGECKO_API_KEY:
                headers["x-cg-pro-api-key"] = COINGECKO_API_KEY

            async with httpx.AsyncClient() as client:
                r = await client.get(url, headers=headers, timeout=10)

                if r.status_code == 429:
                    stale = _cache.get(cache_key)
                    if stale:
                        return stale[0]
                    return f"Rate limit — retry in a moment"

                r.raise_for_status()
                data = r.json()

            tickers = data.get("tickers", [])[:10]
            prices = [
                (t.get("market", {}).get("name", "?"), t.get("last", 0))
                for t in tickers if t.get("last", 0) > 0
            ]

            if not prices:
                return f"No data for {token}"

            prices.sort(key=lambda x: x[1])
            low_ex,  low_price  = prices[0]
            high_ex, high_price = prices[-1]
            diff = ((high_price - low_price) / low_price) * 100

            result = f"""⚡ Arbitrage: {token.upper()}
Lowest:  {low_ex} @ ${low_price:,.4f}
Highest: {high_ex} @ ${high_price:,.4f}
Spread:  {diff:.2f}%"""

            _set_cache(cache_key, result)
            return result

        except Exception as e:
            return f"Error: {e}"
