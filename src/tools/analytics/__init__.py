from .whale import register_whale_tools
from .portfolio import register_portfolio_tools
from .valuation import register_valuation_tools
from .stablecoin import register_stablecoin_tools
from .analytics import register_analytics_tools as register_core_analytics
from .dominance import register_dominance_tools
from .fear_greed import register_fear_greed_tools
from .gas import register_gas_tools
from .news import register_news_tools
from .price import register_price_tools
from .nft_floor import register_nft_floor_tools
from .onchain import register_onchain_tools
from .mempool import register_mempool_tools
from .signal import register_signal_tools
from .liquidation import register_liquidation_tools
from .arbitrage import register_arbitrage_tools
from .exploit import register_exploit_tools
from .narrative import register_narrative_tools
from .heatmap import register_heatmap_tools
from .etf import register_etf_tools
from .macro import register_macro_tools
from .points import register_points_tools
# --- NEW ---
from .birdeye import register_birdeye_tools
from .defilama import register_defilama_tools
from .nansen import register_nansen_tools
from .dune import register_dune_tools

def register_analytics_tools(app):
    register_whale_tools(app)
    register_portfolio_tools(app)
    register_valuation_tools(app)
    register_stablecoin_tools(app)
    register_core_analytics(app)
    register_dominance_tools(app)
    register_fear_greed_tools(app)
    register_gas_tools(app)
    register_news_tools(app)
    register_price_tools(app)
    register_nft_floor_tools(app)
    register_onchain_tools(app)
    register_mempool_tools(app)
    register_signal_tools(app)
    register_liquidation_tools(app)
    register_arbitrage_tools(app)
    register_exploit_tools(app)
    register_narrative_tools(app)
    register_heatmap_tools(app)
    register_etf_tools(app)
    register_macro_tools(app)
    register_points_tools(app)
    # --- NEW ---
    register_birdeye_tools(app)
    register_defilama_tools(app)
    register_nansen_tools(app)
    register_dune_tools(app)
