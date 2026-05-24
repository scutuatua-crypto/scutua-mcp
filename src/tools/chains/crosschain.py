import httpx
from mcp.server.fastmcp import FastMCP

def register_crosschain_tools(app: FastMCP):
    @app.tool()
    async def get_crosschain_info(query: str) -> str:
        """Crosschain tool"""
        try:
            return f"Crosschain info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching crosschain data"
