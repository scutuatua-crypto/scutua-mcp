import httpx
from mcp.server.fastmcp import FastMCP

def register_etf_tools(app: FastMCP):
    @app.tool()
    async def get_etf_info(query: str) -> str:
        """Etf tool"""
        try:
            return f"Etf info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching etf data"
