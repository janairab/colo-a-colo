
from flask import Blueprint, request, session, redirect, url_for, render_template

from colo_a_colo.database import get_db
from colo_a_colo.domain.cuidador import Cuidador

# Blueprint é um recurso que permite organizar uma aplicação em partes menores, separando as funcionalidades por responsabilidade e em ficheiros diferentes

# Cria um Blueprint para agrupar as rotas relacionadas ao cuidador
# O nome "cuidador" identifica esse grupo de rotas dentro da aplicação
cuidador_bp = Blueprint("cuidador", __name__)


# Define a rota responsável pelo cadastro de um novo cuidador
# GET apresenta o formulário e POST recebe os dados enviados por ele
@cuidador_bp.route("/novo/cuidador", methods=["GET", "POST"])
def novo_cuidador():

    # Verifica se o formulário foi enviado
    if request.method == "POST":

        # Recebe os dados enviados pelo formulário
        # strip() remove espaços em branco no início e no final dos textos
        nome = request.form.get("nome", "").strip().title()
        email = request.form.get("email", "").strip()
        data_nascimento = request.form.get("data_nascimento", "")
        password = request.form.get("password", "")

        # Verifica se todos os campos obrigatórios foram preenchidos
        if not nome or not email or not data_nascimento or not password:
            return "Preencha todos os campos", 400

        # Abre a conexão com a base de dados
        conn = get_db()

        try:
            # Chama o método da classe Cuidador para guardar os dados
            Cuidador.registrar_cuidador(
                conn, nome, email, data_nascimento, password
            )

        finally:
            # Fecha a conexão mesmo se ocorrer algum erro durante o cadastro
            conn.close()

        # Apresenta a página de confirmação após o cadastro
        return render_template("cuidador_sucesso.html")

    # Apresenta o formulário quando a página é acessada pelo método GET
    return render_template("cuidador.html")


# Define a rota responsável pela autenticação do cuidador
# GET apresenta o formulário e POST recebe os dados para iniciar a sessão
@cuidador_bp.route("/login", methods=["GET", "POST"])
def iniciar_sessao():

    # Verifica se o formulário de login foi enviado
    if request.method == "POST":

        # Recebe o email e a palavra-passe informados pelo cuidador
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Verifica se os dois campos foram preenchidos
        if not email or not password:
            return "Preencha todos os campos", 400

        # Abre a conexão com a base de dados
        conn = get_db()

        try:
            # Verifica os dados de acesso e recebe o ID do cuidador
            # O método retorna None quando os dados de acesso são inválidos
            id_cuidador = Cuidador.login(conn, email, password)

        finally:
            # Fecha a conexão após consultar os dados
            conn.close()

        # Verifica se o cuidador foi encontrado e autenticado
        if id_cuidador is None:

            # Apresenta novamente o formulário com uma mensagem de erro
            return render_template(
                "login.html",
                erro="Email ou palavra-passe inválidos."
            ), 401

        # Guarda o ID do cuidador na sessão para identificar quem está conectado
        session["id_cuidador"] = id_cuidador

        # Guarda uma mensagem para ser apresentada na página inicial
        session["mensagem"] = "Sessão iniciada com sucesso!"

        # Redireciona o cuidador para a página inicial após o login
        return redirect(url_for("pagina_inicial"))

    # Apresenta o formulário quando a página é acessada pelo método GET
    return render_template("login.html")
