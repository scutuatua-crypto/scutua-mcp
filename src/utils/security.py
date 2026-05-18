"""🔒 Zero-Trust Security"""

import os
import re

REQUIRED_ENV = ["GITHUB_TOKEN", "SOLANA_API"]

def verify_env():
    """ตรวจสอบ env ครบก่อน boot"""
    missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
    if missing:
        raise EnvironmentError(f"❌ Missing secrets: {missing}")

def mask_secret(text: str) -> str:
    """ปิดบัง token ใน logs"""
    return re.sub(r"(ghp_|dckr_pat_|Bearer )\S+", r"\1***MASKED***", text)
