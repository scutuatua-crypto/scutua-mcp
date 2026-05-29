import httpx
from mcp.server.fastmcp import FastMCP

def register_dashboard_tools(app: FastMCP):
    @app.tool()
    async def get_dashboard_summary() -> str:
        """Get WhaleTrucker Dashboard summary"""
        try:
            sites = [
                ("WhaleTrucker Elite",  "https://github.com/scutuatua-crypto/whaletrucker-reef"),
                ("AssetFlow",           "https://assetflow-app-iota.vercel.app"),
                ("Asset Platform",      "https://asset-platform.vercel.app"),
                ("Scutua Command Hub",  "https://scutuatua-crypto.github.io"),
                ("Scutua-MCP",          "https://scutua-mcp.onrender.com/mcp"),
            ]
            result = ["🐋 WhaleTrucker Dashboard Status:"]
            async with httpx.AsyncClient(follow_redirects=True) as client:
                for name, url in sites:
                    try:
                        if "onrender.com/mcp" in url:
                            r = await client.head(url, timeout=8)
                            status = "🟢 Live" if r.status_code in (200, 201, 405, 406) else f"🔴 {r.status_code}"
                        else:
                            r = await client.get(url, timeout=8)
                            status = "🟢 Live" if r.status_code in (200, 201) else f"🔴 {r.status_code}"
                    except Exception:
                        status = "🔴 Down"
                    result.append(f"{name}: {status}")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
