import os
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

FALLBACK_PROJECTS = [
    {"id": "scutua-mcp", "name": "Scutua-MCP", "status": "live", "tier": 1,
     "dimension": "core", "url": "https://scutua-mcp.onrender.com/mcp"},
    {"id": "assetflow", "name": "AssetFlow", "status": "live", "tier": 2,
     "dimension": "portfolio", "url": "https://assetflow-app-iota.vercel.app"},
    {"id": "command-hub", "name": "Scutua Command Hub", "status": "live", "tier": 1,
     "dimension": "hub", "url": "https://scutuatua-crypto.github.io"},
]


def load_ecosystem() -> dict:
    try:
        with open(ECOSYSTEM_DATA) as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"ecosystem.json load failed: {e} — using fallback")
        return {"projects": FALLBACK_PROJECTS}


async def project_biometrics(project_id: str = None) -> dict:
    """🧬 Health check for all or specific project"""
    try:
        data = load_ecosystem()
        projects = data.get("projects", [])

        if project_id:
            projects = [p for p in projects if p.get("id") == project_id]
            if not projects:
                return {"error": f"Project '{project_id}' not found"}

        results = []
        for p in projects:
            results.append({
                "id": p.get("id", "?"),
                "name": p.get("name", "?"),
                "status": p.get("status", "unknown"),
                "tier": f"Tier {p.get('tier', '?')}",
                "dimension": p.get("dimension", "?"),
                "url": p.get("url", ""),
                "health": "✅ Healthy" if p.get("status") == "live" else "⚠️ Offline"
            })

        return {
            "biometrics": results,
            "total": len(results),
            "healthy": len([r for r in results if "Healthy" in r["health"]])
        }
    except Exception as e:
        logger.error(f"biometrics error: {e}")
        return {"error": str(e), "biometrics": [], "total": 0, "healthy": 0}
