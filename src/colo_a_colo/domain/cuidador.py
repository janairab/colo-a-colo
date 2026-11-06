from werkzeug.security import generate_password_hash, check_password_hash

class Cuidador:

    def __init__(self, nome, email, data_nascimento):
        self._nome = nome
        self._email = email
        self._data_nascimento = data_nascimento

    def __str__(self):
        return f"Cuidador: {self._nome} - {self._email}"


    @staticmethod
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
    
    @staticmethod
    def login(conn, email, password):

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # executa a consulta SQL
        cursor.execute("""
            SELECT id_cuidador, password_hash
            FROM cuidador
            WHERE email = ?
        """, (email,))

        # Obtém o primeiro resultado da consulta
        cuidador = cursor.fetchone()

        # Se não encontrar o e-mail, não existe cuidador para autenticar
        if cuidador is None:
            return "Email não registrado"

        # Compara a palavra-passe digitada com o hash guardado no banco de dados
        if check_password_hash(cuidador["password_hash"], password):
            return cuidador["id_cuidador"]

        return None
