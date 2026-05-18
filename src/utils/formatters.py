"""📊 Formatters — Money & Display"""

def format_usd(amount: float) -> str:
    """Format ตัวเลขเงินให้ดูง่าย"""
    if amount >= 1_000_000:
        return f"${amount/1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.2f}K"
    return f"${amount:.2f}"

def format_wallet(address: str, chars: int = 8) -> str:
    """ย่อ wallet address"""
    return f"{address[:chars]}...{address[-4:]}"

def format_tier(score: float) -> str:
    """แปลง score เป็น tier"""
    if score >= 100: return "💎 Diamond Whale"
    if score >= 50:  return "🥇 Gold Whale"
    if score >= 10:  return "🥈 Silver Whale"
    return "🥉 Bronze Whale"

