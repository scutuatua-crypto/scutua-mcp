"""🐚 Reef Tool — NFT Rewards & DeFi"""

import httpx
from mcp.server import Server
from src.utils.logger import get_logger

logger = get_logger(__name__)
REEF_RPC = "https://rpc.reefscan.com"

def register_reef_tools(app: Server):

    @app.tool()
    async def get_reef_balance(wallet: str) -> dict:
        """Get Reef balance from chain"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    REEF_RPC,
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [wallet, "latest"],
                        "id": 1
                    }
                )
                data = r.json()
                balance = int(data["result"], 16) / 1e18
                logger.info(f"🐚 Reef balance: {balance}")
                return {"wallet": wallet[:8] + "...", "reef": balance}
        except Exception as e:
            logger.error(f"Reef error: {str(e)}")
            return {}
