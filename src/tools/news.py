import httpx
from mcp.server.fastmcp import FastMCP

def register_news_tools(app: FastMCP):
    @app.tool()
    async def get_crypto_news() -> str:
        """Get latest crypto news"""
        try:
            url = "https://cryptopanic.com/api/v1/posts/?auth_token=public&kind=news&limit=5"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            posts = data.get("results", [])
            result = ["📰 Latest Crypto News:"]
            for i, post in enumerate(posts[:5], 1):
                title = post.get("title", "N/A")
                result.append(f"{i}. {title}")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_fear_greed_index() -> str:
        """Get Crypto Fear & Greed Index"""
        try:
            url = "https://api.alternative.me/fng/"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            result = data.get("data", [{}])[0]
            value = result.get("value", "N/A")
            classification = result.get("value_classification", "N/A")
            emoji = "😱" if int(value) < 25 else "😰" if int(value) < 45 else "😐" if int(value) < 55 else "😊" if int(value) < 75 else "🤑"
            return f"{emoji} Fear & Greed Index: {value}/100\nSentiment: {classification}"
        except Exception as e:
            return f"Error: {e}"
