# main.py
import asyncio
from mcp.server.fastmcp import FastMCP
from src.tools.registry import register_all_tools

# Initialize the FastMCP server
app = FastMCP("Scutua-MCP")

# Register all tools from the registry
register_all_tools(app)

if __name__ == "__main__":
    # Start the server
    app.run()
