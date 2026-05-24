import httpx
from mcp.server.fastmcp import FastMCP

def register_raydium_tools(app: FastMCP):
    @app.tool()
    async def get_raydium_info(query: str) -> str:
        """Raydium tool"""
        try:
            return f"Raydium info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching raydium data"
