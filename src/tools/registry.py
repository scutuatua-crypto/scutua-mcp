from .chains import register_chain_tools
from .protocols import register_protocols_tools
from .analytics import register_analytics_tools
from .operations import register_operations_tools
from .market import register_market_tools

def register_all_tools(app):
    register_chain_tools(app)
    register_protocols_tools(app)
    register_analytics_tools(app)
    register_operations_tools(app)
    register_market_tools(app)
