from .solana import register_solana_tools
from .polkadot import register_polkadot_tools
from .reef import register_reef_tools
from .ton import register_ton_tools
from .cosmos import register_cosmos_tools
from .base import register_base_tools
from .crosschain import register_crosschain_tools
from .ethereum import register_ethereum_tools
from .arbitrum import register_arbitrum_tools
from .optimism import register_optimism_tools
from .bnb import register_bnb_tools

def register_chain_tools(mcp_app):
    register_solana_tools(mcp_app)
    register_polkadot_tools(mcp_app)
    register_reef_tools(mcp_app)
    register_ton_tools(mcp_app)
    register_cosmos_tools(mcp_app)
    register_base_tools(mcp_app)
    register_crosschain_tools(mcp_app)
    register_ethereum_tools(mcp_app)
    register_arbitrum_tools(mcp_app)
    register_optimism_tools(mcp_app)
    register_bnb_tools(mcp_app)
