
class Banho:

    @staticmethod
    def registrar_banho(conn, id_rotina, notas=None):

        """Registra os dados de um banho na base de dados"""

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # Insere os dados do banho e associa à rotina
        cursor.execute("""
            INSERT INTO banho (id_rotina, notas)
            VALUES (?, ?)
        """, (id_rotina, notas))

        # Retorna o ID da rotina associado ao banho
        return id_rotina
