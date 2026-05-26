import httpx
import json
import os
from datetime import datetime

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

def load_ecosystem():
    with open(ECOSYSTEM_DATA) as f:
        return json.load(f)

async def ecosystem_heartbeat() -> dict:
    """🫀 Scutua Nervous System — ecosystem pulse"""
    data = load_ecosystem()
    
    live = [p for p in data["projects"] if p["status"] == "live"]
    
    return {
        "status": "🟢 ALIVE",
        "timestamp": datetime.utcnow().isoformat(),
        "ecosystem": data["name"],
        "version": data["version"],
        "tagline": data["tagline"],
        "built_by": data["built_by"],
        "deployed_from": data["deployed_from"],
        "stats": data["stats"],
        "projects_live": len(live),
        "chains": data["chains_supported"],
        "pulse": "💓 Beating"
    }
