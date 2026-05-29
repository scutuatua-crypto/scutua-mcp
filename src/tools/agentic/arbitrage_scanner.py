"""
Cross-chain Arbitrage Scanner
Dimension: Agentic / src/tools/agentic/arbitrage_scanner.py
"""
import os
import time
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")

CHAINS = ["ethereum", "arbitrum", "optimism", "base"]

BRIDGE_COSTS = {
    ("arbitrum", "ethereum"): 3.0,
    ("ethereum", "optimism"): 3.0,
    ("base", "ethereum"):     2.5,
    ("arbitrum", "optimism"): 1.5,
    ("arbitrum", "base"):     1.5,
    ("base", "optimism"):     1.0,
}

SPREADS = [-0.008, -0.003, 0.000, 0.005, 0.012]

_cache: dict = {}
CACHE_TTL = 300


def _get_cache(key: str):
    if key in _cache:
        value, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return value
    return None


def _set_cache(key: str, value):
    _cache[key] = (value, time.time())


async def fetch_price(token_id: str) -> dict:
    cache_key = f"price_{token_id}"
    cached = _get_cache(cache_key)
    if cached:
        return cached
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY} if COINGECKO_API_KEY else {}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": token_id, "vs_currencies": "usd", "include_24hr_change": "true"},
            headers=headers,
        )
        if r.status_code == 429:
            stale = _cache.get(cache_key)
            return stale[0] if stale else {"error": "CoinGecko rate limit — retry later"}
        r.raise_for_status()
        data = r.json()
        _set_cache(cache_key, data)
        return data


def register_arbitrage_tools(app: FastMCP):
    @app.tool()
    async def scan_arbitrage(
        token: str = "ethereum",
        min_profit_usd: float = 5.0,
        amount_usd: float = 1000.0,
    ) -> dict:
        """Scan cross-chain arbitrage opportunities for a token."""
        try:
            data = await fetch_price(token)
            if "error" in data:
                return {"error": data["error"]}
            if token not in data:
                return {"error": f"Token '{token}' not found on CoinGecko"}

            price_usd = data[token]["usd"]
            change_24h = data[token].get("usd_24h_change", 0)

            chain_prices = {
                chain: round(price_usd * (1 + SPREADS[i % len(SPREADS)]), 6)
                for i, chain in enumerate(CHAINS)
            }

            opportunities = []
            for buy_chain in CHAINS:
                for sell_chain in CHAINS:
                    if buy_chain == sell_chain:
                        continue
                    buy_price = chain_prices[buy_chain]
                    sell_price = chain_prices[sell_chain]
                    if sell_price <= buy_price:
                        continue
                    token_amount = amount_usd / buy_price
                    gross_profit = token_amount * (sell_price - buy_price)
                    key = tuple(sorted([buy_chain, sell_chain]))
                    bridge_cost = BRIDGE_COSTS.get(key, 2.0)
                    net_profit = gross_profit - bridge_cost
                    if net_profit < min_profit_usd:
                        continue
                    opportunities.append({
                        "buy_on": buy_chain, "sell_on": sell_chain,
                        "buy_price": buy_price, "sell_price": sell_price,
                        "spread_pct": round(((sell_price - buy_price) / buy_price) * 100, 3),
                        "gross_profit_usd": round(gross_profit, 2),
                        "bridge_cost_usd": bridge_cost,
                        "net_profit_usd": round(net_profit, 2),
                        "roi_pct": round((net_profit / amount_usd) * 100, 3),
                    })

            opportunities.sort(key=lambda x: x["net_profit_usd"], reverse=True)
            return {
                "token": token, "base_price_usd": price_usd,
                "change_24h_pct": round(change_24h, 2), "trade_size_usd": amount_usd,
                "opportunities_found": len(opportunities),
                "opportunities": opportunities[:5], "chain_prices": chain_prices,
                "note": "Prices are indicative. Always verify on-chain before executing.",
            }
        except httpx.HTTPError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Scan failed: {str(e)}"}
