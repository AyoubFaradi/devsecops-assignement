from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os
import logging
from pathlib import Path

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("API_KEY")
DATABASE = "users.db"
SAFE_DIR = Path("/app/safe_files")

def get_db():
    return sqlite3.connect(DATABASE)

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row[0]):
        return jsonify({"status": "authenticated"})

    return jsonify({"status": "denied"}), 401

@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.json.get("text", "")
    hashed = bcrypt.hashpw(text.encode(), bcrypt.gensalt())
    return jsonify({"hash": hashed.decode()})

@app.route("/file", methods=["POST"])
def read_file():
    filename = request.json.get("filename")
    path = (SAFE_DIR / filename).resolve()

    if not str(path).startswith(str(SAFE_DIR)):
        return jsonify({"error": "Access denied"}), 403

    if not path.exists():
        return jsonify({"error": "File not found"}), 404

    return jsonify({"content": path.read_text()})

@app.route("/log", methods=["POST"])
def log_data():
    logging.info("User input received")
    return jsonify({"status": "logged"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
