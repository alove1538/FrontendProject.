from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Aapka message Database me permanently save ho gaya hai!"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Database error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
