# 🤖 Agentic Dimension — src/tools/agentic/

> **Dimension 6: Agentic Layer**
> ไม่แค่ดึงข้อมูล — วิเคราะห์ + ตัดสินใจ + แจ้งเตือนอัตโนมัติ

---

## Files

| File | Tool | Description |
|------|------|-------------|
| `arbitrage_scanner.py` | `scan_arbitrage` | Cross-chain price diff + net profit after fees |
| `whale_alert.py` | `monitor_whales`, `test_telegram_alert` | Whale TX monitor → Telegram auto-alert |
| `portfolio_autopilot.py` | `autopilot_analyze` | Portfolio rebalance engine → Telegram report |
| `sentiment_signal.py` | `get_sentiment_signal` | Fear&Greed + Momentum → BUY/SELL/HOLD signal |

---

## Setup

ต้องการ env vars ใน Render (มีอยู่แล้วทุกตัว):

```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=...
```

Whale Alert ต้องการเพิ่ม:
```
WHALE_ALERT_API_KEY=...   # get at whale-alert.io (free tier available)
```

---

## Register ใน registry.py

```python
from tools.agentic.arbitrage_scanner import scan_arbitrage
from tools.agentic.whale_alert import monitor_whales, test_telegram_alert
from tools.agentic.portfolio_autopilot import autopilot_analyze
from tools.agentic.sentiment_signal import get_sentiment_signal
```

---

## สิ่งที่ทำให้ต่างจากคนอื่น

ทุก MCP server อื่นหยุดที่ **"get data"**

Scutua-MCP Agentic Layer ทำ **"get → think → act → notify"**

```
Data Sources → Analysis Engine → Signal/Action → Telegram Alert
```
