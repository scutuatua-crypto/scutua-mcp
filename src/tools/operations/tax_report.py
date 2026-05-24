import httpx
from mcp.server.fastmcp import FastMCP

def register_tax_report_tools(app: FastMCP):
    @app.tool()
    async def get_tax_report_info(query: str) -> str:
        """Tax Report tool"""
        try:
            return f"Tax_Report info for {query}: Not implemented yet"
        except Exception as e:
            return f"Error fetching tax_report data"
