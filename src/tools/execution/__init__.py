"""
Dimension 7: Execution Layer
src/tools/execution/__init__.py
"""

from .swap_executor import get_swap_quote, execute_swap
from .limit_order import place_limit_order, check_limit_orders, cancel_limit_order
from .dca_engine import create_dca_plan, execute_dca_buy, get_dca_plans
from .stop_loss import set_stop_loss, check_stop_losses
from .auto_rebalance import analyze_rebalance, execute_rebalance, get_rebalance_history
from .sniper import analyze_token_safety, snipe_token
from .emergency_exit import preview_emergency_exit, emergency_exit_all


def register_execution_tools(app):
    # Swap
    app.add_tool(get_swap_quote)
    app.add_tool(execute_swap)
    # Limit Orders
    app.add_tool(place_limit_order)
    app.add_tool(check_limit_orders)
    app.add_tool(cancel_limit_order)
    # DCA
    app.add_tool(create_dca_plan)
    app.add_tool(execute_dca_buy)
    app.add_tool(get_dca_plans)
    # Stop Loss
    app.add_tool(set_stop_loss)
    app.add_tool(check_stop_losses)
    # Rebalance
    app.add_tool(analyze_rebalance)
    app.add_tool(execute_rebalance)
    app.add_tool(get_rebalance_history)
    # Sniper
    app.add_tool(analyze_token_safety)
    app.add_tool(snipe_token)
    # Emergency
    app.add_tool(preview_emergency_exit)
    app.add_tool(emergency_exit_all)
