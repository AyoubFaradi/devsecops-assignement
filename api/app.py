from flask import Flask, request, jsonify
import sqlite3
import bcrypt
import os
import logging
from pathlib import Path

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 🔐 Configuration via variables d’environnement
DATABASE = os.getenv("DATABASE_PATH", "users.db")
SAFE_DIR = Path(os.getenv("SAFE_DIR", "/app/safe_files"))
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))


def get_db():
    return sqlite3.connect(DATABASE)


@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

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
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    hashed = bcrypt.hashpw(data["text"].encode(), bcrypt.gensalt())
    return jsonify({"hash": hashed.decode()})


@app.route("/file", methods=["POST"])
def read_file():
    data = request.get_json(silent=True)
    if not data or "filename" not in data:
        return jsonify({"error": "Filename required"}), 400

    requested_path = (SAFE_DIR / data["filename"]).resolve()

    if not str(requested_path).startswith(str(SAFE_DIR)):
        return jsonify({"error": "Access denied"}), 403

    if not requested_path.exists():
        return jsonify({"error": "File not found"}), 404

    return jsonify({"content": requested_path.read_text()})


@app.route("/log", methods=["POST"])
def log_data():
    logging.info("User input received")
    return jsonify({"status": "logged"})


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False)
