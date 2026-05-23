"""
⚡ Cache Layer — Scutua-MCP
"""
import time
from typing import Any, Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MemoryCache:
    def __init__(self, default_ttl: int = 60):
        self._cache: dict = {}
        self._ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expires_at = self._cache[key]
            if time.time() < expires_at:
                logger.info(f"✅ Cache HIT: {key}")
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires_at = time.time() + (ttl or self._ttl)
        self._cache[key] = (value, expires_at)
        logger.info(f"💾 Cache SET: {key} TTL={ttl or self._ttl}s")

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
        logger.info("🧹 Cache CLEARED")

cache = MemoryCache()

