import httpx
from mcp.server.fastmcp import FastMCP

def register_nft_tools(app: FastMCP):
    @app.tool()
    async def get_nft_collection(collection: str) -> str:
        """Get NFT collection stats from OpenSea"""
        try:
            url = f"https://api.opensea.io/api/v2/collections/{collection}"
            headers = {"accept": "application/json"}
            async with httpx.AsyncClient() as client:
                r = await client.get(url, headers=headers, timeout=10)
                data = r.json()
            name = data.get("name", collection)
            floor = data.get("floor_price", {}).get("unit", "N/A")
            owners = data.get("owner_count", "N/A")
            supply = data.get("total_supply", "N/A")
            return f"""🖼 NFT Collection: {name}
Floor Price: {floor} ETH
Owners: {owners:,}
Total Supply: {supply:,}"""
        except Exception as e:
            return f"Error: {e}"

    @app.tool()
    async def get_top_nft_collections() -> str:
        """Get trending NFT collections"""
        try:
            url = "https://api.coingecko.com/api/v3/nfts/list?order=market_cap_usd_desc&per_page=5"
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)
                data = r.json()
            result = ["🎨 Top NFT Collections:"]
            for i, nft in enumerate(data[:5], 1):
                result.append(f"{i}. {nft.get('name')} ({nft.get('symbol', '').upper()})")
            return "\n".join(result)
        except Exception as e:
            return f"Error: {e}"
