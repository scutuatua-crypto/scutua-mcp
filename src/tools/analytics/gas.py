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
                raw = r.json()

            # raw ต้องเป็น dict ก่อน
            if not isinstance(raw, dict):
                return f"Error: unexpected response format"

            result = raw.get("result", {})

            # Etherscan return "result" เป็น string เมื่อ error (เช่น missing API key)
            if not isinstance(result, dict):
                return f"Error: {result}"

            slow = result.get("SafeGasPrice", "N/A")
            avg  = result.get("ProposeGasPrice", "N/A")
            fast = result.get("FastGasPrice", "N/A")
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
            payload = {"jsonrpc": "2.0", "id": 1, "method": "getRecentPerformanceSamples", "params": [1]}
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload, timeout=10)
                data = r.json()

            if not isinstance(data, dict):
                return "Error: unexpected response format"

            samples = data.get("result", [])
            if samples:
                sample = samples[0]
                num_tx = sample.get("numTransactions", 0)
                period = sample.get("samplePeriodSecs", 1) or 1  # กัน division by zero
                tps = num_tx / period
                return f"⚡ Solana TPS: {tps:.0f} transactions/sec"
            return "No TPS data available"
        except Exception as e:
            return f"Error: {e}"
