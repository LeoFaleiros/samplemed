# Desafio SAMPLEMED

Desafio de análise de transações financeiras desenvolvido como parte de um processo seletivo.

## Sobre o Projeto

Este desafio analisa transações bancárias para:
- Calcular saldos atuais
- Listar movimentações recentes
- Identificar padrões de uso

## Configuração

1. Clone o repositório:
```bash
git clone https://github.com/LeoFaleiros/samplemed.git
cd samplemed
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
# Copie o arquivo de exemplo
cp bonus/.env.example bonus/.env

# Edite o arquivo .env com suas credenciais do banco
```

3. Execute o projeto:
```bash
python bonus/main.py
```

## Funcionalidades

O projeto realiza automaticamente:
- Criação da estrutura do banco de dados
- Geração e inserção de dados de teste
- Execução das análises

### Análises Disponíveis

1. Saldo atual por usuário
2. Histórico de transações dos últimos 2 meses
3. Identificação do usuário com maior volume de débitos mensais

## Estrutura

### Banco de Dados
O projeto utiliza três tabelas principais:
- `Usuario`: Dados cadastrais
- `ContaBancaria`: Informações das contas
- `Transacao`: Registro de movimentações

### Tecnologias
- PostgreSQL para armazenamento
- Python para processamento
- AWS QuickSight para visualizações

## Variáveis de Ambiente

O arquivo `.env` requer:
```env
DB_HOST=seu_host
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=usuario
DB_PASSWORD=senha
```

## Documentação

- Resolução teórica: `resolucao.md`
- Resolução prática: pasta `bonus/`
- Dashboard interativo com análises visuais das transações financeiras:
[Acessar Dashboard no AWS QuickSight](https://us-east-2.quicksight.aws.amazon.com/sn/dashboards/36b6411e-1809-440c-9f0f-0d8b1e353307/views/aa679352-f42a-47e1-be9e-3b2a2b8aa66c?directory_alias=leonardofaleiros)

## Visualização do Dashboard

Abaixo está uma visualização do dashboard criado no AWS QuickSight para análise das transações:

![Dashboard de Análise de Transações](bonus/visualizacao_quicksight2.jpg)