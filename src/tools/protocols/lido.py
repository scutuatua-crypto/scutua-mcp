import httpx
from mcp.server.fastmcp import FastMCP

def register_lido_tools(app: FastMCP):
    @app.tool()
    async def get_lido_info(query: str) -> str:
        """Lido tool"""
        try:
            return f"Lido info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching lido data"
