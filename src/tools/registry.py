from .chains import register_chain_tools
from .protocols import register_protocols_tools
from .analytics import register_analytics_tools
from .operations import register_operations_tools
from .market import register_market_tools
from .agentic import register_agentic_tools
from .execution import register_execution_tools
from .ecosystem import register_ecosystem_tools  # ← เพิ่ม

def register_all_tools(app):
    register_chain_tools(app)
    register_protocols_tools(app)
    register_analytics_tools(app)
    register_operations_tools(app)
    register_market_tools(app)
    register_agentic_tools(app)
    register_execution_tools(app)
    register_ecosystem_tools(app)  # ← เพิ่ม
