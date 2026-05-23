"""
🐋 Scutua-MCP — WhaleTrucker Ecosystem V2 (Enterprise Standard)
Zero-Trust Multi-Chain MCP Server 
Powered by: Nokia 3310 Turbo + Claude AI 💙
"""
import asyncio
import os
from fastmcp import FastMCP
from src.utils.logger import get_logger

from src.tools.solana import register_solana_tools
from src.tools.polkadot import register_polkadot_tools
from src.tools.reef import register_reef_tools
from src.tools.ton import register_ton_tools
from src.tools.cosmos import register_cosmos_tools
from src.tools.base import register_base_tools
from src.tools.crosschain import register_crosschain_tools
from src.tools.github import register_github_tools
from src.tools.valuation import register_valuation_tools
from src.tools.stablecoin import register_stablecoin_tools
from src.tools.dashboard import register_dashboard_tools
from src.tools.alerts import register_alert_tools
from src.tools.analytics import register_analytics_tools as core_analytics_loader
from src.tools.defi import register_defi_tools
from src.tools.nft import register_nft_tools
from src.tools.gas import register_gas_tools
from src.tools.news import register_news_tools
from src.tools.converter import register_converter_tools
from src.tools.staking import register_staking_tools
from src.tools.arbitrage import register_arbitrage_tools
from src.tools.wallet import register_wallet_tools
from src.tools.yield_optimizer import register_yield_tools
from src.tools.price import register_price_tools
from src.tools.whale import register_whale_tools
from src.tools.portfolio import register_portfolio_tools
from src.tools.lending import register_lending_tools
from src.tools.bridge import register_bridge_tools
from src.tools.tax import register_tax_tools
from src.tools.signal import register_signal_tools
from src.tools.nft_floor import register_nft_floor_tools
from src.tools.liquidation import register_liquidation_tools
from src.tools.social import register_social_tools
from src.tools.validator import register_validator_tools
from src.tools.mempool import register_mempool_tools
from src.tools.watchlist import register_watchlist_tools
from src.tools.perp import register_perp_tools
from src.tools.onchain import register_onchain_tools
from src.tools.dex import register_dex_tools
from src.tools.options import register_options_tools
from src.tools.rwa import register_rwa_tools
from src.tools.insurance import register_insurance_tools
from src.tools.launchpad import register_launchpad_tools
from src.tools.dao import register_dao_tools
from src.tools.airdrop import register_airdrop_tools
from src.tools.macro import register_macro_tools
from src.tools.scam import register_scam_tools
from src.tools.copy_trade import register_copy_trade_tools
from src.tools.etf import register_etf_tools
from src.tools.heatmap import register_heatmap_tools
from src.tools.exploit import register_exploit_tools
from src.tools.narrative import register_narrative_tools
from src.tools.tax_report import register_tax_report_tools
from src.tools.dominance import register_dominance_tools
from src.tools.points import register_points_tools
from src.tools.jupiter import register_jupiter_tools
from src.tools.drift import register_drift_tools
from src.tools.mango import register_mango_tools
from src.tools.pump_fun import register_pump_fun_tools
from src.tools.raydium import register_raydium_tools
from src.tools.marinade import register_marinade_tools
from src.tools.uniswap import register_uniswap_tools
from src.tools.lido import register_lido_tools
from src.tools.ens import register_ens_tools
from src.tools.aave_live import register_aave_live_tools
from src.tools.fear_greed import register_fear_greed_tools
from src.tools.market import (
    register_coingecko_tools,
    register_cmc_tools,
    register_trending_tools,
    register_sentiment_tools,
    register_fear_index_tools,
)

logger = get_logger(__name__)
port = int(os.environ.get("PORT", 10000))
app = FastMCP("scutua-mcp")

@app.custom_route("/", methods=["GET", "POST"])
async def home_health_check(request):
    from starlette.responses import PlainTextResponse
    return PlainTextResponse("🐋 WhaleTrucker Gateway Status: ONLINE & STABLE")

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
    register_solana_tools(app)
    register_polkadot_tools(app)
    register_reef_tools(app)
    register_ton_tools(app)
    register_cosmos_tools(app)
    register_base_tools(app)
    register_crosschain_tools(app)
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
    register_scam_tools(app)
    register_arbitrage_tools(app)
    register_exploit_tools(app)
    register_narrative_tools(app)
    register_heatmap_tools(app)
    register_etf_tools(app)
    register_macro_tools(app)
    register_points_tools(app)
    register_github_tools(app)
    register_tax_tools(app)
    register_tax_report_tools(app)
    register_converter_tools(app)
    register_alert_tools(app)
    register_dashboard_tools(app)
    register_social_tools(app)
    register_wallet_tools(app)
    register_signal_tools(app)
    register_liquidation_tools(app)
    register_validator_tools(app)
    register_watchlist_tools(app)
    register_airdrop_tools(app)
    register_copy_trade_tools(app)
    register_ens_tools(app)
    register_coingecko_tools(app)
    register_cmc_tools(app)
    register_trending_tools(app)
    register_sentiment_tools(app)
    register_fear_index_tools(app)
    logger.info("🐋 Scutua-MCP V2: Core Framework Loaded Successfully.")

async def main():
    bootstrap()
    await app.run_async(transport="streamable-http", host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(main())
