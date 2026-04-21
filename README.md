# 💈 Sistema de Agendamento - Barbearia (Bodies Barber)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)

Este projeto é um sistema de gerenciamento de agendamentos para barbearias, desenvolvido para a disciplina de **Banco de Dados** (2ª Nota) sob orientação do **Prof. Anderson Costa**. A aplicação integra uma interface web moderna com um banco de dados relacional robusto para controle de clientes, serviços e horários.

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
O sistema tem como objetivo facilitar a gestão de uma barbearia, permitindo que administradores e barbeiros gerenciem fluxos de atendimento, enquanto garantem a integridade dos dados através de um SGBD relacional.

## ✨ Funcionalidades (CRUD)
O sistema contempla todos os requisitos obrigatórios do edital:
- **Autenticação:** Tela de login segura para acesso ao sistema.
- **Cadastro (Insert):** Inclusão de usuários, serviços e agendamentos.
- **Consulta (Select):** Listagem dinâmica com filtros e ordenação.
- **Atualização (Update):** Edição de informações de registros existentes.
- **Exclusão (Delete):** Remoção de dados do sistema.
- **Relatórios:** Consultas complexas utilizando **INNER JOIN** e **LEFT JOIN**.

## 🗄️ Modelagem do Banco
O banco de dados foi modelado no **PostgreSQL** e possui 3 tabelas principais relacionadas:
- `usuarios`: Cadastro de clientes, barbeiros e admins.
- `servicos`: Tabela de procedimentos oferecidos.
- `agendamentos`: Tabela central que conecta clientes, barbeiros e serviços.

### Diagrama Entidade-Relacionamento (DER)
![Diagrama do Banco de Dados](./diagrama/Diagrama_ER.pdf) 

---

## 📁 Estrutura do Repositório
Conforme exigido nas normas do trabalho, o projeto está organizado da seguinte forma:

| Pasta | Descrição |
| :--- | :--- |
| `/diagrama` | Imagem ou PDF do Diagrama Entidade-Relacionamento (DER). |
| `/ddl` | Script SQL de criação das tabelas e restrições (Primary/Foreign Keys). |
| `/dml` | Scripts SQL com exemplos de inserção (população de dados). |
| `/dql` | Scripts SQL com as consultas realizadas (Selects, Joins, Filtros). |
| `/src` | Código-fonte da aplicação desenvolvido em Python/Flask. |

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
