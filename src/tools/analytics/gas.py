import os
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger

logger = get_logger(__name__)

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")

BSC_RPC_ENDPOINTS = [
    "https://bsc-dataseed.binance.org",
    "https://bsc-dataseed1.defibit.io",
    "https://bsc-dataseed1.ninicoin.io",
]

ARBITRUM_RPC = "https://arb1.arbitrum.io/rpc"


async def _fetch_rpc_gas(rpc_url: str) -> dict:
    """ดึง gas ผ่าน JSON-RPC"""
    try:
        payload = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.post(rpc_url, json=payload)
            data = r.json()
        result = data.get("result")
        if not result:
            return {"error": "empty result from RPC"}
        gwei = round(int(result, 16) / 1e9, 4)
        gwei_str = str(gwei)
        return {"slow": gwei_str, "standard": gwei_str, "fast": gwei_str}
    except Exception as e:
        return {"error": str(e)}


async def _fetch_bnb_gas() -> dict:
    """ลอง BSC RPC หลาย endpoint จนกว่าจะสำเร็จ"""
    for rpc in BSC_RPC_ENDPOINTS:
        result = await _fetch_rpc_gas(rpc)
        if "error" not in result:
            return result
    return {"error": "All BSC RPC endpoints failed"}


async def _fetch_etherscan_gas(chain_id: int) -> dict:
    """ดึง gas จาก Etherscan — fallback เป็น RPC ถ้า key ไม่มีหรือ rate limit"""
    try:
        url = f"https://api.etherscan.io/v2/api?chainid={chain_id}&module=gastracker&action=gasoracle"
        if ETHERSCAN_API_KEY:
            url += f"&apikey={ETHERSCAN_API_KEY}"

        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(url)
            raw = r.json()

        # Etherscan return status "0" เมื่อ error หรือ rate limit
        if not isinstance(raw, dict) or raw.get("status") == "0":
            msg = raw.get("result", "Etherscan error") if isinstance(raw, dict) else "bad response"
            logger.warning(f"Etherscan chainid={chain_id} failed: {msg} — fallback to RPC")
            return None  # trigger fallback

        result = raw.get("result", {})
        if not isinstance(result, dict):
            return None

        return {
            "slow":     result.get("SafeGasPrice", "?"),
            "standard": result.get("ProposeGasPrice", "?"),
            "fast":     result.get("FastGasPrice", "?"),
        }
    except Exception as e:
        logger.warning(f"Etherscan error: {e} — fallback to RPC")
        return None


def register_gas_tools(app: FastMCP):
    @app.tool()
    async def get_eth_gas() -> dict:
        """Get Ethereum gas prices"""
        try:
            result = await _fetch_etherscan_gas(1)
            if result is None:
                # Fallback: ETH RPC
                rpc_result = await _fetch_rpc_gas("https://cloudflare-eth.com")
                if "error" in rpc_result:
                    return {"status": "fail", "chain": "ethereum", "error": rpc_result["error"]}
                result = rpc_result
            return {"status": "success", "chain": "ethereum", "data": result}
        except Exception as e:
            return {"status": "fail", "chain": "ethereum", "error": str(e)}

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get Arbitrum gas prices"""
        try:
            result = await _fetch_etherscan_gas(42161)
            if result is None:
                rpc_result = await _fetch_rpc_gas(ARBITRUM_RPC)
                if "error" in rpc_result:
                    return {"status": "fail", "chain": "arbitrum", "error": rpc_result["error"]}
                result = rpc_result
            return {"status": "success", "chain": "arbitrum", "data": result}
        except Exception as e:
            return {"status": "fail", "chain": "arbitrum", "error": str(e)}

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get Optimism gas prices"""
        try:
            result = await _fetch_rpc_gas("https://mainnet.optimism.io")
            if "error" in result:
                return {"status": "fail", "chain": "optimism", "error": result["error"]}
            return {"status": "success", "chain": "optimism", "data": result}
        except Exception as e:
            return {"status": "fail", "chain": "optimism", "error": str(e)}

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get BNB gas prices"""
        try:
            result = await _fetch_bnb_gas()
            if "error" in result:
                return {"status": "fail", "chain": "bnb", "error": result["error"]}
            return {"status": "success", "chain": "bnb", "data": result}
        except Exception as e:
            return {"status": "fail", "chain": "bnb", "error": str(e)}
