"""📊 Portfolio Tool — Multi-Chain Summary"""

import httpx
from mcp.server import Server
from src.utils.logger import get_logger
from src.utils.formatters import format_usd

logger = get_logger(__name__)

def register_portfolio_tools(app: Server):

    @app.tool()
    async def get_portfolio_summary(
        sol_balance: float = 0,
        dot_balance: float = 0,
        reef_balance: float = 0,
        stable_balance: float = 0
    ) -> dict:
        """Get full portfolio summary across all chains"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={
                        "ids": "solana,polkadot,reef-finance",
                        "vs_currencies": "usd"
                    }
                )
                prices = r.json()

            sol_price = prices.get("solana", {}).get("usd", 0)
            dot_price = prices.get("polkadot", {}).get("usd", 0)
            reef_price = prices.get("reef-finance", {}).get("usd", 0)

            sol_usd = sol_balance * sol_price
            dot_usd = dot_balance * dot_price
            reef_usd = reef_balance * reef_price
            total_usd = sol_usd + dot_usd + reef_usd + stable_balance

            honey_score = min(round(total_usd / 1000, 2), 100)

            logger.info(f"📊 Portfolio total: {format_usd(total_usd)}")
            return {
                "breakdown": {
                    "SOL": f"{sol_balance} SOL = {format_usd(sol_usd)}",
                    "DOT": f"{dot_balance} DOT = {format_usd(dot_usd)}",
                    "REEF": f"{reef_balance} REEF = {format_usd(reef_usd)}",
                    "Stables": format_usd(stable_balance)
                },
                "total_usd": format_usd(total_usd),
                "honey_score": honey_score
            }
        except Exception as e:
            logger.error(f"Portfolio error: {str(e)}")
            return {}
