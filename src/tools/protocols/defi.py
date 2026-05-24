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
                total = sum(tvl.values())
                return f"🏦 {protocol.upper()} TVL: ${total/1e6:.2f}M"
            else:
                url = "https://api.llama.fi/global"
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    data = r.json()
                total = data.get("totalLiquidityUSD", 0)
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
            top5 = sorted(data, key=lambda x: x.get("tvl", 0), reverse=True)[:5]
            result = ["🏆 Top 5 DeFi Protocols:"]
            for i, p in enumerate(top5, 1):
                tvl = p.get("tvl", 0)
                result.append(f"{i}. {p['name']}: ${tvl/1e9:.2f}B")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
