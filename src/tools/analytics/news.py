"""
Crypto News Tools — Scutua-MCP
Uses CryptoPanic (with API key) + CoinGecko news as fallback
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP

CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "")


def register_news_tools(app: FastMCP):

    @app.tool()
    async def get_crypto_news() -> str:
        """Get latest crypto news"""
        try:
            # 🔧 FIX 1: ถ้ามี API key ใช้ CryptoPanic v1
            if CRYPTOPANIC_API_KEY:
                url = (
                    f"https://cryptopanic.com/api/v1/posts/"
                    f"?auth_token={CRYPTOPANIC_API_KEY}&kind=news&limit=7&public=true"
                )
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    r.raise_for_status()
                    data = r.json()
                posts = data.get("results", [])
                if posts:
                    result = ["📰 Latest Crypto News (CryptoPanic):"]
                    for i, post in enumerate(posts[:7], 1):
                        title = post.get("title", "N/A")
                        source = post.get("source", {}).get("title", "")
                        source_str = f" — {source}" if source else ""
                        result.append(f"{i}. {title}{source_str}")
                    return "\n".join(result)

            # 🔧 FIX 2: fallback → CoinGecko news (ไม่ต้องใช้ key)
            url = "https://api.coingecko.com/api/v3/news"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                r.raise_for_status()
                data = r.json()

            # CoinGecko news response: {"data": [...]}
            articles = data if isinstance(data, list) else data.get("data", [])
            if not articles:
                return "❌ No news available — add CRYPTOPANIC_API_KEY for better results"

            result = ["📰 Latest Crypto News (CoinGecko):"]
            for i, article in enumerate(articles[:7], 1):
                title = article.get("title") or article.get("name", "N/A")
                author = article.get("author") or article.get("news_site", "")
                author_str = f" — {author}" if author else ""
                result.append(f"{i}. {title}{author_str}")
            return "\n".join(result)

        except Exception as e:
            return f"❌ News error: {e}"

    @app.tool()
    async def get_fear_greed_index() -> str:
        """Get Crypto Fear & Greed Index"""
        try:
            url = "https://api.alternative.me/fng/"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            result = data.get("data", [{}])[0]
            value = int(result.get("value", 0))
            classification = result.get("value_classification", "N/A")
            emoji = (
                "😱" if value < 25 else
                "😰" if value < 45 else
                "😐" if value < 55 else
                "😊" if value < 75 else
                "🤑"
            )
            return f"{emoji} Fear & Greed Index: {value}/100\nSentiment: {classification}"
        except Exception as e:
            return f"Error: {e}"
