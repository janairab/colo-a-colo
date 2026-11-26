# Importa datetime e timedelta para trabalhar com datas e horários
from datetime import datetime, timedelta


def converter_data_hora(valor):
    # Converte o texto recebido em uma data e hora
    try:
        return datetime.fromisoformat(valor)

    except (ValueError, TypeError):
        raise ValueError("Informe uma data e hora válida")



def validar_intervalo_data_hora(data_hora):
    # Obtém a data e hora atuais
    agora = datetime.now()

    # Calcula o limite de um ano antes
    try:
        limite_inferior = agora.replace(year=agora.year - 1)

    except ValueError:
        # Ajusta o dia 29 de fevereiro para 28 de fevereiro
        limite_inferior = agora.replace(
            year=agora.year - 1,
            day=28
        )

    # Verifica se a data está dentro do intervalo permitido
    if not limite_inferior <= data_hora <= agora:
        raise ValueError(
            "A data e hora devem estar entre um ano atrás e o momento atual"
        )



def validar_horario_termino(inicio, termino):
    # Verifica se o término é posterior ao início
    if termino <= inicio:
        raise ValueError(
            "O horário de término deve ser posterior ao início"
        )

    # Verifica se o término não está no futuro
    if termino > datetime.now():
        raise ValueError(
            "O horário de término não pode estar no futuro"
        )



def calcular_fim_amamentacao(inicio, horario_fim):
    # Converte a hora informada pelo cuidador
    try:
        hora = datetime.strptime(horario_fim, "%H:%M").time()

    except (ValueError, TypeError):
        raise ValueError("Informe um horário de término válido")

    # Combina a hora com a data de início
    termino = datetime.combine(inicio.date(), hora)

    # Se a hora for anterior ao início, considera o dia seguinte
    if termino < inicio:
        termino += timedelta(days=1)

    # Valida o horário calculado
    validar_horario_termino(inicio, termino)

    return termino
