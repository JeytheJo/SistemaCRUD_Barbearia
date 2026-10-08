-- SQLBook: Code
-- ============================================================
-- PROCEDURE: sp_confirmar_agendamento
-- Confirma um agendamento pendente pelo seu ID.
-- Só age se o status atual for 'pendente' (segurança extra).
-- ============================================================
-- EXECUTAR NO SUPABASE SQL EDITOR:

CREATE OR REPLACE PROCEDURE sp_confirmar_agendamento(p_id UUID)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE agendamentos
    SET status = 'confirmado'
    WHERE id = p_id
      AND status = 'pendente';
END;
$$;