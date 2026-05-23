"""
⚙ Centralized Configuration — Scutua-MCP
"""
import os
from dataclasses import dataclass

@dataclass
class Settings:
    # Server
    PORT: int = int(os.environ.get("PORT", 10000))
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    ENV: str = os.environ.get("ENV", "production")
    
    # GitHub
    GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
    
    # Crypto APIs
    COINGECKO_API_KEY: str = os.environ.get("COINGECKO_API_KEY", "")
    CMC_API_KEY: str = os.environ.get("CMC_API_KEY", "")
    
    # Solana
    SOLANA_RPC_URL: str = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Cache
    CACHE_TTL: int = int(os.environ.get("CACHE_TTL", 60))
    
    # Rate Limit
    RATE_LIMIT_PER_MIN: int = int(os.environ.get("RATE_LIMIT_PER_MIN", 60))

settings = Settings()

