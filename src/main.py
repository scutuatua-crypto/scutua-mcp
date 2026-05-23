"""
Scutua-MCP — WhaleTrucker Ecosystem V2 (Enterprise Standard)
Central Gateway Routing & Transport Protocol for 5-Dimensional Architecture.
"""
import asyncio
import os
from fastmcp import FastMCP
from src.utils.logger import get_logger

# ==========================================
# DIMENSION 1: Multi-Chain Universe
# ==========================================
from src.tools.chains.solana import register_solana_tools
from src.tools.chains.polkadot import register_polkadot_tools
from src.tools.chains.reef import register_reef_tools
from src.tools.chains.ton import register_ton_tools
from src.tools.chains.cosmos import register_cosmos_tools
from src.tools.chains.base import register_base_tools
from src.tools.chains.crosschain import register_crosschain_tools

# ==========================================
# DIMENSION 2: DeFi Protocol Universe
# ==========================================
from src.tools.protocols.jupiter import register_jupiter_tools
from src.tools.protocols.drift import register_drift_tools
from src.tools.protocols.mango import register_mango_tools
from src.tools.protocols.pump_fun import register_pump_fun_tools
from src.tools.protocols.raydium import register_raydium_tools
from src.tools.protocols.marinade import register_marinade_tools
from src.tools.protocols.uniswap import register_uniswap_tools
from src.tools.protocols.lido import register_lido_tools
from src.tools.protocols.defi import register_defi_tools
from src.tools.protocols.nft import register_nft_tools
from src.tools.protocols.staking import register_staking_tools
from src.tools.protocols.yield_optimizer import register_yield_tools
from src.tools.protocols.lending import register_lending_tools
from src.tools.protocols.bridge import register_bridge_tools
from src.tools.protocols.perp import register_perp_tools
from src.tools.protocols.dex import register_dex_tools
from src.tools.protocols.options import register_options_tools
from src.tools.protocols.dao import register_dao_tools
from src.tools.protocols.launchpad import register_launchpad_tools
from src.tools.protocols.insurance import register_insurance_tools
from src.tools.protocols.rwa import register_rwa_tools
from src.tools.protocols.aave_live import register_aave_live_tools

# ==========================================
# DIMENSION 3: Intelligence & Analytics Engine
# ==========================================
from src.tools.analytics.whale import register_whale_tools
from src.tools.analytics.portfolio import register_portfolio_tools
from src.tools.analytics.valuation import register_valuation_tools
from src.tools.analytics.stablecoin import register_stablecoin_tools
from src.tools.analytics.analytics import register_analytics_tools as core_analytics_loader
from src.tools.analytics.dominance import register_dominance_tools
from src.tools.analytics.fear_greed import register_fear_greed_tools
from src.tools.analytics.gas import register_gas_tools
from src.tools.analytics.news import register_news_tools
from src.tools.analytics.price import register_price_tools
from src.tools.analytics.nft_floor import register_nft_floor_tools
from src.tools.analytics.onchain import register_onchain_tools
from src.tools.analytics.mempool import register_mempool_tools
from src.tools.analytics.arbitrage import register_arbitrage_tools
from src.tools.analytics.exploit import register_exploit_tools
from src.tools.analytics.narrative import register_narrative_tools
from src.tools.analytics.heatmap import register_heatmap_tools
from src.tools.analytics.etf import register_etf_tools
from src.tools.analytics.macro import register_macro_tools
from src.tools.analytics.points import register_points_tools
from src.tools.analytics.signal import register_signal_tools
from src.tools.analytics.liquidation import register_liquidation_tools

