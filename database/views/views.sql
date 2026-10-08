-- SQLBook: Code

CREATE OR REPLACE VIEW vw_agendamentos_completos AS
SELECT
    a.id,
    a.data_hora,
    a.status,
    a.observacoes,
    -- Cliente
    c.id        AS cliente_id,
    c.nome      AS cliente,
    c.telefone  AS cliente_telefone,
    -- Barbeiro
    b.id        AS barbeiro_id,
    b.nome      AS barbeiro,
    -- Serviço
    s.id        AS servico_id,
    s.nome      AS servico,
    s.preco,
    s.duracao_min

FROM agendamentos a
INNER JOIN usuarios c ON c.id = a.cliente_id
INNER JOIN usuarios b ON b.id = a.barbeiro_id
INNER JOIN servicos s  ON s.id = a.servico_id;
-- SQLBook: Code
SELECT * FROM vw_agendamentos_completos;