
from colo_a_colo.domain.rotina import Rotina
from colo_a_colo.domain.fralda import Fralda


# Registra a rotina e os dados da fralda na mesma transação
def registrar_fralda_completa(
    conn,
    id_bebe,
    data_hora,
    xixi=False,
    coco=False,
    notas=None
):

    # Garante que os dois registros sejam confirmados juntos
    # Se ocorrer um erro, as alterações serão revertidas
    with conn:

        # Registra primeiro a rotina e recebe o ID criado
        id_rotina = Rotina.registrar_rotina(
            conn,
            id_bebe,
            "fralda",
            data_hora
        )

        # Registra os detalhes da fralda usando o ID da rotina
        Fralda.registrar_fralda(
            conn,
            id_rotina,
            xixi,
            coco,
            notas
        )

    # Devolve o ID da rotina criada
    return id_rotina
