"""
Curve Finance Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ✅ แก้ URL จาก curve.fi → curve.finance
BASE_URL = "https://api.curve.finance/api"


async def _curve_get(endpoint: str) -> dict:
    cache_key = f"curve:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=10,
        ) as client:
            r = await client.get(f"{BASE_URL}{endpoint}")
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"Curve error: {e}")
        return {"error": str(e)}


def register_curve_tools(app):

    @app.tool()
    async def get_curve_pools() -> dict:
        """Get top Curve Finance liquidity pools with APY"""
        data = await _curve_get("/getPools/ethereum/main")
        if "error" in data:
            return data
        pools = data.get("data", {}).get("poolData", [])
        top = [
            {
                "name": p.get("name"),
                "tvl": p.get("usdTotal"),
                "apy": p.get("latestDailyApy"),
            }
            for p in pools[:10]
        ]
        return {"pools": top, "protocol": "curve"}

    @app.tool()
    async def get_curve_pool_detail(pool_address: str) -> dict:
        """Get detailed info for a specific Curve pool"""
        data = await _curve_get("/getPools/ethereum/main")
        if "error" in data:
            return data
        pools = data.get("data", {}).get("poolData", [])
        pool = next(
            (p for p in pools if p.get("address", "").lower() == pool_address.lower()),
            None,
        )
        return pool or {"error": "Pool not found"}

    @app.tool()
    async def get_curve_tvl() -> dict:
        """Get total TVL across all Curve pools"""
        data = await _curve_get("/getPools/ethereum/main")
        if "error" in data:
            return data

        pools = data.get("data", {}).get("poolData", [])
        total_tvl = sum(p.get("usdTotal", 0) for p in pools)

        return {
            "tvl": round(total_tvl, 2),
            "pool_count": len(pools),
            "protocol": "curve"
        }
