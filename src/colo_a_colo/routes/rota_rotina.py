
from flask import Blueprint, request, session, redirect, url_for, render_template

# Importa datetime para trabalhar com datas e horários
from datetime import datetime

# Importa a função responsável por abrir a conexão com o banco de dados
from colo_a_colo.database import get_db

# Cria um Blueprint para agrupar as rotas relacionadas à rotina
rotina_bp = Blueprint("rotina", __name__)


# Define a rota responsável pelo cadastro de uma nova rotina
# GET apresenta o formulário e POST recebe os dados enviados por ele
@rotina_bp.route("/adicionar/rotina", methods=["GET", "POST"])
def nova_rotina():

    # Verifica se o cuidador iniciou sessão
    if "id_cuidador" not in session:
        return redirect(url_for("cuidador.iniciar_sessao"))

    # Abre a conexão com a base de dados
    conn = get_db()

    try:
        # Cria um cursor para executar consultas SQL
        cursor = conn.cursor()

        # Consulta os bebês pertencentes ao cuidador autenticado
        cursor.execute("""
            SELECT id_bebe, nome
            FROM bebe
            WHERE id_cuidador = ?
            ORDER BY nome
        """, (session["id_cuidador"],))

        # Armazena a lista de bebês encontrados
        bebes = cursor.fetchall()

        # Obtém a data e a hora atuais
        agora = datetime.now()

        # Calcula a data mínima permitida, considerando os últimos 50 anos
        try:
            data_minima = agora.replace(year=agora.year - 50)

        # Corrige a data caso o ano anterior não tenha 29 de fevereiro
        except ValueError:
            data_minima = agora.replace(
                year=agora.year - 50,
                day=28
            )

        # Converte as datas para o formato aceito pelo campo datetime-local do HTML
        data_minima_html = data_minima.strftime("%Y-%m-%dT%H:%M")
        data_maxima_html = agora.strftime("%Y-%m-%dT%H:%M")

        # Verifica se o formulário foi enviado
        if request.method == "POST":

            # Recebe o ID do bebê e valida se é um número inteiro
            try:
                id_bebe = int(request.form.get("id_bebe", ""))

            # Impede o avanço caso o ID não seja válido
            except (ValueError, TypeError):
                return "<h1>Bebê inválido</h1>", 400

            # Verifica se o bebê pertence ao cuidador que iniciou a sessão
            cursor.execute("""
                SELECT id_bebe
                FROM bebe
                WHERE id_bebe = ? AND id_cuidador = ?
            """, (id_bebe, session["id_cuidador"]))

            bebe = cursor.fetchone()

            # Impede o registro caso o bebê não pertença ao cuidador
            if not bebe:
                return "<h1>Bebê inválido</h1>", 400

            # Recebe e converte a data e a hora informadas no formulário
            try:
                data_hora = datetime.fromisoformat(
                    request.form.get("data_hora", "")
                )

            # Apresenta um erro caso a data ou a hora sejam inválidas
            except (ValueError, TypeError):
                return "<h1>Data e hora inválidas</h1>", 400

            # Obtém novamente a data e a hora atuais para realizar as validações
            agora = datetime.now()

            # Calcula o limite inferior dos últimos 50 anos
            try:
                limite_inferior = agora.replace(year=agora.year - 50)

            # Corrige a data caso o ano anterior não tenha 29 de fevereiro
            except ValueError:
                limite_inferior = agora.replace(
                    year=agora.year - 50,
                    day=28
                )

            # Verifica se a data está dentro do período permitido
            # A data não pode ser anterior ao limite nem posterior ao momento atual
            if not limite_inferior <= data_hora <= agora:
                return (
                    "<h1>A data deve estar dentro dos últimos 50 anos e não pode ser futura</h1>",
                    400
                )

            # Recebe o tipo de registro escolhido pelo cuidador
            tipo_registro = request.form.get("tipo_registro", "").strip()

            # Recebe as observações e remove espaços desnecessários
            notas = request.form.get("notas", "").strip() or None

            # Define os destinos permitidos para cada tipo de registro
            destinos = {
                "alimentacao": "alimentacao.nova_alimentacao",
                "sono": "sono.novo_sono",
                "banho": "banho.novo_banho",
                "fralda": "fralda.nova_fralda"
            }

            # Verifica se o tipo de registro informado é permitido
            if tipo_registro not in destinos:
                return "<h1>Tipo de registro inválido</h1>", 400

            # Encaminha o cuidador para o formulário específico do registro escolhido
            # Os dados iniciais são enviados como parâmetros da URL
            return redirect(url_for(
                destinos[tipo_registro],
                id_bebe=id_bebe,
                data_hora=data_hora.isoformat(timespec="minutes"),
                notas=notas or ""
            ))

        # Apresenta o formulário de criação de rotina
        return render_template(
            "rotina.html",
            bebes=bebes,
            data_minima_html=data_minima_html,
            data_maxima_html=data_maxima_html
        )

    finally:
        # Fecha a conexão com a base de dados
        conn.close()
