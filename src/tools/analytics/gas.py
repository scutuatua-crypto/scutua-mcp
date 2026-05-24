import httpx
from mcp.server.fastmcp import FastMCP

def register_gas_tools(app: FastMCP):
    @app.tool()
    async def get_eth_gas() -> str:
        """Get Ethereum gas prices"""
        try:
            url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json().get("result", {})
            slow = data.get("SafeGasPrice", "N/A")
            avg = data.get("ProposeGasPrice", "N/A")
            fast = data.get("FastGasPrice", "N/A")
            return f"""⛽ Ethereum Gas Prices:
🐢 Slow: {slow} Gwei
⚡ Average: {avg} Gwei
🚀 Fast: {fast} Gwei"""
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_solana_tps() -> str:
        """Get Solana current TPS"""
        try:
            url = "https://api.mainnet-beta.solana.com"
            payload = {"jsonrpc":"2.0","id":1,"method":"getRecentPerformanceSamples","params":[1]}
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload, timeout=10)
                data = r.json()
            samples = data.get("result", [])
            if samples:
                tps = samples[0].get("numTransactions", 0) / samples[0].get("samplePeriodSecs", 1)
                return f"⚡ Solana TPS: {tps:.0f} transactions/sec"
            return "No TPS data available"
        except Exception as e:
            return f"Error: {e}"
