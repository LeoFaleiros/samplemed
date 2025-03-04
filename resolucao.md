# Parte 1: Modelagem de Dados

## 1. Modelagem Conceitual e Normalização 

### • Explique brevemente o conceito de normalização e como ela pode impactar a performance de um banco de dados transacional.

A normalização é um processo de organização de dados que elimina redundâncias e garante consistência através da divisão de tabelas complexas em estruturas menores e relacionadas. Embora melhore a integridade dos dados e facilite a manutenção, pode impactar o desempenho em sistemas transacionais devido à necessidade de múltiplos JOINs em consultas complexas. O desafio está em encontrar o equilíbrio entre organização dos dados e performance, considerando os requisitos específicos da aplicação.

---
### • Qual a diferença entre modelo relacional e modelo dimensional? Em quais casos cada um deve ser utilizado?

Os modelos relacional e dimensional são utilizados em diferentes contextos para atender às necessidades específicas de sistemas de banco de dados. O modelo relacional organiza os dados em tabelas normalizadas, com chaves primárias e estrangeiras, priorizando a consistência e a integridade das informações. Ele é ideal para sistemas transacionais (OLTP), como bancos de dados utilizados em gestão de estoques ou operações bancárias.

Já o modelo dimensional é projetado para análise de dados, estruturado em tabelas fato e dimensão, facilitando consultas rápidas e agregações. Ele é amplamente usado em sistemas analíticos (OLAP), como data warehouses, que servem para relatórios e análises de vendas. Enquanto o modelo relacional é mais adequado para transações, o dimensional atende melhor às demandas de análise e geração de insights.

---
## 2. Criação de Esquema Relacional (Prático)
A empresa precisa armazenar informações de transações bancárias. O banco de dados precisa conter as seguintes informações: 
• Usuário (ID, nome, CPF, e-mail)

• Conta Bancária (ID, número da conta, saldo, tipo de conta, ID do usuário) 

• Transações (ID, ID da conta, data, valor, tipo de transação [crédito/débito], descrição) 

Tarefa: Escreva o código SQL para criar as tabelas relacionais, definindo chaves primárias, estrangeiras e índices adequados para melhor desempenho.
```sql
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
---
# Parte 2: SQL 
## 3. Consultas SQL (Prático) 
Considere as tabelas criadas na questão anterior e escreva as queries para: 
### a) Obter o saldo atual de cada usuário.
```sql
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
``` 
### b) Listar todas as transações feitas nos últimos 2 meses ordenadas por valor decrescente. 
```sql
SELECT 
    *
FROM 
    Transacao
WHERE 
    DataTransacao >= NOW() - INTERVAL '2 MONTH'
ORDER BY 
    Valor DESC;
```
---
### c) Encontrar o usuário que realizou o maior número de transações do tipo "débito" no último mês.
```sql
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
```
---
# Parte 3: ETL e Pipelines de Dados 
## 4. Extração e Transformação  
A empresa recebe dados de transações financeiras no seguinte formato JSON: 
```json
{ 
    "id_transacao": "123456", 
    "id_conta": "98765", 
    "data": "2024-02-28T14:30:00", 
    "valor": 150.75,
    "tipo": "credito", 
    "descricao": "Depósito via PIX" 
}
```
Tarefa: Escreva um script Python utilizando Pandas para: 
### 1. Carregar os dados de um arquivo JSON. 
```python
df = pd.read_json('transacoes.json')
```
---
### 2. Criar uma nova coluna chamada valor_dolar, aplicando a divisão no valor do dólar atual
```python
dolar = 5.88
df['valor_dolar'] = df['valor'] / dolar
```
---
### 3. Exportar o resultado final para um arquivo CSV.
```python
df.to_csv('transacoes.csv', index=False, header=True)
```
---
# Parte 4: Big Data e Arquitetura 
Conceitos de Big Data  
Responda brevemente: 
### • O que é um Data Lake e como ele se diferencia de um Data Warehouse?
Um Data Lake armazena dados brutos de diversos formatos (estruturados, semi-estruturados e não estruturados), oferecendo flexibilidade para análises avançadas, como machine learning, mas com desafios maiores em governança. Já um Data Warehouse organiza dados estruturados e processados, com forte governança para garantir qualidade e consistência, sendo otimizado para consultas rápidas e análises de negócio, como relatórios de BI. A diferença está no propósito: o Data Lake é exploratório, enquanto o Data Warehouse é organizado e voltado para análises predefinidas.

---
### • Como um pipeline de dados escalável pode ser implementado utilizando Kubernetes + Airflow? 
A combinação de Kubernetes e Airflow permite implementar pipelines de dados escaláveis e robustos. O Airflow organiza o fluxo de trabalho com DAGs, enquanto o Kubernetes gerencia a infraestrutura, assegurando alta disponibilidade, escalabilidade automática e recuperação de falhas. Juntos, processam grandes volumes de dados de forma eficiente, adaptam-se a demandas variáveis e garantem a continuidade das operações.

---
# Bonus 
Caso ache interessante usar a conta gratuita da Amazon para mostrar na prática alguma dessas implementações, pode-se criar a estrutura de tabelas da Parte 1 no RDS Postgree e mostrar algum gráfico implementado no QuickSight relacionado às consultas SQL da Parte 2 