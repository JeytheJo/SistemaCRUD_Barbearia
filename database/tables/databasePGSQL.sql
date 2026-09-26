-- Habilita a geração automática de UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de Usuários (Clientes e Barbeiros)
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('cliente', 'barbeiro', 'admin')),
    telefone VARCHAR(20),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabela de Serviços
CREATE TABLE servicos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco DECIMAL(8,2) NOT NULL,
    duracao_min INTEGER NOT NULL,
    ativo BOOLEAN DEFAULT TRUE NOT NULL
);

-- Tabela de Agendamentos
CREATE TABLE agendamentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    barbeiro_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    servico_id UUID NOT NULL REFERENCES servicos(id) ON DELETE CASCADE,
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'pendente'
        CHECK (status IN ('pendente', 'confirmado', 'concluido', 'cancelado')),
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Usuários iniciais para teste
INSERT INTO usuarios (nome, email, senha_hash, role) VALUES
('Admin Teste', 'admin@bodies.com', encode(sha256('senha123'), 'hex'), 'admin');

INSERT INTO usuarios (nome, email, senha_hash, role, telefone) VALUES
('Carlos Barbeiro', 'carlos@bodies.com', encode(sha256('senha123'), 'hex'), 'barbeiro', '(86) 99999-0001');

INSERT INTO servicos (nome, descricao, preco, duracao_min) VALUES
('Corte Degradê', 'Corte moderno com máquina', 35.00, 45),
('Barba Completa', 'Barba na navalha com toalha quente', 25.00, 30),
('Combo Corte + Barba', 'Corte degradê e barba completa', 55.00, 75);