"""🎨 NFT Floor Tools — Floor Price & Collection Tracker"""
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
logger = get_logger(__name__)
OPENSEA_API = "https://api.opensea.io/api/v2/collections/{slug}/stats"
MAGICEDEN_API = "https://api-mainnet.magiceden.dev/v2/collections/{symbol}/stats"
MOCK_NFTS = {
    "boredapeyachtclub": {"name":"Bored Ape Yacht Club","chain":"ethereum","floor_eth":11.5,"floor_usd":35650,"volume_24h":245.8,"owners":5412},
    "cryptopunks":       {"name":"CryptoPunks","chain":"ethereum","floor_eth":42.0,"floor_usd":130200,"volume_24h":180.5,"owners":3521},
    "azuki":             {"name":"Azuki","chain":"ethereum","floor_eth":5.8,"floor_usd":17980,"volume_24h":98.2,"owners":4812},
    "pudgypenguins":     {"name":"Pudgy Penguins","chain":"ethereum","floor_eth":7.2,"floor_usd":22320,"volume_24h":112.4,"owners":4251},
    "madlads":           {"name":"Mad Lads","chain":"solana","floor_sol":185.0,"floor_usd":27380,"volume_24h":4820.5,"owners":8124},
    "okaybears":         {"name":"Okay Bears","chain":"solana","floor_sol":42.0,"floor_usd":6216,"volume_24h":1250.8,"owners":6521},
}
def register_nft_floor_tools(app: FastMCP):
    @app.tool()
    async def get_nft_floor(collection: str) -> str:
        \"\"\"Get floor price for an NFT collection. e.g. boredapeyachtclub, madlads, azuki, cryptopunks\"\"\"
        slug=collection.lower().strip().replace(" ","")
        mock=MOCK_NFTS.get(slug)
        if not mock: return f"❌ '{collection}' not found. Try: {', '.join(MOCK_NFTS)}"
        if mock["chain"]=="ethereum": floor=f"{mock['floor_eth']} ETH (~${mock['floor_usd']:,.0f})"
        else: floor=f"{mock['floor_sol']} SOL (~${mock['floor_usd']:,.0f})"
        return f"🎨 {mock['name']}\nChain: {mock['chain'].title()}  Floor: {floor}\nVol 24h: {mock['volume_24h']}  Owners: {mock['owners']:,}"
    @app.tool()
    async def list_nft_collections() -> str:
        \"\"\"List all tracked NFT collections.\"\"\"
        lines=["🎨 NFT Collections\n",f"{'Name':<30} {'Chain':<10} {'Floor':>14} {'Vol 24h':>10}","─"*68]
        for slug,d in MOCK_NFTS.items():
            floor=f"{d.get('floor_eth','?')} ETH" if d['chain']=="ethereum" else f"{d.get('floor_sol','?')} SOL"
            lines.append(f"{d['name']:<30} {d['chain']:<10} {floor:>14} {d['volume_24h']:>10.1f}")
        return "\n".join(lines)
    @app.tool()
    async def compare_nft_floors(collections: str) -> str:
        \"\"\"Compare floors for comma-separated collection slugs.\"\"\"
        slugs=[s.strip().lower() for s in collections.split(",")]
        lines=["🎨 NFT Comparison\n",f"{'Name':<30} {'Floor':>14} {'Owners':>8}","─"*56]
        for s in slugs:
            d=MOCK_NFTS.get(s)
            if not d: lines.append(f"{s:<30} N/A"); continue
            floor=f"{d.get('floor_eth','?')} ETH" if d['chain']=="ethereum" else f"{d.get('floor_sol','?')} SOL"
            lines.append(f"{d['name']:<30} {floor:>14} {d['owners']:>8,}")
        return "\n".join(lines)
