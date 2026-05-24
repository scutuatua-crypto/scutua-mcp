import httpx
from mcp.server.fastmcp import FastMCP

def register_marinade_tools(app: FastMCP):
    @app.tool()
    async def get_marinade_info(query: str) -> str:
        """Marinade tool"""
        try:
            return f"Marinade info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching marinade data"
