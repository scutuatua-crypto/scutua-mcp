import os
from mcp.server.fastmcp import FastMCP
from src.tools.registry import register_all_tools

app = FastMCP("Scutua-MCP")

register_all_tools(app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app.get_asgi_app(), host="0.0.0.0", port=port)
