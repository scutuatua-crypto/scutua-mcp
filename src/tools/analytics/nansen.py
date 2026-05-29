"""
Nansen Analytics Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")

def register_nansen_tools(app):

    @app.tool()
    async def get_smart_money_flows() -> dict:
        """Get smart money wallet flows from Dune Analytics"""
        cache_key = "dune:smart_money_flows"
        cached = get_cached(cache_key)
        if cached:
            return cached
        if not DUNE_API_KEY:
            return {"error": "DUNE_API_KEY not configured"}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.dune.com/api/v1/query/7607813/results",
                    headers={"x-dune-api-key": DUNE_API_KEY},
                    timeout=15
                )
                r.raise_for_status()
                data = r.json()
                set_cached(cache_key, data, ttl=300)
                return data
        except Exception as e:
            logger.error(f"Smart money flows error: {e}")
            return {"error": str(e)}

    @app.tool()
    async def get_nansen_token_god_mode(token_address: str) -> dict:
        """Get token holder analytics via Dune Analytics"""
        if not DUNE_API_KEY:
            return {"error": "DUNE_API_KEY not configured"}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"https://api.dune.com/api/v1/query/7607813/results",
                    headers={"x-dune-api-key": DUNE_API_KEY},
                    timeout=15
                )
                r.raise_for_status()
                return r.json()
        except Exception as e:
            return {"error": str(e)}

    @app.tool()
    async def get_wallet_label(address: str) -> dict:
        """Get wallet label/entity via Dune Analytics"""
        return {"address": address, "label": "unknown", "note": "Nansen disabled"}
