from .arbitrage_scanner import register_arbitrage_tools
from .whale_alert import register_whale_tools
from .portfolio_autopilot import register_autopilot_tools
from .sentiment_signal import register_sentiment_tools


def register_agentic_tools(app):
    register_arbitrage_tools(app)
    register_whale_tools(app)
    register_autopilot_tools(app)
    register_sentiment_tools(app)
