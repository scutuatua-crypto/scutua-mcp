"""
Dune Analytics Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")
BASE_URL = "https://api.dune.com/api/v1"

def _headers() -> dict:
    return {"x-dune-api-key": DUNE_API_KEY}

def register_dune_tools(app):

    @app.tool()
    async def execute_dune_query(query_id: int) -> dict:
        """Execute a Dune Analytics query and return execution id"""
        if not DUNE_API_KEY:
            return {"error": "DUNE_API_KEY not configured"}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    f"{BASE_URL}/query/{query_id}/execute",
                    headers=_headers(),
                    timeout=10
                )
                r.raise_for_status()
                data = r.json()
                return {"execution_id": data.get("execution_id"), "query_id": query_id}
        except Exception as e:
            logger.error(f"Dune execute error: {e}")
            return {"error": str(e)}

    @app.tool()
    async def get_dune_results(execution_id: str) -> dict:
        """Get results from a Dune Analytics execution"""
        if not DUNE_API_KEY:
            return {"error": "DUNE_API_KEY not configured"}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{BASE_URL}/execution/{execution_id}/results",
                    headers=_headers(),
                    timeout=10
                )
                r.raise_for_status()
                return r.json()
        except Exception as e:
            logger.error(f"Dune results error: {e}")
            return {"error": str(e)}

    @app.tool()
    async def get_dune_latest_results(query_id: int) -> dict:
        """Get latest cached results from a Dune query"""
        if not DUNE_API_KEY:
            return {"error": "DUNE_API_KEY not configured"}
        cache_key = f"dune:latest:{query_id}"
        cached = get_cached(cache_key)
        if cached:
            return cached
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{BASE_URL}/query/{query_id}/results",
                    headers=_headers(),
                    timeout=10
                )
                r.raise_for_status()
                data = r.json()
                set_cached(cache_key, data, ttl=300)
                return data
        except Exception as e:
            logger.error(f"Dune latest error: {e}")
            return {"error": str(e)}
