"""🌉 Bridge Tools — Cross-Chain Bridge Fee Estimator"""
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
logger = get_logger(__name__)
LIFI_QUOTE_URL = "https://li.quest/v1/quote"
CHAIN_IDS = {"ethereum":1,"polygon":137,"arbitrum":42161,"optimism":10,"bsc":56,"base":8453}
MOCK_BRIDGES = {
    ("ethereum","polygon"):   [{"bridge":"Polygon PoS","fee_usd":1.20,"time_min":10},{"bridge":"Hop Protocol","fee_usd":2.50,"time_min":3}],
    ("ethereum","arbitrum"):  [{"bridge":"Arbitrum Bridge","fee_usd":3.50,"time_min":15},{"bridge":"Across","fee_usd":1.90,"time_min":2}],
    ("ethereum","optimism"):  [{"bridge":"Optimism Bridge","fee_usd":3.20,"time_min":20},{"bridge":"Across","fee_usd":1.80,"time_min":2}],
    ("ethereum","base"):      [{"bridge":"Base Bridge","fee_usd":2.80,"time_min":15},{"bridge":"Across","fee_usd":1.50,"time_min":2}],
    ("polygon","arbitrum"):   [{"bridge":"Hop Protocol","fee_usd":1.80,"time_min":5},{"bridge":"Across","fee_usd":1.20,"time_min":2}],
}
def register_bridge_tools(app: FastMCP):
    @app.tool()
    async def estimate_bridge_fee(from_chain: str, to_chain: str, token: str = "USDC", amount: float = 1000) -> str:
        \"\"\"Estimate bridge fees between two chains. Args: from_chain, to_chain, token (default USDC), amount USD (default 1000)\"\"\"
        f, t = from_chain.lower().strip(), to_chain.lower().strip()
        data = MOCK_BRIDGES.get((f,t)) or MOCK_BRIDGES.get((t,f))
        source = "Mock (fallback)"
        if not data:
            return f"❌ No bridge data for {f}→{t}. Supported: {', '.join(f'{a}→{b}' for a,b in MOCK_BRIDGES)}"
        lines = [f"🌉 Bridge: {f.upper()} → {t.upper()}  [{source}]\nAmount: ${amount:,.2f} {token}\n"]
        for d in sorted(data, key=lambda x: x['fee_usd']):
            lines.append(f"  {d['bridge']:<22} ${d['fee_usd']:>6.2f}  ~{d['time_min']}min")
        return "\n".join(lines)
    @app.tool()
    async def cheapest_bridge(from_chain: str, to_chain: str) -> str:
        \"\"\"Find cheapest bridge between two chains.\"\"\"
        f, t = from_chain.lower().strip(), to_chain.lower().strip()
        data = MOCK_BRIDGES.get((f,t)) or MOCK_BRIDGES.get((t,f))
        if not data: return f"❌ No data for {f}→{t}."
        best = min(data, key=lambda x: x['fee_usd'])
        return f"💸 Cheapest Bridge\n{f.upper()} → {t.upper()}\nBridge: {best['bridge']}\nFee: ${best['fee_usd']:.2f}\nTime: ~{best['time_min']} min"
    @app.tool()
    async def list_supported_chains() -> str:
        \"\"\"List all chains supported for bridge estimation.\"\"\"
        return "🌉 Supported Chains\n" + "\n".join(f"  {k}" for k in CHAIN_IDS)
