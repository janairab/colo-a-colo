from datetime import date
from calendar import monthrange

class Bebe:

    def __init__(self, nome, sexo, data_nascimento):
        self._nome = nome
        self._sexo = sexo

        # transforma a data recebida no formato AAAA-MM-DD em uma data que o Python consegue calcular (objeto date)
        self._data_nascimento = date.fromisoformat(data_nascimento)

    def calcular_idade(self):
        
        # Obtém a data do dia
        hoje = date.today()

        # Calcula a diferença em meses
        meses_totais = (hoje.year - self._data_nascimento.year) * 12
        meses_totais += hoje.month - self._data_nascimento.month

        # Calcula o ano e o mês do último aniversário mensal
        ano = self._data_nascimento.year + (self._data_nascimento.month - 1 + meses_totais) // 12
        mes = (self._data_nascimento.month - 1 + meses_totais) % 12 + 1

        # Ajusta o dia para meses com menos dias
        dia = min(self._data_nascimento.day, monthrange(ano, mes)[1])

        ultimo_mes = date(ano, mes, dia)

        #  Verifica se o último aniversário mensal já aconteceu
        if ultimo_mes > hoje:
            meses_totais -= 1

            ano = self._data_nascimento.year + (self._data_nascimento.month - 1 + meses_totais) // 12

            mes = (self._data_nascimento.month - 1 + meses_totais) % 12 + 1

            dia = min(self._data_nascimento.day, monthrange(ano, mes)[1])

            ultimo_mes = date(ano, mes, dia)

        # Calcula os dias restantes
        dias = (hoje - ultimo_mes).days

        # Converte os meses em anos e meses restantes
        # O divmod() divide um número por outro e devolve dois resultado: resultado inteiro e o resto da divisão
        anos, meses = divmod(meses_totais, 12)    
      
        # Monta a apresentação da idade
        partes = []

        if anos > 0:
            partes.append(f"{anos} ano{'s' if anos != 1 else ''}")

        if meses > 0:
            partes.append(f"{meses} {'mês' if meses == 1 else 'meses'}")

        if dias > 0:
            partes.append(f"{dias} dia{'s' if dias != 1 else ''}")

        if not partes:
            return "0 dias"
        
        return " e ".join(partes)


    def __str__(self):
        return f"{self._nome} - {self.calcular_idade()}"

    @staticmethod   
    def registrar_bebe(conn, nome, sexo, data_nascimento, id_cuidador):

        """Registra um bebê na base de dados"""

        # Cria o cursor para executar comandos SQL
        cursor = conn.cursor()

        # executa a consulta SQL
        cursor.execute("""
            INSERT INTO bebe (nome, sexo, data_nascimento, id_cuidador)
            VALUES (?, ?, ?, ?)
        """, (nome, sexo, data_nascimento, id_cuidador))

        # Salva as alterações na base de dados
        conn.commit()

        # Retorna o ID gerado pelo SQLite
        return cursor.lastrowid
