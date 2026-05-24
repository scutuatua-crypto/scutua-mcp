import httpx
from mcp.server.fastmcp import FastMCP

def register_drift_tools(app: FastMCP):
    @app.tool()
    async def get_drift_info(query: str) -> str:
        """Drift tool"""
        try:
            return f"Drift info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching drift data"
