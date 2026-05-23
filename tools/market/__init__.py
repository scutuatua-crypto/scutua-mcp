"""
Market Intelligence Universe Initialization — Scutua-MCP (Dimension 5)
Handles local context registration for isolation.
"""
from src.tools.market.coingecko import register_coingecko_tools

def register_market_tools(app):
    """
    Directly boots and mounts Dimension 5 sub-modules.
    """
    register_coingecko_tools(app)
