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

    -- Resultado:
    -- r.id_registro - 1
    -- r.id_bebe - 1
    -- r.tipo_registro - alimentacao
    -- r.data_hora - 2026-11-09 08:22:00
    -- a.tipo_alimentacao - amamentacao
    -- a.mama_lados - esquerda
    -- a.fim_amamentacao - NULL
    -- a.notas - NULL

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

    -- Resultado:
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

    -- Resultado:

    -- r.id_registro - 3
    -- r.id_bebe - 1
    -- r.tipo_registro - alimentacao
    -- r.data_hora - 2026-11-09 09:12:00
    -- a.tipo_alimentacao - solidos
    -- a.alimento - Sopa de Legumes
    -- a.quantidade - 100
    -- a.ml_ou_g - g
    -- a.aceitacao - tudo
    -- a.nota - Comeu bem e aceitou todos os alimentos
  
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

-- RESULTADO 1 — AMAMENTAÇÃO
-- r.id_registro       = 1
-- r.tipo_registro     = alimentacao
-- r.data_hora         = 2026-11-09 08:22:00
-- a.tipo_alimentacao  = amamentacao
-- a.alimento          = NULL
-- a.quantidade        = NULL
-- a.ml_ou_g           = NULL
-- a.mama_lados        = esquerda
-- a.aceitacao         = NULL
-- a.nota              = NULL


-- RESULTADO 2 — MAMADEIRA
-- r.id_registro       = 2
-- r.tipo_registro     = alimentacao
-- r.data_hora         = 2026-11-09 09:01:00
-- a.tipo_alimentacao  = mamadeira
-- a.alimento          = leite_materno
-- a.quantidade        = 100
-- a.ml_ou_g           = ml
-- a.mama_lados        = NULL
-- a.aceitacao         = NULL
-- a.nota              = NULL


-- RESULTADO 3 — SÓLIDOS
-- r.id_registro       = 3
-- r.tipo_registro     = alimentacao
-- r.data_hora         = 2026-11-09 09:12:00
-- a.tipo_alimentacao  = solidos
-- a.alimento          = Sopa de Legumes
-- a.quantidade        = 100
-- a.ml_ou_g           = g
-- a.mama_lados        = NULL
-- a.aceitacao         = tudo
-- a.nota              = Comeu bem e aceitou todos os alimentos