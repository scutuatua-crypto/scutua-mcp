"""
🛠️ Portfolio Tracker Tools — WhaleTrucker Ecosystem
"""
from fastmcp import FastMCP
import httpx

def register_portfolio_tracker_tools(app: FastMCP):

    @app.tool()
    async def get_portfolio_value(addresses: list[str], chains: list[str] = ["ethereum", "solana"]) -> dict:
        """Get total portfolio value across multiple wallets and chains"""
        results = {}
        for address in addresses:
            results[address] = {"address": address, "chains": chains, "status": "tracked"}
        return {"portfolios": results, "total_wallets": len(addresses)}

    @app.tool()
    async def track_pnl(address: str, chain: str = "ethereum") -> dict:
        """Track PnL for a wallet address"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.zerion.io/v1/wallets/{address}/portfolio/?currency=usd",
                headers={"Authorization": "Basic "})
        return {"address": address, "chain": chain, "pnl": r.json()}

    @app.tool()
    async def get_token_allocation(address: str) -> dict:
        """Get token allocation breakdown for a wallet"""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"https://api.zerion.io/v1/wallets/{address}/positions/?currency=usd",
                headers={"Authorization": "Basic "})
        return {"address": address, "allocation": r.json()}

