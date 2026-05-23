"""
Master Tools Registry — Scutua-MCP Central Hub
Aggregates all 5 operational dimensions cleanly.
"""
from mcp.server.fastmcp import FastMCP

# Route cleanly to the Dimension 5 package initialization
from src.tools.market import register_market_tools

def register_master_tools(app: FastMCP) -> None:
    """
    Global bootstrap trigger for aggregating all modular tool dimensions.
    """
    # Execute Dimension 5 Integration
    register_market_tools(app)
