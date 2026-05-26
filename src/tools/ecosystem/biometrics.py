import httpx
import json
import os

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

def load_ecosystem():
    with open(ECOSYSTEM_DATA) as f:
        return json.load(f)

async def project_biometrics(project_id: str = None) -> dict:
    """🧬 Health check for all or specific project"""
    data = load_ecosystem()
    projects = data["projects"]
    
    if project_id:
        projects = [p for p in projects if p["id"] == project_id]
        if not projects:
            return {"error": f"Project '{project_id}' not found"}
    
    results = []
    for p in projects:
        health = {
            "id": p["id"],
            "name": p["name"],
            "status": p["status"],
            "tier": f"Tier {p['tier']}",
            "dimension": p["dimension"],
            "url": p["url"],
            "health": "✅ Healthy" if p["status"] == "live" else "⚠️ Offline"
        }
        results.append(health)
    
    return {
        "biometrics": results,
        "total": len(results),
        "healthy": len([r for r in results if "Healthy" in r["health"]])
    }
