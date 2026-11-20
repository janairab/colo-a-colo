import os
import secrets
from datetime import datetime, timedelta

from colo_a_colo.database import get_db, criar_tabelas
from colo_a_colo.domain.cuidador import Cuidador
from colo_a_colo.domain.bebe import Bebe
from colo_a_colo.domain.rotina import Rotina
from colo_a_colo.domain.alimentacao import Alimentacao
from colo_a_colo.domain.banho import Banho
from werkzeug.security import check_password_hash
from flask import Flask, request, session, redirect, url_for, render_template
# session: guarda a identificação do cuidador que iniciou sessão
# redirect e url_for: permitem encaminhar o utilizador para outra página
# check_password_hash: verifica a palavra-passe sem precisarmos de guardar a palavra-passe original
# carregar um arquivo HTML da pasta templates e apresentá-lo ao usuário pelo navegador, ela permite separar o HTML do código Python.

app = Flask(__name__)
# Chave de sessão aleatória, gerada a cada arranque
app.secret_key = secrets.token_hex(32)


def registrar_alimentacao_completa(
        conn,
        id_bebe,
        data_hora,
        tipo_alimentacao,
        alimento=None,
        fim_amamentacao=None,
        quantidade=None,
        ml_ou_g=None,
        mama_lados=None,
        aceitacao=None,
        notas=None
):
    with conn:

        id_registro = Rotina.registrar_rotina(
            conn,
            id_bebe,
            "alimentacao",
            data_hora,
            notas
        )

        Alimentacao.registrar_alimentacao(
            conn,
            id_registro,
            tipo_alimentacao,
            alimento,
            fim_amamentacao,
            quantidade,
            ml_ou_g,
            mama_lados,
            aceitacao,
            notas
        )

    return id_registro


@app.route("/", methods=["GET"])
def pagina_inicial():

    mensagem = session.pop("mensagem", "")

    return render_template(
        "pagina_inicial.html",
        mensagem=mensagem
    )


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

        return render_template("cuidador_sucesso.html")

    return render_template("cuidador.html")


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
            return render_template(
                "login.html",
                erro="Email ou palavra-passe inválidos."
            ), 401

        # Guarda o Id do cuidador na sessão
        session["id_cuidador"] = id_cuidador

        session["mensagem"] = "Sessão iniciada com sucesso!"
        return redirect(url_for("pagina_inicial"))

    return render_template("login.html")


