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
    "projects": []
}


def load_ecosystem() -> dict:
    try:
        with open(ECOSYSTEM_DATA) as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"ecosystem.json load failed: {e} — using fallback")
        return FALLBACK


async def ecosystem_narrative() -> dict:
    """📖 Auto-generate today's ecosystem story"""
    try:
        data = load_ecosystem()
        today = datetime.utcnow().strftime("%B %d, %Y")
        stats = data.get("stats", FALLBACK["stats"])
        projects = data.get("projects", [])

        project_lines = "\n".join(
            [f"  → {p.get('name','?')}: {p.get('description','')}" for p in projects]
        ) or "  → Scutua-MCP: World's first Agentic DeFi MCP"

        story = f"""
🐋 SCUTUA + WHALETRUCKER ECOSYSTEM — {today}

Built by one person. From an iPad. Zero budget. Maximum impact.

Today the ecosystem stands at:
• {stats.get('repos','?')}+ repositories
• {stats.get('tools','?')} MCP tools across 7 dimensions
• {stats.get('platforms_live','?')}+ live platforms
• {stats.get('chains','?')} blockchains supported
• {stats.get('ci_cd_runs','?')}+ CI/CD pipeline runs
• Smithery Quality Score: {stats.get('smithery_score','?')}/100

Active Projects:
{project_lines}

{data.get('tagline', 'no money · no cry · just build')}
{data.get('deployed_from', 'iPad. No PC required. 😤')}
        """.strip()

        return {
            "date": today,
            "narrative": story,
            "author": data.get("built_by", "scutuatua-crypto"),
            "universe": "Scutua + WhaleTrucker 🌌"
        }
    except Exception as e:
        logger.error(f"narrative error: {e}")
        return {"error": str(e), "narrative": "❌ Narrative generation failed", "date": ""}
