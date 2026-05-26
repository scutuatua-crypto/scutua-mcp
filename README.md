# 🐋 Scutua-MCP

[![Deploy](https://img.shields.io/badge/Render-Live-brightgreen?logo=render)](https://scutua-mcp.onrender.com)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.3.1-blue?logo=python)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)
[![Claude](https://img.shields.io/badge/Claude.ai-Connected-orange?logo=anthropic)](https://claude.ai)
[![smithery badge](https://smithery.ai/badge/scutuatua/scutua-mcp)](https://smithery.ai/servers/scutuatua/scutua-mcp)

> **Model Context Protocol Server** — WhaleTrucker Ecosystem V2  
> Built with Python | FastMCP 3.3.1 | Streamable HTTP Transport  
> Live: `https://scutua-mcp.onrender.com/mcp`

---

## Overview

Scutua-MCP is a production MCP server powering the WhaleTrucker Ecosystem.  
**130 tools** across 5 dimensions: Multi-Chain, DeFi Protocols, Analytics, Operations, and Market Intelligence — connected to Claude.ai and Smithery.

---

## Architecture — 6 Dimensions

| Dimension | Folder | Tools | Coverage |
|-----------|--------|-------|----------|
| 🌐 Multi-Chain Universe | `src/tools/chains/` | 11 | Solana, Ethereum, Arbitrum, Optimism, BNB, Polkadot, Reef, TON, Cosmos, Base, CrossChain |
| ⚡ DeFi Protocol Universe | `src/tools/protocols/` | 26 | Jupiter, Drift, Uniswap, Lido, Aave, Curve, Compound, GMX, Pendle, and more |
| 🧠 Intelligence & Analytics | `src/tools/analytics/` | 26 | Whale tracking, Birdeye, DeFiLlama, Nansen, Dune, Price feeds, Fear & Greed |
| 🛠️ Operations & DevOps | `src/tools/operations/` | 17 | GitHub, Tax, Wallet, Alerts, Telegram, Discord, Portfolio Tracker |
| 📊 Market Intelligence | `src/tools/market/` | 8 | CoinGecko, CMC, Trending, Sentiment, Kaito, LunarCrush, Alternative.me |
| 🤖 Agentic Layer | `src/tools/agentic/` | 4 | Arbitrage, Whale Alert, Autopilot, Sentiment |

---

## Project Structure

```
src/
├── tools/
│   ├── registry.py                # Master registry
│   ├── chains/                    # 🌐 Dimension 1 (11 chains)
│   │   ├── solana.py
│   │   ├── ethereum.py
│   │   ├── arbitrum.py
│   │   ├── optimism.py
│   │   ├── bnb.py
│   │   ├── polkadot.py
│   │   ├── reef.py
│   │   ├── ton.py
│   │   ├── cosmos.py
│   │   ├── base.py
│   │   └── crosschain.py
│   ├── protocols/                 # ⚡ Dimension 2 (26 protocols)
│   │   ├── jupiter.py / drift.py / mango.py / pump_fun.py
│   │   ├── raydium.py / marinade.py / uniswap.py / lido.py
│   │   ├── aave_live.py / curve.py / compound.py / gmx.py
│   │   ├── pendle.py / defi.py / nft.py / staking.py
│   │   ├── yield_optimizer.py / lending.py / bridge.py
│   │   └── perp.py / dex.py / options.py / dao.py / launchpad.py / insurance.py / rwa.py
│   ├── analytics/                 # 🧠 Dimension 3 (26 tools)
│   │   ├── whale.py / portfolio.py / valuation.py / stablecoin.py
│   │   ├── analytics.py / dominance.py / fear_greed.py / gas.py
│   │   ├── news.py / price.py / nft_floor.py / onchain.py
│   │   ├── mempool.py / signal.py / liquidation.py / arbitrage.py
│   │   ├── exploit.py / narrative.py / heatmap.py / etf.py
│   │   ├── macro.py / points.py
│   │   └── birdeye.py / defilama.py / nansen.py / dune.py
│   ├── operations/                # 🛠️ Dimension 4 (17 tools)
│   │   ├── github.py / tax.py / tax_report.py / converter.py
│   │   ├── alerts.py / dashboard.py / social.py / wallet.py
│   │   ├── validator.py / watchlist.py / airdrop.py / copy_trade.py
│   │   ├── scam.py / ens.py
│   │   └── telegram.py / discord.py / portfolio_tracker.py
│   └── market/                    # 📊 Dimension 5 (8 tools)
│       ├── coingecko.py / cmc.py / trending.py
│       ├── sentiment.py / fear_index.py
│       └── kaito.py / lunarcrush.py / alternative.py
├── utils/
│   ├── logger.py / security.py / cache.py
│   ├── rate_limiter.py / validator.py
├── config/
│   └── settings.py
├── tests/
│   ├── test_chains.py / test_protocols.py
│   ├── test_analytics.py / test_operations.py / test_market.py
└── main.py
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BIRDEYE_API_KEY` | Birdeye — Solana token data |
| `DUNE_API_KEY` | Dune Analytics — on-chain queries |
| `GH_TOKEN` | GitHub — repo operations |
| `LUNARCRUSH_API_KEY` | LunarCrush — social sentiment |
| `SOLANA_API` | Solana RPC endpoint |
| `TELEGRAM_BOT_TOKEN` | Telegram bot alerts |
| `TELEGRAM_CHANNEL_ID` | Telegram channel target |

---

## Status

- ✅ Render: Live  
- ✅ Smithery: Published  
- ✅ Claude.ai: Connected (130 tools)  
- ✅ Transport: Streamable HTTP (FastMCP 3.3.1)  
- ✅ Architecture: 5-Dimensional V2  
- ✅ CI/CD: GitHub Actions (1,298+ runs)  

---

## Quick Connect

### Claude.ai
1. Settings → Customize → Connectors → **Add custom connector**
2. Name: `Scutua-MCP`
3. URL: `https://scutua-mcp.onrender.com/mcp`

### VS Code / Cursor
```json
{
  "mcpServers": {
    "scutua-mcp": {
      "url": "https://scutua-mcp.onrender.com/mcp"
    }
  }
}
```

### Smithery
[https://smithery.ai/servers/scutuatua/scutua-mcp](https://smithery.ai/servers/scutuatua/scutua-mcp)
