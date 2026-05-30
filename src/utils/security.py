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
        r'ghp_\S+',
        r'dckr_pat_\S+',
        r'sk-\S+',
        r'Bearer\s+\S+',
    ]
    for pattern in patterns:
        value = re.sub(pattern, lambda m: m.group()[:4] + "****", value)
    
    return value
