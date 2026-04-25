# Sistema de Agendamento para Barbearia - 2ª Nota

Este repositório contém o projeto prático da disciplina de Banco de Dados (2ª Nota). O objetivo é demonstrar a integração de uma aplicação Python com um banco de dados relacional PostgreSQL, realizando operações de CRUD e consultas complexas com JOIN.

## 📌 Sobre o Projeto

O tema escolhido foi um **Sistema de Agendamento para Barbearia (Bodies Barber)**, permitindo o gerenciamento de clientes, barbeiros, serviços e agendamentos através de uma interface web com autenticação de usuários.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Banco de Dados:** PostgreSQL
- **Driver de Conexão:** `psycopg2`
- **Framework Web:** Flask
- **Interface:** Web (Flask + HTML/CSS) — *Interface Gráfica (Bônus +1,0 ponto)*

## 📂 Estrutura do Repositório

A organização das pastas segue rigorosamente as exigências do professor:

- `/diagrama`: Modelo Entidade-Relacionamento (DER).
- `/ddl`: Scripts de criação (`CREATE TABLE`, Constraints, PKs e FKs).
- `/dml`: Scripts de manipulação (`INSERT`, `UPDATE`, `DELETE`).
- `/dql`: Scripts de consulta (`SELECT`, `JOINs`, Filtros, Ordenação).
- `/src`: Código-fonte da aplicação Python/Flask.

## 📸 Demonstração (Prints do Sistema)

### 1. Tela de Login
![Login](./docs/login.png)

### 2. Menu Principal e Operações CRUD
![Dashboard](./docs/dashboard.png)

### 3. Consulta Complexa (Inner/Left Join)
![Agendamentos](./docs/agendamentos.png)

## 📺 Vídeo Demonstrativo

Confira a explicação detalhada do sistema e do código no link abaixo:
👉 [ASSISTIR VÍDEO NO YOUTUBE/DRIVE](#)

## 🚀 Como Executar o Projeto

### Configuração do Banco de Dados

1. Execute o script contido em `/ddl/databasePGSQL.sql`.
2. (Opcional) Popule o banco com `/dml/inserts.sql`.

### Executando em Python

1. Instale as dependências:
```bash
pip install flask psycopg2-binary python-dotenv
```
2. Dentro de `/src`, crie um arquivo `.env` com as credenciais do banco:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=CRUD_Barbearia
DB_USER=postgres
DB_PASSWORD=sua_senha
```
3. Execute o comando:
```bash
cd src
python app.py
```
4. Acesse em **http://127.0.0.1:5000**

### Credenciais de Teste

| E-mail | Senha | Perfil |
|---|---|---|
| admin@bodies.com | senha123 | admin |
| carlos@bodies.com | senha123 | barbeiro |

## 📄 Regras de Negócio e Consultas Complexas

O sistema realiza consultas complexas para exibir os dados integrados das três tabelas:

- **INNER JOIN:** Para listar agendamentos com nome do cliente, barbeiro e serviço — retorna apenas agendamentos com todos os vínculos válidos.
- **LEFT JOIN:** Para listar todos os barbeiros e clientes com o total de agendamentos — inclui mesmo os que não possuem nenhum agendamento cadastrado.

## 👤 Autor

- **João Eduardo** — [@JeytheJo](https://github.com/JeytheJo)
- Centro Universitário Santo Agostinho (UNIFSA)
- Disciplina: Banco de Dados — Prof. Anderson Costa — [andersoncosta@unifsa.com.br](mailto:andersoncosta@unifsa.com.br)