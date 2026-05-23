"""
Market Intelligence Universe Initialization — Scutua-MCP (Dimension 5)
Strict local isolation using relative imports to bypass cloud deployment path bugs.
"""
from mcp.server.fastmcp import FastMCP

# Force strict local resolution inside Dimension 5
from .coingecko import register_coingecko_tools

def register_market_tools(app: FastMCP) -> None:
    """
    Centralized registration hub for all Dimension 5 data feeds.
    """
    register_coingecko_tools(app)
