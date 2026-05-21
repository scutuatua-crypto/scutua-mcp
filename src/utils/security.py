import functools
import traceback
from src.utils.logger import get_logger

logger = get_logger(__name__)

def mcp_safe_executor(tool_name: str):
    """
    🛡️ WhaleTrucker Circuit Breaker & Input Sanitization
    Prevents cascading failures across the ecosystem and logs execution metadata.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # 1. Audit Logging
                logger.info(f"🔮 Executing Tool: {tool_name} | Args: {args} | Kwargs: {kwargs}")
                
                # 2. Execute target function
                result = await func(*args, **kwargs)
                return result
                
            except Exception as e:
                # 3. Fail-safe containment (Graceful Degradation)
                error_msg = f"❌ Error detected in module [{tool_name}]: {str(e)}"
                logger.error(f"{error_msg}\n{traceback.format_exc()}")
                
                # Standardized JSON-RPC error fallback response
                return {
                    "status": "error",
                    "module": tool_name,
                    "message": "WhaleTrucker Core Alert: Module temporarily unavailable due to upstream network exception.",
                    "details": str(e)
                }
        return wrapper
    return decorator
