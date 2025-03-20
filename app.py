from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import sqlite3
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Create a database connection
def get_db_connection():
    conn = sqlite3.connect(os.getenv('DATABASE_URL', 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript('DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS packages;')
        conn.executescript(f.read().decode('utf8'))
    conn.commit()
    conn.close()

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)