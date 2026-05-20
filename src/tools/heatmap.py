import httpx
from mcp.server.fastmcp import FastMCP

def register_heatmap_tools(app: FastMCP):
    @app.tool()
    async def get_heatmap_info(query: str) -> str:
        """Heatmap tool"""
        try:
            return f"Heatmap info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching heatmap data"
