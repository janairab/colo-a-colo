-- database: ../data/colo_a_colo.db

--Teste Amamentação, confirmar no SQL
SELECT
    r.id_registro,
    r.id_bebe,
    r.tipo_registro,
    r.data_hora,
    a.tipo_alimentacao,
    a.mama_lados,
    a.fim_amamentacao,
    a.notas
FROM registro_rotina r
INNER JOIN alimentacao a
    ON r.id_registro = a.id_registro
WHERE r.id_registro = 1;

-----------------------------------------------

-- Teste Mamadeira, confirmar no SQL
SELECT
    r.id_registro,
    r.id_bebe,
    r.tipo_registro,
    r.data_hora,
    a.tipo_alimentacao,
    a.alimento,
    a.quantidade,
    a.ml_ou_g,
    a.notas
FROM registro_rotina r
INNER JOIN alimentacao a
    ON r.id_registro = a.id_registro
WHERE r.id_registro = 2;

    -- r.id_registro - 2
    -- r.id_bebe - 1
    -- r.tipo_registro - alimentacao
    -- r.data_hora - 2026-11-09 09:01:00
    -- a.tipo_alimentacao - mamadeira
    -- a.alimento - leite_materno
    -- a.quantidade - 100
    -- a.ml_ou_g - ml
    -- a.notas - NULL
    
--------------------------------------------------

-- Teste Sólidos, confirmar no SQL

SELECT
    r.id_registro,
    r.id_bebe,
    r.tipo_registro,
    r.data_hora,
    a.tipo_alimentacao,
    a.alimento,
    a.quantidade,
    a.ml_ou_g,
    a.aceitacao,
    a.notas
FROM registro_rotina r
INNER JOIN alimentacao a
    ON r.id_registro = a.id_registro
WHERE r.id_registro = 3;


---------------------------------------------------

-- Confirmar os testes no SQL
SELECT
    r.id_registro,
    r.tipo_registro,
    r.data_hora,
    a.tipo_alimentacao,
    a.alimento,
    a.quantidade,
    a.ml_ou_g,
    a.mama_lados,
    a.aceitacao,
    a.notas
FROM registro_rotina r
INNER JOIN alimentacao a
    ON r.id_registro = a.id_registro
ORDER BY r.id_registro;