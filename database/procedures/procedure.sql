-- SQLBook: Code


CREATE OR REPLACE PROCEDURE sp_confirmar_agendamento(p_id UUID)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE agendamentos
    SET status = 'confirmado'
    WHERE id = p_id
      AND status = 'pendente';
END;
$$;