"""
🏦 Lending Tools — DeFi Borrow/Supply Rates
Real API: DeFiLlama Yields
Mock fallback included
"""
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)
LLAMA_POOLS_URL = "https://yields.llama.fi/pools"
MOCK_LENDING = {
    "USDC": [
        {"protocol": "Aave v3",    "chain": "Ethereum", "supply_apy": 4.82, "borrow_apy": 5.91},
        {"protocol": "Compound v3","chain": "Ethereum", "supply_apy": 4.51, "borrow_apy": 5.63},
        {"protocol": "Aave v3",    "chain": "Polygon",  "supply_apy": 5.10, "borrow_apy": 6.20},
    ],
    "ETH": [
        {"protocol": "Aave v3",    "chain": "Ethereum", "supply_apy": 1.92, "borrow_apy": 2.85},
        {"protocol": "Compound v3","chain": "Ethereum", "supply_apy": 1.75, "borrow_apy": 2.70},
    ],
    "USDT": [
        {"protocol": "Aave v3",    "chain": "Ethereum", "supply_apy": 4.70, "borrow_apy": 5.80},
    ],
    "DAI": [
        {"protocol": "Aave v3",    "chain": "Ethereum", "supply_apy": 4.60, "borrow_apy": 5.70},
        {"protocol": "Spark",      "chain": "Ethereum", "supply_apy": 5.00, "borrow_apy": 5.50},
    ],
}
LENDING_PROTOCOLS = {"aave", "compound", "spark", "morpho"}

async def _fetch_llama_lending(token):
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            resp = await client.get(LLAMA_POOLS_URL)
            resp.raise_for_status()
            pools = resp.json().get("data", [])
        results = []
        for p in pools:
            sym = p.get("symbol", "").upper()
            proj = p.get("project", "").lower()
            if token.upper() not in sym:
                continue
            if not any(lp in proj for lp in LENDING_PROTOCOLS):
                continue
            supply = p.get("apy") or 0
            borrow = p.get("apyBorrow") or 0
            if supply <= 0 and borrow <= 0:
                continue
            results.append({"protocol": p.get("project","?"), "chain": p.get("chain","?"),
                            "supply_apy": round(supply,2), "borrow_apy": round(borrow,2)})
        return sorted(results, key=lambda x: x["supply_apy"], reverse=True)[:10]
    except Exception as e:
        logger.warning(f"DeFiLlama lending fetch failed: {e}")
    return []

def register_lending_tools(app: FastMCP):
    @app.tool()
    async def get_lending_rates(token: str) -> str:
        """Get supply and borrow APY for a token across lending protocols."""
        token = token.upper().strip()
        data = await _fetch_llama_lending(token)
        source = "Live (DeFiLlama)"
        if not data:
            data = MOCK_LENDING.get(token)
            if not data:
                return f"❌ No lending data for {token}. Try: {', '.join(MOCK_LENDING.keys())}"
            source = "Mock (fallback)"
        lines = [f"🏦 Lending Rates — {token}  [{source}]\n"]
        lines.append(f"{'Protocol':<18} {'Chain':<12} {'Supply APY':>10} {'Borrow APY':>10}")
        lines.append("-" * 54)
        for d in data:
            lines.append(f"{d['protocol']:<18} {d['chain']:<12} {d['supply_apy']:>9.2f}% {d['borrow_apy']:>9.2f}%")
        return "\n".join(lines)

    @app.tool()
    async def best_supply_rate(token: str) -> str:
        """Find the best supply APY for a token."""
        token = token.upper().strip()
        data = await _fetch_llama_lending(token) or MOCK_LENDING.get(token, [])
        if not data:
            return f"❌ No data for {token}."
        best = max(data, key=lambda x: x["supply_apy"])
        return f"💰 Best Supply — {token}\nProtocol: {best['protocol']} ({best['chain']})\nAPY: {best['supply_apy']}%"

    @app.tool()
    async def estimate_lending_income(token: str, amount: float, days: int = 365) -> str:
        """Estimate income from supplying tokens to a lending protocol."""
        token = token.upper().strip()
        data = await _fetch_llama_lending(token) or MOCK_LENDING.get(token, [])
        if not data:
            return f"❌ No data for {token}."
        best = max(data, key=lambda x: x["supply_apy"])
        income = amount * (best["supply_apy"]/100) * (days/365)
        return f"📈 Lending Income — {token}\nProtocol: {best['protocol']}\nAPY: {best['supply_apy']}%\nAmount: {amount:,.4f} {token}\nDays: {days}\nIncome: +{income:,.4f} {token}"