@app.route("/novo/bebe", methods=["GET", "POST"])
def novo_bebe():

    if "id_cuidador" not in session:
        return redirect(url_for("iniciar_sessao"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        genero = request.form.get("genero", "")
        data_nascimento = request.form.get("data_nascimento", "")

        if not nome or not genero or not data_nascimento:
            return "Preenche todos os campos.", 400

        id_cuidador = session["id_cuidador"]

        conn = get_db()

        try:
            Bebe.registrar_bebe(
                conn, nome, genero, data_nascimento, id_cuidador
            )

        finally:
            conn.close()

        return render_template("bebe_sucesso.html")

    return render_template("bebe.html")


@app.route("/consultar/bebes", methods=["GET"])
def consultar_bebes():

    if "id_cuidador" not in session:
        return redirect(url_for("iniciar_sessao"))

    conn = get_db()

    try:
        bebes = Bebe.consultar_bebes(
            conn, session["id_cuidador"]
        )

        lista_bebes = ""

        for bebe in bebes:
            lista_bebes += f"<li>{bebe[1]}</li>"

        if not bebes:
            lista_bebes = "<li>Nenhum bebê cadastrado!</li>"

        return f"""
        <h1>Meus bebês</h1>
        <ul>
            {lista_bebes}
        </ul>
        <a href="/">Voltar à página inicial</a>
        """

    finally:
        conn.close()

@app.route("/novo/alimentacao", methods=["GET", "POST"])
def novo_alimentacao():

    if "id_cuidador" not in session:
        return redirect(url_for("iniciar_sessao"))

    conn = get_db()

    try:

        agora = datetime.now()

        try:
            data_minima = agora.replace(year=agora.year - 50)
        except ValueError:
            data_minima = agora.replace(
                year=agora.year - 50,
                day=28
            )

        data_minima_html = data_minima.strftime("%Y-%m-%dT%H:%M")
        data_maxima_html = agora.strftime("%Y-%m-%dT%H:%M")

        if request.method == "POST":

            # Recebe os dados do formulário
            id_bebe = request.form.get("id_bebe")
            tipo_alimentacao = request.form.get("tipo_alimentacao")

            # Valida o ID do bebê
            try:
                id_bebe = int(id_bebe)

            except (ValueError, TypeError):
                return "<h1>Bebê inválido</h1>", 400

            # Valida o tipo de alimentação
            if tipo_alimentacao not in (
                "amamentacao", "mamadeira", "solidos"
            ):
                return "<h1>Tipo de alimentação inválida</h1>", 400

            # Verifica se o bebê pertence ao cuidador autenticado
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_bebe
                FROM bebe
                WHERE id_bebe = ? AND id_cuidador = ?
            """, (id_bebe, session["id_cuidador"]))

            # Recebe os dados da consulta
            bebe = cursor.fetchone()

            if not bebe:
                return "<h1>Bebê inválido</h1>", 400

            # Recebe e valida a data e hora
            try:
                data_hora = datetime.fromisoformat(
                    request.form.get("data_hora", "")
                )

            except ValueError:
                return "<h1>Data e hora inválidas</h1>", 400

            agora = datetime.now()

            try:
                limite_inferior = agora.replace(year=agora.year - 50)

            except ValueError:
                limite_inferior = agora.replace(
                    year=agora.year - 50,
                    day=28
                )

            if not limite_inferior <= data_hora <= agora:
                return "<h1>A data deve estar dentro dos últimos 50 anos e não pode ser futura.</h1>", 400

            # Inicializa os campos opcionais
            alimento = None
            fim_amamentacao = None
            quantidade = None
            ml_ou_g = None
            mama_lados = None
            aceitacao = None

            # Valida os dados da amamentação
            if tipo_alimentacao == "amamentacao":

                mama_lados = request.form.get("mama_lados")

                if mama_lados not in (
                    "esquerda", "direita", "ambas"
                ):
                    return "<h1>Selecione a mama utilizada.</h1>", 400

                parou_de_mamar = request.form.get("fim_amamentacao")

                if parou_de_mamar:

                    try:
                        fim_amamentacao = datetime.fromisoformat(
                            parou_de_mamar
                        )

                    except ValueError:
                        return "<h1>Horário de término inválido.</h1>", 400

                    if fim_amamentacao <= data_hora:
                        return (
                            "<h1>O término deve ser posterior ao início</h1>",
                            400
                        )

                    if fim_amamentacao > agora:
                        return (
                            "<h1>O término não pode ser futuro</h1>",
                            400
                        )

            # Valida os dados da mamadeira
            elif tipo_alimentacao == "mamadeira":

                alimento = request.form.get("alimento")

                if alimento not in ("leite_materno", "formula"):
                    return "<h1>Selecione o alimento</h1>", 400

                try:
                    quantidade = float(
                        request.form.get("quantidade", "")
                    )

                except ValueError:
                    return "<h1>Informe uma quantidade válida</h1>", 400

                if quantidade <= 0:
                    return "<h1>A quantidade deve ser maior que zero</h1>", 400

                ml_ou_g = "ml"

            # Valida os dados dos alimentos sólidos
            elif tipo_alimentacao == "solidos":

                alimento = request.form.get("alimento", "").strip()

                if not alimento:
                    return "<h1>Informe o alimento</h1>", 400

                try:
                    quantidade = float(
                        request.form.get("quantidade", "")
                    )

                except ValueError:
                    return "<h1>Informe uma quantidade válida</h1>", 400

                if quantidade <= 0:
                    return "<h1>A quantidade deve ser maior que zero</h1>", 400

                ml_ou_g = "g"

                aceitacao = request.form.get("aceitacao")

                if aceitacao not in ("tudo", "suficiente", "pouco"):
                    return "<h1>Selecione a aceitação</h1>", 400

            # Recebe as notas, caso existam
            notas = request.form.get("notas") or None

            # Registra a alimentação e a rotina na mesma transação
            id_registro = registrar_alimentacao_completa(
                conn,
                id_bebe,
                data_hora,
                tipo_alimentacao,
                alimento,
                fim_amamentacao,
                quantidade,
                ml_ou_g,
                mama_lados,
                aceitacao,
                notas
            )

            return f"""
            <h1>Alimentação registrada com sucesso!</h1>
            <p>Registro número: {id_registro}</p>
            <br>
            <a href="/novo/alimentacao">Registrar outra alimentação</a>
            <br><br>
            <a href="/">Voltar à página inicial</a>
            """

        bebes = Bebe.consultar_bebes(conn, session["id_cuidador"])

        if not bebes:
            return """
            <h1>Registrar alimentação</h1>
            <p>Você ainda não tem bebês cadastrados.</p>
            <a href="/novo/bebe">Registrar bebê</a>
            """

        # Carrega o template alimentacao.html e apresenta
        # o formulário de registro de alimentação no navegador
        return render_template(

            # Nome do arquivo HTML que será apresentado
            "alimentacao.html",

            # Envia a lista de bebês cadastrados pelo cuidador
            # para preencher a lista de seleção no formulário
            bebes=bebes,

            # Envia a data mínima permitida para o campo de data e hora
            data_minima_html=data_minima_html,

            # Envia a data máxima permitida para o campo de data e hora
            data_maxima_html=data_maxima_html
        )


    finally:
        conn.close()


if __name__ == "__main__":

    # Cria as tabelas necessárias no banco de dados
    criar_tabelas()

    # Verifica se o modo de depuração está ativado
    # através da variável de ambiente FLASK_DEBUG
    modo_debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    # Inicia o servidor Flask
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=modo_debug
    )

