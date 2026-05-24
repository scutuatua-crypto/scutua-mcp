from .jupiter import register_jupiter_tools
from .drift import register_drift_tools
from .mango import register_mango_tools
from .raydium import register_raydium_tools
from .marinade import register_marinade_tools
from .uniswap import register_uniswap_tools
from .lido import register_lido_tools
from .aave_live import register_aave_live_tools

def register_protocols_tools(app):
    register_jupiter_tools(app)
    register_drift_tools(app)
    register_mango_tools(app)
    register_raydium_tools(app)
    register_marinade_tools(app)
    register_uniswap_tools(app)
    register_lido_tools(app)
    register_aave_live_tools(app)
