import httpx
from mcp.server.fastmcp import FastMCP

# Public Cosmos LCD endpoints — fallback chain
COSMOS_LCD_URLS = [
    "https://cosmos-rest.publicnode.com",
    "https://rest.cosmos.directory/cosmoshub",
    "https://lcd.cosmos.network",
]

def register_cosmos_tools(app: FastMCP):
    @app.tool()
    async def get_cosmos_balance(address: str) -> str:
        """Get Cosmos ATOM wallet balance"""
        last_error = ""
        for base_url in COSMOS_LCD_URLS:
            try:
                url = f"{base_url}/cosmos/bank/v1beta1/balances/{address}"
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    r.raise_for_status()
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
                last_error = str(e)
                continue
        return f"Error: All endpoints failed — {last_error}"
