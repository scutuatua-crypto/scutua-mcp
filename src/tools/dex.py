import httpx
from mcp.server.fastmcp import FastMCP

def register_dex_tools(app: FastMCP):
    @app.tool()
    async def get_dex_info(query: str) -> str:
        """Dex tool"""
        try:
            return f"Dex info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching dex data"
