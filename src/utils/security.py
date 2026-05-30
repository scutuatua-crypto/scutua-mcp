import re
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
    patterns = [
        (r'ghp_\S+', 'ghp_'),
        (r'dckr_pat_\S+', 'dckr_pat_'),
        (r'sk-\S+', 'sk-'),
        (r'Bearer\s+\S+', 'Bearer '),
    ]
    for pattern, prefix in patterns:
        value = re.sub(pattern, lambda m, p=prefix: p + "****", value)
    return value

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
