import httpx
from mcp.server.fastmcp import FastMCP

def register_yield_tools(app: FastMCP):
    @app.tool()
    async def get_best_yields(token: str = "usdc") -> str:
        """Get best DeFi yields for a token"""
        try:
            url = "https://yields.llama.fi/pools"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json().get("data", [])
            filtered = [p for p in data if token.upper() in p.get("symbol", "").upper() and p.get("apy", 0) > 0]
            top5 = sorted(filtered, key=lambda x: x.get("apy", 0), reverse=True)[:5]
            if not top5:
                return f"No yields found for {token.upper()}"
            result = [f"🌾 Best {token.upper()} Yields:"]
            for i, p in enumerate(top5, 1):
                result.append(f"{i}. {p.get('project')} ({p.get('chain')}): {p.get('apy', 0):.2f}% APY")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def compare_yields(token_a: str, token_b: str) -> str:
        """Compare yields between two tokens"""
        try:
            url = "https://yields.llama.fi/pools"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json().get("data", [])
            def best(token):
                f = [p for p in data if token.upper() in p.get("symbol","").upper() and p.get("apy",0) > 0]
                return max(f, key=lambda x: x.get("apy",0)) if f else None
            a = best(token_a)
            b = best(token_b)
            result = [f"📊 Yield Comparison:"]
            if a:
                result.append(f"{token_a.upper()}: {a.get('apy',0):.2f}% APY @ {a.get('project')} ({a.get('chain')})")
            if b:
                result.append(f"{token_b.upper()}: {b.get('apy',0):.2f}% APY @ {b.get('project')} ({b.get('chain')})")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
