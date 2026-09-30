from flask import Flask, request, jsonify
import os, mysql.connector
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST","127.0.0.1"),
        port=int(os.getenv("DB_PORT","3306")),
        user=os.getenv("DB_USERNAME","root"),
        password=os.getenv("DB_PASSWORD",""),
        database=os.getenv("DB_DATABASE","budgetai")
    )

@app.get("/api/health")
def health():
    try:
        c=conn(); c.close()
        return jsonify({"ok":True,"database":"mysql"})
    except Exception as e:
        return jsonify({"ok":False,"error":str(e)}),500

@app.get("/api/transactions")
def get_transactions():
    c=conn(); cur=c.cursor(dictionary=True)
    cur.execute("SELECT * FROM transactions ORDER BY date DESC,id DESC LIMIT 100")
    rows=cur.fetchall(); cur.close(); c.close()
    return jsonify(rows)

@app.post("/api/transactions")
def create_transaction():
    d=request.json or {}
    required=["kind","amount","currency","category"]
    if any(k not in d for k in required):
        return jsonify({"error":"kind, amount, currency and category are required"}),400
    c=conn(); cur=c.cursor()
    cur.execute("""INSERT INTO transactions
      (kind,amount,currency,category,account,merchant,note,date)
      VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
      (d["kind"],d["amount"],d["currency"],d["category"],
       d.get("account","Cash"),d.get("merchant",""),d.get("note",""),
       d.get("date")))
    c.commit(); new_id=cur.lastrowid; cur.close(); c.close()
    return jsonify({"id":new_id,"saved":True}),201

@app.get("/api/accounts")
def get_accounts():
    c=conn(); cur=c.cursor(dictionary=True)
    cur.execute("SELECT * FROM accounts WHERE active=1 ORDER BY name")
    rows=cur.fetchall(); cur.close(); c.close()
    return jsonify(rows)

@app.get("/api/budgets")
def get_budgets():
    c=conn(); cur=c.cursor(dictionary=True)
    cur.execute("SELECT * FROM budgets ORDER BY month DESC,category")
    rows=cur.fetchall(); cur.close(); c.close()
    return jsonify(rows)

@app.get("/api/goals")
def get_goals():
    c=conn(); cur=c.cursor(dictionary=True)
    cur.execute("SELECT * FROM goals ORDER BY deadline")
    rows=cur.fetchall(); cur.close(); c.close()
    return jsonify(rows)

@app.get("/api/summary")
def summary():
    c=conn(); cur=c.cursor(dictionary=True)
    cur.execute("""SELECT currency,kind,SUM(amount) total
                   FROM transactions
                   WHERE date >= DATE_FORMAT(CURDATE(),'%Y-%m-01')
                   GROUP BY currency,kind""")
    rows=cur.fetchall(); cur.close(); c.close()
    return jsonify(rows)

if __name__=="__main__":
    app.run(host=os.getenv("API_HOST","127.0.0.1"),
            port=int(os.getenv("API_PORT","8000")),
            debug=False)
