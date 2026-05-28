"""
GMX Protocol Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ✅ endpoints ที่ยังใช้ได้
GMX_INFRA   = "https://arbitrum-api.gmxinfra.io"
GMX_INFRA2  = "https://arbitrum-api.gmxinfra2.io"


async def _gmx_get(url: str, cache_ttl: int = 60) -> dict:
    cache_key = f"gmx:{url}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=10,
        ) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=cache_ttl)
            return data
    except Exception as e:
        logger.error(f"GMX error [{url}]: {e}")
        return {"error": str(e)}


async def _gmx_get_with_fallback(path: str, cache_ttl: int = 60) -> dict:
    """ลอง primary ก่อน ถ้าไม่ได้ → fallback infra2"""
    data = await _gmx_get(f"{GMX_INFRA}{path}", cache_ttl)
    if "error" in data:
        logger.warning(f"GMX primary failed, trying fallback for {path}")
        data = await _gmx_get(f"{GMX_INFRA2}{path}", cache_ttl)
    return data


def register_gmx_tools(app):

    @app.tool()
    async def get_gmx_stats() -> dict:
        """Get GMX protocol stats — volume, fees, open interest"""
        # ✅ ใช้ tokens endpoint แทน stats.gmx.io ที่ตายแล้ว
        data = await _gmx_get_with_fallback("/tokens")
        if "error" in data:
            return data
        tokens = data if isinstance(data, list) else data.get("tokens", [])
        # สรุป stats จาก token data
        total_pool_usd = sum(
            float(t.get("poolAmount", 0)) * float(t.get("minPrice", 0)) / 1e30
            for t in tokens
            if isinstance(t, dict)
        )
        return {
            "protocol": "gmx",
            "source": "gmxinfra.io",
            "total_tokens": len(tokens),
            "estimated_pool_usd": round(total_pool_usd, 2),
            "note": "stats.gmx.io deprecated — using gmxinfra.io",
        }

    @app.tool()
    async def get_gmx_prices() -> dict:
        """Get GMX token prices for supported assets"""
        data = await _gmx_get_with_fallback("/prices/tickers")
        if "error" in data:
            return data
        tickers = data if isinstance(data, list) else []
        # เอาแค่ตัวสำคัญ
        symbols = {"BTC", "ETH", "SOL", "ARB", "LINK", "UNI"}
        filtered = [
            {
                "symbol": t.get("tokenSymbol"),
                "price": t.get("maxPrice"),
            }
            for t in tickers
            if isinstance(t, dict) and t.get("tokenSymbol") in symbols
        ]
        return {"prices": filtered, "protocol": "gmx"}

    @app.tool()
    async def get_gmx_pools() -> dict:
        """Get GMX V2 liquidity pools (GM pools)"""
        data = await _gmx_get_with_fallback("/markets")
        if "error" in data:
            return data
        markets = data if isinstance(data, list) else data.get("markets", [])
        top = [
            {
                "name": m.get("name"),
                "index_token": m.get("indexTokenSymbol"),
                "pool_value": m.get("poolValueMax"),
            }
            for m in markets[:10]
            if isinstance(m, dict)
        ]
        return {"pools": top, "protocol": "gmx"}
