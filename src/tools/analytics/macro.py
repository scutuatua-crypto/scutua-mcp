import httpx
from mcp.server.fastmcp import FastMCP

def register_macro_tools(app: FastMCP):
    @app.tool()
    async def get_macro_info(query: str) -> str:
        """Macro tool"""
        try:
            return f"Macro info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching macro data"
