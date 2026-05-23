"""
🛡️ Rate Limiter — Scutua-MCP
"""
import time
from collections import defaultdict
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self, max_calls: int = 60, period: int = 60):
        self._max_calls = max_calls
        self._period = period
        self._calls: dict = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        calls = self._calls[key]
        self._calls[key] = [t for t in calls if now - t < self._period]
        if len(self._calls[key]) < self._max_calls:
            self._calls[key].append(now)
            return True
        logger.warning(f"⛔ Rate limit exceeded: {key}")
        return False

    def remaining(self, key: str) -> int:
        now = time.time()
        calls = [t for t in self._calls[key] if now - t < self._period]
        return max(0, self._max_calls - len(calls))

rate_limiter = RateLimiter()

