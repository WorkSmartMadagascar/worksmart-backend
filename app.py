from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# DB INIT
def init_db():
    conn = sqlite3.connect("database.db")
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

# -------- EMPLOYES --------
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute("""
        INSERT INTO employees (matricule, nom, adresse, section, fonction, statut, etat)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["matricule"],
            data["nom"],
            data["adresse"],
            data["section"],
            data["fonction"],
            data["statut"],
            data["etat"]
        ))
        conn.commit()
    except:
        return jsonify({"error": "Matricule déjà existant"}), 400

    conn.close()
    return jsonify({"message": "Ajouté avec succès"})

# -------- PRESENCE --------
@app.route("/presence", methods=["POST"])
def add_presence():
    data = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO presence (matricule, shift, date)
    VALUES (?, ?, ?)
    """, (data["matricule"], data["shift"], data["date"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Présence ajoutée"})

@app.route("/presence", methods=["GET"])
def get_presence():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM presence")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
