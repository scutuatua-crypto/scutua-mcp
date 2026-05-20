import httpx
from mcp.server.fastmcp import FastMCP

def register_scam_tools(app: FastMCP):
    @app.tool()
    async def get_scam_info(query: str) -> str:
        """Scam tool"""
        try:
            return f"Scam info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching scam data"
