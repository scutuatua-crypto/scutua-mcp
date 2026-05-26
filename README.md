# 🐋 Scutua-MCP

[![Deploy](https://img.shields.io/badge/Render-Live-brightgreen?logo=render)](https://scutua-mcp.onrender.com)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.3.1-blue?logo=python)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)](https://python.org)
[![Tools](https://img.shields.io/badge/Tools-152-orange)](https://github.com/scutuatua-crypto/scutua-mcp)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)
[![Claude](https://img.shields.io/badge/Claude.ai-Connected-orange?logo=anthropic)](https://claude.ai)
[![smithery badge](https://smithery.ai/badge/scutuatua/scutua-mcp)](https://smithery.ai/servers/scutuatua/scutua-mcp)
[![Quality](https://img.shields.io/badge/Smithery_Score-84%2F100-brightgreen)](https://smithery.ai/servers/scutuatua/scutua-mcp)

> **Model Context Protocol Server** — WhaleTrucker Ecosystem V2
> Built with Python | FastMCP 3.3.1 | Streamable HTTP Transport
> Live: `https://scutua-mcp.onrender.com/mcp`

---

## Overview

Scutua-MCP is a production MCP server powering the WhaleTrucker Ecosystem.

**152 tools** across **7 dimensions** — the world's first Agentic DeFi MCP server.

Not just data retrieval. **Get → Think → Act → Notify.**

Connected to Claude.ai and Smithery. Deployed from iPad. No PC required. 😤

---

## Architecture — 7 Dimensions

| Dimension | Folder | Tools | Coverage |
|-----------|--------|-------|----------|
| 🌐 Multi-Chain Universe | `src/tools/chains/` | 11 | Solana, Ethereum, Arbitrum, Optimism, BNB, Polkadot, Reef, TON, Cosmos, Base, CrossChain |
| ⚡ DeFi Protocol Universe | `src/tools/protocols/` | 26 | Jupiter, Drift, Uniswap, Lido, Aave, Curve, Compound, GMX, Pendle, and more |
| 🧠 Intelligence & Analytics | `src/tools/analytics/` | 26 | Whale tracking, Birdeye, DeFiLlama, Nansen, Dune, Price feeds, Fear & Greed |
| 🛠️ Operations & DevOps | `src/tools/operations/` | 17 | GitHub, Tax, Wallet, Alerts, Telegram, Discord, Portfolio Tracker |
| 📊 Market Intelligence | `src/tools/market/` | 8 | CoinGecko, CMC, Trending, Sentiment, Kaito, LunarCrush, Alternative.me |
| 🤖 Agentic Layer | `src/tools/agentic/` | 5 | Arbitrage Scanner, Whale Alert, Portfolio Autopilot, Sentiment Signal |
| ⚡ Execution Layer | `src/tools/execution/` | 18 | Swap, Limit Order, DCA, Stop Loss, Rebalance, Sniper, Emergency Exit |

---

## Agentic Flow

```
Market Data (Dim 1-5)
       ↓
Sentiment Signal → BUY / SELL / HOLD
       ↓
Claude AI Decision Engine
       ↓
Execute: Swap / DCA / Limit Order / Stop Loss
       ↓
Telegram Alert → Confirmed
```

---

## Project Structure

```
src/
├── tools/
│   ├── registry.py
│   ├── chains/          # 🌐 Dimension 1 (11 chains)
│   ├── protocols/       # ⚡ Dimension 2 (26 protocols)
│   ├── analytics/       # 🧠 Dimension 3 (26 tools)
│   ├── operations/      # 🛠️ Dimension 4 (17 tools)
│   ├── market/          # 📊 Dimension 5 (8 tools)
│   ├── agentic/         # 🤖 Dimension 6 (5 tools)
│   └── execution/       # ⚡ Dimension 7 (18 tools)
│       ├── swap_executor.py
│       ├── limit_order.py
│       ├── dca_engine.py
│       ├── stop_loss.py
│       ├── auto_rebalance.py
│       ├── sniper.py
│       └── emergency_exit.py
├── utils/
│   ├── logger.py / security.py / cache.py
│   └── rate_limiter.py / validator.py
├── config/
│   └── settings.py
├── tests/
└── main.py
```

---

## Environment Variables

| Variable | Description | Status |
|----------|-------------|--------|
| `BIRDEYE_API_KEY` | Birdeye — Solana token data | ✅ |
| `DUNE_API_KEY` | Dune Analytics — on-chain queries | ✅ |
| `GH_TOKEN` | GitHub — repo operations | ✅ |
| `LUNARCRUSH_API_KEY` | LunarCrush — social sentiment | ✅ |
| `SOLANA_API` | Solana RPC endpoint | ✅ |
| `SOLANA_WALLET_PRIVATE_KEY` | Solana trading wallet | ✅ |
| `TELEGRAM_BOT_TOKEN` | Telegram bot alerts | ✅ |
| `TELEGRAM_CHANNEL_ID` | Telegram channel target | ✅ |

---

## Execution Layer Safety

Every execution tool is built with safety-first design:

- `dry_run=True` by default — simulate before real execution
- Telegram alert before AND after every trade
- Safety score check before sniping
- `confirmed=True` required for emergency exit
- Dedicated trading wallet — never use main wallet

---

## Status

- ✅ Render: Live
- ✅ Smithery: Published (Score: 84/100)
- ✅ Claude.ai: Connected (152 tools)
- ✅ Transport: Streamable HTTP (FastMCP 3.3.1)
- ✅ Architecture: 7-Dimensional V2
- ✅ CI/CD: GitHub Actions (1,300+ runs)
- ✅ Execution Layer: Live (Swap, DCA, Stop Loss, Sniper)

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

---

## WhaleTrucker Standard

> *"No Money, No Honey"* 🚚💿
> **Too fast for the API, too safe for the chain.**
> **Powered by: Nokia 3310 Wind Power + Claude AI** 💙💨

*Deployed from iPad. No PC required. 😤*
