import httpx
from mcp.server.fastmcp import FastMCP

def register_mempool_tools(app: FastMCP):
    @app.tool()
    async def get_mempool_info(query: str) -> str:
        """Mempool tool"""
        try:
            return f"Mempool info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching mempool data"
