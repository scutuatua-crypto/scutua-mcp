from datetime import datetime
import json
import os

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

def load_ecosystem():
    with open(ECOSYSTEM_DATA) as f:
        return json.load(f)

async def ecosystem_narrative() -> dict:
    """📖 Auto-generate today's ecosystem story"""
    data = load_ecosystem()
    today = datetime.utcnow().strftime("%B %d, %Y")
    
    story = f"""
🐋 SCUTUA + WHALETRUCKER ECOSYSTEM — {today}

Built by one person. From an iPad. Zero budget. Maximum impact.

Today the ecosystem stands at:
• {data['stats']['repos']}+ repositories
• {data['stats']['tools']} MCP tools across 7 dimensions  
• {data['stats']['platforms_live']}+ live platforms
• {data['stats']['chains']} blockchains supported
• {data['stats']['ci_cd_runs']}+ CI/CD pipeline runs
• Smithery Quality Score: {data['stats']['smithery_score']}/100

Active Projects:
{chr(10).join([f"  → {p['name']}: {p['description']}" for p in data['projects']])}

{data['tagline']}
{data['deployed_from']}
    """.strip()
    
    return {
        "date": today,
        "narrative": story,
        "author": data["built_by"],
        "universe": "Scutua + WhaleTrucker 🌌"
    }
