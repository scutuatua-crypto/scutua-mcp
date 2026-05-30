#!/usr/bin/env node

/**
 * scutua-mcp
 * WhaleTrucker MCP Server — 157 tools across 8 Dimensions
 * 
 * This package provides connection info and a quick-connect helper
 * for the Scutua MCP server hosted at https://scutua-mcp.onrender.com/mcp
 * 
 * Usage:
 *   npx scutua-mcp            → prints connection instructions
 *   npx scutua-mcp --config   → outputs Claude Desktop JSON config
 *   npx scutua-mcp --test     → tests if the MCP server is reachable
 */

const https = require("https");
const args = process.argv.slice(2);

const MCP_URL = "https://scutua-mcp.onrender.com/mcp";
const REPO_URL = "https://github.com/scutuatua-crypto/scutua-mcp";
const SMITHERY_URL = "https://smithery.ai/servers/scutuatua/scutua-mcp";

const CLAUDE_CONFIG = {
  mcpServers: {
    "scutua-mcp": {
      url: MCP_URL
    }
  }
};

const VSCODE_CONFIG = {
  mcpServers: {
    "scutua-mcp": {
      url: MCP_URL
    }
  }
};

function printBanner() {
  console.log(`
🐋 ============================================
   SCUTUA-MCP — WhaleTrucker Ecosystem V2
   157 tools | 8 Dimensions | Avalanche + DeFi
   Built from iPad. No PC required. 😤
🐋 ============================================
`);
}

function printHelp() {
  printBanner();
  console.log(`MCP Server URL:
  ${MCP_URL}

Quick Connect:

  Claude Desktop  →  add to claude_desktop_config.json:
  Claude.ai       →  Settings → Integrations → Add custom connector
  VS Code/Cursor  →  add to .vscode/mcp.json

Run with flags:
  npx scutua-mcp --config    Print Claude Desktop JSON config
  npx scutua-mcp --vscode    Print VS Code/Cursor JSON config  
  npx scutua-mcp --test      Test if MCP server is reachable
  npx scutua-mcp --info      Show all 8 dimensions

Links:
  Repo      ${REPO_URL}
  Smithery  ${SMITHERY_URL}
`);
}

function printConfig() {
  printBanner();
  console.log("📋 Claude Desktop config (claude_desktop_config.json):\n");
  console.log(JSON.stringify(CLAUDE_CONFIG, null, 2));
  console.log("\nPath: ~/Library/Application Support/Claude/claude_desktop_config.json\n");
}

function printVSCode() {
  printBanner();
  console.log("📋 VS Code / Cursor config (.vscode/mcp.json):\n");
  console.log(JSON.stringify(VSCODE_CONFIG, null, 2));
}

function printInfo() {
  printBanner();
  console.log(`8 Dimensions — 157 Tools Total:

  🌐 Dimension 1 — Multi-Chain Universe    (11 tools)
     Solana, Ethereum, Arbitrum, Optimism, BNB,
     Polkadot, Reef, TON, Cosmos, Base, CrossChain

  ⚡ Dimension 2 — DeFi Protocol Universe  (26 tools)
     Jupiter, Drift, Uniswap, Lido, Aave, Curve,
     Compound, GMX, Pendle, and more

  🧠 Dimension 3 — Intelligence & Analytics (26 tools)
     Whale tracking, Birdeye, DeFiLlama, Nansen,
     Dune, Price feeds, Fear & Greed

  🛠️  Dimension 4 — Operations & DevOps    (17 tools)
     GitHub, Tax, Wallet, Alerts, Telegram, Discord,
     Portfolio Tracker

  📊 Dimension 5 — Market Intelligence     (8 tools)
     CoinGecko, CMC, Trending, Sentiment, Kaito,
     LunarCrush, Alternative.me

  🤖 Dimension 6 — Agentic Layer           (5 tools)
     Arbitrage Scanner, Whale Alert,
     Portfolio Autopilot, Sentiment Signal

  ⚡ Dimension 7 — Execution Layer         (18 tools)
     Swap, Limit Order, DCA, Stop Loss,
     Rebalance, Sniper, Emergency Exit

  🌌 Dimension 8 — Ecosystem Consciousness (5 tools)
     Heartbeat, Biometrics, Intelligence,
     Narrative, What Should I Build
`);
}

function testConnection() {
  printBanner();
  console.log(`🔍 Testing connection to ${MCP_URL} ...\n`);

  const url = new URL(MCP_URL);
  const options = {
    hostname: url.hostname,
    path: url.pathname,
    method: "GET",
    timeout: 10000
  };

  const req = https.request(options, (res) => {
    if (res.statusCode < 500) {
      console.log(`✅ Server is LIVE — HTTP ${res.statusCode}`);
      console.log(`   Ready to connect at: ${MCP_URL}\n`);
    } else {
      console.log(`⚠️  Server responded with HTTP ${res.statusCode}`);
      console.log(`   Server may be starting up (Render cold start ~30s)\n`);
    }
  });

  req.on("timeout", () => {
    req.destroy();
    console.log("⏳ Request timed out — server may be cold starting (~30s on Render)");
    console.log(`   Try again or visit: ${MCP_URL}\n`);
  });

  req.on("error", (err) => {
    console.log(`❌ Connection failed: ${err.message}`);
    console.log(`   Check status at: ${REPO_URL}\n`);
  });

  req.end();
}

// Route based on args
if (args.includes("--config")) {
  printConfig();
} else if (args.includes("--vscode")) {
  printVSCode();
} else if (args.includes("--info")) {
  printInfo();
} else if (args.includes("--test")) {
  testConnection();
} else {
  printHelp();
}
