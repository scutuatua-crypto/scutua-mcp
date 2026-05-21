"""
🐋 Scutua-MCP — WhaleTrucker Ecosystem V2 (Enterprise Standard)
Zero-Trust Multi-Chain MCP Server 
Powered by: Nokia 3310 Turbo + Claude AI 💙
"""
import asyncio
import os
from fastmcp import FastMCP
from src.utils.logger import get_logger
from src.utils.security import verify_env

# Import all tools from legacy structure
from src.tools.github import register_github_tools
from src.tools.solana import register_solana_tools
from src.tools.polkadot import register_polkadot_tools
from src.tools.reef import register_reef_tools
from src.tools.valuation import register_valuation_tools
from src.tools.stablecoin import register_stablecoin_tools
from src.tools.ton import register_ton_tools
from src.tools.cosmos import register_cosmos_tools
from src.tools.base import register_base_tools
from src.tools.dashboard import register_dashboard_tools
from src.tools.alerts import register_alert_tools
from src.tools.analytics import register_analytics_tools
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
from src.tools.crosschain import register_crosschain_tools
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

logger = get_logger(__name__)
port = int(os.environ.get("PORT", 10000))
app = FastMCP("scutua-mcp")

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
        "url": "https://scutua-mcp.onrender.com/sse",
        "author": "scutuatua-crypto",
        "license": "MIT"
    }, headers=headers)

# 🛠️ Modular Domains Mapping
def register_chain_tools(mcp_app):
    """Domain 1: Layer 1 / Layer 2 Networks"""
    register_solana_tools(mcp_app)
    register_polkadot_tools(mcp_app)
    register_reef_tools(mcp_app)
    register_ton_tools(mcp_app)
    register_cosmos_tools(mcp_app)
    register_base_tools(mcp_app)
    register_crosschain_tools(mcp_app)

def register_protocol_tools(mcp_app):
    """Domain 2: DeFi / DEX / Smart Contracts"""
    register_jupiter_tools(mcp_app)
    register_drift_tools(mcp_app)
    register_mango_tools(mcp_app)
    register_pump_fun_tools(mcp_app)
    register_raydium_tools(mcp_app)
    register_marinade_tools(mcp_app)
    register_uniswap_tools(mcp_app)
    register_lido_tools(mcp_app)
    register_aave_live_tools(mcp_app)
    register_defi_tools(mcp_app)
    register_nft_tools(mcp_app)
    register_staking_tools(mcp_app)
    register_yield_tools(mcp_app)
    register_lending_tools(mcp_app)
    register_bridge_tools(mcp_app)
    register_perp_tools(mcp_app)
    register_dex_tools(mcp_app)
    register_options_tools(mcp_app)
    register_dao_tools(mcp_app)
    register_launchpad_tools(mcp_app)

def register_analytics_tools(mcp_app):
    """Domain 3: On-Chain Analytics & Intelligence Engines"""
    register_whale_tools(mcp_app)
    register_portfolio_tools(mcp_app)
    register_valuation_tools(mcp_app)
    register_stablecoin_tools(mcp_app)
    register_analytics_tools(mcp_app)
    register_dominance_tools(mcp_app)
    register_fear_greed_tools(mcp_app)
    register_gas_tools(mcp_app)
    register_news_tools(mcp_app)
    register_price_tools(mcp_app)
    register_nft_floor_tools(mcp_app)
    register_onchain_tools(mcp_app)
    register_mempool_tools(mcp_app)
    register_scam_tools(mcp_app)
    register_arbitrage_tools(mcp_app)
    register_exploit_tools(mcp_app)
    register_narrative_tools(mcp_app)
    register_heatmap_tools(mcp_app)
    register_etf_tools(mcp_app)
    register_macro_tools(mcp_app)

def register_operation_tools(mcp_app):
    """Domain 4: DevOps, Financial & Operations Management"""
    register_github_tools(mcp_app)
    register_tax_tools(mcp_app)
    register_tax_report_tools(mcp_app)
    register_converter_tools(mcp_app)
    register_alerts_tools(mcp_app)
    register_dashboard_tools(mcp_app)
    register_social_tools(mcp_app)
    register_wallet_tools(mcp_app)
    register_signal_tools(mcp_app)
    register_liquidation_tools(mcp_app)
    register_validator_tools(mcp_app)
    register_watchlist_tools(mcp_app)
    register_airdrop_tools(mcp_app)
    register_copy_trade_tools(mcp_app)
    register_ens_tools(mcp_app)

def bootstrap():
    verify_env()
    
    # Initialize structured registry sequentially
    register_chain_tools(app)
    register_protocol_tools(app)
    register_analytics_tools(app)
    register_operation_tools(app)
    
    logger.info("🐋 Scutua-MCP V2: Core Framework Loaded Successfully.")

async def main():
    bootstrap()
    await app.run_async(transport="sse", host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(main())
