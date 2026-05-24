import httpx
from mcp.server.fastmcp import FastMCP

def register_converter_tools(app: FastMCP):
    @app.tool()
    async def convert_crypto(amount: float, from_token: str, to_token: str) -> str:
        """Convert between crypto and fiat currencies"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_token.lower()}&vs_currencies={to_token.lower()}"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            rate = data.get(from_token.lower(), {}).get(to_token.lower(), 0)
            if rate == 0:
                return f"Cannot convert {from_token} to {to_token}"
            result = amount * rate
            return f"💱 Conversion:\n{amount} {from_token.upper()} = {result:,.4f} {to_token.upper()}\nRate: 1 {from_token.upper()} = {rate:,.4f} {to_token.upper()}"
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
            names = {"bitcoin":"BTC","ethereum":"ETH","solana":"SOL","ripple":"XRP"}
            for coin, symbol in names.items():
                price = data.get(coin, {}).get(base, "N/A")
                result.append(f"{symbol}: {price:,.2f} {base.upper()}")
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
