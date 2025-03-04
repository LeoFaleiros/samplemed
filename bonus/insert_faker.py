import random
from faker import Faker
import os

def main():
    # Obter o diretório do script atual
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Inicializando o Faker
    fake = Faker('pt_BR')  # Gera dados no formato brasileiro
    
    # Quantidade de registros fictícios
    num_usuarios = 10
    num_contas = 20
    num_transacoes = 50
    
    # Listas para armazenar os dados
    usuarios = []
    contas = []
    transacoes = []
    
    # Gerar usuários
    for _ in range(num_usuarios):
        usuario = {
            "Nome": fake.name(),
            "CPF": fake.cpf(),
            "Email": fake.email()
        }
        usuarios.append(usuario)
    
    # Gerar contas bancárias
    for _ in range(num_contas):
        numero_conta = str(fake.random_number(digits=10)) + str(fake.random_number(digits=8))
        conta = {
            "NumeroConta": numero_conta,
            "Saldo": round(random.uniform(100, 10000), 2),
            "TipoConta": random.choice(['Corrente', 'Poupança']),
            "UsuarioID": random.randint(1, num_usuarios)
        }
        contas.append(conta)
    
    # Gerar transações
    for _ in range(num_transacoes):
        transacao = {
            "ContaID": random.randint(1, num_contas),
            "DataTransacao": fake.date_time_between(start_date="-90d", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "Valor": round(random.uniform(10, 1000), 2),
            "TipoTransacao": random.choice(['Crédito', 'Débito']),
            "Descricao": fake.sentence(nb_words=6)
        }
        transacoes.append(transacao)
    
    # Função para escapar strings para SQL
    def escape_sql_string(s):
        return s.replace("'", "''")
    
    # Gerar script SQL para inserir os dados
    output_file = os.path.join(SCRIPT_DIR, "dados_ficticios.sql")
    
    with open(output_file, "w", encoding='utf-8') as file:
        # Configuração de codificação
        file.write("-- Configuração de codificação\n")
        file.write("SET client_encoding = 'UTF8';\n\n")
        
        # Inserir usuários
        file.write("-- Inserindo usuários\n")
        for usuario in usuarios:
            nome_escaped = escape_sql_string(usuario['Nome'])
            file.write(f"INSERT INTO Usuario (Nome, CPF, Email) VALUES "
                      f"('{nome_escaped}', '{usuario['CPF']}', '{usuario['Email']}');\n")

        # Inserir contas bancárias
        file.write("\n-- Inserindo contas bancárias\n")
        for conta in contas:
            file.write(f"INSERT INTO ContaBancaria (NumeroConta, Saldo, TipoConta, UsuarioID) VALUES "
                      f"('{conta['NumeroConta']}', {conta['Saldo']}, '{conta['TipoConta']}', {conta['UsuarioID']});\n")
        
        # Inserir transações
        file.write("\n-- Inserindo transações\n")
        for transacao in transacoes:
            descricao_escaped = escape_sql_string(transacao['Descricao'])
            file.write(f"INSERT INTO Transacao (ContaID, DataTransacao, Valor, TipoTransacao, Descricao) VALUES "
                      f"({transacao['ContaID']}, '{transacao['DataTransacao']}', {transacao['Valor']}, "
                      f"'{transacao['TipoTransacao']}', '{descricao_escaped}');\n")

if __name__ == "__main__":
    main()