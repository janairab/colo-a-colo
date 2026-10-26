def registrar_cuidador(conn, nome, email, data_nascimento):

    """Registra um cuidador na base de dados"""

    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO cuidador (nome, email, data_nascimento)
        VALUES (?, ?, ?)
    """, (nome, email, data_nascimento))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID gerado pelo SQLite
    return cursor.lastrowid
