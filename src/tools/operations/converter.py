import httpx
from mcp.server.fastmcp import FastMCP

# Map symbol → CoinGecko ID
SYMBOL_TO_ID = {
    "btc": "bitcoin", "eth": "ethereum", "sol": "solana",
    "xrp": "ripple", "bnb": "binancecoin", "dot": "polkadot",
    "atom": "cosmos", "ton": "the-open-network", "reef": "reef",
    "avax": "avalanche-2", "matic": "matic-network", "op": "optimism",
    "arb": "arbitrum", "link": "chainlink", "uni": "uniswap",
    "ada": "cardano", "doge": "dogecoin", "shib": "shiba-inu",
    "ltc": "litecoin", "near": "near", "apt": "aptos",
    "sui": "sui", "hype": "hyperliquid", "bonk": "bonk",
}

# Fiat currencies supported by CoinGecko
FIAT = {"usd", "thb", "eur", "gbp", "jpy", "aud", "cad", "sgd", "hkd"}

def _resolve(token: str) -> str:
    """Resolve symbol or id to CoinGecko id"""
    t = token.lower().strip()
    return SYMBOL_TO_ID.get(t, t)

def register_converter_tools(app: FastMCP):

    @app.tool()
    async def convert_crypto(amount: float, from_token: str, to_token: str) -> str:
        """Convert between crypto and fiat currencies"""
        try:
            from_id = _resolve(from_token)
            to_lower = to_token.lower().strip()

            # crypto → fiat หรือ fiat ที่ CoinGecko รองรับ
            if to_lower in FIAT:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_id}&vs_currencies={to_lower}"
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    data = r.json()
                rate = data.get(from_id, {}).get(to_lower, 0)
                if rate == 0:
                    return f"Cannot convert {from_token} to {to_token} — token not found"
                result = amount * rate
                return f"💱 {amount} {from_token.upper()} = {result:,.4f} {to_token.upper()}\nRate: 1 {from_token.upper()} = {rate:,.4f} {to_token.upper()}"

            # crypto → crypto (ผ่าน USD)
            else:
                to_id = _resolve(to_token)
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_id},{to_id}&vs_currencies=usd"
                async with httpx.AsyncClient() as client:
                    r = await client.get(url, timeout=10)
                    data = r.json()
                from_usd = data.get(from_id, {}).get("usd", 0)
                to_usd = data.get(to_id, {}).get("usd", 0)
                if from_usd == 0 or to_usd == 0:
                    return f"Cannot convert {from_token} to {to_token} — price not found"
                rate = from_usd / to_usd
                result = amount * rate
                return f"💱 {amount} {from_token.upper()} = {result:,.6f} {to_token.upper()}\nRate: 1 {from_token.upper()} = {rate:,.6f} {to_token.upper()}"

        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_exchange_rates(base: str = "usd") -> str:
        """Get crypto exchange rates vs fiat"""
        try:
            tokens = "bitcoin,ethereum,solana,ripple"
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={tokens}&vs_currencies={base}"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            result = [f"💹 Exchange Rates (vs {base.upper()}):"]
            names = {"bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "ripple": "XRP"}
            for coin, symbol in names.items():
                price = data.get(coin, {}).get(base, "N/A")
                if isinstance(price, (int, float)):
                    result.append(f"{symbol}: {price:,.2f} {base.upper()}")
                else:
                    result.append(f"{symbol}: N/A")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def calculate_profit_loss(buy_price: float, current_price: float, amount: float) -> str:
        """Calculate crypto profit or loss"""
        try:
            invested = buy_price * amount
            current = current_price * amount
            pnl = current - invested
            pnl_pct = ((current_price - buy_price) / buy_price) * 100
            emoji = "🟢" if pnl >= 0 else "🔴"
            return f"""{emoji} P&L Calculator:
Amount: {amount} tokens
Buy Price: ${buy_price:,.4f}
Current Price: ${current_price:,.4f}
Invested: ${invested:,.2f}
Current Value: ${current:,.2f}
P&L: ${pnl:+,.2f} ({pnl_pct:+.2f}%)"""
        except Exception as e:
            return f"Error: {e}"
