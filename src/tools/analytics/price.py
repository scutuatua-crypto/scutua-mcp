"""💰 Price Tool — Token Realtime Prices"""
import os
import httpx
from mcp.server import Server
from src.utils.logger import get_logger
from src.utils.formatters import format_usd

logger = get_logger(__name__)

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

# เพิ่ม coin ได้เรื่อยๆ
SYMBOL_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "DOT": "polkadot",
    "REEF": "reef-finance",
    "TON": "the-open-network",
    "ATOM": "cosmos",
    "AVAX": "avalanche-2",
    "MATIC": "matic-network",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "NEAR": "near",
    "ARB": "arbitrum",
    "OP": "optimism",
}


def register_price_tools(app: Server):

    @app.tool()
    async def get_token_price(symbol: str) -> dict:
        """Get realtime token price from CoinGecko"""
        try:
            coin_id = SYMBOL_MAP.get(symbol.upper(), symbol.lower())

            # ✅ ใส่ API key ใน header แก้ rate limit
            headers = {"accept": "application/json"}
            if COINGECKO_API_KEY:
                headers["x-cg-demo-api-key"] = COINGECKO_API_KEY

            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    headers=headers,
                    params={
                        "ids": coin_id,
                        "vs_currencies": "usd",
                        "include_24hr_change": "true",
                        "include_market_cap": "true",
                    },
                    timeout=10,
                )
                r.raise_for_status()
                data = r.json()

            if coin_id not in data:
                return {"error": f"Token '{symbol}' not found"}

            price = data[coin_id]["usd"]
            change = data[coin_id].get("usd_24h_change", 0) or 0
            mcap = data[coin_id].get("usd_market_cap", 0) or 0

            logger.info(f"💰 {symbol}: ${price}")
            return {
                "symbol": symbol.upper(),
                "price_usd": format_usd(price),
                "change_24h": f"{change:+.2f}%",
                "market_cap": format_usd(mcap),
            }

        except Exception as e:
            logger.error(f"Price error: {str(e)}")
            return {"error": str(e)}
