"""
📊 CoinMarketCap Feed — Scutua-MCP
Fallback to CoinGecko if CMC_API_KEY is not set
"""
import httpx
import os
from src.utils.security import mcp_safe_executor
from src.utils.cache import cache
from src.utils.logger import get_logger

logger = get_logger(__name__)

CMC_API_KEY = os.environ.get("CMC_API_KEY", "")
COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY", "")


def register_cmc_tools(app):
    @app.tool()
    @mcp_safe_executor("get_cmc_listings")
    async def get_cmc_listings(limit: int = 10) -> dict:
        """Get top crypto listings from CoinMarketCap (fallback: CoinGecko)"""

        cache_key = f"cmc_listings_{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # ✅ ถ้ามี CMC key → ใช้ CMC ปกติ
        if CMC_API_KEY:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
                    headers={"X-CMC_PRO_API_KEY": CMC_API_KEY},
                    params={"limit": limit, "convert": "USD"},
                    timeout=10,
                )
                data = r.json()
                cache.set(cache_key, data, ttl=120)
                return data

        # 🔄 Fallback → CoinGecko (ใช้ key ที่มีอยู่แล้ว)
        logger.warning("CMC_API_KEY not set — falling back to CoinGecko")
        async with httpx.AsyncClient() as client:
            headers = {}
            if COINGECKO_API_KEY:
                headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

            r = await client.get(
                "https://api.coingecko.com/api/v3/coins/markets",
                headers=headers,
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": limit,
                    "page": 1,
                    "sparkline": False,
                },
                timeout=10,
            )
            coins = r.json()

        # แปลง format ให้เหมือน CMC response
        result = {
            "status": {"error_code": 0, "error_message": None, "source": "coingecko_fallback"},
            "data": [
                {
                    "id": i + 1,
                    "name": c["name"],
                    "symbol": c["symbol"].upper(),
                    "slug": c["id"],
                    "quote": {
                        "USD": {
                            "price": c.get("current_price", 0),
                            "volume_24h": c.get("total_volume", 0),
                            "percent_change_24h": c.get("price_change_percentage_24h", 0),
                            "market_cap": c.get("market_cap", 0),
                        }
                    },
                }
                for i, c in enumerate(coins)
            ],
        }
        cache.set(cache_key, result, ttl=120)
        return result
