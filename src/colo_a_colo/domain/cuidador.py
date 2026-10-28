from werkzeug.security import generate_password_hash

def registrar_cuidador(conn, nome, email, data_nascimento, password):

    """Registra um cuidador na base de dados"""

    password_hash = generate_password_hash(password)
    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # executa a consulta SQL
    cursor.execute("""
        INSERT INTO cuidador (nome, email, data_nascimento, password_hash)
        VALUES (?, ?, ?, ?)
    """, (nome, email, data_nascimento, password_hash))

    # Salva as alterações na base de dados
    conn.commit()

    # Retorna o ID gerado pelo SQLite
    return cursor.lastrowid
