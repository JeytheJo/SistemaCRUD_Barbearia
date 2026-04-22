-- Usuários
INSERT INTO usuarios (nome, email, senha_hash, role, telefone) VALUES
('Admin Teste', 'admin@bodies.com', encode(sha256('senha123'), 'hex'), 'admin', '(86) 99000-0000'),
('Carlos Barbeiro', 'carlos@bodies.com', encode(sha256('senha123'), 'hex'), 'barbeiro', '(86) 99999-0001'),
('João Cliente', 'joao@gmail.com', encode(sha256('senha123'), 'hex'), 'cliente', '(86) 98888-0001'),
('Maria Cliente', 'maria@gmail.com', encode(sha256('senha123'), 'hex'), 'cliente', '(86) 98888-0002');

-- Serviços
INSERT INTO servicos (nome, descricao, preco, duracao_min) VALUES
('Corte Degradê', 'Corte moderno com máquina', 35.00, 45),
('Barba Completa', 'Barba na navalha com toalha quente', 25.00, 30),
('Combo Corte + Barba', 'Corte degradê e barba completa', 55.00, 75);

-- Agendamentos
INSERT INTO agendamentos (cliente_id, barbeiro_id, servico_id, data_hora, status) VALUES
(
    (SELECT id FROM usuarios WHERE email = 'joao@gmail.com'),
    (SELECT id FROM usuarios WHERE email = 'carlos@bodies.com'),
    (SELECT id FROM servicos WHERE nome = 'Corte Degradê'),
    NOW() + INTERVAL '1 day',
    'confirmado'
),
(
    (SELECT id FROM usuarios WHERE email = 'maria@gmail.com'),
    (SELECT id FROM usuarios WHERE email = 'carlos@bodies.com'),
    (SELECT id FROM servicos WHERE nome = 'Combo Corte + Barba'),
    NOW() + INTERVAL '2 days',
    'pendente'
);

UPDATE agendamentos 
SET status = 'concluido' 
WHERE cliente_id = (SELECT id FROM usuarios WHERE email = 'joao@gmail.com');

DELETE FROM agendamentos 
WHERE status = 'cancelado';