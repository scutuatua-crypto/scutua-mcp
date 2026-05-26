# ⚡ Execution Layer — src/tools/execution/

> **Dimension 7: Execution Layer**
> ไม่แค่ suggest — **ลงมือจริง** ผ่าน DEX โดยตรง

-----

## Tools (18 tools)

|File               |Tools                                                            |Description                 |
|-------------------|-----------------------------------------------------------------|----------------------------|
|`swap_executor.py` |`get_swap_quote`, `execute_swap`                                 |Jupiter swap on Solana      |
|`limit_order.py`   |`place_limit_order`, `check_limit_orders`, `cancel_limit_order`  |On-chain limit orders       |
|`dca_engine.py`    |`create_dca_plan`, `execute_dca_buy`, `get_dca_plans`            |Dollar-cost averaging       |
|`stop_loss.py`     |`set_stop_loss`, `check_stop_losses`                             |Auto stop loss + take profit|
|`auto_rebalance.py`|`analyze_rebalance`, `execute_rebalance`, `get_rebalance_history`|Portfolio rebalancing       |
|`sniper.py`        |`analyze_token_safety`, `snipe_token`                            |New token sniper w/ safety  |
|`emergency_exit.py`|`preview_emergency_exit`, `emergency_exit_all`                   |Nuclear exit → USDC         |

-----

## Required ENV (add to Render)

```
SOLANA_WALLET_PRIVATE_KEY=...   # ⚠️ Never commit to repo
```

Already configured:

```
SOLANA_API=...          ✅
TELEGRAM_BOT_TOKEN=...  ✅
TELEGRAM_CHANNEL_ID=... ✅
BIRDEYE_API_KEY=...     ✅
```

## Required Package (add to requirements.txt)

```
solders>=0.21.0
```

-----

## Safety Design

Every execution tool has:

- `dry_run=True` by default — simulate before real execution
- Telegram alert before AND after every trade
- Safety score check (sniper)
- Confirmation gate (emergency exit requires `confirmed=True`)

-----

## Registry update (registry.py)

```python
from .execution import register_execution_tools

def register_all_tools(app):
    ...
    register_execution_tools(app)  # Dimension 7
```

-----

## Flow

```
Sentiment Signal (Dim 6)
        ↓
  Claude Decision
        ↓
  execute_swap / place_limit_order / start_dca
        ↓
  Telegram Confirmation (Dim 4)
```

**135 tools → 153 tools. World’s first Agentic DeFi MCP.** 🌍
