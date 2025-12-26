from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os
import logging
from pathlib import Path

app = Flask(__name__)

# 🔐 Secret via variable d’environnement
API_KEY = os.getenv("API_KEY", "CHANGE_ME")

# 🔒 Logging sécurisé
logging.basicConfig(level=logging.INFO)

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

    if not text:
        return jsonify({"error": "Empty input"}), 400

    hashed = bcrypt.hashpw(text.encode(), bcrypt.gensalt())
    return jsonify({"hash": hashed.decode()})


@app.route("/file", methods=["POST"])
def read_file():
    filename = request.json.get("filename")

    if not filename:
        return jsonify({"error": "Filename required"}), 400

    requested_path = (SAFE_DIR / filename).resolve()

    if not str(requested_path).startswith(str(SAFE_DIR)):
        return jsonify({"error": "Access denied"}), 403

    if not requested_path.exists():
        return jsonify({"error": "File not found"}), 404

    return jsonify({"content": requested_path.read_text()})


@app.route("/log", methods=["POST"])
def log_data():
    data = request.json
    logging.info("User input received")
    return jsonify({"status": "logged"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
