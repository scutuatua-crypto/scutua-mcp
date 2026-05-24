"""💰 Valuation Tool — Honey Score & Total Assets"""

from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
from src.utils.formatters import format_usd

logger = get_logger(__name__)

def register_valuation_tools(app: FastMCP):

    @app.tool()
    async def calculate_honey_score(sol: float, dot: float, reef: float, stables: float) -> dict:
        """Calculate WhaleTrucker Honey Score"""
        try:
            total = (sol * 150) + (dot * 7) + (reef * 0.005) + stables
            if total >= 100000:
                tier = "💎 Diamond"
            elif total >= 10000:
                tier = "🥇 Gold"
            elif total >= 1000:
                tier = "🥈 Silver"
            else:
                tier = "🥉 Bronze"
            score = min(round(total / 1000, 2), 100)
            logger.info(f"💰 Honey Score: {score} | Tier: {tier}")
            return {
                "total_usd": format_usd(total),
                "honey_score": score,
                "tier": tier
            }
        except Exception as e:
            logger.error(f"Valuation error: {str(e)}")
            return {}

