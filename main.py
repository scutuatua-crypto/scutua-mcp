import os
from mcp.server.fastmcp import FastMCP
from src.tools.registry import register_all_tools

app = FastMCP("Scutua-MCP")

register_all_tools(app)

if __name__ == "__main__":
   port = int(os.environ.get("PORT", 10000))
   app.run(host="0.0.0.0", port=port)
