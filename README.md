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

## Architecture — 5 Dimensions

| Dimension | Folder | Coverage |
|-----------|--------|----------|
| 🌐 Multi-Chain Universe | `src/tools/chains/` | Solana, Polkadot, Reef, TON, Cosmos, Base, CrossChain |
| ⚡ DeFi Protocol Universe | `src/tools/protocols/` | Jupiter, Drift, Uniswap, Lido, Aave, Curve, Compound, GMX, and more |
| 🧠 Intelligence & Analytics | `src/tools/analytics/` | Whale tracking, Portfolio, Price feeds, Fear & Greed, LunarCrush |
| 🛠️ Operations & DevOps | `src/tools/operations/` | GitHub, Tax, Wallet, Alerts, Telegram, Dune Analytics |
| 📊 Market Intelligence | `src/tools/market/` | CoinGecko, CMC, Trending, Sentiment, ETF, NFT floors |

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
- ✅ README: Synced  

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
