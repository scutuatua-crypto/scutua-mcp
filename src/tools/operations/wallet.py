import httpx
from mcp.server.fastmcp import FastMCP

def register_wallet_tools(app: FastMCP):
    @app.tool()
    async def scan_wallet_multichain(address: str) -> str:
        """Scan wallet across multiple chains"""
        try:
            result = [f"👛 Multi-Chain Wallet: {address[:8]}...{address[-6:]}"]
            async with httpx.AsyncClient() as client:
                # SOL
                try:
                    sol_url = "https://api.mainnet-beta.solana.com"
                    payload = {"jsonrpc":"2.0","id":1,"method":"getBalance","params":[address]}
                    r = await client.post(sol_url, json=payload, timeout=5)
                    sol = r.json().get("result", {}).get("value", 0) / 1e9
                    result.append(f"◎ SOL: {sol:.4f}")
                except:
                    result.append("◎ SOL: N/A")
                # ETH Base
                try:
                    base_url = "https://mainnet.base.org"
                    payload = {"jsonrpc":"2.0","method":"eth_getBalance","params":[address,"latest"],"id":1}
                    r = await client.post(base_url, json=payload, timeout=5)
                    eth = int(r.json().get("result", "0x0"), 16) / 1e18
                    result.append(f"🔵 Base ETH: {eth:.6f}")
                except:
                    result.append("🔵 Base ETH: N/A")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
