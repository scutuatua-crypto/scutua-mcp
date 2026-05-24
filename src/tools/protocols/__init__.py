from .jupiter import register_jupiter_tools
from .drift import register_drift_tools
from .mango import register_mango_tools
from .raydium import register_raydium_tools
from .marinade import register_marinade_tools
from .uniswap import register_uniswap_tools
from .lido import register_lido_tools
from .aave_live import register_aave_live_tools
from .pump_fun import register_pump_fun_tools
from .defi import register_defi_tools
from .nft import register_nft_tools
from .staking import register_staking_tools
from .yield_optimizer import register_yield_tools
from .lending import register_lending_tools
from .bridge import register_bridge_tools
from .perp import register_perp_tools
from .dex import register_dex_tools
from .options import register_options_tools
from .dao import register_dao_tools
from .launchpad import register_launchpad_tools
from .insurance import register_insurance_tools
from .rwa import register_rwa_tools

def register_protocols_tools(app):
    register_jupiter_tools(app)
    register_drift_tools(app)
    register_mango_tools(app)
    register_raydium_tools(app)
    register_marinade_tools(app)
    register_uniswap_tools(app)
    register_lido_tools(app)
    register_aave_live_tools(app)
    register_pump_fun_tools(app)
    register_defi_tools(app)
    register_nft_tools(app)
    register_staking_tools(app)
    register_yield_tools(app)
    register_lending_tools(app)
    register_bridge_tools(app)
    register_perp_tools(app)
    register_dex_tools(app)
    register_options_tools(app)
    register_dao_tools(app)
    register_launchpad_tools(app)
    register_insurance_tools(app)
    register_rwa_tools(app)