# ==========================================
# DIMENSION 4: Operations & DevOps
# ==========================================
from src.tools.operations.github import register_github_tools
from src.tools.operations.tax import register_tax_tools
from src.tools.operations.tax_report import register_tax_report_tools
from src.tools.operations.converter import register_converter_tools
from src.tools.operations.alerts import register_alert_tools
from src.tools.operations.dashboard import register_dashboard_tools
from src.tools.operations.social import register_social_tools
from src.tools.operations.wallet import register_wallet_tools
from src.tools.operations.validator import register_validator_tools
from src.tools.operations.watchlist import register_watchlist_tools
from src.tools.operations.airdrop import register_airdrop_tools
from src.tools.operations.copy_trade import register_copy_trade_tools
from src.tools.operations.scam import register_scam_tools
from src.tools.operations.ens import register_ens_tools

# ==========================================
# DIMENSION 5: Market Intelligence
# ==========================================
from src.tools.market.coingecko import register_coingecko_tools
from src.tools.market.cmc import register_cmc_tools
from src.tools.market.trending import register_trending_tools
from src.tools.market.sentiment import register_sentiment_tools
from src.tools.market.fear_index import register_fear_index_tools

logger = get_logger(__name__)
port = int(os.environ.get("PORT", 10000))
app = FastMCP("scutua-mcp")

@app.custom_route("/", methods=["GET", "POST"])
async def home_health_check(request):
    from starlette.responses import PlainTextResponse
    return PlainTextResponse("WhaleTrucker Gateway Status: ONLINE & STABLE")

@app.custom_route("/.well-known/mcp/server-card.json", methods=["GET", "POST", "OPTIONS"])
async def server_card(request):
    from starlette.responses import JSONResponse
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }
    if request.method == "OPTIONS":
        return JSONResponse({}, headers=headers)
    return JSONResponse({
        "name": "scutua-mcp",
        "description": "WhaleTrucker MCP Server - Ultra Stable Multi-Chain Universe",
        "version": "2.0.0",
        "url": "https://scutua-mcp.onrender.com/mcp",
        "author": "scutuatua-crypto"
    }, headers=headers)

def bootstrap():
    # Dimension 1 Execution
    register_solana_tools(app)
    register_polkadot_tools(app)
    register_reef_tools(app)
    register_ton_tools(app)
    register_cosmos_tools(app)
    register_base_tools(app)
    register_crosschain_tools(app)
    
    # Dimension 2 Execution
    register_jupiter_tools(app)
    register_drift_tools(app)
    register_mango_tools(app)
    register_pump_fun_tools(app)
    register_raydium_tools(app)
    register_marinade_tools(app)
    register_uniswap_tools(app)
    register_lido_tools(app)
    register_aave_live_tools(app)
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
    
    # Dimension 3 Execution
    register_whale_tools(app)
    register_portfolio_tools(app)
    register_valuation_tools(app)
    register_stablecoin_tools(app)
    core_analytics_loader(app)
    register_dominance_tools(app)
    register_fear_greed_tools(app)
    register_gas_tools(app)
    register_news_tools(app)
    register_price_tools(app)
    register_nft_floor_tools(app)
    register_onchain_tools(app)
    register_mempool_tools(app)
    register_arbitrage_tools(app)
    register_exploit_tools(app)
    register_narrative_tools(app)
    register_heatmap_tools(app)
    register_etf_tools(app)
    register_macro_tools(app)
    register_points_tools(app)
    register_signal_tools(app)
    register_liquidation_tools(app)
    
    # Dimension 4 Execution
    register_github_tools(app)
    register_tax_tools(app)
    register_tax_report_tools(app)
    register_converter_tools(app)
    register_alert_tools(app)
    register_dashboard_tools(app)
    register_social_tools(app)
    register_wallet_tools(app)
    register_validator_tools(app)
    register_watchlist_tools(app)
    register_airdrop_tools(app)
    register_copy_trade_tools(app)
    register_scam_tools(app)
    register_ens_tools(app)
    
    # Dimension 5 Execution
    register_coingecko_tools(app)
    register_cmc_tools(app)
    register_trending_tools(app)
    register_sentiment_tools(app)
    register_fear_index_tools(app)
    
    logger.info("Scutua-MCP V2: 5-Dimensional Core Framework Loaded Successfully.")

async def main():
    bootstrap()
    await app.run_async(transport="streamable-http", host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(main())
