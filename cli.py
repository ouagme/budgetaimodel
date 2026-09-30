import os,re,requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()
BASE=os.getenv("API_URL","http://127.0.0.1:8000")

def api(method,path,**kw):
    try:
        r=requests.request(method,BASE+path,timeout=5,**kw)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Cannot reach local API:",e)
        return None

def add(kind,amount,currency,category):
    x=api("POST","/api/transactions",json={
        "kind":kind,"amount":amount,"currency":currency.upper(),
        "category":category,"account":"Cash",
        "date":date.today().isoformat()
    })
    if x:
        print("Saved locally in MySQL. ID:",x["id"])

def dashboard():
    rows=api("GET","/api/summary") or []
    print("\nBudgetAI — MySQL Local Dashboard")
    for r in rows:
        print(f'{r["currency"]}: {r["kind"]} {float(r["total"]):.2f}')

def natural(t):
    l=t.lower()
    if "dashboard" in l or "summary" in l:
        dashboard(); return
    if "transactions" in l:
        rows=api("GET","/api/transactions") or []
        for r in rows:
            print(r)
        return
    m=re.search(r"(\d+(?:[.,]\d+)?)\s*(MAD|EUR|USD|GBP|CAD|CHF)?",l)
    if m and any(x in l for x in ["spent","paid","bought","expense","received","salary","income"]):
        amount=float(m.group(1).replace(",",".")); cur=m.group(2) or "MAD"
        kind="income" if any(x in l for x in ["received","salary","income"]) else "expense"
        words=re.findall(r"[a-zA-ZÀ-ÿ]+",l.replace(m.group(0),""))
        stop={"i","spent","paid","bought","expense","received","salary","income","on","for","my","today"}
        cat=next((w for w in reversed(words) if w not in stop),"other")
        add(kind,amount,cur,cat); return
    print("Examples: I spent 120 MAD on food | I received 9000 MAD salary | dashboard")

print("BudgetAI v3 — Local MySQL/MariaDB")
print("API:",BASE)
print("Type 'exit' to quit.")

while True:
    try:
        q=input("\nYou: ").strip()
    except (EOFError,KeyboardInterrupt):
        break
    if q.lower() in ("exit","quit"):
        break
    if q:
        natural(q)
