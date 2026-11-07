class Alimentacao:

    @staticmethod
    def registrar_alimentacao(
            conn,
            id_registro,
            tipo_alimentacao,
            alimento=None,
            fim_amamentacao=None,
            quantidade=None,
            ml_ou_g=None,
            mama_lados=None,
            aceitacao=None,
            notas=None):
        """Registra uma alimentação na base de dados"""

        # Valida o alimento conforme o tipo de alimentação
        # verifica se o valor está vazio ou é None.
        if tipo_alimentacao == "amamentacao":
            alimento = None

        # verifica se o texto está vazio ou contém apenas espaços.
        elif not alimento or not alimento.strip():
            raise ValueError("O alimento é obrigatório.")

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # executa a consulta SQL
        cursor.execute("""
            INSERT INTO alimentacao (
            id_registro, 
            tipo_alimentacao, 
            alimento, 
            fim_amamentacao, 
            quantidade, 
            ml_ou_g, 
            mama_lados, 
            aceitacao, 
            notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_registro, tipo_alimentacao, alimento, fim_amamentacao, quantidade, ml_ou_g, mama_lados, aceitacao, notas))

        # Retorna o ID do registro associado
        return id_registro
