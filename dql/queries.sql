SELECT 
    a.id,
    a.data_hora,
    a.status,
    a.observacoes,
    c.nome AS cliente,
    b.nome AS barbeiro,
    s.nome AS servico,
    s.preco
FROM agendamentos a
INNER JOIN usuarios c ON c.id = a.cliente_id
INNER JOIN usuarios b ON b.id = a.barbeiro_id
INNER JOIN servicos s ON s.id = a.servico_id
ORDER BY a.data_hora DESC;

SELECT 
    u.nome AS barbeiro,
    u.email,
    u.telefone,
    COUNT(a.id) AS total_atendimentos
FROM usuarios u
LEFT JOIN agendamentos a ON a.barbeiro_id = u.id
WHERE u.role = 'barbeiro'
GROUP BY u.id, u.nome, u.email, u.telefone
ORDER BY total_atendimentos DESC;

SELECT 
    u.nome AS cliente,
    u.email,
    COUNT(a.id) AS total_agendamentos
FROM usuarios u
LEFT JOIN agendamentos a ON a.cliente_id = u.id
WHERE u.role = 'cliente'
GROUP BY u.id, u.nome, u.email
ORDER BY total_agendamentos DESC;

-- Filtro por status
SELECT 
    c.nome AS cliente,
    b.nome AS barbeiro,
    s.nome AS servico,
    a.data_hora,
    a.status
FROM agendamentos a
INNER JOIN usuarios c ON c.id = a.cliente_id
INNER JOIN usuarios b ON b.id = a.barbeiro_id
INNER JOIN servicos s ON s.id = a.servico_id
WHERE a.status = 'pendente'
ORDER BY a.data_hora ASC;

-- Ordenação por data
SELECT 
    c.nome AS cliente,
    s.nome AS servico,
    a.data_hora
FROM agendamentos a
INNER JOIN usuarios c ON c.id = a.cliente_id
INNER JOIN servicos s ON s.id = a.servico_id
ORDER BY a.data_hora ASC;