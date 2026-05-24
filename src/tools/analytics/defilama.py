"""
🧠 DeFiLlama Analytics Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_defilama_tools(app: FastMCP):

    @app.tool()
    async def get_protocol_tvl(protocol: str) -> dict:
        """Get TVL history for a DeFi protocol from DeFiLlama"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.llama.fi/protocol/{protocol}")
        return r.json()

    @app.tool()
    async def get_top_protocols() -> dict:
        """Get top DeFi protocols by TVL"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.llama.fi/protocols")
        protocols = r.json()[:20]
        return {"protocols": [{"name": p.get("name"), "tvl": p.get("tvl"), "chain": p.get("chain")} for p in protocols]}

    @app.tool()
    async def get_chain_tvl(chain: str) -> dict:
        """Get total TVL for a specific blockchain"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.llama.fi/v2/historicalChainTvl/{chain}")
        return {"chain": chain, "history": r.json()[-30:]}

    @app.tool()
    async def get_yields() -> dict:
        """Get top yield farming opportunities from DeFiLlama"""
        async with httpx.AsyncClient() as client:
            r = await client.get("https://yields.llama.fi/pools")
        pools = r.json().get("data", [])
        top = sorted(pools, key=lambda x: x.get("apy", 0), reverse=True)[:20]
        return {"pools": top}

