from src.tools.coingecko import register_coingecko_tools
from src.tools.cmc import register_cmc_tools
from src.tools.trending import register_trending_tools
from src.tools.sentiment import register_sentiment_tools
from src.tools.fear_index import register_fear_index_tools

def register_market_tools(app):
    register_coingecko_tools(app)
    register_cmc_tools(app)
    register_trending_tools(app)
    register_sentiment_tools(app)
    register_fear_index_tools(app)
