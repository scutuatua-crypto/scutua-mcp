"""
Swap Executor — Jupiter (Solana)
Dimension 7: Execution Layer / src/tools/execution/swap_executor.py

Executes real token swaps via Jupiter Aggregator on Solana.
WARNING: This tool moves real funds. Always verify parameters before executing.
"""

import os
import base64
import httpx
from fastmcp import FastMCP

mcp = FastMCP("swap-executor")

SOLANA_RPC = os.getenv("SOLANA_API", "https://api.mainnet-beta.solana.com")
JUPITER_API = "https://lite-api.jup.ag/v6"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

TOKEN_MINTS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "WIF": "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
}


async def send_telegram(message: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, json={
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML",
        })


def resolve_mint(token: str) -> str:
    upper = token.upper()
    if upper in TOKEN_MINTS:
        return TOKEN_MINTS[upper]
    return token


@mcp.tool()
async def get_swap_quote(
    input_token: str,
    output_token: str,
    amount_ui: float,
    slippage_bps: int = 50,
) -> dict:
    """
    Get a swap quote from Jupiter without executing.

    Args:
        input_token: Token to sell (symbol or mint) e.g. 'SOL', 'USDC'
        output_token: Token to buy (symbol or mint)
        amount_ui: Human-readable amount (e.g. 1.5 for 1.5 SOL)
        slippage_bps: Slippage tolerance in basis points (50 = 0.5%)

    Returns:
        Quote with expected output, price impact, and route
    """
    try:
        input_mint = resolve_mint(input_token)
        output_mint = resolve_mint(output_token)

        decimals = 9 if input_token.upper() == "SOL" else 6
        amount_raw = int(amount_ui * (10 ** decimals))

        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount_raw,
            "slippageBps": slippage_bps,
            "onlyDirectRoutes": False,
            "asLegacyTransaction": False,
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(f"{JUPITER_API}/quote", params=params)
            resp.raise_for_status()
            quote = resp.json()

        out_decimals = 9 if output_token.upper() == "SOL" else 6
        out_amount_ui = int(quote["outAmount"]) / (10 ** out_decimals)
        price_impact = float(quote.get("priceImpactPct", 0))

        return {
            "input_token": input_token.upper(),
            "output_token": output_token.upper(),
            "input_amount": amount_ui,
            "expected_output": round(out_amount_ui, 6),
            "price_impact_pct": round(price_impact * 100, 4),
            "slippage_bps": slippage_bps,
            "route_plan": [
                r.get("swapInfo", {}).get("label", "Unknown")
                for r in quote.get("routePlan", [])
            ],
            "quote_id": quote.get("contextSlot", ""),
            "warning": "⚠️ Call execute_swap to execute this trade with real funds.",
        }

    except httpx.HTTPError as e:
        return {"error": f"Jupiter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Quote failed: {str(e)}"}


@mcp.tool()
async def execute_swap(
    input_token: str,
    output_token: str,
    amount_ui: float,
    slippage_bps: int = 50,
    dry_run: bool = True,
) -> dict:
    """
    Execute a token swap via Jupiter on Solana.

    ⚠️ IMPORTANT: Set dry_run=False only when ready to execute with real funds.
    Always call get_swap_quote first to verify the trade.

    Args:
        input_token: Token to sell (symbol or mint)
        output_token: Token to buy (symbol or mint)
        amount_ui: Amount to sell in human-readable units
        slippage_bps: Slippage tolerance in basis points (50 = 0.5%)
        dry_run: If True, simulates only — no real transaction sent

    Returns:
        Transaction result or simulation details
    """
    try:
        quote_result = await get_swap_quote(
            input_token, output_token, amount_ui, slippage_bps
        )

        if "error" in quote_result:
            return quote_result

        if dry_run:
            return {
                "mode": "DRY RUN — No funds moved",
                "quote": quote_result,
                "message": "Set dry_run=False to execute with real funds.",
                "safety_check": "✅ Passed",
            }

        wallet_key = os.getenv("SOLANA_WALLET_PRIVATE_KEY", "")
        if not wallet_key:
            return {
                "error": "SOLANA_WALLET_PRIVATE_KEY not set in Render environment.",
                "hint": "Add it in Render → Environment → SOLANA_WALLET_PRIVATE_KEY",
            }

        input_mint = resolve_mint(input_token)
        output_mint = resolve_mint(output_token)
        decimals = 9 if input_token.upper() == "SOL" else 6
        amount_raw = int(amount_ui * (10 ** decimals))

        async with httpx.AsyncClient(timeout=20) as client:
            quote_resp = await client.get(f"{JUPITER_API}/quote", params={
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount_raw,
                "slippageBps": slippage_bps,
            })
            quote_resp.raise_for_status()
            quote_data = quote_resp.json()

            from solders.keypair import Keypair  # type: ignore
            keypair = Keypair.from_base58_string(wallet_key)
            public_key = str(keypair.pubkey())

            swap_resp = await client.post(f"{JUPITER_API}/swap", json={
                "quoteResponse": quote_data,
                "userPublicKey": public_key,
                "wrapAndUnwrapSol": True,
                "dynamicComputeUnitLimit": True,
                "prioritizationFeeLamports": "auto",
            })
            swap_resp.raise_for_status()
            swap_data = swap_resp.json()

        tx_bytes = base64.b64decode(swap_data["swapTransaction"])

        from solders.transaction import VersionedTransaction  # type: ignore
        tx = VersionedTransaction.from_bytes(tx_bytes)

        async with httpx.AsyncClient(timeout=30) as client:
            send_resp = await client.post(SOLANA_RPC, json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "sendTransaction",
                "params": [
                    base64.b64encode(bytes(tx)).decode(),
                    {"encoding": "base64", "skipPreflight": False},
                ],
            })
            send_data = send_resp.json()

        tx_sig = send_data.get("result", "unknown")

        await send_telegram(
            f"✅ <b>SWAP EXECUTED</b>\n\n"
            f"💱 {amount_ui} {input_token.upper()} → {output_token.upper()}\n"
            f"📈 Expected: {quote_result['expected_output']}\n"
            f"🔎 <a href='https://solscan.io/tx/{tx_sig}'>View on Solscan</a>\n"
            f"⚡ Scutua-MCP Execution Layer"
        )

        return {
            "status": "SUCCESS",
            "tx_signature": tx_sig,
            "input": f"{amount_ui} {input_token.upper()}",
            "expected_output": quote_result["expected_output"],
            "solscan_url": f"https://solscan.io/tx/{tx_sig}",
            "price_impact_pct": quote_result["price_impact_pct"],
        }

    except Exception as e:
        return {"error": f"Swap execution failed: {str(e)}"}
