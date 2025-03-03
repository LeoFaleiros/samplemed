# Parte 1: Modelagem de Dados

## 1. Modelagem Conceitual e Normalização 

### • Explique brevemente o conceito de normalização e como ela pode impactar a performance de um banco de dados transacional.

```resposta
A normalização é uma técnica utilizada em bancos de dados para organizar informações, reduzindo redundâncias e garantindo a integridade dos dados. Esse processo consiste em dividir tabelas grandes em tabelas menores e interligadas, seguindo regras conhecidas como formas normais. Com isso, a normalização economiza espaço de armazenamento, facilita a manutenção e minimiza inconsistências, já que cada dado é armazenado de forma única e centralizada.

Por outro lado, a normalização pode impactar negativamente o desempenho em alguns cenários, especialmente em sistemas transacionais que realizam muitas leituras e escritas. Isso ocorre porque consultas mais complexas frequentemente exigem a junção (JOIN) de várias tabelas, o que pode aumentar o tempo de processamento. Por isso, é importante equilibrar os benefícios da organização e integridade dos dados com a necessidade de desempenho, dependendo do tipo de aplicação.
```
---
### • Qual a diferença entre modelo relacional e modelo dimensional? Em quais casos cada um deve ser utilizado?
```resposta
Os modelos relacional e dimensional são utilizados em diferentes contextos para atender às necessidades específicas de sistemas de banco de dados. O modelo relacional organiza os dados em tabelas normalizadas, com chaves primárias e estrangeiras, priorizando a consistência e a integridade das informações. Ele é ideal para sistemas transacionais (OLTP), como bancos de dados utilizados em gestão de estoques ou operações bancárias.

Já o modelo dimensional é projetado para análise de dados, estruturado em tabelas fato e dimensão, facilitando consultas rápidas e agregações. Ele é amplamente usado em sistemas analíticos (OLAP), como data warehouses, que servem para relatórios e análises de vendas. Enquanto o modelo relacional é mais adequado para transações, o dimensional atende melhor às demandas de análise e geração de insights.
```
---
## 2. Criação de Esquema Relacional (Prático) A empresa precisa armazenar informações de transações bancárias. O banco de dados precisa conter as seguintes informações: 
• Usuário (ID, nome, CPF, e-mail)

• Conta Bancária (ID, número da conta, saldo, tipo de conta, ID do usuário) 

• Transações (ID, ID da conta, data, valor, tipo de transação [crédito/débito], descrição) 

Tarefa: Escreva o código SQL para criar as tabelas relacionais, definindo chaves primárias, estrangeiras e índices adequados para melhor desempenho.
```resposta
-- Criação da tabela de Usuários
CREATE TABLE Usuario (
    ID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    CPF VARCHAR(14) NOT NULL UNIQUE,
    Email VARCHAR(150) NOT NULL UNIQUE
);

-- Criação da tabela de Contas Bancárias
CREATE TABLE ContaBancaria (
    ID SERIAL PRIMARY KEY,
    NumeroConta VARCHAR(20) NOT NULL UNIQUE,
    Saldo NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
    TipoConta VARCHAR(10) NOT NULL CHECK (TipoConta IN ('Corrente', 'Poupança')),
    UsuarioID INT NOT NULL,
    FOREIGN KEY (UsuarioID) REFERENCES Usuario(ID) ON DELETE CASCADE
);

-- Criar índice para UsuarioID na tabela ContaBancaria
CREATE INDEX idx_usuarioid ON ContaBancaria(UsuarioID);

-- Criação da tabela de Transações
CREATE TABLE Transacao (
    ID SERIAL PRIMARY KEY,
    ContaID INT NOT NULL,
    DataTransacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Valor NUMERIC(15, 2) NOT NULL,
    TipoTransacao VARCHAR(10) NOT NULL CHECK (TipoTransacao IN ('Crédito', 'Débito')),
    Descricao TEXT,
    FOREIGN KEY (ContaID) REFERENCES ContaBancaria(ID) ON DELETE CASCADE
);

-- Criar índice para ContaID e DataTransacao na tabela Transacao
CREATE INDEX idx_contaid_data ON Transacao(ContaID, DataTransacao);
```
