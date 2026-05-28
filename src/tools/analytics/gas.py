import os
import httpx
from mcp.server.fastmcp import FastMCP

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
OPTIMISM_API_KEY  = os.getenv("OPTIMISM_API_KEY", "")
BSC_API_KEY       = os.getenv("BSC_API_KEY", "")

CHAIN_CONFIG = {
    "ethereum": {
        "url": "https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle",
        "key": ETHERSCAN_API_KEY,
    },
    "arbitrum": {
        "url": "https://api.etherscan.io/v2/api?chainid=42161&module=gastracker&action=gasoracle",
        "key": ETHERSCAN_API_KEY,
    },
    "optimism": {
        "url": "https://api.etherscan.io/v2/api?chainid=10&module=gastracker&action=gasoracle",
        "key": OPTIMISM_API_KEY,
    },
    "bnb": {
        "url": "https://api.etherscan.io/v2/api?chainid=56&module=gastracker&action=gasoracle",
        "key": BSC_API_KEY,
    },
}


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


async def _format_gas_response(chain: str) -> dict:
    config = CHAIN_CONFIG[chain]
    result = await _fetch_evm_gas(config["url"], config["key"])
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
