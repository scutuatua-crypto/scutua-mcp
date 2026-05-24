import httpx
from mcp.server.fastmcp import FastMCP

def register_fear_greed_tools(app: FastMCP):
    @app.tool()
    async def get_fear_greed_info(query: str) -> str:
        """Fear Greed tool"""
        try:
            return f"Fear_Greed info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching fear_greed data"
