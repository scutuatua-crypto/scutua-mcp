import httpx
from mcp.server.fastmcp import FastMCP

def register_rwa_tools(app: FastMCP):
    @app.tool()
    async def get_rwa_info(query: str) -> str:
        """Rwa tool"""
        try:
            return f"Rwa info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching rwa data"
