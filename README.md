# Sistema de Agendamento para Barbearia - 2ª Nota

Este repositório apresenta o projeto prático da disciplina de Banco de Dados (2ª Nota), cujo objetivo é demonstrar a integração de uma aplicação Python com um banco de dados relacional PostgreSQL, realizando operações de CRUD e consultas complexas com JOIN.

---

## 📌 Sobre o Projeto

O sistema **Bodies Barber** permite o gerenciamento de clientes, barbeiros, serviços e agendamentos, tudo através de uma interface web com autenticação de usuários.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Banco de Dados:** PostgreSQL
- **Driver de Conexão:** `psycopg2`
- **Framework Web:** Flask
- **Interface:** Web (Flask + HTML/CSS) — *Interface Gráfica (Bônus +1,0 ponto)*
- **Containerização:** Docker + Docker Compose

---

## 📂 Estrutura do Repositório

Organização das pastas conforme exigências da disciplina:

```
├── diagrama   # Modelo Entidade-Relacionamento (DER)
├── ddl        # Scripts de criação (CREATE TABLE, Constraints, PKs e FKs)
├── dml        # Scripts de manipulação (INSERT, UPDATE, DELETE)
├── dql        # Scripts de consulta (SELECT, JOINs, Filtros, Ordenação)
└── src        # Código-fonte da aplicação Python/Flask
```

---

## 📸 Demonstração

**1. Tela de Login**

![Login](./docs/login.png)

**2. Menu Principal e Operações CRUD**

![Dashboard](./docs/dashboard.png)

**3. Consulta Complexa (Inner/Left Join)**

![Agendamentos](./docs/agendamentos.png)

---

## 📺 Vídeo Demonstrativo

Assista à explicação detalhada do sistema e do código:

👉 [ASSISTIR VÍDEO NO DRIVE](https://drive.google.com/file/d/1uxiMJJlk_rlrPU8ZC60f0ZPfR79aiIlz/view?usp=sharing)

---

## 🚀 Como Executar o Projeto

### 1. Com Docker (Recomendado)

**Pré-requisitos:** Docker e Docker Compose instalados.

1. Clone o repositório:
   ```bash
   git clone https://github.com/JeytheJo/SistemaCRUD_Barbearia.git
   cd SistemaCRUD_Barbearia
   ```
2. Suba os containers:
   ```bash
   docker compose up --build
   ```
3. Acesse em **http://localhost:5000**

> O banco de dados é criado e populado automaticamente na primeira execução.

---

### 2. Execução Local (Sem Docker)

**Pré-requisitos:** Python 3.10+ e PostgreSQL rodando localmente.

1. Configure o banco de dados:
   - Execute o script em `/ddl/databasePGSQL.sql`.
   - (Opcional) Popule com `/dml/inserts.sql`.
2. Dentro de `/src`, crie um arquivo `.env` com as credenciais do banco:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=CRUD_Barbearia
   DB_USER=postgres
   DB_PASSWORD=minha_senha_segura
   ```
3. Instale as dependências:
   ```bash
   pip install flask psycopg2-binary python-dotenv
   ```
4. Execute o sistema:
   ```bash
   cd src
   python app.py
   ```
5. Acesse em **http://127.0.0.1:5000**

---

### 👤 Credenciais de Teste

| E-mail               | Senha     | Perfil    |
|----------------------|-----------|-----------|
| admin@bodies.com     | senha123  | admin     |
| carlos@bodies.com    | senha123  | barbeiro  |

---

## 📄 Regras de Negócio e Consultas Complexas

O sistema realiza consultas complexas para exibir dados integrados das tabelas:

- **INNER JOIN:** Lista agendamentos com nome do cliente, barbeiro e serviço (apenas agendamentos com todos os vínculos válidos).
- **LEFT JOIN:** Lista todos os barbeiros e clientes com o total de agendamentos (inclui quem não possui nenhum agendamento).

---

## 👤 Autor

- **João Eduardo** — [@JeytheJo](https://github.com/JeytheJo)
- Centro Universitário Santo Agostinho (UNIFSA)
- Disciplina: Banco de Dados — Prof. Anderson Costa — [andersoncosta@unifsa.com.br](mailto:andersoncosta@unifsa.com.br)
