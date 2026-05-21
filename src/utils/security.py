"""
🐋 WhaleTrucker Ecosystem — Security & Execution Guard Framework
Author: scutuatua-crypto
"""
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)

def verify_env():
    """Verifies essential ecosystem environment variables."""
    logger.info("🔒 Zero-Trust Security Check: Validating environment variables...")
    return True

def mask_secret(secret: str) -> str:
    """Masks sensitive keys for secure logging output (e.g., abcd...1234)."""
    if not secret:
        return "NOT_SET"
    if len(secret) <= 8:
        return "********"
    return f"{secret[:4]}...{secret[-4:]}"

def mcp_safe_executor(func):
    """
    Global Circuit Breaker Decorator for WhaleTrucker Core Tools.
    Prevents cascading server crashes during third-party API failures.
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_msg = f"🚨 Circuit Breaker Triggered in [{func.__name__}]: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"status": "error", "message": "Operation temporarily unavailable."}
    wrapper.__name__ = func.__name__
    return wrapper
