"""🐚 Reef Tool — NFT Rewards & DeFi"""
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

# เปลี่ยน RPC endpoint ที่เสถียรกว่า
REEF_RPC = "https://reef.api.onfinality.io/public-ws"
REEF_RPC_HTTP = "https://rpc.reef.io"

def register_reef_tools(app: FastMCP):

    @app.tool()
    async def get_reef_balance(wallet: str) -> dict:
        """Get Reef balance from chain"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    REEF_RPC_HTTP,
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [wallet, "latest"],
                        "id": 1
                    },
                    headers={"Content-Type": "application/json"}
                )
                r.raise_for_status()
                data = r.json()
                if "result" not in data:
                    return {"wallet": wallet[:8] + "...", "reef": 0, "note": "No result from RPC"}
                balance = int(data["result"], 16) / 1e18
                logger.info(f"🐚 Reef balance: {balance}")
                return {"wallet": wallet[:8] + "...", "reef": round(balance, 4)}
        except Exception as e:
            logger.error(f"Reef error: {str(e)}")
            return {"wallet": wallet[:8] + "...", "reef": 0, "error": str(e)}
