"""
Arbitrum Chain Tools — Scutua-MCP
"""
import os
import httpx
from src.utils.cache import get_cached, set_cached
from src.utils.logger import get_logger

logger = get_logger(__name__)

# 🔧 FIX: ใช้ Etherscan v2 แทน Arbiscan — key เดียวกัน รองรับ Arbitrum (chainid=42161)
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
BASE_URL = "https://api.etherscan.io/v2/api"
ARBITRUM_RPC = "https://arb1.arbitrum.io/rpc"


async def _etherscan_get(params: dict) -> dict:
    cache_key = f"arbitrum:{str(sorted(params.items()))}"
    cached = get_cached(cache_key)
    if cached:
        return cached
    try:
        params["chainid"] = 42161
        if ETHERSCAN_API_KEY:
            params["apikey"] = ETHERSCAN_API_KEY
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(BASE_URL, params=params)
            r.raise_for_status()
            data = r.json()

        # 🔧 FIX: เช็ค Etherscan status — status "0" = error
        if data.get("status") == "0":
            msg = data.get("message", "Etherscan error")
            result = data.get("result", "")
            # rate limit หรือ key ไม่มี
            if "rate limit" in str(result).lower() or "invalid" in str(result).lower():
                return {"error": f"Etherscan: {result}"}
            return {"error": f"{msg}: {result}"}

        set_cached(cache_key, data, ttl=60)
        return data
    except Exception as e:
        logger.error(f"Arbitrum Etherscan error: {e}")
        return {"error": str(e)}


async def _rpc_get(method: str, params: list) -> dict:
    """Fallback: JSON-RPC สำหรับ query ที่ไม่ต้องการ API key"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                ARBITRUM_RPC,
                json={"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
            )
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def register_arbitrum_tools(app):

    @app.tool()
    async def get_arbitrum_balance(address: str) -> dict:
        """Get ETH balance on Arbitrum L2"""
        try:
            # ลอง Etherscan v2 ก่อน
            data = await _etherscan_get({
                "module": "account", "action": "balance",
                "address": address, "tag": "latest",
            })
            if "error" not in data:
                wei = data.get("result", "0")
                balance = int(wei) / 1e18 if wei and wei.isdigit() else 0
                return {"address": address[:8] + "...", "balance_eth": round(balance, 6), "chain": "arbitrum"}

            # Fallback: RPC
            rpc = await _rpc_get("eth_getBalance", [address, "latest"])
            hex_val = rpc.get("result", "0x0")
            balance = int(hex_val, 16) / 1e18
            return {"address": address[:8] + "...", "balance_eth": round(balance, 6),
                    "chain": "arbitrum", "source": "rpc"}
        except Exception as e:
            return {"error": str(e), "chain": "arbitrum"}

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get current Arbitrum gas price"""
        try:
            data = await _etherscan_get({
                "module": "gastracker", "action": "gasoracle",
            })
            if "error" not in data:
                result = data.get("result", {})
                if isinstance(result, dict):
                    return {"chain": "arbitrum",
                            "slow": result.get("SafeGasPrice", "?"),
                            "standard": result.get("ProposeGasPrice", "?"),
                            "fast": result.get("FastGasPrice", "?")}

            # Fallback: RPC
            rpc = await _rpc_get("eth_gasPrice", [])
            hex_val = rpc.get("result", "0x0")
            gwei = round(int(hex_val, 16) / 1e9, 4)
            return {"chain": "arbitrum", "slow": str(gwei),
                    "standard": str(gwei), "fast": str(gwei), "source": "rpc"}
        except Exception as e:
            return {"error": str(e), "chain": "arbitrum"}

    @app.tool()
    async def get_arbitrum_tx_history(address: str, limit: int = 10) -> dict:
        """Get recent transactions on Arbitrum"""
        try:
            data = await _etherscan_get({
                "module": "account", "action": "txlist",
                "address": address, "page": 1,
                "offset": limit, "sort": "desc",
            })
            if "error" in data:
                return {"error": data["error"], "chain": "arbitrum",
                        "address": address[:8] + "...", "transactions": []}

            txs = data.get("result", [])
            if not isinstance(txs, list):
                return {"error": "unexpected tx format", "chain": "arbitrum",
                        "address": address[:8] + "...", "transactions": []}

            # 🔧 FIX: trim tx data ให้เหลือแค่ field สำคัญ
            clean_txs = []
            for tx in txs[:limit]:
                clean_txs.append({
                    "hash": tx.get("hash", "")[:16] + "...",
                    "from": tx.get("from", "")[:8] + "...",
                    "to": (tx.get("to") or "")[:8] + "...",
                    "value_eth": round(int(tx.get("value", 0)) / 1e18, 6),
                    "gas_used": tx.get("gasUsed", "?"),
                    "timestamp": tx.get("timeStamp", "?"),
                    "status": "✅" if tx.get("txreceipt_status") == "1" else "❌",
                })

            return {"address": address[:8] + "...", "chain": "arbitrum",
                    "count": len(clean_txs), "transactions": clean_txs}
        except Exception as e:
            return {"error": str(e), "chain": "arbitrum",
                    "address": address[:8] + "...", "transactions": []}
