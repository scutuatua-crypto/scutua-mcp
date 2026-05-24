import httpx
from mcp.server.fastmcp import FastMCP

def register_perp_tools(app: FastMCP):
    @app.tool()
    async def get_perp_info(query: str) -> str:
        """Perp tool"""
        try:
            return f"Perp info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching perp data"
