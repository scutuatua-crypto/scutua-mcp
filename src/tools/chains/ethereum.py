import os
import httpx
from mcp.server.fastmcp import FastMCP

# Etherscan V2 — key เดียวรองรับทุก EVM chain
ETHERSCAN_API_KEY = (
    os.getenv("ETHERSCAN_API_KEY") or
    os.getenv("ETHERS_API_KEY") or
    ""
)

BASE_URL_V2 = "https://api.etherscan.io/v2/api"

# Chain IDs
CHAIN_ETH       = 1
CHAIN_ARBITRUM  = 42161
CHAIN_OPTIMISM  = 10
CHAIN_BNB       = 56


# ฟังก์ชัน fetch จริงๆ — ไม่ใช่ tool
async def _fetch_evm_gas(chain_id: int) -> dict:
    params = {
        "chainid": chain_id,
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": ETHERSCAN_API_KEY,
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(BASE_URL_V2, params=params, timeout=10)
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


async def _format_gas_response(result: dict, chain_name: str) -> dict:
    if "error" in result:
        return {"status": "fail", "chain": chain_name, "error": result["error"]}
    return {
        "status": "success",
        "chain": chain_name,
        "data": {
            "slow":     result.get("slow"),
            "standard": result.get("standard"),
            "fast":     result.get("fast"),
        }
    }


def register_ethereum_tools(app: FastMCP):
    @app.tool()
    async def get_eth_gas() -> dict:
        """Get Ethereum gas prices"""
        result = await _fetch_evm_gas(CHAIN_ETH)
        return await _format_gas_response(result, "ethereum")

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get Arbitrum gas prices"""
        result = await _fetch_evm_gas(CHAIN_ARBITRUM)
        return await _format_gas_response(result, "arbitrum")

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get Optimism gas prices"""
        result = await _fetch_evm_gas(CHAIN_OPTIMISM)
        return await _format_gas_response(result, "optimism")

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get BNB gas prices"""
        result = await _fetch_evm_gas(CHAIN_BNB)
        return await _format_gas_response(result, "bnb")
