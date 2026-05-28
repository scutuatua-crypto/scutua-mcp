"""
GMX Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

GMX_BASE = "https://arbitrum-api.gmxinfra.io"


async def _gmx_get(endpoint: str) -> dict:
    cache_key = f"gmx:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{GMX_BASE}{endpoint}")
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=60)
            return data
    except Exception as e:
        logger.error(f"GMX error: {e}")
        return {"error": str(e)}


def register_gmx_tools(app):

    @app.tool()
    async def get_gmx_stats() -> dict:
        """Get GMX protocol stats — volume, fees, open interest"""
        data = await _gmx_get("/markets/info")
        if "error" in data:
            return data

        markets = data.get("markets", [])
        total_oi_long = 0
        total_oi_short = 0
        total_liquidity = 0

        for m in markets:
            if not m.get("isListed"):
                continue
            # values are in 30-decimal fixed point
            oi_long = int(m.get("openInterestLong", 0)) / 1e30
            oi_short = int(m.get("openInterestShort", 0)) / 1e30
            liq_long = int(m.get("availableLiquidityLong", 0)) / 1e30
            liq_short = int(m.get("availableLiquidityShort", 0)) / 1e30
            total_oi_long += oi_long
            total_oi_short += oi_short
            total_liquidity += liq_long + liq_short

        return {
            "protocol": "gmx",
            "total_markets": len(markets),
            "open_interest_long_usd": round(total_oi_long, 2),
            "open_interest_short_usd": round(total_oi_short, 2),
            "total_available_liquidity_usd": round(total_liquidity, 2),
            "source": "arbitrum-api.gmxinfra.io",
        }

    @app.tool()
    async def get_gmx_pools() -> dict:
        """Get GMX V2 liquidity pools (GM pools)"""
        data = await _gmx_get("/markets/info")
        if "error" in data:
            return data

        markets = data.get("markets", [])
        pools = []
        for m in markets:
            if not m.get("isListed"):
                continue
            liq_long = int(m.get("availableLiquidityLong", 0)) / 1e30
            liq_short = int(m.get("availableLiquidityShort", 0)) / 1e30
            pools.append({
                "name": m.get("name"),
                "index_token": m.get("indexToken"),
                "pool_value_usd": round(liq_long + liq_short, 2),
            })

        pools.sort(key=lambda x: x["pool_value_usd"], reverse=True)

        return {"pools": pools[:10], "total_markets": len(markets), "protocol": "gmx"}

    @app.tool()
    async def get_gmx_prices() -> dict:
        """Get GMX token prices for supported assets"""
        data = await _gmx_get("/prices/tickers")
        if "error" in data:
            return data

        tickers = data if isinstance(data, list) else data.get("tickers", [])
        prices = []
        for t in tickers:
            symbol = t.get("tokenSymbol") or t.get("symbol", "")
            price_raw = t.get("minPrice") or t.get("maxPrice") or t.get("price", "0")
            prices.append({
                "symbol": symbol,
                "price": price_raw,
            })

        return {"prices": prices[:10], "protocol": "gmx"}
