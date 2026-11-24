
# Importa os recursos necessários do Flask
from flask import Blueprint, request, session, redirect, url_for, render_template

# Importa math para validar números
import math

# Importa datetime e timedelta para trabalhar com datas e horários
from datetime import datetime, timedelta

# Importa a função responsável por abrir a conexão com o banco de dados
from colo_a_colo.database import get_db

# Importa a classe responsável pelas consultas relacionadas aos bebês
from colo_a_colo.domain.bebe import Bebe

# Importa a função que registra a rotina e os dados da alimentação na mesma transação
from colo_a_colo.services.serv_alimentacao import registrar_alimentacao_completa


# Cria um Blueprint para agrupar as rotas relacionadas à alimentação
alimentacao_bp = Blueprint("alimentacao", __name__)


# Define a rota para registrar uma alimentação
# GET apresenta o formulário e POST recebe os dados enviados
@alimentacao_bp.route("/novo/alimentacao", methods=["GET", "POST"])
def nova_alimentacao():

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

        # Obtém a data e a hora atuais para realizar as validações
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

            # Recebe o tipo de alimentação selecionado no formulário
            tipo_alimentacao = request.form.get("tipo_alimentacao")

            # Verifica se o tipo de alimentação corresponde a uma opção permitida
            if tipo_alimentacao not in (
                "amamentacao", "mamadeira", "solidos"
            ):
                return "<h1>Tipo de alimentação inválida</h1>", 400

            # Recebe o ID do bebê enviado pelo formulário
            id_bebe = request.form.get("id_bebe")

            # Verifica se o ID do bebê é um número inteiro
            try:
                id_bebe = int(id_bebe)

            # Impede o registro caso o ID seja inválido
            except (TypeError, ValueError):
                return "<h1>Selecione um bebê válido</h1>", 400

            # Recebe a data e a hora enviadas pelo formulário
            data_hora_texto = request.form.get("data_hora", "")

            # Converte a data e a hora recebidas para um objeto datetime
            try:
                data_hora = datetime.fromisoformat(data_hora_texto)

            # Apresenta um erro caso a data e a hora sejam inválidas
            except ValueError:
                return "<h1>Informe uma data e hora válidas</h1>", 400

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

            # Atualiza a data e a hora atuais para realizar as validações
            agora = datetime.now()

            # Calcula novamente o limite inferior dos últimos 50 anos
            try:
                limite_inferior = agora.replace(year=agora.year - 50)

            # Corrige a data caso o ano anterior não tenha 29 de fevereiro
            except ValueError:
                limite_inferior = agora.replace(
                    year=agora.year - 50,
                    day=28
                )

            # Verifica se a alimentação está dentro do período permitido
            # A data não pode ser anterior ao limite nem posterior ao momento atual
            if not limite_inferior <= data_hora <= agora:
                return (
                    "<h1>A data deve estar dentro dos últimos 50 anos e não pode ser futura</h1>",
                    400
                )

            # Inicializa os campos opcionais antes de validar cada tipo de alimentação
            alimento = None
            fim_amamentacao = None
            quantidade = None
            ml_ou_g = None
            mama_lados = None
            aceitacao = None

            # Valida os dados específicos da amamentação
            if tipo_alimentacao == "amamentacao":

                # Recebe a informação sobre qual mama foi utilizada
                mama_lados = request.form.get("mama_lados")

                # Verifica se foi selecionada uma opção válida
                if mama_lados not in (
                    "esquerda", "direita", "ambas"
                ):
                    return "<h1>Selecione a mama utilizada</h1>", 400

                # Recebe o horário de término, caso tenha sido informado
                parou_de_mamar = request.form.get("fim_amamentacao", "")

                # O término é opcional, pois a amamentação pode ainda estar em andamento
                if parou_de_mamar:

                    # Converte o horário recebido para um objeto de hora
                    try:
                        horario_fim = datetime.strptime(
                            parou_de_mamar, "%H:%M"
                        ).time()

                    # Apresenta um erro caso o horário seja inválido
                    except ValueError:
                        return "<h1>Horário de término inválido</h1>", 400

                    # Combina a data de início com o horário de término informado
                    fim_amamentacao = datetime.combine(
                        data_hora.date(),
                        horario_fim
                    )

                    # Se o término for antes do início, considera que ocorreu no dia seguinte
                    if fim_amamentacao < data_hora:
                        fim_amamentacao += timedelta(days=1)

                    # Verifica se o término aconteceu depois do início
                    if fim_amamentacao <= data_hora:
                        return (
                            "<h1>O término deve ser posterior ao início</h1>",
                            400
                        )

                    # Impede que seja informado um horário de término futuro
                    if fim_amamentacao > agora:
                        return (
                            "<h1>O término não pode ser futuro</h1>",
                            400
                        )

            # Valida os dados específicos da mamadeira
            elif tipo_alimentacao == "mamadeira":

                # Recebe o tipo de leite utilizado
                alimento = request.form.get("alimento")

                # Verifica se foi selecionado leite materno ou fórmula
                if alimento not in ("leite_materno", "formula"):
                    return "<h1>Selecione o alimento</h1>", 400

                # Converte a quantidade informada para número decimal
                try:
                    quantidade = float(
                        request.form.get("quantidade", "")
                    )

                # Apresenta um erro caso a quantidade não seja válida
                except (TypeError, ValueError):
                    return "<h1>Informe uma quantidade válida</h1>", 400

                # Verifica se a quantidade é um número finito e maior que zero
                if not math.isfinite(quantidade) or quantidade <= 0:
                    return "<h1>A quantidade deve ser maior que zero</h1>", 400

                # Define a unidade de medida utilizada na mamadeira
                ml_ou_g = "ml"

            # Valida os dados específicos dos alimentos sólidos
            elif tipo_alimentacao == "solidos":

                # Recebe o nome do alimento e remove espaços desnecessários
                alimento = request.form.get("alimento", "").strip()

                # Verifica se foi informado algum alimento
                if not alimento:
                    return "<h1>Informe o alimento</h1>", 400

                # Converte a quantidade informada para número decimal
                try:
                    quantidade = float(
                        request.form.get("quantidade", "")
                    )

                # Apresenta um erro caso a quantidade não seja válida
                except (TypeError, ValueError):
                    return "<h1>Informe uma quantidade válida</h1>", 400

                # Verifica se a quantidade é um número finito e maior que zero
                if not math.isfinite(quantidade) or quantidade <= 0:
                    return "<h1>A quantidade deve ser maior que zero</h1>", 400

                # Define a unidade de medida utilizada nos alimentos sólidos
                ml_ou_g = "g"

                # Recebe a informação sobre a aceitação da refeição
                aceitacao = request.form.get("aceitacao")

                # Verifica se foi selecionada uma opção válida
                if aceitacao not in ("tudo", "suficiente", "pouco"):
                    return "<h1>Selecione a aceitação</h1>", 400

            # Recebe as observações e remove espaços desnecessários
            notas = request.form.get("notas", "").strip() or None

            # Registra a alimentação e a rotina na mesma transação
            registrar_alimentacao_completa(
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

            # Apresenta a confirmação depois de salvar a alimentação
            return """
            <h1>Alimentação registrada com sucesso!</h1>

            <a href="/novo/alimentacao">Registrar outra alimentação</a>
            <br><br>
            <a href="/">Voltar à página inicial</a>
            """

        # Consulta os bebês pertencentes ao cuidador que iniciou a sessão
        bebes = Bebe.consultar_bebes(
            conn,
            session["id_cuidador"]
        )

        # Verifica se o cuidador já possui algum bebê cadastrado
        if not bebes:
            return """
            <h1>Registrar alimentação</h1>
            <p>Você ainda não tem bebês cadastrados.</p>
            <a href="/novo/bebe">Registrar bebê</a>
            """

        # Carrega o template alimentacao.html e apresenta o formulário no navegador
        return render_template(
            "alimentacao.html",

            # Envia a lista de bebês para preencher o campo de seleção
            bebes=bebes,

            # Envia a data mínima permitida para o formulário
            data_minima_html=data_minima_html,

            # Envia a data máxima permitida para o formulário
            data_maxima_html=data_maxima_html,

            # Envia o ID do bebê recebido pela rota de rotina
            id_bebe=id_bebe,

            # Envia a data e a hora recebidas pela rota de rotina
            data_hora=(
                data_hora.strftime("%Y-%m-%dT%H:%M")
                if isinstance(data_hora, datetime)
                else data_hora
            ),

            # Envia as notas recebidas pela rota de rotina
            notas=notas
        )

    # Garante que a conexão com o banco de dados seja fechada
    finally:
        conn.close()
