from flask import Blueprint, request, session, redirect, url_for, render_template

from colo_a_colo.database import get_db
from colo_a_colo.domain.bebe import Bebe


# Cria um Blueprint para agrupar as rotas relacionadas aos bebês
bebe_bp = Blueprint("bebe", __name__)


# Define a rota responsável pelo cadastro de um novo bebê
# GET apresenta o formulário e POST recebe os dados enviados por ele
@bebe_bp.route("/novo/bebe", methods=["GET", "POST"])
def novo_bebe():

    # Verifica se o cuidador iniciou sessão
    if "id_cuidador" not in session:
        return redirect(url_for("cuidador.iniciar_sessao"))

    # Verifica se o formulário foi enviado
    if request.method == "POST":

        # Recebe os dados enviados pelo formulário
        nome = request.form.get("nome", "").strip().title()
        genero = request.form.get("genero", "")
        data_nascimento = request.form.get("data_nascimento", "")

        # Verifica se todos os campos obrigatórios foram preenchidos
        if not nome or not genero or not data_nascimento:
            return "Preenche todos os campos.", 400

        # Obtém o ID do cuidador que iniciou sessão
        id_cuidador = session["id_cuidador"]

        # Abre a conexão com a base de dados
        conn = get_db()

        try:
            # Chama o método da classe Bebe para guardar os dados
            Bebe.registrar_bebe(
                conn, nome, genero, data_nascimento, id_cuidador
            )

        finally:
            # Fecha a conexão mesmo se ocorrer algum erro
            conn.close()

        # Apresenta a página de confirmação após o cadastro
        return render_template("bebe_sucesso.html")

    # Apresenta o formulário quando a página é acessada pelo método GET
    return render_template("bebe.html")


# Define a rota responsável pela consulta dos bebês do cuidador
@bebe_bp.route("/consultar/bebes", methods=["GET"])
def consultar_bebes():

    # Verifica se o cuidador iniciou sessão
    if "id_cuidador" not in session:
        return redirect(url_for("cuidador.iniciar_sessao"))

    # Abre a conexão com a base de dados
    conn = get_db()

    try:
        # Consulta apenas os bebês pertencentes ao cuidador autenticado
        bebes = Bebe.consultar_bebes(
            conn, session["id_cuidador"]
        )

        # Inicializa a lista que apresentará os nomes dos bebês
        lista_bebes = ""

        # Percorre os bebês encontrados na consulta
        for bebe in bebes:
            lista_bebes += f"<li>{bebe[1]}</li>"

        # Apresenta uma mensagem caso não existam bebês cadastrados
        if not bebes:
            lista_bebes = "<li>Nenhum bebê cadastrado!</li>"

        # Apresenta a lista de bebês no navegador
        return f"""
        <h1>Meus bebês</h1>
        <ul>
            {lista_bebes}
        </ul>
        <a href="/">Voltar à página inicial</a>
        """

    finally:
        # Fecha a conexão após a consulta
        conn.close()
