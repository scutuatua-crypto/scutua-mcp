"""
Crypto News Tools — Scutua-MCP
Uses RSS feeds (CoinDesk + Decrypt + Cointelegraph) — no API key needed
"""
import os
import httpx
import xml.etree.ElementTree as ET
from mcp.server.fastmcp import FastMCP

logger_import = None
try:
    from src.utils.logger import get_logger
    logger_import = get_logger(__name__)
except Exception:
    pass


RSS_FEEDS = [
    ("CoinDesk",      "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Cointelegraph", "https://cointelegraph.com/rss"),
    ("Decrypt",       "https://decrypt.co/feed"),
]


async def _fetch_rss(name: str, url: str, limit: int = 4) -> list[str]:
    """Fetch and parse RSS feed, return list of formatted strings"""
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 ScutuaMCP/1.0"},
            timeout=10,
        ) as client:
            r = await client.get(url)
            r.raise_for_status()

        root = ET.fromstring(r.text)
        items = root.findall(".//item")[:limit]
        results = []
        for item in items:
            title = item.findtext("title", "").strip()
            if title:
                results.append(f"• {title} [{name}]")
        return results
    except Exception as e:
        return []


def register_news_tools(app: FastMCP):

    @app.tool()
    async def get_crypto_news() -> str:
        """Get latest crypto news from RSS feeds (CoinDesk, Cointelegraph, Decrypt)"""
        try:
            all_news = []
            for name, url in RSS_FEEDS:
                items = await _fetch_rss(name, url, limit=3)
                all_news.extend(items)

            if not all_news:
                return "❌ Could not fetch news — all RSS feeds failed"

            result = ["📰 Latest Crypto News:\n"]
            result.extend(all_news[:9])
            return "\n".join(result)

        except Exception as e:
            return f"❌ News error: {e}"

    @app.tool()
    async def get_fear_greed_index() -> str:
        """Get Crypto Fear & Greed Index"""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://api.alternative.me/fng/", timeout=10
                )
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
