"""
DeFi Protocol Tools — Scutua-MCP
"""
import httpx
from mcp.server.fastmcp import FastMCP


def register_defi_tools(app: FastMCP):

    @app.tool()
    async def get_defi_tvl(protocol: str = "") -> str:
        """Get DeFi protocol TVL from DeFiLlama"""
        try:
            if protocol:
                url = f"https://api.llama.fi/protocol/{protocol.lower()}"
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    data = r.json()
                tvl = data.get("currentChainTvls", {})
                # 🔧 FIX: filter None values ก่อน sum
                total = sum(v for v in tvl.values() if isinstance(v, (int, float)))
                return f"🏦 {protocol.upper()} TVL: ${total/1e6:.2f}M"
            else:
                url = "https://api.llama.fi/global"
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    data = r.json()
                total = data.get("totalLiquidityUSD", 0) or 0
                return f"🏦 Total DeFi TVL: ${total/1e9:.2f}B"
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_top_defi_protocols() -> str:
        """Get top DeFi protocols by TVL"""
        try:
            url = "https://api.llama.fi/protocols"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()

            # 🔧 FIX: แทนที่ None ด้วย 0 ก่อน sort — ป้องกัน NoneType comparison crash
            def safe_tvl(x):
                tvl = x.get("tvl")
                return tvl if isinstance(tvl, (int, float)) else 0

            top10 = sorted(data, key=safe_tvl, reverse=True)[:10]

            result = ["🏆 Top 10 DeFi Protocols by TVL:"]
            for i, p in enumerate(top10, 1):
                tvl = safe_tvl(p)
                chain = p.get("chain", "Multi")
                category = p.get("category", "")
                change = p.get("change_1d")
                change_str = f" ({change:+.1f}%)" if isinstance(change, (int, float)) else ""
                result.append(
                    f"{i}. {p['name']} [{chain}] — ${tvl/1e9:.2f}B{change_str}"
                    + (f" · {category}" if category else "")
                )
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_chain_tvl(chain: str) -> str:
        """Get total TVL for a specific blockchain"""
        try:
            url = f"https://api.llama.fi/v2/historicalChainTvl/{chain}"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            if not data or not isinstance(data, list):
                return f"❌ No TVL data for chain: {chain}"
            latest = data[-1]
            tvl = latest.get("tvl", 0) or 0
            return f"⛓️ {chain.upper()} TVL: ${tvl/1e9:.2f}B"
        except Exception as e:
            return f"Error: {e}"
