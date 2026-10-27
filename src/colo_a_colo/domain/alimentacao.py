def registrar_alimentacao(
        conn, 
        id_registro, 
        tipo_alimentacao, 
        alimento, 
        inicio_alimentacao=None, 
        fim_alimentacao=None, 
        quantidade=None, 
        ml_ou_g=None, 
        mama_lados=None, 
        aceitacao=None, 
        notas=None):
    
    """Registra uma alimentação na base de dados"""

    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO alimentacao (
        id_registro, 
        tipo_alimentacao, 
        alimento, 
        inicio_alimentacao, 
        fim_alimentacao, 
        quantidade, 
        ml_ou_g, 
        mama_lados, 
        aceitacao, 
        notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_registro, tipo_alimentacao, alimento, inicio_alimentacao, fim_alimentacao, quantidade, ml_ou_g, mama_lados, aceitacao, notas))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID do registro associado
    return id_registro
