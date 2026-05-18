"""💵 Stablecoin Tool — USDT/USDC Multi-Chain"""

import httpx
from mcp.server import Server
from src.utils.logger import get_logger
from src.utils.formatters import format_usd

logger = get_logger(__name__)

STABLECOIN_APIS = {
    "solana": "https://pro-api.solscan.io/v2.0",
    "ethereum": "https://api.etherscan.io/api",
}

def register_stablecoin_tools(app: Server):

    @app.tool()
    async def get_stable_balance(wallet: str, chain: str = "solana") -> dict:
        """Get USDT/USDC balance across chains"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{STABLECOIN_APIS.get(chain, STABLECOIN_APIS['solana'])}/account/tokens",
                    params={"address": wallet}
                )
                data = r.json()
                logger.info(f"💵 Stables on {chain}: {wallet[:8]}...")
                return {"chain": chain, "wallet": wallet[:8] + "...", "data": data}
        except Exception as e:
            logger.error(f"Stablecoin error: {str(e)}")
            return {}

