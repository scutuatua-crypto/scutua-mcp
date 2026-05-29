import os
import json
from src.utils.logger import get_logger

logger = get_logger(__name__)

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

FALLBACK_STATS = {"smithery_score": 84, "tools": 152, "repos": 80}


def load_ecosystem() -> dict:
    try:
        with open(ECOSYSTEM_DATA) as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"ecosystem.json load failed: {e} — using fallback")
        return {"stats": FALLBACK_STATS}


async def ecosystem_intelligence() -> dict:
    """🧠 Cross-project analysis + insights"""
    try:
        data = load_ecosystem()
        stats = data.get("stats", FALLBACK_STATS)

        insights = []
        if stats.get("smithery_score", 100) < 90:
            insights.append({
                "type": "improvement", "priority": "high",
                "insight": f"Smithery score is {stats.get('smithery_score', '?')}/100 — add configSchema to reach 90+"
            })
        insights.append({
            "type": "growth", "priority": "medium",
            "insight": f"{stats.get('tools', '?')} tools across 7 dimensions — Dimension 8 Ecosystem layer will make it self-aware"
        })
        insights.append({
            "type": "expansion", "priority": "medium",
            "insight": "11 chains supported — consider adding Sui and Aptos for Move ecosystem coverage"
        })

        return {
            "ecosystem_iq": "🧠 HIGH",
            "total_insights": len(insights),
            "insights": insights,
            "recommendation": "You're building what no one else is building. Keep going. 🛸"
        }
    except Exception as e:
        logger.error(f"intelligence error: {e}")
        return {"error": str(e), "ecosystem_iq": "❌ ERROR", "insights": []}


async def what_should_i_build() -> dict:
    """🚀 AI-powered next move advisor"""
    try:
        return {
            "next_moves": [
                {"priority": 1, "action": "Complete Dimension 8 — Ecosystem Consciousness",
                 "why": "Makes Scutua-MCP truly self-aware and self-describing",
                 "effort": "Low — structure already designed"},
                {"priority": 2, "action": "Add configSchema to MCP server",
                 "why": "Push Smithery score from 84 → 90+", "effort": "Low"},
                {"priority": 3, "action": "Connect Command Hub to ecosystem.json",
                 "why": "Single source of truth — update once, reflect everywhere",
                 "effort": "Medium"},
            ],
            "motto": "Too fast for the API, too safe for the chain. 🚚💿"
        }
    except Exception as e:
        logger.error(f"what_should_i_build error: {e}")
        return {"error": str(e), "next_moves": []}
