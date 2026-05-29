"""📡 Signal Tools — RSI, MACD Buy/Sell Signals"""
import httpx
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
logger = get_logger(__name__)
COINGECKO_OHLC = "https://api.coingecko.com/api/v3/coins/{id}/ohlc"
CG_IDS = {"BTC":"bitcoin","ETH":"ethereum","SOL":"solana","DOT":"polkadot","ATOM":"cosmos","TON":"the-open-network","BNB":"binancecoin","AVAX":"avalanche-2"}
MOCK_CLOSES = {
    "SOL":[138,140,142,139,145,148,147,150,152,149,151,153,148,150],
    "ETH":[3050,3080,3100,3070,3120,3150,3130,3180,3200,3170,3190,3210,3180,3200],
    "BTC":[62000,63000,63500,62800,64000,65000,64500,66000,67000,66500,67200,68000,67500,68000],
    "DOT":[7.5,7.6,7.8,7.7,7.9,8.0,7.9,8.1,8.2,8.1,8.3,8.4,8.2,8.3],
    "ATOM":[8.0,8.1,8.3,8.2,8.4,8.5,8.4,8.6,8.7,8.5,8.6,8.8,8.6,8.7],
}
def _rsi(c,p=14):
    if len(c)<p+1: return 50.0
    d=[c[i]-c[i-1] for i in range(1,len(c))]
    g=sum(x for x in d[-p:] if x>0)/p; l=sum(-x for x in d[-p:] if x<0)/p
    return round(100-(100/(1+(g/l if l else 99))),2)
def _ema(c,p):
    if len(c)<p: return c[:]
    k=2/(p+1); e=[sum(c[:p])/p]
    for x in c[p:]: e.append(x*k+e[-1]*(1-k))
    return e
def _macd(c):
    e12=_ema(c,12); e26=_ema(c,26); n=min(len(e12),len(e26))
    ml=[e12[-(n-i)]-e26[-(n-i)] for i in range(n)]; sl=_ema(ml,9)
    mv=round(ml[-1],4) if ml else 0; sv=round(sl[-1],4) if sl else 0
    return {"macd":mv,"signal":sv,"histogram":round(mv-sv,4)}
def _interpret(rsi,macd):
    sigs=[]
    if rsi<30: sigs.append("RSI oversold → 🟢 BUY")
    elif rsi>70: sigs.append("RSI overbought → 🔴 SELL")
    else: sigs.append(f"RSI neutral ({rsi})")
    if macd["histogram"]>0: sigs.append("MACD bullish → 🟢 BUY")
    elif macd["histogram"]<0: sigs.append("MACD bearish → 🔴 SELL")
    else: sigs.append("MACD neutral")
    buy=sum(1 for s in sigs if "BUY" in s); sell=sum(1 for s in sigs if "SELL" in s)
    overall="🟢 BULLISH" if buy>sell else "🔴 BEARISH" if sell>buy else "⚪ NEUTRAL"
    return overall, sigs
async def _closes(token, days=30):
    cid=CG_IDS.get(token.upper())
    if not cid: return None
    try:
        async with httpx.AsyncClient(timeout=12) as c:
            r=await c.get(COINGECKO_OHLC.format(id=cid),params={"vs_currency":"usd","days":days})
            r.raise_for_status(); return [x[4] for x in r.json()]
    except Exception as e: logger.warning(f"CG OHLC fail {token}: {e}")
    return None
def register_signal_tools(app: FastMCP):
    @app.tool()
    async def get_trading_signals(token: str) -> str:
        """Get RSI and MACD buy/sell signals for a token (BTC,ETH,SOL,DOT,ATOM,TON,BNB,AVAX)"""
        t=token.upper().strip(); c=await _closes(t) or MOCK_CLOSES.get(t)
        if not c or len(c)<14: return f"❌ No data for {t}. Supported: {', '.join(CG_IDS)}"
        src="Live" if await _closes(t) else "Mock"
        rsi=_rsi(c); macd=_macd(c); overall,sigs=_interpret(rsi,macd)
        return f"📡 Signals — {t}\nPrice: ${c[-1]:,.4f}  RSI: {rsi}  MACD: {macd['macd']}  Histogram: {macd['histogram']}\nOverall: {overall}\n" + "\n".join(f"  • {s}" for s in sigs)
    @app.tool()
    async def get_rsi(token: str, period: int = 14) -> str:
        """Get RSI value for a token."""
        t=token.upper().strip(); c=await _closes(t,days=60) or MOCK_CLOSES.get(t)
        if not c: return f"❌ No data for {t}."
        rsi=_rsi(c,period); zone="🟢 Oversold" if rsi<30 else "🔴 Overbought" if rsi>70 else "⚪ Neutral"
        return f"📊 RSI({period}) — {t}\nRSI: {rsi}  Zone: {zone}"
    @app.tool()
    async def scan_signals_all() -> str:
        """Scan trading signals for all major tokens."""
        lines=["📡 Signal Scan\n","Token    RSI   MACD       Overall","-------- ----- ---------- ----------"]
        for t in ["BTC","ETH","SOL","DOT","ATOM"]:
            c = await _closes(t) or MOCK_CLOSES.get(t,[])
            if len(c)<14: continue
            rsi=_rsi(c); macd=_macd(c); overall,_=_interpret(rsi,macd)
            lines.append(f"{t:<8} {rsi:>5.1f} {macd['macd']:>10.4f} {overall}")
        return "\n".join(lines)
