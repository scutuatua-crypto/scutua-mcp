"""☀️ Solana Tool — Wallet & Solscan v2"""

import os
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
from src.utils.formatters import format_usd

logger = get_logger(__name__)
SOLSCAN_API = "https://pro-api.solscan.io/v2.0"

def register_solana_tools(app: FastMCP):

    @app.tool()
    async def get_solana_balance(wallet: str) -> dict:
        """Get SOL balance and token holdings"""
        try:
            headers = {"token": os.getenv("SOLANA_API")}
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{SOLSCAN_API}/account/balance",
                    params={"address": wallet},
                    headers=headers
                )
                data = r.json()
                sol = data.get("data", {}).get("lamports", 0) / 1e9
                logger.info(f"☀️ Wallet {wallet[:8]}... = {sol} SOL")
                return {"wallet": wallet[:8] + "...", "sol": sol, "formatted": format_usd(sol * 150)}
        except Exception as e:
            logger.error(f"Solana error: {str(e)}")
            return {}

