"""
DeFiLlama Analytics Tools — Scutua-MCP
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.llama.fi"

async def _llama_get(endpoint: str) -> dict:
    cache_key = f"defilama:{endpoint}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE_URL}{endpoint}", timeout=10)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=120)
            return data
    except Exception as e:
        logger.error(f"DeFiLlama error: {e}")
        return {"error": str(e)}

def register_defilama_tools(app):

    @app.tool()
    async def get_protocol_tvl(protocol: str) -> dict:
        """Get TVL history for a DeFi protocol from DeFiLlama"""
        return await _llama_get(f"/protocol/{protocol}")

    @app.tool()
    async def get_top_protocols() -> dict:
        """Get top DeFi protocols by TVL"""
        data = await _llama_get("/protocols")
        if "error" in data:
            return data
        protocols = data[:20]
        return {"protocols": [{"name": p.get("name"), "tvl": p.get("tvl"), "chain": p.get("chain")} for p in protocols]}

    @app.tool()
    async def get_chain_tvl(chain: str) -> dict:
        """Get total TVL for a specific blockchain"""
        data = await _llama_get(f"/v2/historicalChainTvl/{chain}")
        if "error" in data:
            return data
        return {"chain": chain, "history": data[-30:]}

    @app.tool()
    async def get_yields() -> dict:
        """Get top yield farming opportunities from DeFiLlama"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get("https://yields.llama.fi/pools", timeout=10)
                r.raise_for_status()
                pools = r.json().get("data", [])
                top = sorted(pools, key=lambda x: x.get("apy", 0), reverse=True)[:20]
                return {"pools": top}
        except Exception as e:
            logger.error(f"DeFiLlama yields error: {e}")
            return {"error": str(e)}
