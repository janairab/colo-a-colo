
from datetime import datetime


class Rotina:

    @staticmethod
    def registrar_rotina(conn, id_bebe, tipo_registro, data_hora):

        """Registra uma rotina na base de dados"""

        # Converte a data e hora caso sejam recebidas como texto
        if isinstance(data_hora, str):
            data_hora = datetime.fromisoformat(data_hora)

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # Obtém somente a data do acontecimento
        data = data_hora.date()

        # Procura uma folha diária do bebê para a data informada
        cursor.execute("""
            SELECT id_registro_diario
            FROM registro_diario
            WHERE id_bebe = ? AND data = ?
        """, (id_bebe, data))

        registro_diario = cursor.fetchone()

        # Cria uma folha diária caso ainda não exista
        if registro_diario is None:

            cursor.execute("""
                INSERT INTO registro_diario (id_bebe, data)
                VALUES (?, ?)
            """, (id_bebe, data))

            id_registro_diario = cursor.lastrowid

        else:

            # Recupera o ID da folha diária existente
            id_registro_diario = registro_diario[0]

        # Insere o acontecimento na tabela de rotina
        cursor.execute("""
            INSERT INTO rotina (
                id_registro_diario,
                tipo_registro,
                data_hora
            )
            VALUES (?, ?, ?)
        """, (id_registro_diario, tipo_registro, data_hora))

        # Retorna o ID gerado para o acontecimento
        return cursor.lastrowid