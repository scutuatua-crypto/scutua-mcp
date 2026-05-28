"""
Compound Finance Tools — Scutua-MCP
✅ Migrated from API v2 (dead) → Compound V3 + DeFiLlama fallback
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# ✅ Compound V3 endpoints (api/v2 ตายแล้ว → 410 Gone)
COMPOUND_V3_API = "https://v3-api.compound.finance"
DEFILLAMA_API   = "https://yields.llama.fi"


async def _get(url: str, ttl: int = 120) -> dict:
    cache_key = f"compound:{url}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            set_cached(cache_key, data, ttl=ttl)
            return data
    except Exception as e:
        logger.error(f"Compound error [{url}]: {e}")
        return {"error": str(e)}


def register_compound_tools(app):

    @app.tool()
    async def get_compound_markets() -> dict:
        """Get Compound V3 markets with supply/borrow APY from DeFiLlama"""
        # ✅ ดึงจาก DeFiLlama yields — filter เฉพาะ compound
        data = await _get(f"{DEFILLAMA_API}/pools")
        if "error" in data:
            return data

        pools = data.get("data", [])
        compound_pools = [
            p for p in pools
            if "compound" in p.get("project", "").lower()
        ][:15]

        markets = [
            {
                "symbol":     p.get("symbol", "N/A"),
                "chain":      p.get("chain", "N/A"),
                "protocol":   p.get("project", "N/A"),
                "supply_apy": round(p.get("apyBase") or 0, 2),
                "reward_apy": round(p.get("apyReward") or 0, 2),
                "total_apy":  round(p.get("apy") or 0, 2),
                "tvl_usd":    round(p.get("tvlUsd") or 0, 0),
            }
            for p in compound_pools
        ]

        return {
            "markets":  markets,
            "count":    len(markets),
            "protocol": "compound-v3",
            "source":   "defillama",
        }

    @app.tool()
    async def get_compound_account(address: str) -> dict:
        """Get Compound V3 account positions via on-chain subgraph"""
        # ✅ ใช้ The Graph subgraph แทน API v2 ที่ตายแล้ว
        GRAPH_URL = (
            "https://api.thegraph.com/subgraphs/name/"
            "graphprotocol/compound-v3-mainnet"
        )
        query = """
        {
          account(id: "%s") {
            id
            health
            positions {
              balance
              asset { symbol }
              side
            }
          }
        }
        """ % address.lower()

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    GRAPH_URL,
                    json={"query": query},
                )
                r.raise_for_status()
                result = r.json()

            account = result.get("data", {}).get("account")
            if not account:
                return {
                    "address":  address,
                    "found":    False,
                    "message":  "Address not found in Compound V3",
                    "protocol": "compound-v3",
                }

            return {
                "address":   address,
                "health":    account.get("health"),
                "positions": account.get("positions", []),
                "protocol":  "compound-v3",
            }

        except Exception as e:
            logger.error(f"Compound account error: {e}")
            return {"error": str(e), "address": address}
