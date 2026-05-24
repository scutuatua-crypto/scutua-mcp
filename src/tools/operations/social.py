import httpx
from mcp.server.fastmcp import FastMCP

def register_social_tools(app: FastMCP):
    @app.tool()
    async def get_social_info(query: str) -> str:
        """Social tool"""
        try:
            return f"Social info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching social data"
