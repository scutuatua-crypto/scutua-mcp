"""🐋 Whale Tool — Track Whale Wallets"""

import httpx
from mcp.server import Server
from src.utils.logger import get_logger
from src.utils.formatters import format_usd, format_wallet

logger = get_logger(__name__)

WHALE_THRESHOLD = 100000  # $100k+

def register_whale_tools(app: Server):

    @app.tool()
    async def track_whale_wallet(wallet: str) -> dict:
        """Track whale wallet activity on Solana"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://pro-api.solscan.io/v2.0/account/transfer",
                    params={
                        "address": wallet,
                        "limit": 10,
                        "sort_by": "block_time",
                        "sort_order": "desc"
                    }
                )
                data = r.json().get("data", [])
                transfers = []
                for tx in data:
                    amount = tx.get("amount", 0)
                    transfers.append({
                        "from": format_wallet(tx.get("from_address", "")),
                        "to": format_wallet(tx.get("to_address", "")),
                        "amount": amount,
                        "token": tx.get("token_symbol", "SOL"),
                        "time": tx.get("block_time", "")
                    })
                is_whale = len([t for t in transfers if t["amount"] >= WHALE_THRESHOLD]) > 0
                logger.info(f"🐋 Wallet {format_wallet(wallet)} — Whale: {is_whale}")
                return {
                    "wallet": format_wallet(wallet),
                    "is_whale": is_whale,
                    "recent_transfers": transfers[:5]
                }
        except Exception as e:
            logger.error(f"Whale error: {str(e)}")
            return {}

    @app.tool()
    async def get_whale_tier(total_usd: float) -> dict:
        """Get WhaleTrucker tier based on total USD value"""
        if total_usd >= 1_000_000:
            tier = "💎 Diamond Whale"
            badge = "DIAMOND"
        elif total_usd >= 100_000:
            tier = "🥇 Gold Whale"
            badge = "GOLD"
        elif total_usd >= 10_000:
            tier = "🥈 Silver Whale"
            badge = "SILVER"
        elif total_usd >= 1_000:
            tier = "🥉 Bronze Whale"
            badge = "BRONZE"
        else:
            tier = "🐟 Small Fish"
            badge = "FISH"
        logger.info(f"🐋 Tier: {tier} | ${format_usd(total_usd)}")
        return {
            "tier": tier,
            "badge": badge,
            "total_usd": format_usd(total_usd)
        }
