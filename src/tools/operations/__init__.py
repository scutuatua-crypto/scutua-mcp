# src/tools/operations/__init__.py
from .alerts import register_alerts_tools
from .arbitrage import register_arbitrage_tools
from .converter import register_converter_tools
from .copy_trade import register_copy_trade_tools
from .dashboard import register_dashboard_tools
from .dao import register_dao_tools
from .ens import register_ens_tools
from .exploit import register_exploit_tools
from .gas import register_gas_tools
from .github import register_github_tools
from .heatmap import register_heatmap_tools
from .insurance import register_insurance_tools
from .launchpad import register_launchpad_tools
from .liquidation import register_liquidation_tools
from .news import register_news_tools
from .scam import register_scam_tools
from .signal import register_signal_tools
from .social import register_social_tools
from .tax import register_tax_tools
from .tax_report import register_tax_report_tools
from .validator import register_validator_tools
from .wallet import register_wallet_tools
from .watchlist import register_watchlist_tools

def register_operations_tools(app):
    register_alerts_tools(app)
    register_arbitrage_tools(app)
    register_converter_tools(app)
    register_copy_trade_tools(app)
    register_dashboard_tools(app)
    register_dao_tools(app)
    register_ens_tools(app)
    register_exploit_tools(app)
    register_gas_tools(app)
    register_github_tools(app)
    register_heatmap_tools(app)
    register_insurance_tools(app)
    register_launchpad_tools(app)
    register_liquidation_tools(app)
    register_news_tools(app)
    register_scam_tools(app)
    register_signal_tools(app)
    register_social_tools(app)
    register_tax_tools(app)
    register_tax_report_tools(app)
    register_validator_tools(app)
    register_wallet_tools(app)
    register_watchlist_tools(app)
