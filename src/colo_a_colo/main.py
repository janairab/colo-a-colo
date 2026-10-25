
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

# Verficiar se a DB foi criada   
if os.path.exists(DB_PATH):
    print("A base de dados existe!")
else:
    print("A base de dados não existe!")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    # ativar a verificação das chaves estrangeiras
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@app.route("/", methods=["GET"])

def pagina_inicial():
    return """
    <h1>Colo a Colo</h1>
    
    <p>Cada cuidado é um gesto de amor.</p>
    <p>Cuidar. Acompanhar. Organizar.</p>

    <h2>Rotina do Bebé</h2>

    <ul>
        <li><a href="/tabelas">Consultar tabelas</a></li>
        <li><a href="/rotinas">Consultar rotinas</a></li>
    </ul>
    """
