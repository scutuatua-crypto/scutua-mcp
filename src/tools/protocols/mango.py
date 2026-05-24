import httpx
from mcp.server.fastmcp import FastMCP

def register_mango_tools(app: FastMCP):
    @app.tool()
    async def get_mango_info(query: str) -> str:
        """Mango tool"""
        try:
            return f"Mango info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching mango data"
