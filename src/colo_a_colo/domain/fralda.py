def registrar_fralda(conn, id_registro, miccao=None, coco=None, notas=None):

    """Registra uma fralda na base de dados"""

    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO fralda (id_registro, miccao, coco, notas)
        VALUES (?, ?, ?, ?)
    """, (id_registro, miccao, coco, notas))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID do registro associado
    return id_registro