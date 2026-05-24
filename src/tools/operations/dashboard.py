import httpx
from mcp.server.fastmcp import FastMCP

def register_dashboard_tools(app: FastMCP):
    @app.tool()
    async def get_dashboard_summary() -> str:
        """Get WhaleTrucker Dashboard summary"""
        try:
            sites = [
                ("AssetFlow", "https://assetflow-whaletrucker.vercel.app"),
                ("WhaleTrucker Reef", "https://whaletrucker-reef.vercel.app"),
                ("Yields Tracker", "https://yield-hunter.vercel.app"),
            ]
            result = ["🐋 WhaleTrucker Dashboard Status:"]
            async with httpx.AsyncClient() as client:
                for name, url in sites:
                    try:
                        r = await client.get(url, timeout=5)
                        status = "🟢 Live" if r.status_code == 200 else f"🔴 {r.status_code}"
                    except:
                        status = "🔴 Down"
                    result.append(f"{name}: {status}")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
