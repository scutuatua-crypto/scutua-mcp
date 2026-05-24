import httpx
from mcp.server.fastmcp import FastMCP

def register_uniswap_tools(app: FastMCP):
    @app.tool()
    async def get_uniswap_info(query: str) -> str:
        """Uniswap tool"""
        try:
            return f"Uniswap info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching uniswap data"
