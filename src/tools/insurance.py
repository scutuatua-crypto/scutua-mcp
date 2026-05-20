import httpx
from mcp.server.fastmcp import FastMCP

def register_insurance_tools(app: FastMCP):
    @app.tool()
    async def get_insurance_info(query: str) -> str:
        """Insurance tool"""
        try:
            return f"Insurance info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching insurance data"
