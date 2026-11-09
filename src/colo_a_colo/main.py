import os
import secrets
from datetime import datetime, timedelta

from colo_a_colo.database import get_db, criar_tabelas
from colo_a_colo.domain.cuidador import Cuidador
from colo_a_colo.domain.bebe import Bebe
from colo_a_colo.domain.rotina import Rotina
from colo_a_colo.domain.alimentacao import Alimentacao
from werkzeug.security import check_password_hash
from flask import Flask, request, session, redirect, url_for
# session: guarda a identificação do cuidador que iniciou sessão
# redirect e url_for: permitem encaminhar o utilizador para outra página
# check_password_hash: verifica a palavra-passe sem precisarmos de guardar a palavra-passe original

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
<li><a href="/login">Iniciar Sessão</a></li>
<br>
<li><a href="/novo/cuidador">Registrar Cuidador</a></li>
<li><a href="/novo/bebe">Registrar Bebê</a></li>
<br>
<li><a href="/consultar/bebes">Consultar Bebês</a></li>
<br>
<li><a href="/novo/alimentacao">Novo Alimentação</a></li>
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

                fim_texto = request.form.get("fim_amamentacao")

                if fim_texto:

                    try:
                        fim_amamentacao = datetime.fromisoformat(
                            fim_texto
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

        opcoes_bebes = ""

        for bebe in bebes:
            opcoes_bebes += (
                f'<option value="{bebe[0]}">{bebe[1]}</option>'
            )

        return f"""
        <h1>Registrar Alimentação</h1>

        <form method="POST" action="/novo/alimentacao">

            <label for="id_bebe">Bebê:</label>
            <br>
            <select id="id_bebe" name="id_bebe" required>
                <option value="">Selecione o bebê</option>
                {opcoes_bebes}
            </select>

            <br><br>

            <label for="tipo_alimentacao">Tipo de Alimentação:</label>
            <br>
            <select id="tipo_alimentacao" name="tipo_alimentacao" required>
                <option value="">Selecione uma opção</option>
                <option value="amamentacao">Amamentação</option>
                <option value="mamadeira">Mamadeira</option>
                <option value="solidos">Sólidos</option>
            </select>

            <br><br>

            <label for="data_hora">Data e hora:</label>

            <br>

            <input
                type="datetime-local"
                id="data_hora"
                name="data_hora"
                min="{data_minima_html}"
                max="{data_maxima_html}"
                required
            >

            <br><br>

            <fieldset id="campos_amamentacao" hidden>
                <legend>Detalhes da Amamentação</legend>

                <label for="mama_lados">Mama utilizada:</label>
                <br>
                <select id="mama_lados" name="mama_lados">
                    <option value="">Selecione uma opção</option>
                    <option value="esquerda">Esquerda</option>
                    <option value="direita">Direita</option>
                    <option value="ambas">Ambas</option>
                </select>

                <br><br>

                <label for="fim_amamentacao">Horário de término:</label>

                <br>

                <input
                    type="datetime-local"
                    id="fim_amamentacao"
                    name="fim_amamentacao"
                >

            </fieldset>

            <br>

            <fieldset id="campos_mamadeira" hidden>
                <legend>Detalhes da mamadeira</legend>

                <label for="alimento_mamadeira">Alimento:</label>

                <br>

                <select id="alimento_mamadeira" name="alimento">
                    <option value="">Selecione uma opção</option>
                    <option value="leite_materno">Leite materno</option>
                    <option value="formula">Fórmula</option>
                </select>

                <br>

                <label for="quantidade_mamadeira">Quantidade:</label>
                <br>
                <input
                    type="number"
                    id="quantidade_mamadeira"
                    name="quantidade"
                    min="10"
                    step="1"
                >

                <input type="hidden" name="ml_ou_g" value="ml">

                <span>ml</span>

            </fieldset>            
            
            <fieldset id="campos_solidos" hidden>
                <legend>Detalhes dos alimentos sólidos</legend>

                <label for="alimento_solido">Alimento:</label>
                <br>
                <input
                    type="text"
                    id="alimento_solido"
                    name="alimento"
                    placeholder="Ex.: Papa de legumes"
                >

                <br><br>

                <label for="quantidade_solidos">Quantidade:</label>
                <br>
                <input
                    type="number"
                    id="quantidade_solidos"
                    name="quantidade"
                    min="10"
                    step="1"
                >

                <input type="hidden" name="ml_ou_g" value="g">

                <span>g</span>

                <br><br>

                <label for="aceitacao">Aceitação:</label>
                <br>
                <select id="aceitacao" name="aceitacao">
                    <option value="">Selecione uma opção</option>
                    <option value="tudo">Tudo</option>
                    <option value="suficiente">Suficiente</option>
                    <option value="pouco">Pouco</option>
                </select>

            </fieldset>

                <br>
                
                <label for="notas">Observações:</label>
                <br>
                <textarea
                    id="notas"
                    name="notas"
                    rows="3"
                    placeholder="Adicione alguma observação..."
                ></textarea>

                <br><br>

            <button type="submit">Salvar</button>

        </form>

        <script>
            const tipoAlimentacao = document.getElementById("tipo_alimentacao");

            const camposAmamentacao = document.getElementById("campos_amamentacao");
            const camposMamadeira = document.getElementById("campos_mamadeira");
            const camposSolidos = document.getElementById("campos_solidos");

            function atualizarCampos() {{

                camposAmamentacao.hidden = true;
                camposMamadeira.hidden = true;
                camposSolidos.hidden = true;

                const grupos = [
                    camposAmamentacao,
                    camposMamadeira,
                    camposSolidos
                ];

                grupos.forEach(grupo => {{
                    grupo.querySelectorAll("input, select").forEach(campo => {{
                        campo.disabled = true;
                        campo.required = false;
                    }});
                }});

                let grupoAtivo;

                if (tipoAlimentacao.value === "amamentacao") {{
                    grupoAtivo = camposAmamentacao;
                }} else if (tipoAlimentacao.value === "mamadeira") {{
                    grupoAtivo = camposMamadeira;
                }} else if (tipoAlimentacao.value === "solidos") {{
                    grupoAtivo = camposSolidos;
                }}

                if (grupoAtivo) {{
                grupoAtivo.hidden = false;

                grupoAtivo.querySelectorAll("input, select").forEach(campo => {{
                    campo.disabled = false;
                }});

                if (grupoAtivo === camposAmamentacao) {{
                    document.getElementById("mama_lados").required = true;
                }}

                else if (grupoAtivo === camposMamadeira) {{
                    document.getElementById("alimento_mamadeira").required = true;
                    document.getElementById("quantidade_mamadeira").required = true;
                }}

                else if (grupoAtivo === camposSolidos) {{
                    document.getElementById("alimento_solido").required = true;
                    document.getElementById("quantidade_solidos").required = true;
                    document.getElementById("aceitacao").required = true;
                }}
            }}
        }}

        tipoAlimentacao.addEventListener("change", atualizarCampos);

        atualizarCampos();

        </script>
        """

    finally:
        conn.close()


if __name__ == "__main__":
    criar_tabelas()
    modo_debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=modo_debug)
