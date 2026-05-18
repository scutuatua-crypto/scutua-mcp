"""⭕ Polkadot Tool — Chain & Governance"""

import os
from substrateinterface import SubstrateInterface
from mcp.server import Server
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_polkadot_tools(app: Server):

    @app.tool()
    async def get_dot_balance(wallet: str) -> dict:
        """Get DOT balance from Polkadot chain"""
        try:
            substrate = SubstrateInterface(url="wss://rpc.polkadot.io")
            result = substrate.query("System", "Account", [wallet])
            free = result["data"]["free"].value / 1e10
            logger.info(f"⭕ DOT balance: {free}")
            return {"wallet": wallet[:8] + "...", "dot": free}
        except Exception as e:
            logger.error(f"Polkadot error: {str(e)}")
            return {}

