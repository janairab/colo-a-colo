import sqlite3
from colo_a_colo.config import DB_PATH, SQL_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)

    # Permite acessar os resultados pelo nome das colunas, ao invés do indice
    conn.row_factory = sqlite3.Row

    # Ativar a verificação das chaves estrangeiras
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def criar_tabelas():
    conn = get_db()

    try:
        with open(SQL_PATH, "r", encoding="utf-8") as ficheiro:
            sql = ficheiro.read()

        conn.executescript(sql)
        print("Tabelas criadas com sucesso!")

    finally:
        conn.close()
