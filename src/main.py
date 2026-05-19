"""
🐋 Scutua-MCP — WhaleTrucker Ecosystem
Zero-Trust Multi-Chain MCP Server
Powered by: โนเกีย 3310 พลังลม + Claude AI 💙
"""
import asyncio
import os
from mcp.server.fastmcp import FastMCP
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
from src.tools.price import register_price_tools
from src.tools.whale import register_whale_tools
from src.tools.portfolio import register_portfolio_tools
from src.utils.logger import get_logger
from src.utils.security import verify_env

logger = get_logger(__name__)
port = int(os.environ.get("PORT", 10000))
app = FastMCP("scutua-mcp", host="0.0.0.0", port=port)

def bootstrap():
    verify_env()
    register_github_tools(app)
    register_solana_tools(app)
    register_polkadot_tools(app)
    register_reef_tools(app)
    register_valuation_tools(app)
    register_stablecoin_tools(app)
    register_ton_tools(app)
    register_cosmos_tools(app)
    register_base_tools(app)
    register_dashboard_tools(app)
    register_alert_tools(app)
    register_analytics_tools(app)
    register_price_tools(app)
    register_whale_tools(app)
    register_portfolio_tools(app)
    logger.info("🐋 Scutua-MCP server ready")

async def main():
    bootstrap()
    await app.run_sse_async()

if __name__ == "__main__":
    asyncio.run(main())
