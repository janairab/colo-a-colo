import os
import secrets
from flask import Flask, render_template, session

from colo_a_colo.database import criar_tabelas

# Importa o Blueprint que reúne as rotas relacionadas ao cuidador
from colo_a_colo.routes.rota_cuidador import cuidador_bp

# Importa o Blueprint que reúne as rotas relacionadas aos bebês
from colo_a_colo.routes.rota_bebe import bebe_bp

# Importa o Blueprint que reúne as rotas relacionadas à alimentação
from colo_a_colo.routes.rota_alimentacao import alimentacao_bp

# Importa o Blueprint que reúne as rotas relacionadas à banho
from colo_a_colo.routes.rota_banho import banho_bp

# Importa o Blueprint que reúne as rotas relacionadas à fralda
from colo_a_colo.routes.rota_fralda import fralda_bp

# Importa o Blueprint que reúne as rotas relacionadas à sono
from colo_a_colo.routes.rota_sono import sono_bp

# Importa o Blueprint que reúne as rotas relacionadas à rotina
from colo_a_colo.routes.rota_rotina import rotina_bp

app = Flask(__name__)

# Registra na aplicação as rotas definidas no módulo de cuidador
app.register_blueprint(cuidador_bp)

# Registra na aplicação as rotas definidas no módulo de bebês
app.register_blueprint(bebe_bp)

# Registra na aplicação as rotas definidas no módulo da alimentação
app.register_blueprint(alimentacao_bp)

# Registra na aplicação as rotas definidas no módulo do banho
app.register_blueprint(banho_bp)

# Registra na aplicação as rotas definidas no módulo da fralda
app.register_blueprint(fralda_bp)

# Registra na aplicação as rotas definidas no módulo do sono
app.register_blueprint(sono_bp)

# Registra na aplicação as rotas definidas no módulo da rotina
app.register_blueprint(rotina_bp)

# Chave de sessão aleatória, gerada a cada arranque
app.secret_key = secrets.token_hex(32)


@app.route("/", methods=["GET"])
def pagina_inicial():

    mensagem = session.pop("mensagem", "")

    return render_template(
        "pagina_inicial.html",
        mensagem=mensagem
    )


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
