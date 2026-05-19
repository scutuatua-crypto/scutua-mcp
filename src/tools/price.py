"""💰 Price Tool — Token Realtime Prices"""

import httpx
from mcp.server import Server
from src.utils.logger import get_logger
from src.utils.formatters import format_usd

logger = get_logger(__name__)

def register_price_tools(app: Server):

    @app.tool()
    async def get_token_price(symbol: str) -> dict:
        """Get realtime token price from CoinGecko"""
        try:
            symbol_map = {
                "SOL": "solana",
                "DOT": "polkadot", 
                "REEF": "reef-finance",
                "BTC": "bitcoin",
                "ETH": "ethereum"
            }
            coin_id = symbol_map.get(symbol.upper(), symbol.lower())
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={"ids": coin_id, "vs_currencies": "usd", "include_24hr_change": "true"}
                )
                data = r.json()
                price = data[coin_id]["usd"]
                change = data[coin_id].get("usd_24h_change", 0)
                logger.info(f"💰 {symbol}: ${price}")
                return {
                    "symbol": symbol.upper(),
                    "price_usd": format_usd(price),
                    "change_24h": f"{change:.2f}%"
                }
        except Exception as e:
            logger.error(f"Price error: {str(e)}")
            return {}
