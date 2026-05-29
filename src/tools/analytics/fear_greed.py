import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

FEAR_GREED_URL = "https://api.alternative.me/fng/"


def _classify(value: int) -> str:
    if value >= 75: return "🟢 Extreme Greed"
    if value >= 55: return "🟡 Greed"
    if value >= 45: return "⚪ Neutral"
    if value >= 25: return "🟠 Fear"
    return "🔴 Extreme Fear"


def register_fear_greed_tools(app: FastMCP):
    @app.tool()
    async def get_fear_greed_info(query: str = "now") -> str:
        """Get Crypto Fear & Greed Index (now/week/month)"""
        try:
            limit = 30 if query == "month" else 7 if query == "week" else 1

            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(FEAR_GREED_URL, params={"limit": limit})
                r.raise_for_status()
                data = r.json()

            entries = data.get("data", [])
            if not entries:
                return "❌ No Fear & Greed data available"

            if limit == 1:
                entry = entries[0]
                value = int(entry.get("value", 0))
                label = entry.get("value_classification", _classify(value))
                ts    = entry.get("timestamp", "")
                return (f"😨 Crypto Fear & Greed Index\n\n"
                        f"Score: {value}/100\n"
                        f"Status: {_classify(value)}\n"
                        f"Label: {label}\n"
                        f"Updated: {ts}")
            else:
                title = "7-Day" if limit == 7 else "30-Day"
                lines = [f"😨 Fear & Greed — {title} History\n"]
                lines.append(f"{'Date':<12} {'Score':>6} {'Status'}") 
                lines.append("─" * 36)
                for e in entries:
                    value = int(e.get("value", 0))
                    ts    = e.get("timestamp", "")[:10] if e.get("timestamp") else "?"
                    lines.append(f"{ts:<12} {value:>6}   {_classify(value)}")
                avg = sum(int(e.get("value", 0)) for e in entries) / len(entries)
                lines.append(f"\n📊 Average: {avg:.1f} — {_classify(int(avg))}")
                return "\n".join(lines)

        except Exception as e:
            logger.error(f"fear_greed error: {e}")
            return f"❌ Error: {e}"
