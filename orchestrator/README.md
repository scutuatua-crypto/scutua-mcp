# 🤖 WhaleTrucker Orchestrator Router

**Coordinates scutua-mcp (DeFi execution) + github-mcp-server (GitHub logging)**

Enables autonomous workflows:
- DeFi signal generation
- GitHub logging & issue tracking
- Telegram notifications
- Full audit trail

---

## 🏗️ Architecture

```
┌────────────────────────────────────────���
│      Claude AI (Decision Engine)       │
└────────────┬─────────────────┬─────────┘
             │                 │
             ▼                 ▼
      scutua-mcp          github-mcp
      (DeFi Execute)      (GitHub Log)
             │                 │
      ┌──────┴─────────────────┴──────┐
      │                               │
      ▼                               ▼
  Market Data              GitHub Issues
  Whale Tracking           Audit Trail
  Trade Execution          Workflow Updates
             │                 │
             └─────────┬───────┘
                       ▼
              Telegram Notifications
```

---

## 📊 Workflow Flow

```
1. Signal Generated (scutua-mcp)
   ↓
2. Validation
   ↓
3. Execution (DRY RUN → STAGED → AUTO)
   ↓
4. GitHub Logging
   ↓
5. Workflow Update
   ↓
6. Telegram Alert
   ↓
7. Confirmation
```

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your tokens
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Demo (DRY RUN - Safe)
```bash
python router.py
```

**Output:**
```
🐳 WhaleTrucker Orchestrator - Demo

============================================================
PROCESSING: [WHALE-001] BUY 10.5 SOL @ $145.32 (87.0% confidence)
============================================================

[STEP 1] Validating signal...
  ✓ ID
  ✓ Chain
  ✓ Action
  ✓ Amount
  ✓ Price
  ✓ Confidence
✓ Signal validated

[STEP 2] Executing trade (mode: dry_run)...
[scutua-mcp] Executing: [WHALE-001] BUY 10.5 SOL @ $145.32 (87.0% confidence)
[scutua-mcp] DRY RUN - Preview: ...
✓ Execution dry-run completed

[STEP 3] Logging to GitHub...
[github-mcp] Creating log for: [WHALE-001] BUY 10.5 SOL @ $145.32
[github-mcp] Issue created: https://github.com/.../issues/999
✓ Logged: https://github.com/.../issues/999

[STEP 4] Updating workflow...
[github-mcp] Updating status: logged
[github-mcp] Would commit to: whaletrucker-ecosystem/TRADES.md
✓ Workflow updated

[STEP 5] Sending notification...
[Telegram] Would send: ✅ **EXECUTED**: [WHALE-001] BUY 10.5 SOL @ $145.32
✓ Notification sent

============================================================
✅ WORKFLOW COMPLETE: WHALE-001-1717420851.123456
============================================================
```

---

## 🔒 Execution Modes

### **DRY_RUN** (Default - Safe)
- Preview execution
- No actual trades
- No GitHub commits
- Perfect for testing

```python
orchestrator = Orchestrator(mode=ExecutionMode.DRY_RUN)
```

### **STAGED** (Manual Confirmation)
- Execute trade
- Wait for approval
- Then log to GitHub

```python
orchestrator = Orchestrator(mode=ExecutionMode.STAGED)
```

### **AUTO** (Production)
- Full automation
- Execute + log immediately
- Requires extensive testing

```python
orchestrator = Orchestrator(mode=ExecutionMode.AUTO)
```

---

## 🛠️ Components

### ScutuaMCPBridge
```python
bridge = ScutuaMCPBridge(endpoint="https://scutua-mcp.onrender.com/mcp")

# Execute trade
result = await bridge.execute_trade(signal, dry_run=True)
```

**Features:**
- Multi-chain execution (Solana, Ethereum, etc.)
- DeFi protocol integration (Jupiter, Uniswap, etc.)
- Real-time market data
- Dry-run support

### GitHubMCPBridge
```python
bridge = GitHubMCPBridge(token=GH_TOKEN, repo="owner/repo")

# Create trade log
issue_url = await bridge.create_trade_log(result)

# Update workflow
await bridge.update_workflow_status(result, commit=True)
```

**Features:**
- Automatic issue creation
- Workflow status updates
- GitHub commit logging
- Audit trail

### TelegramNotifier
```python
notifier = TelegramNotifier(bot_token=BOT, chat_id=CHAT)

# Send alert
msg_id = await notifier.notify_execution(result)
```

---

## 📋 TradeSignal Format

```python
signal = TradeSignal(
    signal_id="WHALE-001",
    chain="solana",                    # solana, ethereum, arbitrum, etc.
    action="BUY",                      # BUY, SELL, SWAP
    asset="SOL",
    amount=10.5,
    price=145.32,
    reason="Large whale accumulation detected by Birdeye",
    confidence=0.87,                   # 0.0 - 1.0
    timestamp=datetime.utcnow().isoformat(),
)
```

---

## 🔗 Integration with Claude AI

Add both MCPs to Claude Desktop config:

```json
{
  "mcpServers": {
    "orchestrator": {
      "command": "python",
      "args": ["./orchestrator/router.py"]
    },
    "scutua-mcp": {
      "url": "https://scutua-mcp.onrender.com/mcp"
    },
    "github-mcp": {
      "url": "https://github.com/scutuatua-crypto/github-mcp-server"
    }
  }
}
```

**Usage in Claude:**
```
"Use orchestrator to process this whale signal, execute via scutua-mcp, 
and log to GitHub using github-mcp"
```

---

## 📊 Result Format

```json
{
  "workflow_id": "WHALE-001-1717420851.123456",
  "status": "confirmed",
  "signal": {
    "signal_id": "WHALE-001",
    "chain": "solana",
    "action": "BUY",
    "asset": "SOL",
    "amount": 10.5,
    "price": 145.32,
    "reason": "Large whale accumulation detected by Birdeye",
    "confidence": 0.87,
    "timestamp": "2024-06-03T14:00:00.000000"
  },
  "gh_issue_url": "https://github.com/.../issues/999",
  "telegram_msg_id": "msg_placeholder_id",
  "tx_hash": "0x000...",
  "error": null,
  "timestamp": "2024-06-03T14:00:01.000000"
}
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Test
```bash
# Test with live scutua-mcp
EXECUTION_MODE=staged python router.py --test
```

### End-to-End Test
```bash
# Full workflow (dry-run)
python orchestrator_e2e_test.py
```

---

## 🔐 Security

✅ **Dry-run by default** — No accidental trades  
✅ **Environment variables** — Secrets not in code  
✅ **Staging mode** — Manual confirmation available  
✅ **Audit logging** — Full GitHub trail  
✅ **Telegram alerts** — Real-time notifications  

---

## 📚 Documentation

- [scutua-mcp](https://github.com/scutuatua-crypto/scutua-mcp)
- [github-mcp-server](https://github.com/scutuatua-crypto/github-mcp-server)
- [whaletrucker-ecosystem](https://github.com/scutuatua-crypto/whaletrucker-ecosystem)

---

## 🚀 Next Steps

- [ ] Add more validation rules
- [ ] Implement webhook triggers
- [ ] Create dashboard
- [ ] Add more chains support
- [ ] Performance optimization

---

*Built for WhaleTrucker Ecosystem | Coordinates scutua-mcp + github-mcp-server*
