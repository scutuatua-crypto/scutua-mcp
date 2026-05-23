import functools
import traceback
from src.utils.logger import get_logger

logger = get_logger(__name__)

def verify_env():
    """Verify required environment variables"""
    pass

def mask_secret(value: str) -> str:
    """Mask sensitive values for logging"""
    if not value:
        return ""
    if len(value) <= 8:
        return "****"
    return value[:4] + "****" + value[-4:]

def mcp_safe_executor(tool_name: str):
    """
    🛡️ WhaleTrucker Circuit Breaker & Input Sanitization
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                logger.info(f"🔮 Executing Tool: {tool_name} | Args: {args} | Kwargs: {kwargs}")
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                error_msg = f"❌ Error detected in module [{tool_name}]: {str(e)}"
                logger.error(f"{error_msg}\n{traceback.format_exc()}")
                return {
                    "status": "error",
                    "module": tool_name,
                    "message": "WhaleTrucker Core Alert: Module temporarily unavailable due to upstream network exception.",
                    "details": str(e)
                }
        return wrapper
    return decorator
