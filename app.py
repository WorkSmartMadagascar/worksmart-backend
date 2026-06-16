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

    c.execute("""
    CREATE TABLE IF NOT EXISTS presence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricule TEXT,
        shift TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- GET EMPLOYEES ----------------
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM employees")
    rows = c.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])

# ---------------- ADD EMPLOYEE ----------------
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

    return jsonify({"message": "Ajouté avec succès"})

# ---------------- PRESENCE ----------------
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

# ---------------- GET PRESENCE ----------------
@app.route("/presence", methods=["GET"])
def get_presence():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM presence")
    rows = c.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
