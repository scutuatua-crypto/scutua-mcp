#!/usr/bin/env node

/**
 * scutua-mcp
 * WhaleTrucker MCP Server — 157 tools across 8 Dimensions
 * Live: https://scutua-mcp.onrender.com/mcp
 */

const https = require("https");
const args = process.argv.slice(2);

const MCP_URL      = "https://scutua-mcp.onrender.com/mcp";
const REPO_URL     = "https://github.com/scutuatua-crypto/scutua-mcp";
const SMITHERY_URL = "https://smithery.ai/servers/scutuatua/scutua-mcp";
const NPM_URL      = "https://www.npmjs.com/package/scutua-mcp";

// ─── CONFIGS ──────────────────────────────────────────────────────────────────

const CONFIGS = {
  claude_desktop: {
    label: "Claude Desktop  (~/.config/claude/claude_desktop_config.json)",
    json: { mcpServers: { "scutua-mcp": { url: MCP_URL } } }
  },
  vscode: {
    label: "VS Code / Cursor  (.vscode/mcp.json)",
    json: { mcpServers: { "scutua-mcp": { url: MCP_URL } } }
  },
  windsurf: {
    label: "Windsurf  (~/.codeium/windsurf/mcp_config.json)",
    json: { mcpServers: { "scutua-mcp": { serverUrl: MCP_URL, disabled: false } } }
  },
  continue: {
    label: "Continue  (~/.continue/config.json  →  mcpServers array)",
    json: { name: "scutua-mcp", url: MCP_URL }
  }
};

// ─── DIMENSIONS ───────────────────────────────────────────────────────────────

const DIMENSIONS = [
  { icon: "🌐", name: "Multi-Chain Universe",    count: 11, desc: "Solana · Ethereum · Arbitrum · Optimism · BNB · Polkadot · Reef · TON · Cosmos · Base · CrossChain" },
  { icon: "⚡", name: "DeFi Protocol Universe",  count: 26, desc: "Jupiter · Drift · Uniswap · Lido · Aave · Curve · Compound · GMX · Pendle · and more" },
  { icon: "🧠", name: "Intelligence & Analytics",count: 26, desc: "Whale tracking · Birdeye · DeFiLlama · Nansen · Dune · Price feeds · Fear & Greed" },
  { icon: "🛠️", name: "Operations & DevOps",     count: 17, desc: "GitHub · Tax · Wallet · Alerts · Telegram · Discord · Portfolio Tracker" },
  { icon: "📊", name: "Market Intelligence",     count:  8, desc: "CoinGecko · CMC · Trending · Sentiment · Kaito · LunarCrush · Alternative.me" },
  { icon: "🤖", name: "Agentic Layer",           count:  5, desc: "Arbitrage Scanner · Whale Alert · Portfolio Autopilot · Sentiment Signal" },
  { icon: "⚡", name: "Execution Layer",         count: 18, desc: "Swap · Limit Order · DCA · Stop Loss · Rebalance · Sniper · Emergency Exit" },
  { icon: "🌌", name: "Ecosystem Consciousness", count:  5, desc: "Heartbeat · Biometrics · Intelligence · Narrative · What Should I Build" },
];

// ─── HELPERS ──────────────────────────────────────────────────────────────────

const bold  = (s) => `\x1b[1m${s}\x1b[0m`;
const cyan  = (s) => `\x1b[36m${s}\x1b[0m`;
const green = (s) => `\x1b[32m${s}\x1b[0m`;
const yellow= (s) => `\x1b[33m${s}\x1b[0m`;
const red   = (s) => `\x1b[31m${s}\x1b[0m`;
const dim   = (s) => `\x1b[2m${s}\x1b[0m`;

function banner() {
  console.log(`
${cyan("🐋 ════════════════════════════════════════════════")}
${bold("   SCUTUA-MCP  —  WhaleTrucker Ecosystem V2")}
   ${yellow("157 tools")} · ${yellow("8 Dimensions")} · Avalanche + Multi-Chain
   Built from iPad. No PC required. ${bold("😤")}
${cyan("🐋 ════════════════════════════════════════════════")}
`);
}

// ─── COMMANDS ─────────────────────────────────────────────────────────────────

