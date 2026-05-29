"""
Smart Money Analytics — Dune Analytics (replaces Nansen)
src/tools/analytics/nansen.py
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")
DUNE_BASE = "https://api.dune.com/api/v1"

# Dune query IDs — public queries for smart money tracking
QUERY_SMART_MONEY_FLOWS = 2450792   # Smart money wallet flows (ETH)
QUERY_WALLET_LABEL      = 3385009   # Wallet label / entity lookup
QUERY_TOKEN_GOD_MODE    = 2396071   # Token holder analytics


async def _dune_get(query_id: int, params: dict = None) -> dict:
    """Execute a Dune query and return latest results."""
    if not DUNE_API_KEY:
        return {"error": "DUNE_API_KEY not configured"}

    cache_key = f"dune:{query_id}:{params}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    try:
        headers = {"X-DUNE-API-KEY": DUNE_API_KEY}

        # Execute query
        async with httpx.AsyncClient(timeout=30) as client:
            # Get latest results directly (faster than re-executing)
            url = f"{DUNE_BASE}/query/{query_id}/results"
            r = await client.get(url, headers=headers, params={"limit": 20})
            r.raise_for_status()
            data = r.json()

        rows = data.get("result", {}).get("rows", [])
        set_cached(cache_key, rows, ttl=180)
        return rows

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return {"error": "Invalid DUNE_API_KEY"}
        return {"error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Dune error: {e}")
        return {"error": str(e)}


def register_nansen_tools(app):

    @app.tool()
    async def get_smart_money_flows() -> dict:
        """Get smart money wallet flows from Dune Analytics"""
        rows = await _dune_get(QUERY_SMART_MONEY_FLOWS)
        if isinstance(rows, dict) and "error" in rows:
            return rows

        if not rows:
            return {"message": "No smart money flow data available"}

        result = []
        for r in rows[:10]:
            result.append({
                "wallet":    r.get("address", r.get("wallet", "unknown")),
                "label":     r.get("label", r.get("entity", "Smart Money")),
                "inflow_usd":  r.get("inflow_usd", r.get("amount_in_usd", 0)),
                "outflow_usd": r.get("outflow_usd", r.get("amount_out_usd", 0)),
                "net_flow":    r.get("net_flow_usd", 0),
                "chain":       r.get("blockchain", "ethereum"),
            })

        return {
            "source": "Dune Analytics",
            "smart_money_flows": result,
            "count": len(result),
        }

    @app.tool()
    async def get_nansen_token_god_mode(token_address: str) -> dict:
        """Get token holder analytics via Dune Analytics"""
        rows = await _dune_get(QUERY_TOKEN_GOD_MODE, {"token": token_address})
        if isinstance(rows, dict) and "error" in rows:
            return rows

        if not rows:
            return {"message": f"No data found for token {token_address}"}

        return {
            "source": "Dune Analytics",
            "token": token_address,
            "holders": rows[:20],
        }

    @app.tool()
    async def get_wallet_label(address: str) -> dict:
        """Get wallet label/entity via Dune Analytics"""
        rows = await _dune_get(QUERY_WALLET_LABEL, {"address": address})
        if isinstance(rows, dict) and "error" in rows:
            return rows

        if not rows:
            return {
                "address": address,
                "label":   "Unknown",
                "source":  "Dune Analytics",
            }

        row = rows[0]
        return {
            "address": address,
            "label":   row.get("label", row.get("entity", "Unknown")),
            "type":    row.get("type", row.get("category", "wallet")),
            "source":  "Dune Analytics",
        }
