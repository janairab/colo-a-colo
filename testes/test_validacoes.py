# Importa recursos para trabalhar com datas e horários
from datetime import datetime, timedelta

# Importa o pytest para realizar os testes
import pytest

# Importa as funções que serão testadas
from colo_a_colo.utils.validacoes import (
    converter_data_hora,
    validar_intervalo_data_hora,
    validar_horario_termino,
    calcular_fim_amamentacao
)


def test_converter_data_hora():
    resultado = converter_data_hora("2026-11-24T15:30")

    assert resultado == datetime(2026, 11, 24, 15, 30)


def test_converter_data_hora_invalida():
    with pytest.raises(ValueError):
        converter_data_hora("data inválida")


def test_converter_data_hora_valor_nulo():
    with pytest.raises(ValueError):
        converter_data_hora(None)


def test_validar_intervalo_data_hora_valido():
    data_hora = datetime.now() - timedelta(days=30)

    validar_intervalo_data_hora(data_hora)


def test_validar_intervalo_data_hora_antigo():
    data_hora = datetime.now() - timedelta(days=400)

    with pytest.raises(ValueError):
        validar_intervalo_data_hora(data_hora)


def test_validar_intervalo_data_hora_futuro():
    data_hora = datetime.now() + timedelta(days=1)

    with pytest.raises(ValueError):
        validar_intervalo_data_hora(data_hora)


def test_validar_horario_termino_valido():
    inicio = datetime.now() - timedelta(hours=2)
    termino = datetime.now() - timedelta(hours=1)

    validar_horario_termino(inicio, termino)


def test_validar_horario_termino_anterior():
    inicio = datetime.now() - timedelta(hours=1)
    termino = inicio - timedelta(minutes=30)

    with pytest.raises(ValueError):
        validar_horario_termino(inicio, termino)


def test_validar_horario_termino_futuro():
    inicio = datetime.now() - timedelta(hours=1)
    termino = datetime.now() + timedelta(hours=1)

    with pytest.raises(ValueError):
        validar_horario_termino(inicio, termino)



def test_calcular_fim_amamentacao_mesmo_dia():
    inicio = (datetime.now() - timedelta(days=1)).replace(
        hour=10, minute=0, second=0, microsecond=0
    )

    resultado = calcular_fim_amamentacao(inicio, "11:30")

    assert resultado == inicio.replace(hour=11, minute=30)



def test_calcular_fim_amamentacao_dia_seguinte():
    inicio = datetime.now().replace(
        hour=23, minute=0, second=0, microsecond=0
    ) - timedelta(days=1)

    resultado = calcular_fim_amamentacao(inicio, "00:30")

    esperado = inicio.replace(
        hour=0, minute=30
    ) + timedelta(days=1)

    assert resultado == esperado


def test_calcular_fim_amamentacao_horario_invalido():
    inicio = datetime.now() - timedelta(hours=2)

    with pytest.raises(ValueError):
        calcular_fim_amamentacao(inicio, "25:90")


def test_calcular_fim_amamentacao_futuro():
    inicio = datetime.now() - timedelta(minutes=10)

    with pytest.raises(ValueError):
        calcular_fim_amamentacao(inicio, "23:59")
