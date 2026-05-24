import httpx
from mcp.server.fastmcp import FastMCP

def register_points_tools(app: FastMCP):
    @app.tool()
    async def get_points_info(query: str) -> str:
        """Points tool"""
        try:
            return f"Points info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching points data"
