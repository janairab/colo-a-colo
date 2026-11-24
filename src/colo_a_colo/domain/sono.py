
class Sono:

    @staticmethod
    def registrar_sono(conn, id_rotina, fim_sono=None, notas=None):
        """Registra soneca ou sono noturno na base de dados"""

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # Insere os dados do sono na base de dados
        cursor.execute("""
            INSERT INTO sono (id_rotina, fim_sono, notas)
            VALUES (?, ?, ?)
        """, (id_rotina, fim_sono, notas))

        # Retorna o ID da rotina associado ao sono
        return id_rotina