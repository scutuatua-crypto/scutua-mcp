# 🐋 Scutua-MCP

[![Deploy](https://img.shields.io/badge/Render-Live-brightgreen?logo=render)](https://scutua-mcp.onrender.com)
[![MCP](https://img.shields.io/badge/MCP-1.27.1-blue?logo=python)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)
[![Claude](https://img.shields.io/badge/Claude.ai-Connected-orange?logo=anthropic)](https://claude.ai)

> **Model Context Protocol Server** — WhaleTrucker Ecosystem
> Built with Python | Zero-Trust Security | Multi-Chain Ready
> Live: `https://scutua-mcp.onrender.com/sse`

---

## Overview

Scutua-MCP is a private MCP server powering the WhaleTrucker Ecosystem.
Connecting GitHub, Solana, Polkadot, Reef, and Stablecoin data into one secure AI-ready interface.

---

## Quick Connect

### Claude.ai
1. Settings → Customize → Connectors → **Add custom connector**
2. Name: `Scutua-MCP`
3. URL: `https://scutua-mcp.onrender.com/sse`

### VS Code / Cursor
```json
{
  "mcpServers": {
    "scutua-mcp": {
      "url": "https://scutua-mcp.onrender.com/sse"
    }
  }
}
