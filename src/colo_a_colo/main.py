import os
import secrets
import sqlite3

from flask import Flask, request, jsonify
from database import get_db, criar_tabelas
from domain.cuidador import registar_cuidador


app = Flask(__name__)
# Chave de sessão aleatória, gerada a cada arranque
app.secret_key = secrets.token_hex(32)

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
<li><a href="/tabelas">Consultar Tabelas</a></li>
<li><a href="/cuidador/novo">Registar Cuidador</a></li>
<li><a href="#">Consultar Rotinas</a></li>
</ul>
"""


@app.route("/tabelas", methods=["GET"])
def consultar_tabelas():
    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """)

        # obtém todas as linhas devolvidas pela consulta
        tabelas = cursor.fetchall()
        conn.close()

        lista_tabelas = ""

        for tabela in tabelas:
            lista_tabelas += f"<li>{tabela[0]}</li>"

        # <br> Linha em branco para dar distancia do parágrafo
        # Ou 
        # <p style="margin-top: 40px;"> 
        # <a href="/">Voltar à página inicial</a> </p>
        return f"""
        <p style="margin-top: 40px;"></p>
        <h1>Tabelas da Base de Dados</h1>
        <ul>
        {lista_tabelas}
        </ul>
        <p style="margin-top: 40px;"> 
        <a href="/">Voltar à página inicial</a> </p>"""

    # fecha a ligação à base de dados.
    finally:
        conn.close()

@app.route("/cuidador/novo", methods=["GET", "POST"])
def novo_cuidador():
    
    conn = get_db()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        data_nascimento = request.form.get("data_nascimento", "")

        if not nome or not email or not data_nascimento:
            return "Preenche todos os campos.", 400

        try:
            registar_cuidador(
                conn, nome, email, data_nascimento
            )

        finally:
            conn.close()

        return """
        <h1>Cuidador registrado com sucesso!</h1>
        <p>Os dados foram guardados.</p>
        
        <a href="/cuidador/novo">Registar outro cuidador</a>
        <br>
        <a href="/">Voltar à página inicial</a>
        """

    return """
    <h1>Registar Cuidador</h1>

    <form method="POST" action="/cuidador/novo">
        <label for="nome">
        Nome:</label>
        <input 
        type="text" 
        id="nome" 
        name="nome" 
        required>
        <br><br>

        <label for="email">
        Email:</label>
        <input 
        type="email" 
        id="email" 
        name="email" 
        required>
        <br><br>

        <label for="data_nascimento">
            Data de nascimento:</label>
        <input
            type="date"
            id="data_nascimento"
            name="data_nascimento"
            required>
        <br><br>

        <button type="submit">Guardar cuidador</button>
    </form>
    <p><a href="/">Voltar à página inicial</a></p>
    """


if __name__ == "__main__":
    criar_tabelas()
    modo_debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=modo_debug)
