from .github import register_github_tools
from .tax import register_tax_tools
from .tax_report import register_tax_report_tools
from .converter import register_converter_tools
from .alerts import register_alert_tools
from .dashboard import register_dashboard_tools
from .social import register_social_tools
from .wallet import register_wallet_tools
from .validator import register_validator_tools
from .watchlist import register_watchlist_tools
from .airdrop import register_airdrop_tools
from .copy_trade import register_copy_trade_tools
from .scam import register_scam_tools
from .ens import register_ens_tools

def register_operations_tools(app):
    register_github_tools(app)
    register_tax_tools(app)
    register_tax_report_tools(app)
    register_converter_tools(app)
    register_alert_tools(app)
    register_dashboard_tools(app)
    register_social_tools(app)
    register_wallet_tools(app)
    register_validator_tools(app)
    register_watchlist_tools(app)
    register_airdrop_tools(app)
    register_copy_trade_tools(app)
    register_scam_tools(app)
    register_ens_tools(app)
