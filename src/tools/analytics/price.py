import os
import httpx
from mcp.server.fastmcp import FastMCP

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")


async def _fetch_evm_gas(url: str) -> dict:
    try:
        if ETHERSCAN_API_KEY:
            url += f"&apikey={ETHERSCAN_API_KEY}"  # ✅ ใส่ key
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


async def _format_gas_response(chain: str) -> dict:
    result = await _fetch_evm_gas_by_chain(chain)
    if "error" in result:
        return {"status": "fail", "chain": chain, "error": result["error"]}
    return {"status": "success", "chain": chain, "data": result}


async def _fetch_evm_gas_by_chain(chain: str) -> dict:
    urls = {
        "ethereum": "https://api.etherscan.io/api?module=gastracker&action=gasoracle",
        "arbitrum": "https://api.arbiscan.io/api?module=gastracker&action=gasoracle",
        "optimism": "https://api-optimistic.etherscan.io/api?module=gastracker&action=gasoracle",
        "bnb":      "https://api.bscscan.com/api?module=gastracker&action=gasoracle",
    }
    return await _fetch_evm_gas(urls[chain])


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
