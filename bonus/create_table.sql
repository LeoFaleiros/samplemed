-- Drop das tabelas existentes. Necessário pois a pipeline executa todas as etapas sempre que é chamada.
DROP TABLE IF EXISTS Transacao;
DROP TABLE IF EXISTS ContaBancaria;
DROP TABLE IF EXISTS Usuario;

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