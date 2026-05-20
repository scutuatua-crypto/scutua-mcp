import httpx
from mcp.server.fastmcp import FastMCP

def register_copy_trade_tools(app: FastMCP):
    @app.tool()
    async def get_copy_trade_info(query: str) -> str:
        """Copy Trade tool"""
        try:
            return f"Copy_Trade info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching copy_trade data"
