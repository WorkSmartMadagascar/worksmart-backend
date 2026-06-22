from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"

# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # EMPLOYEES (tu peux garder)
    c.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricule TEXT UNIQUE,
        nom TEXT,
        adresse TEXT,
        section TEXT,
        fonction TEXT,
        statut TEXT,
        etat TEXT
    )
    """)

    # PRESENCE (tu peux garder)
    c.execute("""
    CREATE TABLE IF NOT EXISTS presence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricule TEXT,
        shift TEXT,
        date TEXT
    )
    """)

    # 🟡 PRODUCTS (SHOP)
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        description TEXT,
        image TEXT
    )
    """)

    # 🟡 ORDERS (SHOP)
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        items TEXT,
        total INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- EMPLOYEES ----------------
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM employees")
    rows = c.fetchall()

    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("""
        INSERT INTO employees (matricule, nom, adresse, section, fonction, statut, etat)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("matricule"),
            data.get("nom"),
            data.get("adresse"),
            data.get("section"),
            data.get("fonction"),
            data.get("statut"),
            data.get("etat")
        ))
        conn.commit()

    except sqlite3.IntegrityError:
        return jsonify({"error": "Matricule déjà existant"}), 400

    finally:
        conn.close()

    return jsonify({"message": "Employé ajouté"})


# ---------------- PRESENCE ----------------
@app.route("/presence", methods=["GET"])
def get_presence():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM presence")
    rows = c.fetchall()

    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/presence", methods=["POST"])
def add_presence():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO presence (matricule, shift, date)
    VALUES (?, ?, ?)
    """, (
        data.get("matricule"),
        data.get("shift"),
        data.get("date")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Présence ajoutée"})


# ---------------- 🛒 PRODUCTS ----------------
@app.route("/products", methods=["GET"])
def get_products():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    rows = c.fetchall()

    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO products (name, price, description, image)
    VALUES (?, ?, ?, ?)
    """, (
        data.get("name"),
        data.get("price"),
        data.get("description"),
        data.get("image")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Produit ajouté"})


# ---------------- 🛒 ORDERS ----------------
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM orders")
    rows = c.fetchall()

    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO orders (items, total, date)
    VALUES (?, ?, ?)
    """, (
        str(data.get("items")),
        data.get("total"),
        data.get("date")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Commande enregistrée"})


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
