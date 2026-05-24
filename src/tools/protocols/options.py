import httpx
from mcp.server.fastmcp import FastMCP

def register_options_tools(app: FastMCP):
    @app.tool()
    async def get_options_info(query: str) -> str:
        """Options tool"""
        try:
            return f"Options info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching options data"
