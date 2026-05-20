import httpx
from mcp.server.fastmcp import FastMCP

def register_aave_live_tools(app: FastMCP):
    @app.tool()
    async def get_aave_live_info(query: str) -> str:
        """Aave Live tool"""
        try:
            return f"Aave_Live info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching aave_live data"
