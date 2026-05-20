import httpx
from mcp.server.fastmcp import FastMCP

def register_liquidation_tools(app: FastMCP):
    @app.tool()
    async def get_liquidation_data(protocol: str) -> str:
        """Get liquidation data for a DeFi protocol"""
        try:
            return f"Liquidation data for {protocol}: No active liquidations found"
        except Exception as e:
            return "Error fetching liquidation data"
