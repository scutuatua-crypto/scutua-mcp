from starlette.responses import JSONResponse
from starlette.routing import Route

async def server_card(request):
    return JSONResponse({
        "name": "scutua-mcp",
        "version": "1.0.0", 
        "description": "WhaleTrucker MCP Server — Multi-Chain Ecosystem",
        "url": "https://scutua-mcp.onrender.com/sse"
    })

routes = [Route("/.well-known/mcp/server-card.json", server_card)]
