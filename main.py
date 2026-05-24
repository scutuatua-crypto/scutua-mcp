import os
from mcp.server.fastmcp import FastMCP
from tools.registry import register_all_tools

app = FastMCP("Scutua-MCP")

register_all_tools(app)

if __name__ == "__main__":
    # Get the port from Render, default to 10000
    port = int(os.environ.get("PORT", 10000))
    # Run the server on 0.0.0.0 to be accessible
    app.run(host="0.0.0.0", port=port)
