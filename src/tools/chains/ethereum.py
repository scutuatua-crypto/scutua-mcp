import httpx
from mcp.server.fastmcp import FastMCP


# ฟังก์ชัน fetch จริงๆ — ไม่ใช่ tool
async def _fetch_evm_gas(url: str) -> dict:
    try:
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
        result = await _fetch_evm_gas(
            "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
        )
        return await _format_gas_response(result, "ethereum")

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get Arbitrum gas prices"""
        result = await _fetch_evm_gas(
            "https://api.arbiscan.io/api?module=gastracker&action=gasoracle"
        )
        return await _format_gas_response(result, "arbitrum")

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get Optimism gas prices"""
        result = await _fetch_evm_gas(
            "https://api-optimistic.etherscan.io/api?module=gastracker&action=gasoracle"
        )
        return await _format_gas_response(result, "optimism")

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get BNB gas prices"""
        result = await _fetch_evm_gas(
            "https://api.bscscan.com/api?module=gastracker&action=gasoracle"
        )
        return await _format_gas_response(result, "bnb")
