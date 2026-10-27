def registrar_banho(conn, id_registro, notas=None):

    """Registra um banho na base de dados"""

    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO banho (id_registro, notas)
        VALUES (?, ?)
    """, (id_registro, notas))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID do registro associado
    return id_registro