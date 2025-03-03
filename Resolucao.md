#Parte 1: Modelagem de Dados

##1. Modelagem Conceitual e Normalização 

###• Explique brevemente o conceito de normalização e como ela pode impactar a performance de um banco de dados transacional.

A normalização é uma técnica utilizada em bancos de dados para organizar informações, reduzindo redundâncias e garantindo a integridade dos dados. Esse processo consiste em dividir tabelas grandes em tabelas menores e interligadas, seguindo regras conhecidas como formas normais. Com isso, a normalização economiza espaço de armazenamento, facilita a manutenção e minimiza inconsistências, já que cada dado é armazenado de forma única e centralizada.

Por outro lado, a normalização pode impactar negativamente o desempenho em alguns cenários, especialmente em sistemas transacionais que realizam muitas leituras e escritas. Isso ocorre porque consultas mais complexas frequentemente exigem a junção (JOIN) de várias tabelas, o que pode aumentar o tempo de processamento. Por isso, é importante equilibrar os benefícios da organização e integridade dos dados com a necessidade de desempenho, dependendo do tipo de aplicação.

• Qual a diferença entre modelo relacional e modelo dimensional? Em quais casos cada um deve ser 
utilizado? 
2. Criação de Esquema Relacional (Prático) A empresa precisa armazenar informações de transações 
bancárias. O banco de dados precisa conter as seguintes informações: 
• Usuário (ID, nome, CPF, e-mail) 
• Conta Bancária (ID, número da conta, saldo, tipo de conta, ID do usuário) 
• Transações (ID, ID da conta, data, valor, tipo de transação [crédito/débito], descrição) 
Tarefa: Escreva o código SQL para criar as tabelas relacionais, definindo chaves primárias, estrangeiras 
e índices adequados para melhor desempenho.