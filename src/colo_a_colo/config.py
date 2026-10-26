import os

# Caminho da pasta principal do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Caminho da base de dados SQLite
DB_PATH = os.path.join(BASE_DIR, "data", "colo_a_colo.db")

# Caminho do ficheiro SQL
SQL_PATH = os.path.join(BASE_DIR, "docs", "criar_tabelas.sql")