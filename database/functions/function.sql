-- SQLBook: Code
CREATE OR REPLACE FUNCTION fn_faturamento_barbeiro(p_barbeiro_id UUID)
RETURNS DECIMAL AS $$
DECLARE
    total DECIMAL;
BEGIN
    SELECT COALESCE(SUM(s.preco), 0)
    INTO total
    FROM agendamentos a
    JOIN servicos s ON s.id = a.servico_id
    WHERE a.barbeiro_id = p_barbeiro_id
      AND a.status = 'concluido';

    RETURN total;
END;
$$ LANGUAGE plpgsql;
-- SQLBook: Code
SELECT id, nome FROM usuarios WHERE role = 'barbeiro';
-- SQLBook: Code
SELECT fn_faturamento_barbeiro('f2def3c3-ffc3-4950-8fcd-d9ba578d9bd6');