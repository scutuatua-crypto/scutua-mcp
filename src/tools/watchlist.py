import httpx
from mcp.server.fastmcp import FastMCP

def register_watchlist_tools(app: FastMCP):
    @app.tool()
    async def get_watchlist_info(query: str) -> str:
        """Watchlist tool"""
        try:
            return f"Watchlist info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching watchlist data"
