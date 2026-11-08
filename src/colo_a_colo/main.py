import os
import secrets
import sqlite3

from colo_a_colo.database import get_db, criar_tabelas
from colo_a_colo.domain.cuidador import Cuidador
from colo_a_colo.domain.bebe import Bebe
from werkzeug.security import check_password_hash
from flask import Flask, request, session, redirect, url_for
# session: guarda a identificação do cuidador que iniciou sessão
# redirect e url_for: permitem encaminhar o utilizador para outra página
# check_password_hash: verifica a palavra-passe sem precisarmos de guardar a palavra-passe original

app = Flask(__name__)
# Chave de sessão aleatória, gerada a cada arranque
app.secret_key = secrets.token_hex(32)

@app.route("/", methods=["GET"])
def pagina_inicial():

    mensagem = session.pop("mensagem", "")

    return f"""
<h1>Colo a Colo</h1>
{f'<p>{mensagem}</p>' if mensagem else ''}
<p style="margin-bottom: 2px;">
    Cada cuidado é um gesto de amor
</p>

<hr style="width: 220px; margin: 4px 0;">

<p style="margin-top: 2px;">
    Cuidar. Acompanhar. Organizar.
</p>

<ul>
<li><a href="/novo/cuidador">Registrar Cuidador</a></li>
<li><a href="/login">Iniciar Sessão</a></li>
<li><a href="/novo/bebe">Registrar Bebé</a></li>
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

@app.route("/novo/cuidador", methods=["GET", "POST"])
def novo_cuidador():
    
    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        data_nascimento = request.form.get("data_nascimento", "")
        password = request.form.get("password", "")

        if not nome or not email or not data_nascimento or not password:
            return "Preenche todos os campos", 400

        # A conexão com a base de dados só é aberta quando precisamos registrar o cuidador
        conn = get_db()

        try:
            Cuidador.registrar_cuidador(
                conn, nome, email, data_nascimento, password
            )

        finally:
            conn.close()

        return """
        <br><br>
        <h1>Cuidador registrado com sucesso!</h1>
        <p>O cadastro está feito!</p>
        <a href="/novo/cuidador">Registrar outro cuidador</a>
        <br><br>
        <a href="/login">Iniciar sessão</a>
        <br>
        <a href="/">Voltar à página inicial</a>
        """
    
    return """
    <h1>Registrar Cuidador</h1>

    <form method="POST" action="/novo/cuidador">

        <label for="nome">Nome:</label>
        <input type="text" id="nome" name="nome" required>
        <br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <br><br>

        <label for="data_nascimento">Data de nascimento:</label>
        <input type="date" id="data_nascimento"
               name="data_nascimento" required>
        <br><br>

        <label for="password">Palavra-passe:</label>
        <input type="password" id="password"
               name="password" required>
        <br><br>

        <button type="submit">Registrar cuidador</button>

    </form>

    <p><a href="/">Voltar à página inicial</a></p>
    """

@app.route("/login", methods=["GET", "POST"])
def iniciar_sessao():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            return "Preencha todos os campos", 400

        conn = get_db()

        try:
            id_cuidador = Cuidador.login(conn, email, password)

        finally:
            conn.close()

        if id_cuidador is None:
            return """
            <h1>Credenciais inválidas</h1>
            <p>Verifique o email e a palavra-passe.</p>
            <a href="/login">Tentar novamente</a>
            """, 401 

        # Guarda o Id do cuidador na sessão
        session["id_cuidador"] = id_cuidador

        session["mensagem"] = "Sessão iniciada com sucesso!"
        return redirect(url_for("pagina_inicial"))

    return """
    <h1>Iniciar Sessão</h1>

    <form method="POST" action="/login">

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <br><br>

        <label for="password">Palavra-passe:</label>
        <input type="password" id="password" name="password" required>
        <br><br>

        <button type="submit">Iniciar sessão</button>

    </form>

    <p><a href="/">Voltar à página inicial</a></p>
    """


@app.route("/novo/bebe", methods=["GET", "POST"])
def novo_bebe():

    if "id_cuidador" not in session:
        return redirect(url_for("iniciar_sessao"))


    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        sexo = request.form.get("sexo", "")
        data_nascimento = request.form.get("data_nascimento", "")


        if not nome or not sexo or not data_nascimento:
            return "Preenche todos os campos.", 400

        id_cuidador = session["id_cuidador"]

        conn = get_db()

        try:
            Bebe.registrar_bebe(
                conn, nome, sexo, data_nascimento, id_cuidador
            )

        finally:
            conn.close()

        return """
        <h1>Bebé registrado com sucesso!</h1>
        <p>Os dados foram guardados.</p>
        
        <a href="/novo/bebe">Registar outro bebé</a>
        <br><br>
        <a href="/">Voltar à página inicial</a>
        """

    return """
    <h1>Registrar Bebé</h1>

    <form method="POST" action="/novo/bebe">
        <label for="nome">
        Nome:</label>
        <input 
        type="text" 
        id="nome" 
        name="nome" 
        required>
        <br><br>

        <label for="sexo">Sexo:</label>
        <select id="sexo" name="sexo" required>
        <option value="">Seleciona uma opção</option>
        <option value="Masculino">Masculino</option>
        <option value="Feminino">Feminino</option>
        </select>
        <br><br>

        <label for="data_nascimento">
            Data de nascimento:</label>
        <input
            type="date"
            id="data_nascimento"
            name="data_nascimento"
            required>
        <br><br>

        <button type="submit">Guardar bebé</button>
    </form>
    <p><a href="/">Voltar à página inicial</a></p>
    """

if __name__ == "__main__":
    criar_tabelas()
    modo_debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=modo_debug)
