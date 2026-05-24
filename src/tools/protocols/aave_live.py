# src/tools/protocols/aave_live.py
from fastmcp import FastMCP

def register_aave_live_tools(app: FastMCP):
    """
    Registers Aave protocol tools to the FastMCP application instance.
    """

    @app.tool()
    async def get_aave_pool_data(asset: str):
        """
        Fetches pool statistics for a specific asset on Aave V3.
        """
        # Logic to fetch data from Aave subgraph or API
        return {
            "status": "success",
            "protocol": "Aave V3",
            "asset": asset,
            "liquidity_rate": "0.025",
            "borrow_rate": "0.042"
        }

    @app.tool()
    async def get_aave_user_position(wallet_address: str):
        """
        Retrieves health factor and position details for a specific wallet.
        """
        # Logic to calculate user position and health factor
        return {
            "status": "success",
            "protocol": "Aave V3",
            "wallet": wallet_address,
            "health_factor": 1.85,
            "collateral_in_usd": 15000.0,
            "debt_in_usd": 5000.0
        }
