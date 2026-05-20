import httpx
from mcp.server.fastmcp import FastMCP

def register_jupiter_tools(app: FastMCP):
    @app.tool()
    async def get_jupiter_info(query: str) -> str:
        """Jupiter tool"""
        try:
            return f"Jupiter info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching jupiter data"
