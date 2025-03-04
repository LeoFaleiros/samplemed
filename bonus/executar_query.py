import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do banco usando variáveis de ambiente
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def executar_query(query, descricao=""):
    print(f"\n{descricao}")
    print("-" * 50)
    
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute(query)
    
    if cur.description:
        resultados = cur.fetchall()
        for linha in resultados:
            print(linha)
    else:
        conn.commit()
        print("Query executada!")

    cur.close()
    conn.close()

if __name__ == "__main__":
    # Query a) Saldo atual de cada usuário
    query1 = """
    SELECT 
        u.Nome AS NomeUsuario,
        COALESCE(cb.Saldo, 0) + COALESCE(SUM(CASE 
            WHEN t.TipoTransacao = 'Crédito' THEN t.Valor
            WHEN t.TipoTransacao = 'Débito' THEN -t.Valor
            ELSE 0
        END), 0) AS SaldoAtual
    FROM 
        Usuario u
    JOIN 
        ContaBancaria cb ON u.ID = cb.UsuarioID
    LEFT JOIN 
        Transacao t ON cb.ID = t.ContaID
    GROUP BY 
        u.Nome, cb.Saldo;
    """

    # Query b) Transações dos últimos 2 meses
    query2 = """
    SELECT 
        *
    FROM 
        Transacao
    WHERE 
        DataTransacao >= NOW() - INTERVAL '2 MONTH'
    ORDER BY 
        Valor DESC;
    """

    # Query c) Usuário com mais débitos no último mês
    query3 = """
    SELECT 
        u.Nome AS NomeUsuario,
        COUNT(t.ID) AS TotalDebitos
    FROM 
        Usuario u
    JOIN 
        ContaBancaria cb ON u.ID = cb.UsuarioID
    JOIN 
        Transacao t ON cb.ID = t.ContaID
    WHERE 
        t.TipoTransacao = 'Débito'
        AND t.DataTransacao >= NOW() - INTERVAL '1 MONTH'
    GROUP BY 
        u.Nome
    ORDER BY 
        TotalDebitos DESC
    LIMIT 1;
    """

    executar_query(query1, "a) Saldo atual de cada usuário:")
    executar_query(query2, "b) Transações dos últimos 2 meses:")
    executar_query(query3, "c) Usuário com mais débitos no último mês:")
