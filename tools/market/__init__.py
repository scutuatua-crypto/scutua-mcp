"""
Market Intelligence Universe Initialization — Scutua-MCP (Dimension 5)
Uses local relative routing to completely bypass cloud environment mapping bugs.
"""
from mcp.server.fastmcp import FastMCP

# Force Python to look at the file next to it (.coingecko) instead of the global path
from .coingecko import register_coingecko_tools

def register_market_tools(app: FastMCP) -> None:
    """
    Centralized registration for Dimension 5 metrics tools.
    """
    register_coingecko_tools(app)
