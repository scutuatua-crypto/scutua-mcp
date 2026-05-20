import httpx
from mcp.server.fastmcp import FastMCP

def register_pump_fun_tools(app: FastMCP):
    @app.tool()
    async def get_pump_fun_info(query: str) -> str:
        """Pump Fun tool"""
        try:
            return f"Pump_Fun info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching pump_fun data"
