-- Habilita a geração automática de UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de Usuários (Clientes e Barbeiros)
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- Conforme seu diagrama [cite: 72]
    nome VARCHAR(150) NOT NULL, -- [cite: 80]
    email VARCHAR(100) UNIQUE NOT NULL, -- [cite: 81]
    senha_hash VARCHAR(255) NOT NULL, -- [cite: 82]
    role VARCHAR(20) NOT NULL CHECK (role IN ('cliente', 'barbeiro', 'admin')), -- Enum do diagrama [cite: 88]
    telefone VARCHAR(20), -- [cite: 84]
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- [cite: 85]
);


-- Tabela de Serviços
CREATE TABLE servicos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- [cite: 94]
    nome VARCHAR(150) NOT NULL, -- [cite: 95]
    descricao TEXT, -- [cite: 102]
    preco DECIMAL(8,2) NOT NULL, -- [cite: 103, 106]
    duracao_min INTEGER NOT NULL, -- [cite: 104, 107]
    ativo BOOLEAN DEFAULT TRUE NOT NULL -- [cite: 105, 108]
);

-- Tabela de Agendamentos (Tabela central que faz os JOINs)
CREATE TABLE agendamentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- [cite: 115]
    
    -- Chaves Estrangeiras ligando as tabelas [cite: 116, 118, 120]
    cliente_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE, -- [cite: 109, 117]
    barbeiro_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE, -- [cite: 110, 119]
    servico_id UUID NOT NULL REFERENCES servicos(id) ON DELETE CASCADE, -- [cite: 111, 121]
    
    data_hora TIMESTAMP NOT NULL, -- [cite: 127]
    status VARCHAR(30) NOT NULL DEFAULT 'pendente' 
        CHECK (status IN ('pendente', 'confirmado', 'concluido', 'cancelado')), -- Enum do diagrama [cite: 130]
    observacoes TEXT, -- [cite: 132]
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- [cite: 134]
);

INSERT INTO usuarios (nome, email, senha_hash, role)
VALUES (
    'Admin Teste',
    'admin@bodies.com',
    encode(sha256('senha123'), 'hex'),
    'admin'
);
