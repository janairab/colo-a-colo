import os
import secrets 
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)   # chave de sessão aleatória, gerada a cada arranque 

# Caminho da pasta principal do projeto
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# Caminho da base de dados
DB_PATH = os.path.join(BASE_DIR, "data", "colo_a_colo.db")

# Abre ligação da base de dados
def get_db():
    conn = sqlite3.connect(DB_PATH)
    # ativar a verificação das chaves estrangeiras
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    conn = get_db()

    caminho_sql = os.path.join(
        BASE_DIR, "docs", "criar_tabelas.sql"
    )
    # Abre o ficheiro da base de dados com os comandos sql
    with open(caminho_sql, "r", encoding="utf-8") as ficheiro:
        sql = ficheiro.read()

    # Executa os comandos sql
    conn.executescript(sql)   

    # Fecha ligação da base de dados
    conn.close() 

    print("Tabelas criadas com sucesso!")


@app.route("/", methods=["GET"])

def pagina_inicial():
    return """
<h1>Colo a Colo</h1>

<p style="margin-bottom: 2px;">
    Cada cuidado é um gesto de amor
</p>

<hr style="width: 220px; margin: 4px 0;">

<p style="margin-top: 2px;">
    Cuidar. Acompanhar. Organizar.
</p>

<ul>
<li><a href="/tabelas">Consultar tabelas</a></li>
    <li><a href="#">Consultar rotinas</a></li>
</ul>
"""

@app.route("/tabelas", methods=["GET"])
def consultar_tabelas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tabelas = cursor.fetchall()
    conn.close()

    return jsonify(tabelas)


if __name__ == "__main__": 
    criar_tabelas()
    modo_debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true" 
    app.run(debug=modo_debug)
