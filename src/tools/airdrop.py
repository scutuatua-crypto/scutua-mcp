import httpx
from mcp.server.fastmcp import FastMCP

def register_airdrop_tools(app: FastMCP):
    @app.tool()
    async def get_airdrop_info(query: str) -> str:
        """Airdrop tool"""
        try:
            return f"Airdrop info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching airdrop data"
