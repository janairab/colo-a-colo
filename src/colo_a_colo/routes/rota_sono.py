# Importa os recursos necessários do Flask
from flask import Blueprint, request, session, redirect, url_for, render_template

# Importa datetime para trabalhar com datas e horários
from datetime import datetime

# Importa a função responsável por abrir a conexão com o banco de dados
from colo_a_colo.database import get_db

# Importa a classe responsável pelas consultas relacionadas aos bebês
from colo_a_colo.domain.bebe import Bebe

# Importa a função que registra a rotina e os dados do sono na mesma transação
from colo_a_colo.services.serv_sono import registrar_sono_completo

# Cria um Blueprint para agrupar as rotas relacionadas ao sono
sono_bp = Blueprint("sono", __name__)


# Define a rota para registrar um sono
# GET apresenta o formulário e POST recebe os dados enviados
@sono_bp.route("/novo/sono", methods=["GET", "POST"])
def novo_sono():

    # Verifica se existe um cuidador com sessão iniciada
    if "id_cuidador" not in session:
        return redirect(url_for("cuidador.iniciar_sessao"))

    # Recebe os dados enviados pela rota de rotina
    id_bebe = request.args.get("id_bebe")
    data_hora = request.args.get("data_hora")
    notas = request.args.get("notas", "")
    
    # Abre a conexão com o banco de dados
    conn = get_db()

    try:

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

            # Apresenta um erro caso o ID não seja válido
            except (ValueError, TypeError):
                return "<h1>Bebê inválido</h1>", 400

            # Verifica se o bebê pertence ao cuidador que iniciou a sessão
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id_bebe
                FROM bebe
                WHERE id_bebe = ? AND id_cuidador = ?
            """, (id_bebe, session["id_cuidador"]))

            # Recebe o resultado da consulta
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

            # Atualiza a data e a hora atuais para realizar as validações
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

            # Recebe a data e a hora de término do sono, caso tenham sido informadas
            fim_sono_formulario = request.form.get("fim_sono")

            # Inicializa o término como None, pois ele é opcional
            fim_sono = None

            # Converte o término para datetime somente se o campo foi preenchido
            if fim_sono_formulario:
                try:
                    fim_sono = datetime.fromisoformat(fim_sono_formulario)

                # Apresenta um erro caso a data ou a hora sejam inválidas
                except (ValueError, TypeError):
                    return "<h1>Data e hora de término inválidas</h1>", 400

                # Verifica se o término não é anterior ao início
                if fim_sono < data_hora:
                    return "<h1>O término do sono não pode ser anterior ao início</h1>", 400

                # Verifica se o término não está no futuro
                if fim_sono > agora:
                    return "<h1>O término do sono não pode ser futuro</h1>", 400

            # Recebe as observações e remove espaços desnecessários
            notas = request.form.get("notas", "").strip() or None

            # Registra o sono e a rotina na mesma transação
            registrar_sono_completo(
                conn,
                id_bebe,
                data_hora,
                fim_sono,
                notas
            )
            
            # Apresenta a confirmação depois de salvar o sono
            return """
            <h1>Sono registrado com sucesso!</h1>

            <a href="/novo/sono">Registrar outro sono</a>
            <br><br>
            <a href="/">Voltar à página inicial</a>
            """

        # Consulta os bebês pertencentes ao cuidador que iniciou a sessão
        bebes = Bebe.consultar_bebes(conn, session["id_cuidador"])

        # Verifica se o cuidador já possui algum bebê cadastrado
        if not bebes:
            return """
            <h1>Registrar sono</h1>
            <p>Você ainda não tem bebês cadastrados</p>
            <a href="/novo/bebe">Registrar bebê</a>
            """

        # Carrega o template sono.html e apresenta o formulário no navegador
        return render_template(
            # Indica o nome do arquivo HTML que será apresentado            
            "sono.html",
            
            # Envia a lista de bebês para preencher o campo de seleção
            bebes=bebes,

            # Envia a data mínima permitida para o formulário
            data_minima_html=data_minima_html,

            # Envia a data máxima permitida para o formulário
            data_maxima_html=data_maxima_html,

            # Envia o ID do bebê recebido pela rota de rotina
            id_bebe=id_bebe,

            # Envia a data e a hora recebidas pela rota de rotina
            data_hora=data_hora,

            # Envia as notas recebidas pela rota de rotina
            notas=notas
            )

    # Garante que a conexão com o banco de dados seja fechada
    finally:
        conn.close()
