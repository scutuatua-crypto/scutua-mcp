import json
import os

ECOSYSTEM_DATA = os.path.join(os.path.dirname(__file__), "data/ecosystem.json")

def load_ecosystem():
    with open(ECOSYSTEM_DATA) as f:
        return json.load(f)

async def ecosystem_intelligence() -> dict:
    """🧠 Cross-project analysis + what to build next"""
    data = load_ecosystem()
    stats = data["stats"]
    
    insights = []
    
    if stats["smithery_score"] < 90:
        insights.append({
            "type": "improvement",
            "priority": "high",
            "insight": f"Smithery score is {stats['smithery_score']}/100 — add configSchema to reach 90+"
        })
    
    insights.append({
        "type": "growth",
        "priority": "medium", 
        "insight": f"152 tools across 7 dimensions — Dimension 8 Ecosystem layer will make it self-aware"
    })
    
    insights.append({
        "type": "expansion",
        "priority": "medium",
        "insight": "11 chains supported — consider adding Sui and Aptos for Move ecosystem coverage"
    })

    return {
        "ecosystem_iq": "🧠 HIGH",
        "total_insights": len(insights),
        "insights": insights,
        "recommendation": "You're building what no one else is building. Keep going. 🛸"
    }

async def what_should_i_build() -> dict:
    """🚀 AI-powered next move advisor"""
    data = load_ecosystem()
    
    return {
        "next_moves": [
            {
                "priority": 1,
                "action": "Complete Dimension 8 — Ecosystem Consciousness",
                "why": "Makes Scutua-MCP truly self-aware and self-describing",
                "effort": "Low — structure already designed"
            },
            {
                "priority": 2,
                "action": "Add configSchema to MCP server",
                "why": "Push Smithery score from 84 → 90+",
                "effort": "Low"
            },
            {
                "priority": 3,
                "action": "Connect Command Hub to ecosystem.json",
                "why": "Single source of truth — update once, reflect everywhere",
                "effort": "Medium"
            }
        ],
        "motto": "Too fast for the API, too safe for the chain. 🚚💿"
    }