function help() {
  banner();
  console.log(`${bold("MCP Server URL")}
  ${cyan(MCP_URL)}

${bold("Quick Connect")}
  ${green("Claude.ai")}     Settings → Integrations → Add custom connector → paste URL above
  ${green("Claude Desktop")}  npx scutua-mcp --config
  ${green("VS Code/Cursor")}  npx scutua-mcp --vscode
  ${green("Windsurf")}        npx scutua-mcp --windsurf
  ${green("Continue")}        npx scutua-mcp --continue

${bold("Commands")}
  ${yellow("npx scutua-mcp")}               Show this help
  ${yellow("npx scutua-mcp --config")}      Claude Desktop JSON config
  ${yellow("npx scutua-mcp --vscode")}      VS Code / Cursor JSON config
  ${yellow("npx scutua-mcp --windsurf")}    Windsurf JSON config
  ${yellow("npx scutua-mcp --continue")}    Continue JSON config
  ${yellow("npx scutua-mcp --all-configs")} Print ALL client configs at once
  ${yellow("npx scutua-mcp --info")}        Show all 8 Dimensions + tool count
  ${yellow("npx scutua-mcp --test")}        Test if server is live
  ${yellow("npx scutua-mcp --version")}     Show package version

${bold("Links")}
  ${dim("Repo      ")} ${REPO_URL}
  ${dim("Smithery  ")} ${SMITHERY_URL}
  ${dim("npm       ")} ${NPM_URL}
`);
}

function printConfig(key) {
  const c = CONFIGS[key];
  banner();
  console.log(`${bold("📋 " + c.label)}\n`);
  console.log(JSON.stringify(c.json, null, 2));
  console.log();
}

function allConfigs() {
  banner();
  console.log(`${bold("📋 All Client Configs\n")}`);
  for (const [key, c] of Object.entries(CONFIGS)) {
    console.log(`${green("─── " + c.label)}`);
    console.log(JSON.stringify(c.json, null, 2));
    console.log();
  }
}

function info() {
  banner();
  const total = DIMENSIONS.reduce((s, d) => s + d.count, 0);
  console.log(`${bold(`8 Dimensions  —  ${total} Tools Total\n`)}`);
  DIMENSIONS.forEach((d, i) => {
    console.log(`  ${d.icon}  ${bold(`Dimension ${i+1}`)} — ${yellow(d.name)}  ${dim("(" + d.count + " tools)")}`);
    console.log(`     ${dim(d.desc)}\n`);
  });

  console.log(`${bold("Agentic Flow")}`);
  console.log(dim("  Market Data (Dim 1–5)"));
  console.log(dim("       ↓"));
  console.log(dim("  Sentiment Signal → BUY / SELL / HOLD"));
  console.log(dim("       ↓"));
  console.log(dim("  Claude AI Decision Engine"));
  console.log(dim("       ↓"));
  console.log(dim("  Execute: Swap / DCA / Limit Order / Stop Loss"));
  console.log(dim("       ↓"));
  console.log(dim("  Telegram Alert → Confirmed"));
  console.log(dim("       ↓"));
  console.log(dim("  Ecosystem Consciousness → Self-Aware 🌌\n"));
}

function testConnection() {
  banner();
  console.log(`🔍 Testing connection to ${cyan(MCP_URL)} ...\n`);

  const url = new URL(MCP_URL);
  const req = https.request(
    { hostname: url.hostname, path: url.pathname, method: "GET", timeout: 12000 },
    (res) => {
      if (res.statusCode < 500) {
        console.log(green(`✅ Server is LIVE — HTTP ${res.statusCode}`));
        console.log(`   Ready to connect at: ${cyan(MCP_URL)}\n`);
      } else {
        console.log(yellow(`⚠️  Server responded with HTTP ${res.statusCode}`));
        console.log(`   Server may be cold-starting (~30s on Render free tier)\n`);
      }
    }
  );

  req.on("timeout", () => {
    req.destroy();
    console.log(yellow("⏳ Timeout — server may be cold-starting (~30s on Render)"));
    console.log(`   Try again in 30s or visit: ${REPO_URL}\n`);
  });

  req.on("error", (err) => {
    console.log(red(`❌ Connection failed: ${err.message}`));
    console.log(`   Check status at: ${REPO_URL}\n`);
  });

  req.end();
}

function version() {
  const pkg = require("./package.json");
  console.log(`scutua-mcp v${pkg.version}`);
}

// ─── ROUTER ───────────────────────────────────────────────────────────────────

if      (args.includes("--config"))      printConfig("claude_desktop");
else if (args.includes("--vscode"))      printConfig("vscode");
else if (args.includes("--windsurf"))    printConfig("windsurf");
else if (args.includes("--continue"))    printConfig("continue");
else if (args.includes("--all-configs")) allConfigs();
else if (args.includes("--info"))        info();
else if (args.includes("--test"))        testConnection();
else if (args.includes("--version"))     version();
else                                     help();
