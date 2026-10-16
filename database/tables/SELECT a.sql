 SELECT a.id,
    a.data_hora,
    a.status,
    a.observacoes,
    c.nome AS cliente,
    c.telefone AS cliente_telefone,
    b.nome AS barbeiro,
    s.nome AS servico,
    s.preco,
    s.duracao_min
   FROM (((agendamentos a
     JOIN usuarios c ON ((c.id = a.cliente_id)))
     JOIN usuarios b ON ((b.id = a.barbeiro_id)))
     JOIN servicos s ON ((s.id = a.servico_id)));
     
  