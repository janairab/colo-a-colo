
from colo_a_colo.domain.rotina import Rotina
from colo_a_colo.domain.banho import Banho


# Registra a rotina e os dados do banho na mesma transação
def registrar_banho_completo(
    conn,
    id_bebe,
    data_hora,
    notas=None
):

    # Garante que os dois registros sejam confirmados juntos
    # Se ocorrer um erro, as alterações serão revertidas
    with conn:

        # Registra primeiro a rotina e recebe o ID criado
        id_rotina = Rotina.registrar_rotina(
            conn,
            id_bebe,
            "banho",
            data_hora
        )

        # Registra os detalhes do banho usando o ID da rotina
        Banho.registrar_banho(
            conn,
            id_rotina,
            notas
        )

    # Devolve o ID da rotina criada
    return id_rotina