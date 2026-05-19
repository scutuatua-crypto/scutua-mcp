import httpx
from mcp.server.fastmcp import FastMCP

def register_cosmos_tools(app: FastMCP):
    @app.tool()
    async def get_cosmos_balance(address: str) -> str:
        """Get Cosmos ATOM wallet balance"""
        try:
            url = f"https://lcd-cosmoshub.blockapsis.com/cosmos/bank/v1beta1/balances/{address}"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            balances = data.get("balances", [])
            if not balances:
                return "No balance found"
            result = []
            for b in balances:
                amount = int(b["amount"]) / 1e6
                denom = b["denom"].replace("u", "", 1).upper()
                result.append(f"{denom}: {amount:.4f}")
            return "Cosmos Balances:\n" + "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
