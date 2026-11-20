
import sqlite3
import pytest

from colo_a_colo.domain.fralda import Fralda


# Cria uma base de dados temporária para realizar os testes
@pytest.fixture
def conn():

    # Abre uma conexão com uma base de dados que existe apenas em memória
    conexao = sqlite3.connect(":memory:")

    # Cria a tabela fralda com a mesma estrutura utilizada no projeto
    conexao.execute("""
        CREATE TABLE fralda (
            id_registro INTEGER PRIMARY KEY,

            -- Armazena 0 para não e 1 para sim
            xixi INTEGER NOT NULL DEFAULT 0
                CHECK (xixi IN (0, 1)),

            -- Armazena 0 para não e 1 para sim
            coco INTEGER NOT NULL DEFAULT 0
                CHECK (coco IN (0, 1)),

            -- Guarda observações sobre a troca da fralda
            notas TEXT,

            -- Exige que pelo menos uma eliminação esteja selecionada
            CHECK (xixi = 1 OR coco = 1)
        )
    """)

    # Disponibiliza a conexão para cada teste
    yield conexao

    # Fecha a conexão depois que o teste termina
    conexao.close()


# Testa o registro de uma fralda com apenas xixi
def test_registrar_so_xixi(conn):

    # Registra a fralda com xixi selecionado e cocô desmarcado
    Fralda.registrar_fralda(conn, 1, xixi=True, coco=False)

    # Consulta os valores armazenados na tabela
    resultado = conn.execute(
        "SELECT xixi, coco FROM fralda WHERE id_registro = 1"
    ).fetchone()

    # Confirma que xixi foi registrado como 1 e cocô como 0
    assert resultado == (1, 0)


# Testa o registro de uma fralda com apenas cocô
def test_registrar_so_coco(conn):

    # Registra a fralda com cocô selecionado e xixi desmarcado
    Fralda.registrar_fralda(conn, 2, xixi=False, coco=True)

    # Consulta os valores armazenados na tabela
    resultado = conn.execute(
        "SELECT xixi, coco FROM fralda WHERE id_registro = 2"
    ).fetchone()

    # Confirma que xixi foi registrado como 0 e cocô como 1
    assert resultado == (0, 1)


# Testa o registro de uma fralda com xixi e cocô
def test_registrar_ambos(conn):

    # Registra a fralda com as duas opções selecionadas
    Fralda.registrar_fralda(conn, 3, xixi=True, coco=True)

    # Consulta os valores armazenados na tabela
    resultado = conn.execute(
        "SELECT xixi, coco FROM fralda WHERE id_registro = 3"
    ).fetchone()

    # Confirma que os dois campos foram registrados como 1
    assert resultado == (1, 1)


# Testa se o sistema impede o registro sem nenhuma seleção
def test_impedir_registro_sem_selecao(conn):

    # Verifica se a classe apresenta um erro quando nenhuma opção é marcada
    with pytest.raises(ValueError):

        # Tenta registrar uma fralda sem xixi e sem cocô
        Fralda.registrar_fralda(conn, 4, xixi=False, coco=False)

    # Consulta se algum registro foi inserido
    resultado = conn.execute(
        "SELECT * FROM fralda WHERE id_registro = 4"
    ).fetchone()

    # Confirma que nenhum registro foi criado
    assert resultado is None
