"""
🐋 WhaleTrucker Ecosystem — Domain 1: Layer 1 / Layer 2 Networks Registry
Author: scutuatua-crypto
"""
from src.tools.solana import register_solana_tools
from src.tools.polkadot import register_polkadot_tools
from src.tools.reef import register_reef_tools
from src.tools.ton import register_ton_tools
from src.tools.cosmos import register_cosmos_tools
from src.tools.base import register_base_tools
from src.tools.crosschain import register_crosschain_tools

def register_chain_tools(mcp_app):
    """Aggregates and registers all blockchain network layer tools into the core application context."""
    register_solana_tools(mcp_app)
    register_polkadot_tools(mcp_app)
    register_reef_tools(mcp_app)
    register_ton_tools(mcp_app)
    register_cosmos_tools(mcp_app)
    register_base_tools(mcp_app)
    register_crosschain_tools(mcp_app)
