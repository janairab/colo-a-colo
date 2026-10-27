def registrar_bebe(conn, nome, sexo, data_nascimento, id_cuidador):

    """Registra um bebé na base de dados"""

    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO bebe (nome, sexo, data_nascimento)
        VALUES (?, ?, ?, ?)
    """, (nome, sexo, data_nascimento, id_cuidador))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID gerado pelo SQLite
    return cursor.lastrowid