from .arbitrage_scanner import scan_arbitrage
from .whale_alert import monitor_whales, test_telegram_alert
from .portfolio_autopilot import autopilot_analyze
from .sentiment_signal import get_sentiment_signal

def register_agentic_tools(app):
    app.add_tool(scan_arbitrage)
    app.add_tool(monitor_whales)
    app.add_tool(test_telegram_alert)
    app.add_tool(autopilot_analyze)
    app.add_tool(get_sentiment_signal)
