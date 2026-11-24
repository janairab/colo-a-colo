from colo_a_colo.domain.rotina import Rotina
from colo_a_colo.domain.sono import Sono


# Registra a rotina e os dados do sono na mesma transação
def registrar_sono_completo(
    conn,
    id_bebe,
    data_hora,
    fim_sono=None,
    notas=None
):

    # Garante que os dois registros sejam confirmados juntos
    # Se ocorrer um erro, as alterações serão revertidas
    with conn:

        # Registra primeiro a rotina e recebe o ID criado
        id_rotina = Rotina.registrar_rotina(
            conn,
            id_bebe,
            "sono",
            data_hora
        )

        # Registra os detalhes do sono usando o ID da rotina
        Sono.registrar_sono(
            conn,
            id_rotina,
            fim_sono,
            notas
        )

    # Devolve o ID da rotina criada
    return id_rotina