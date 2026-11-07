from werkzeug.security import generate_password_hash, check_password_hash

class Cuidador:

    # inicializa os dados do cuidador
    def __init__(self, nome, email, data_nascimento):
        # Atributos internos
        self._nome = nome
        self._email = email
        self._data_nascimento = data_nascimento

    # define como o objeto será apresentado em texto
    def __str__(self):
        return f"Cuidador: {self._nome}"

    # registra o cuidador no SQLite e guarda o hash da senha
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

    # verifica o e-mail e a senha
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
            return None

        # Compara a palavra-passe digitada com o hash guardado no banco de dados
        if check_password_hash(cuidador["password_hash"], password):
            return cuidador["id_cuidador"]

        return None
