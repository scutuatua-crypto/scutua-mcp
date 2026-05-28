from tools.market.coingecko import register_coingecko_tools
from tools.market.cmc import register_cmc_tools
from tools.market.trending import register_trending_tools
from tools.market.sentiment import register_sentiment_tools
from tools.market.fear_index import register_fear_index_tools
from tools.market.overview import register_market_overview_tools  # ✅ เพิ่ม

def register_market_tools(app):
    register_coingecko_tools(app)
    register_cmc_tools(app)
    register_trending_tools(app)
    register_sentiment_tools(app)
    register_fear_index_tools(app)
    register_market_overview_tools(app)  # ✅ เพิ่ม
