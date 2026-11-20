
class Fralda:

    @staticmethod
    def registrar_fralda(conn, id_registro, xixi=False, coco=False, notas=None):

        """Registra uma fralda na base de dados"""

        # Verifica se pelo menos uma das opções foi selecionada
        if not xixi and not coco:
            raise ValueError("Selecione xixi, cocô ou ambos.")

        # Converte os valores booleanos para inteiros:
        # False = 0 e True = 1, conforme a estrutura da tabela
        xixi = int(xixi)
        coco = int(coco)

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # Insere os dados da fralda na tabela
        cursor.execute("""
            INSERT INTO fralda (id_registro, xixi, coco, notas)
            VALUES (?, ?, ?, ?)
        """, (id_registro, xixi, coco, notas))

        # Retorna o ID do registro associado à rotina
        return id_registro
