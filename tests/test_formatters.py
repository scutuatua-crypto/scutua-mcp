"""📊 Test Formatters"""

from src.utils.formatters import format_usd, format_wallet, format_tier

def test_format_usd_millions():
    assert format_usd(1_500_000) == "$1.50M"

def test_format_usd_thousands():
    assert format_usd(5_000) == "$5.00K"

def test_format_usd_small():
    assert format_usd(99.5) == "$99.50"

def test_format_wallet():
    addr = "0x1234567890abcdef1234"
    result = format_wallet(addr)
    assert "..." in result

def test_format_tier():
    assert "Diamond" in format_tier(100)
    assert "Bronze" in format_tier(1)
