"""
Centralized Configuration — Scutua-MCP
Manages system-wide environment variables and infrastructure configurations.
"""
import os
from dataclasses import dataclass

@dataclass
class Settings:
    # Infrastructure & Runtime Execution
    PORT: int = int(os.environ.get("PORT", 10000))
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    ENV: str = os.environ.get("ENV", "production")
    
    # Core Utilities Layer
    CACHE_TTL: int = int(os.environ.get("CACHE_TTL", 60))
    RATE_LIMIT_PER_MIN: int = int(os.environ.get("RATE_LIMIT_PER_MIN", 60))
    
    # Dimension 1: Multi-Chain Universe RPC Gateways
    SOLANA_RPC_URL: str = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    
    # Dimension 4: Operations & DevOps Integration
    GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")
    
    # Dimension 5: Market Intelligence Provider Authentication
    COINGECKO_API_KEY: str = os.environ.get("COINGECKO_API_KEY", "")
    CMC_API_KEY: str = os.environ.get("CMC_API_KEY", "")

settings = Settings()
