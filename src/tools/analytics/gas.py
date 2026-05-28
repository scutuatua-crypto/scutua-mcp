import os
import httpx
from mcp.server.fastmcp import FastMCP

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")


async def _fetch_evm_gas(url: str, api_key: str) -> dict:
    try:
        if api_key:
            url += f"&apikey={api_key}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url, timeout=10)
            raw = r.json()
        if not isinstance(raw, dict):
            return {"error": "unexpected response format"}
        result = raw.get("result", {})
        if not isinstance(result, dict):
            return {"error": result}
        return {
            "slow":     result.get("SafeGasPrice"),
            "standard": result.get("ProposeGasPrice"),
            "fast":     result.get("FastGasPrice"),
        }
    except Exception as e:
        return {"error": str(e)}


async def _fetch_rpc_gas(rpc_url: str) -> dict:
    """ดึง gas ผ่าน JSON-RPC — ใช้กับ chain ที่ Etherscan free ไม่รองรับ"""
    try:
        payload = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
        async with httpx.AsyncClient() as client:
            r = await client.post(rpc_url, json=payload, timeout=10)
            data = r.json()
        hex_price = data.get("result", "0x0")
        gwei = int(hex_price, 16) / 1e9
        gwei_str = f"{gwei:.4f}"
        return {
            "slow":     gwei_str,
            "standard": gwei_str,
            "fast":     gwei_str,
        }
    except Exception as e:
        return {"error": str(e)}


async def _format_gas_response(chain: str) -> dict:
    if chain == "optimism":
        result = await _fetch_rpc_gas("https://mainnet.optimism.io")
    elif chain == "bnb":
        result = await _fetch_rpc_gas("https://bsc-dataseed.binance.org")
    elif chain == "ethereum":
        result = await _fetch_evm_gas(
            "https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle",
            ETHERSCAN_API_KEY,
        )
    elif chain == "arbitrum":
        result = await _fetch_evm_gas(
            "https://api.etherscan.io/v2/api?chainid=42161&module=gastracker&action=gasoracle",
            ETHERSCAN_API_KEY,
        )
    else:
        return {"status": "fail", "chain": chain, "error": "unknown chain"}

    if "error" in result:
        return {"status": "fail", "chain": chain, "error": result["error"]}
    return {"status": "success", "chain": chain, "data": result}


def register_gas_tools(app: FastMCP):
    @app.tool()
    async def get_eth_gas() -> dict:
        """Get Ethereum gas prices"""
        return await _format_gas_response("ethereum")

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get Arbitrum gas prices"""
        return await _format_gas_response("arbitrum")

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get Optimism gas prices"""
        return await _format_gas_response("optimism")

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get BNB gas prices"""
        return await _format_gas_response("bnb")
