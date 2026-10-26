import sqlite3
from config import DB_PATH, SQL_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)

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
