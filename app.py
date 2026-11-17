import random
import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)
DB = "inventory.db"

ITEMS = [
    {"name":"MP9 | Cobalt Grid","rarity":"Mil-Spec","color":"#4b69ff","weight":79.92},
    {"name":"Glock-18 | Violet Circuit","rarity":"Restricted","color":"#8847ff","weight":15.98},
    {"name":"AK-47 | Neon Ember","rarity":"Classified","color":"#d32ce6","weight":3.20},
    {"name":"AWP | Crimson Pulse","rarity":"Covert","color":"#eb4b4b","weight":0.64},
    {"name":"Rare Special Item","rarity":"Special","color":"#ffd700","weight":0.26},
]

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, rarity TEXT, color TEXT, opened_at DATETIME DEFAULT CURRENT_TIMESTAMP)")

@app.route('/')
def index():
    return render_template('index.html', items=ITEMS)

@app.post('/api/open')
def open_case():
    item=random.choices(ITEMS, weights=[x['weight'] for x in ITEMS], k=1)[0]
    with sqlite3.connect(DB) as con:
        con.execute("INSERT INTO inventory(name,rarity,color) VALUES(?,?,?)", (item['name'],item['rarity'],item['color']))
    return jsonify(item)

@app.get('/api/inventory')
def inventory():
    with sqlite3.connect(DB) as con:
        con.row_factory=sqlite3.Row
        rows=con.execute("SELECT * FROM inventory ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
