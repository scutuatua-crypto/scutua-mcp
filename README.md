# 🐋 Scutua-MCP

[![Deploy](https://img.shields.io/badge/Render-Live-brightgreen?logo=render)](https://scutua-mcp.onrender.com)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.3.1-blue?logo=python)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)](https://python.org)
[![Tools](https://img.shields.io/badge/Tools-157-orange)](https://github.com/scutuatua-crypto/scutua-mcp)
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

**157 tools** across **8 dimensions** — the world's first Self-Aware Agentic DeFi MCP server.

Not just data retrieval. **Get → Think → Act → Notify → Know Thyself.**

Connected to Claude.ai and Smithery. Deployed from iPad. No PC required. 😤

---

## Architecture — 8 Dimensions

| Dimension | Folder | Tools | Coverage |
|-----------|--------|-------|----------|
| 🌐 Multi-Chain Universe | `src/tools/chains/` | 11 | Solana, Ethereum, Arbitrum, Optimism, BNB, Polkadot, Reef, TON, Cosmos, Base, CrossChain |
| ⚡ DeFi Protocol Universe | `src/tools/protocols/` | 26 | Jupiter, Drift, Uniswap, Lido, Aave, Curve, Compound, GMX, Pendle, and more |
| 🧠 Intelligence & Analytics | `src/tools/analytics/` | 26 | Whale tracking, Birdeye, DeFiLlama, Nansen, Dune, Price feeds, Fear & Greed |
| 🛠️ Operations & DevOps | `src/tools/operations/` | 17 | GitHub, Tax, Wallet, Alerts, Telegram, Discord, Portfolio Tracker |
| 📊 Market Intelligence | `src/tools/market/` | 8 | CoinGecko, CMC, Trending, Sentiment, Kaito, LunarCrush, Alternative.me |
| 🤖 Agentic Layer | `src/tools/agentic/` | 5 | Arbitrage Scanner, Whale Alert, Portfolio Autopilot, Sentiment Signal |
| ⚡ Execution Layer | `src/tools/execution/` | 18 | Swap, Limit Order, DCA, Stop Loss, Rebalance, Sniper, Emergency Exit |
| 🌌 Ecosystem Consciousness | `src/tools/ecosystem/` | 5 | Heartbeat, Biometrics, Intelligence, Narrative, What Should I Build |

---

## Agentic Flow

```text
Market Data (Dim 1-5)
       ↓
Sentiment Signal → BUY / SELL / HOLD
       ↓
Claude AI Decision Engine
       ↓
Execute: Swap / DCA / Limit Order / Stop Loss
       ↓
Telegram Alert → Confirmed
       ↓
Ecosystem Consciousness → Self-Aware 🌌

## Project Structure — Linked to Dimensions

src/
├── tools/
│   ├── registry.py
│   ├── chains/          # 🌐 Dimension 1 — Multi-Chain Universe (11 chains)
│   ├── protocols/       # ⚡ Dimension 2 — DeFi Protocol Universe (26 protocols)
│   ├── analytics/       # 🧠 Dimension 3 — Intelligence & Analytics (26 tools)
│   ├── operations/      # 🛠️ Dimension 4 — Operations & DevOps (17 tools)
│   ├── market/          # 📊 Dimension 5 — Market Intelligence (8 tools)
│   ├── agentic/         # 🤖 Dimension 6 — Agentic Layer (5 tools)
│   ├── execution/       # ⚡ Dimension 7 — Execution Layer (18 tools)
│   │   ├── swap_executor.py
│   │   ├── limit_order.py
│   │   ├── dca_engine.py
│   │   ├── stop_loss.py
│   │   ├── auto_rebalance.py
│   │   ├── sniper.py
│   │   └── emergency_exit.py
│   └── ecosystem/       # 🌌 Dimension 8 — Ecosystem Consciousness (5 tools)
│       ├── heartbeat.py
│       ├── biometrics.py
│       ├── intelligence.py
│       ├── narrative.py
│       └── data/ecosystem.json
├── utils/               # Shared utilities (logger, security, cache, rate limiter, validator)
├── config/              # Global settings
├── tests/               # Unit & integration tests
└── main.py              # Entry point

Environment Variables
Every execution tool is built with safety-first design:
	•	dry_run=True by default — simulate before real execution
	•	Telegram alert before AND after every trade
	•	Safety score check before sniping
	•	confirmed=True required for emergency exit
	•	Dedicated trading wallet — never use main wallet

Status
	•	✅ Render: Live
	•	✅ Smithery: Published (Score: 84/100)
	•	✅ Claude.ai: Connected (157 tools)
	•	✅ Transport: Streamable HTTP (FastMCP 3.3.1)
	•	✅ Architecture: 8-Dimensional V2
	•	✅ CI/CD: GitHub Actions (1,300+ runs)
	•	✅ Execution Layer: Live (Swap, DCA, Stop Loss, Sniper)
	•	✅ Ecosystem Consciousness: Live 🌌

Quick Connect
Claude.ai
	1.	Settings → Customize → Connectors → Add custom connector
	2.	Name: Scutua-MCP
	3.	URL: https://scutua-mcp.onrender.com/mcp

VS Code / Cursor

{
  "mcpServers": {
    "scutua-mcp": {
      "url": "https://scutua-mcp.onrender.com/mcp"
    }
  }
}

Smithery
https://smithery.ai/servers/scutuatua/scutua-mcp

WhaleTrucker Standard
“No Money, No Honey” 🚚💿
Too fast for the API, too safe for the chain.
Powered by: Nokia 3310 Wind Power + Claude AI 💙💨
