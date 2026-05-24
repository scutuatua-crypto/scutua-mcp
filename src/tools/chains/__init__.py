"""
🐋 WhaleTrucker Ecosystem — Domain 1: Layer 1 / Layer 2 Networks Registry
Author: scutuatua-crypto
"""
from .solana import register_solana_tools
from .polkadot import register_polkadot_tools
from .reef import register_reef_tools
from .ton import register_ton_tools
from .cosmos import register_cosmos_tools
from .base import register_base_tools
from .crosschain import register_crosschain_tools

def register_chain_tools(mcp_app):
    register_solana_tools(mcp_app)
    register_polkadot_tools(mcp_app)
    register_reef_tools(mcp_app)
    register_ton_tools(mcp_app)
    register_cosmos_tools(mcp_app)
    register_base_tools(mcp_app)
    register_crosschain_tools(mcp_app)
