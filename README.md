# 💈 Sistema de Agendamento - Barbearia (Bodies Barber)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)

Este projeto é um sistema de gerenciamento de agendamentos para barbearias, desenvolvido para a disciplina de **Banco de Dados** (2ª Nota) sob orientação do **Prof. [cite_start]Anderson Costa**[cite: 1, 3]. A aplicação integra uma interface web moderna com um banco de dados relacional robusto para controle de clientes, serviços e horários.

---

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Modelagem do Banco](#-modelagem-do-banco)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Executar](#-como-executar)
- [Demonstração](#-demonstração)
- [Vídeo](#-vídeo)

---

## 📝 Sobre o Projeto
[cite_start]O sistema tem como objetivo facilitar a gestão de uma barbearia, permitindo que administradores e barbeiros gerenciem fluxos de atendimento, enquanto garantem a integridade dos dados através de um SGBD relacional[cite: 8, 10].

## ✨ Funcionalidades (CRUD)
[cite_start]O sistema contempla todos os requisitos obrigatórios do edital[cite: 21]:
- [cite_start]**Autenticação:** Tela de login segura para acesso ao sistema[cite: 19].
- [cite_start]**Cadastro (Insert):** Inclusão de usuários, serviços e agendamentos[cite: 22].
- [cite_start]**Consulta (Select):** Listagem dinâmica com filtros e ordenação[cite: 25, 26].
- [cite_start]**Atualização (Update):** Edição de informações de registros existentes[cite: 23].
- [cite_start]**Exclusão (Delete):** Remoção de dados do sistema[cite: 24].
- [cite_start]**Relatórios:** Consultas complexas utilizando **INNER JOIN** e **LEFT JOIN**[cite: 27].

## 🗄️ Modelagem do Banco
[cite_start]O banco de dados foi modelado no **PostgreSQL** e possui 3 tabelas principais relacionadas[cite: 12, 41]:
- `usuarios`: Cadastro de clientes, barbeiros e admins.
- `servicos`: Tabela de procedimentos oferecidos.
- `agendamentos`: Tabela central que conecta clientes, barbeiros e serviços.

### Diagrama Entidade-Relacionamento (DER)
![Diagrama do Banco de Dados](./diagrama/Diagrama_ER.pdf) 

---

## 📁 Estrutura do Repositório
[cite_start]Conforme exigido nas normas do trabalho, o projeto está organizado da seguinte forma[cite: 32]:

| Pasta | Descrição |
| :--- | :--- |
| `/diagrama` | [cite_start]Imagem ou PDF do Diagrama Entidade-Relacionamento (DER)[cite: 33]. |
| `/ddl` | [cite_start]Script SQL de criação das tabelas e restrições (Primary/Foreign Keys)[cite: 34]. |
| `/dml` | [cite_start]Scripts SQL com exemplos de inserção (população de dados)[cite: 35]. |
| `/dql` | [cite_start]Scripts SQL com as consultas realizadas (Selects, Joins, Filtros)[cite: 36]. |
| `/src` | [cite_start]Código-fonte da aplicação desenvolvido em Python/Flask[cite: 37]. |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado.
- PostgreSQL rodando localmente.
- Biblioteca `psycopg2` ou `flask-sqlalchemy`.

### Passo a Passo
1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/JeytheJo/SistemaCRUD_Barbearia.git](https://github.com/JeytheJo/SistemaCRUD_Barbearia.git)
   
2. **Configure o Banco de Dados:**
   - Abra o seu **pgAdmin** ou **QueryTool**.
   - Execute o script contido em `/ddl/databasePGSQL.sql` para criar a estrutura de tabelas e restrições.
   - (Opcional) Execute os scripts em `/dml` para inserir dados de teste.

3. **Instale as dependências:**
   ```bash
   pip install flask psycopg2