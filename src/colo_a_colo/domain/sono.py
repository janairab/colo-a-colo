def registrar_sono(conn, id_registro, inicio_sono, fim_sono=None, notas=None):

    """Registra soneca ou sono noturno na base de dados"""

    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO sono (id_registro, inicio_sono, fim_sono, notas)
        VALUES (?, ?, ?, ?)
    """, (id_registro, inicio_sono, fim_sono, notas))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID do registro associado
    return id_registro