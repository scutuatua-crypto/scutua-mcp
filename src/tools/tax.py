"""🧾 Tax Tools — Crypto P&L & Capital Gains Calculator"""
from mcp.server.fastmcp import FastMCP
from src.utils.logger import get_logger
logger = get_logger(__name__)
def _calc_pnl(trades, method="FIFO"):
    lots, realized, proceeds, cost_total, details = [], 0.0, 0.0, 0.0, []
    for t in trades:
        amt, price, date = float(t["amount"]), float(t["price"]), t.get("date","N/A")
        if t["type"].lower() == "buy":
            lots.append({"amount":amt,"cost":price,"date":date})
        elif t["type"].lower() == "sell":
            proc = amt * price; proceeds += proc; remaining = amt; cb = 0.0
            src = lots if method=="FIFO" else list(reversed(lots)) if method=="LIFO" else sorted(lots,key=lambda x:x["cost"],reverse=True)
            new_lots = []
            for lot in src:
                if remaining <= 0: new_lots.append(lot); continue
                use = min(lot["amount"], remaining); cb += use*lot["cost"]; remaining -= use
                if lot["amount"]-use > 0: new_lots.append({"amount":lot["amount"]-use,"cost":lot["cost"],"date":lot["date"]})
            lots = list(reversed(new_lots)) if method=="LIFO" else new_lots
            pnl = proc - cb; realized += pnl; cost_total += cb
            details.append({"date":date,"amount":amt,"price":price,"proceeds":proc,"cost_basis":cb,"pnl":pnl})
    return {"realized_pnl":round(realized,4),"total_proceeds":round(proceeds,4),"total_cost_basis":round(cost_total,4),"trades_detail":details}
def register_tax_tools(app: FastMCP):
    @app.tool()
    async def calculate_pnl(token: str, trades_csv: str, method: str = "FIFO") -> str:
        \"\"\"Calculate realized P&L. trades_csv format: type,amount,price,date per line. method: FIFO/LIFO/HIFO\"\"\"
        method = method.upper()
        if method not in ("FIFO","LIFO","HIFO"): return "❌ Method must be FIFO/LIFO/HIFO"
        trades = []
        for line in trades_csv.strip().splitlines():
            p = [x.strip() for x in line.split(",")]
            if len(p) >= 3:
                try: trades.append({"type":p[0],"amount":float(p[1]),"price":float(p[2]),"date":p[3] if len(p)>3 else "N/A"})
                except: pass
        if not trades: return "❌ No valid trades. Format: type,amount,price,date"
        r = _calc_pnl(trades, method)
        sign = "+" if r["realized_pnl"]>=0 else ""
        status = "✅ Profit" if r["realized_pnl"]>=0 else "🔴 Loss"
        out = [f"🧾 P&L — {token.upper()} ({method})\n{sign}${r['realized_pnl']:,.4f}  {status}\nProceeds: ${r['total_proceeds']:,.4f}  Cost: ${r['total_cost_basis']:,.4f}\n"]
        for t in r["trades_detail"]:
            s = "+" if t["pnl"]>=0 else ""; out.append(f"  {t['date']}  {t['amount']} @ ${t['price']:,.2f}  P&L: {s}${t['pnl']:,.4f}")
        return "\n".join(out)
    @app.tool()
    async def estimate_tax_liability(realized_pnl_usd: float, holding_days: int, income_bracket: str = "medium", country: str = "US") -> str:
        \"\"\"Estimate tax on crypto gains. income_bracket: low/medium/high. country: US/TH\"\"\"
        if realized_pnl_usd <= 0: return "✅ No taxable gain."
        c, b = country.upper(), income_bracket.lower()
        if c == "US":
            if holding_days >= 365: rate = {"low":0.0,"medium":0.15,"high":0.20}.get(b,0.15); gt = "Long-term"
            else: rate = {"low":0.12,"medium":0.22,"high":0.37}.get(b,0.22); gt = "Short-term"
        elif c == "TH": rate = 0.15; gt = "Withholding"
        else: rate = 0.20; gt = "Estimated"
        tax = realized_pnl_usd * rate
        return f"🧾 Tax Estimate — {c}\nType: {gt} ({holding_days}d)  Rate: {rate*100:.1f}%\nGross: ${realized_pnl_usd:,.2f}  Tax: ${tax:,.2f}  Net: ${realized_pnl_usd-tax:,.2f}\nNote: Consult a tax professional."
    @app.tool()
    async def compare_cost_methods(token: str, trades_csv: str) -> str:
        \"\"\"Compare P&L across FIFO, LIFO, HIFO methods.\"\"\"
        trades = []
        for line in trades_csv.strip().splitlines():
            p = [x.strip() for x in line.split(",")]
            if len(p)>=3:
                try: trades.append({"type":p[0],"amount":float(p[1]),"price":float(p[2]),"date":p[3] if len(p)>3 else "N/A"})
                except: pass
        if not trades: return "❌ No valid trades."
        lines = [f"🧾 Cost Methods — {token.upper()}\n{'Method':<8} {'P&L':>14}"]
        for m in ("FIFO","LIFO","HIFO"):
            r = _calc_pnl(trades, m); s = "+" if r["realized_pnl"]>=0 else ""
            lines.append(f"{m:<8} {s}${r['realized_pnl']:>12,.4f}")
        return "\n".join(lines)
