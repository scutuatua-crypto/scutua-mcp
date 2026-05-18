"""🐚 Reef Tool — NFT Rewards & DeFi"""

import os
import httpx
from mcp.server import Server
from src.utils.logger import get_logger

logger = get_logger(__name__)

def register_reef_tools(app: Server):

    @app.tool()
    async def get_reef_rewards(wallet: str) -> dict:
        """Get Reef staking rewards and NFT status"""
        try:
            key = os.getenv("REEF_KEY")
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.reef.io/v1/rewards",
                    params={"address": wallet},
                    headers={"Authorization": f"Bearer {key}"}
                )
                data = r.json()
                logger.info(f"🐚 Reef rewards fetched for {wallet[:8]}...")
                return data
        except Exception as e:
            logger.error(f"Reef error: {str(e)}")
            return {}

