import psycopg2
import os
import subprocess
from contextlib import closing
from dotenv import load_dotenv
import sys

# Carregar variáveis de ambiente do arquivo .env
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, '.env'))

# Configurações do banco usando variáveis de ambiente
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def executar_sql(arquivo_sql):
    caminho_completo = os.path.join(SCRIPT_DIR, arquivo_sql)
    if not os.path.exists(caminho_completo):
        raise FileNotFoundError(f"Arquivo {caminho_completo} não encontrado.")

    with open(caminho_completo, "r", encoding="utf-8") as arquivo, \
         closing(psycopg2.connect(**db_config)) as conn, \
         closing(conn.cursor()) as cursor:
        cursor.execute(arquivo.read())
        conn.commit()
        print(f"Arquivo {arquivo_sql} executado com sucesso!")

def main():
    print("Iniciando o pipeline...")

    try:
        # Etapa 1: Criar tabelas
        executar_sql("create_table.sql")

        # Etapa 2: Gerar dados fictícios
        print("Gerando dados fictícios...")
        insert_faker_path = os.path.join(SCRIPT_DIR, "insert_faker.py")
        result = subprocess.run(['python', insert_faker_path], 
                              capture_output=True, 
                              text=True,
                              cwd=SCRIPT_DIR)  # Definir o diretório de trabalho
        
        if result.returncode != 0:
            print(f"Erro ao executar insert_faker.py: {result.stderr}")
            raise RuntimeError("Erro ao executar insert_faker.py")

        # Etapa 3: Inserir dados fictícios
        dados_ficticios_path = os.path.join(SCRIPT_DIR, "dados_ficticios.sql")
        if not os.path.exists(dados_ficticios_path):
            raise FileNotFoundError("Arquivo dados_ficticios.sql não foi gerado.")
        
        executar_sql("dados_ficticios.sql")
        print("Pipeline concluído com sucesso!")

        # Etapa 4: Executar queries de consulta
        print("\nExecutando consultas...")
        executar_query_path = os.path.join(SCRIPT_DIR, "executar_query.py")
        result = subprocess.run([sys.executable, executar_query_path],
                              text=True,
                              cwd=SCRIPT_DIR)

    except Exception as e:
        print(f"Erro no pipeline: {e}")
        exit(1)

# Garantir que o script só é executado diretamente
if __name__ == "__main__" and not hasattr(main, "_has_run"):
    main._has_run = True
    main()