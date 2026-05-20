import httpx
from mcp.server.fastmcp import FastMCP

def register_onchain_tools(app: FastMCP):
    @app.tool()
    async def get_onchain_info(query: str) -> str:
        """Onchain tool"""
        try:
            return f"Onchain info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching onchain data"
