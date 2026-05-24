import httpx
from mcp.server.fastmcp import FastMCP

def register_narrative_tools(app: FastMCP):
    @app.tool()
    async def get_narrative_info(query: str) -> str:
        """Narrative tool"""
        try:
            return f"Narrative info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching narrative data"
