def registrar_rotina(conn, id_bebe, tipo_registro, data_hora, notas=None):

    """Registra uma rotina na base de dados"""

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registro_rotina (id_bebe, tipo_registro, data_hora, notas)
        VALUES (?, ?, ?, ?)
    """, (id_bebe, tipo_registro, data_hora, notas))

    conn.commit()

    return cursor.lastrowid