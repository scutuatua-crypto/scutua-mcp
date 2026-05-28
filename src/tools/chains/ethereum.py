    @app.tool()
    async def get_eth_gas() -> dict:
        """Get Ethereum gas prices"""
        return await _format_gas_response(await get_eth_gas_price(), "ethereum")

    @app.tool()
    async def get_arbitrum_gas_price() -> dict:
        """Get Arbitrum gas prices"""
        # สมมติว่าคุณมีฟังก์ชันดึงค่าของ Arbitrum แล้ว
        return await _format_gas_response(await get_arbitrum_gas_price(), "arbitrum")

    @app.tool()
    async def get_optimism_gas_price() -> dict:
        """Get Optimism gas prices"""
        return await _format_gas_response(await get_optimism_gas_price(), "optimism")

    @app.tool()
    async def get_bnb_gas_price() -> dict:
        """Get BNB gas prices"""
        return await _format_gas_response(await get_bnb_gas_price(), "bnb")

# สร้างฟังก์ชันกลางเพื่อจัด Format (จะช่วยให้โค้ดสะอาดขึ้นมาก ไม่ต้องเขียนซ้ำๆ)
async def _format_gas_response(result: dict, chain_name: str) -> dict:
    if "error" in result:
        return {"status": "fail", "chain": chain_name, "error": result['error']}
    
    return {
        "status": "success",
        "chain": chain_name,
        "data": {
            "slow": result.get("slow"),
            "standard": result.get("standard"),
            "fast": result.get("fast"),
            "base_fee": result.get("base_fee")
        }
    }
