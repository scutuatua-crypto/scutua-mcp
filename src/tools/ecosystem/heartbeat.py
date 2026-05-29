import os
import json
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

FALLBACK = {
    "name": "Scutua + WhaleTrucker Ecosystem",
    "version": "3.3.1",
    "tagline": "no money · no cry · just build",
    "built_by": "scutuatua-crypto",
    "deployed_from": "iPad. No PC required. 😤",
    "stats": {"repos": 80, "tools": 152, "platforms_live": 4,
               "chains": 11, "ci_cd_runs": 1300, "smithery_score": 84},
    "projects": [],
    "chains_supported": ["Solana","Ethereum","Arbitrum","Optimism",
                         "BNB","Reef","TON","Polkadot","Cosmos","Base","CrossChain"]
}


def load_ecosystem() -> dict:
    try:
        with open(ECOSYSTEM_DATA) as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"ecosystem.json load failed: {e} — using fallback")
        return FALLBACK


async def ecosystem_heartbeat() -> dict:
    """🫀 Scutua Nervous System — ecosystem pulse"""
    try:
        data = load_ecosystem()
        live = [p for p in data.get("projects", []) if p.get("status") == "live"]
        return {
            "status": "🟢 ALIVE",
            "timestamp": datetime.utcnow().isoformat(),
            "ecosystem": data.get("name", "Scutua"),
            "version": data.get("version", "?"),
            "tagline": data.get("tagline", ""),
            "built_by": data.get("built_by", ""),
            "deployed_from": data.get("deployed_from", ""),
            "stats": data.get("stats", {}),
            "projects_live": len(live),
            "chains": data.get("chains_supported", []),
            "pulse": "💓 Beating"
        }
    except Exception as e:
        logger.error(f"heartbeat error: {e}")
        return {"status": "🔴 ERROR", "error": str(e), "pulse": "💔 Flatline"}
