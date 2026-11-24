class Alimentacao:

    @staticmethod
    def registrar_alimentacao(
        conn,
        id_rotina,
        tipo_alimentacao,
        alimento=None,
        fim_amamentacao=None,
        quantidade=None,
        ml_ou_g=None,
        mama_lados=None,
        aceitacao=None,
        notas=None
    ):
        """Registra uma alimentação na base de dados"""

        # Valida o alimento conforme o tipo de alimentação
        if tipo_alimentacao == "amamentacao":
            alimento = None

        # Verifica se o texto está vazio ou contém apenas espaços
        elif not alimento or not alimento.strip():
            raise ValueError("O alimento é obrigatório.")

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # Executa a consulta SQL
        cursor.execute("""
            INSERT INTO alimentacao (
                id_rotina,
                tipo_alimentacao,
                alimento,
                fim_amamentacao,
                quantidade,
                ml_ou_g,
                mama_lados,
                aceitacao,
                notas
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_rotina,
            tipo_alimentacao,
            alimento,
            fim_amamentacao,
            quantidade,
            ml_ou_g,
            mama_lados,
            aceitacao,
            notas
        ))

        # Retorna o ID da rotina associado à alimentação
        return id_rotina
