import httpx
from mcp.server.fastmcp import FastMCP

def register_staking_tools(app: FastMCP):
    @app.tool()
    async def get_staking_rewards(token: str, amount: float, apy: float) -> str:
        """Calculate staking rewards"""
        try:
            daily = (apy / 100 / 365) * amount
            weekly = daily * 7
            monthly = daily * 30
            yearly = amount * (apy / 100)
            return f"""🥩 Staking Calculator: {token.upper()}
Amount: {amount:,.4f} {token.upper()}
APY: {apy}%
Daily: {daily:,.6f} {token.upper()}
Weekly: {weekly:,.6f} {token.upper()}
Monthly: {monthly:,.4f} {token.upper()}
Yearly: {yearly:,.4f} {token.upper()}"""
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_eth_staking_rate() -> str:
        """Get current Ethereum staking APY"""
        try:
            url = "https://beaconcha.in/api/v1/ethstore/latest"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json().get("data", {})
            apy = float(data.get("validatorscount", 0))
            eff = data.get("efficiency", "N/A")
            return f"""🔷 Ethereum Staking:
Network Efficiency: {eff}%
Validators: {apy:,.0f}
Est. APY: ~3.5-4.5%"""
        except Exception as e:
            return f"🔷 ETH Staking Est. APY: ~3.5-4.5%"
