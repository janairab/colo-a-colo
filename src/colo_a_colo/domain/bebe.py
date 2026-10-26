def registrar_bebe(conn, nome, sexo, data_nascimento, id_cuidador):

    """Registra um bebé na base de dados"""

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bebe (nome, sexo, data_nascimento)
        VALUES (?, ?, ?, ?)
    """, (nome, sexo, data_nascimento, id_cuidador))

    conn.commit()

    return cursor.lastrowid