from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Inicializa o banco de dados
def init_db():
    with sqlite3.connect('telemetria.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hostname TEXT,
                sistema TEXT,
                cpu_percent REAL,
                memoria TEXT,
                disco TEXT,
                screenshot TEXT
            )
        ''')
        conn.commit()

@app.route('/api/dados', methods=['POST'])
def receber_dados():
    dados = request.json
    with sqlite3.connect('telemetria.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dados (hostname, sistema, cpu_percent, memoria, disco, screenshot)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (dados['hostname'], dados['sistema'], dados['cpu_percent'],
              str(dados['memoria']), str(dados['disco']), dados['screenshot']))
        conn.commit()
    return jsonify({'status': 'sucesso'})

@app.route('/')
def index():
    with sqlite3.connect('telemetria.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dados')
        registros = cursor.fetchall()
    return render_template('index.html', registros=registros)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')