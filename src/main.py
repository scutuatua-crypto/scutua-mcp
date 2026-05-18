"""
🐋 Scutua-MCP — WhaleTrucker Ecosystem
Zero-Trust Multi-Chain MCP Server
Powered by: โนเกีย 3310 พลังลม + Claude AI 💙
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from src.tools.github import register_github_tools
from src.tools.solana import register_solana_tools
from src.tools.polkadot import register_polkadot_tools
from src.tools.reef import register_reef_tools
from src.tools.valuation import register_valuation_tools
from src.tools.stablecoin import register_stablecoin_tools
from src.utils.logger import get_logger
from src.utils.security import verify_env

logger = get_logger(__name__)

app = Server("scutua-mcp")

def bootstrap():
    verify_env()
    register_github_tools(app)
    register_solana_tools(app)
    register_polkadot_tools(app)
    register_reef_tools(app)
    register_valuation_tools(app)
    register_stablecoin_tools(app)
    logger.info("🐋 Scutua-MCP server ready")

async def main():
    bootstrap()
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())

