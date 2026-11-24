from colo_a_colo.domain.rotina import Rotina
from colo_a_colo.domain.alimentacao import Alimentacao


# Registra a rotina e os dados da alimentação na mesma transação
def registrar_alimentacao_completa(
    conn,
    id_bebe,
    data_hora,
    tipo_alimentacao,
    alimento=None,
    fim_amamentacao=None,
    quantidade=None,
    ml_ou_g=None,
    mama_lados=None,
    aceitacao=None,
    notas=None
):

    # Garante que os dois registros sejam confirmados juntos
    # Se ocorrer um erro, as alterações serão revertidas
    with conn:

        # Registra primeiro a rotina e recebe o ID criado
        id_rotina = Rotina.registrar_rotina(
            conn,
            id_bebe,
            "alimentacao",
            data_hora
        )

        # Registra os detalhes da alimentação usando o ID da rotina
        Alimentacao.registrar_alimentacao(
            conn,
            id_rotina,
            tipo_alimentacao,
            alimento,
            fim_amamentacao,
            quantidade,
            ml_ou_g,
            mama_lados,
            aceitacao,
            notas
        )

    # Devolve o ID da rotina criada
    return id_rotina