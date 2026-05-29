"""
Optimism Chain Tools — Scutua-MCP
Uses public Optimism RPC — no API key needed
"""
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Public Optimism RPC endpoints
OP_RPC_URLS = [
    "https://mainnet.optimism.io",
    "https://optimism.publicnode.com",
    "https://op-pokt.nodies.app",
]

async def _rpc_call(method: str, params: list) -> dict:
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    cache_key = f"op_rpc:{method}:{str(params)}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    for url in OP_RPC_URLS:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(url, json=payload, timeout=10)
                r.raise_for_status()
                data = r.json()
                if "result" in data:
                    set_cached(cache_key, data, ttl=30)
                    return data
        except Exception as e:
            logger.warning(f"OP RPC {url} failed: {e}")
            continue
    return {"error": "All Optimism RPC endpoints failed"}

def register_optimism_tools(app):

    @app.tool()
    async def get_optimism_balance(address: str) -> dict:
        """Get ETH balance on Optimism L2"""
        data = await _rpc_call("eth_getBalance", [address, "latest"])
        if "error" in data:
            return data
        hex_balance = data.get("result", "0x0")
        balance_wei = int(hex_balance, 16)
        balance_eth = balance_wei / 1e18
        return {
            "address": address,
            "balance_wei": str(balance_wei),
            "balance_eth": f"{balance_eth:.6f}",
            "chain": "optimism"
        }

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get current Optimism gas price"""
        data = await _rpc_call("eth_gasPrice", [])
        if "error" in data:
            return data
        hex_gas = data.get("result", "0x0")
        gas_wei = int(hex_gas, 16)
        gas_gwei = gas_wei / 1e9
        return {
            "gas_price": f"{gas_gwei:.6f}",
            "gas_price_wei": str(gas_wei),
            "chain": "optimism"
        }

    @app.tool()
    async def get_optimism_tx_history(address: str, limit: int = 10) -> dict:
        """Get transaction count on Optimism (RPC mode)"""
        data = await _rpc_call("eth_getTransactionCount", [address, "latest"])
        if "error" in data:
            return data
        tx_count = int(data.get("result", "0x0"), 16)
        return {
            "address": address,
            "total_tx_count": tx_count,
            "note": "Full tx history requires Etherscan Pro — RPC mode shows tx count only",
            "chain": "optimism"
        }
