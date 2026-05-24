import httpx
from mcp.server.fastmcp import FastMCP

def register_ens_tools(app: FastMCP):
    @app.tool()
    async def get_ens_info(query: str) -> str:
        """Ens tool"""
        try:
            return f"Ens info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching ens data"
