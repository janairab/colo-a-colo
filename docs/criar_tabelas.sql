
-- =====================================================
-- PROJETO COLO A COLO
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS
-- =====================================================

-- Habilita a verificação das chaves estrangeiras
PRAGMA foreign_keys = ON;


-- =====================================================
-- TABELA CUIDADOR
-- Armazena os dados dos cuidadores cadastrados
-- =====================================================

CREATE TABLE IF NOT EXISTS cuidador (
    id_cuidador INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    password_hash TEXT NOT NULL
);


-- =====================================================
-- TABELA BEBE
-- Armazena os dados dos bebês cadastrados
-- Cada bebê pertence a um cuidador
-- =====================================================

CREATE TABLE IF NOT EXISTS bebe (
    id_bebe INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    id_cuidador INTEGER NOT NULL,

    -- Relaciona o bebê ao cuidador responsável
    FOREIGN KEY (id_cuidador)
        REFERENCES cuidador(id_cuidador)
);


-- =====================================================
-- TABELA REGISTRO_DIARIO
-- Armazena uma folha diária para cada bebê
-- Cada bebê pode ter apenas uma folha por data
-- =====================================================

CREATE TABLE IF NOT EXISTS registro_diario (
    id_registro_diario INTEGER PRIMARY KEY,
    id_bebe INTEGER NOT NULL,
    data DATE NOT NULL,

    -- Relaciona a folha diária ao bebê
    FOREIGN KEY (id_bebe)
        REFERENCES bebe(id_bebe)
);


-- Garante que não existam duas folhas para o mesmo
-- bebê na mesma data
CREATE UNIQUE INDEX IF NOT EXISTS uk_bebe_data
ON registro_diario(id_bebe, data);


-- =====================================================
-- TABELA ROTINA
-- Armazena os acontecimentos individuais da rotina
-- Cada acontecimento pertence a uma folha diária
-- =====================================================

CREATE TABLE IF NOT EXISTS rotina (
    id_rotina INTEGER PRIMARY KEY,
    id_registro_diario INTEGER NOT NULL,

    -- Identifica o tipo de acontecimento registrado
    tipo_registro VARCHAR(50) NOT NULL
        CHECK (tipo_registro IN (
            'alimentacao',
            'sono',
            'banho',
            'fralda'
        )),

    -- Armazena a data e a hora de início do acontecimento
    data_hora DATETIME NOT NULL,

    -- Armazena automaticamente a data e a hora da criação
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Relaciona o acontecimento à folha diária
    FOREIGN KEY (id_registro_diario)
        REFERENCES registro_diario(id_registro_diario)
);


-- Facilita a consulta dos acontecimentos de cada folha
CREATE INDEX IF NOT EXISTS idx_rotina_registro_diario
ON rotina(id_registro_diario);


-- =====================================================
-- TABELA ALIMENTACAO
-- Armazena os detalhes dos registros de alimentação
-- =====================================================

CREATE TABLE IF NOT EXISTS alimentacao (
    id_rotina INTEGER PRIMARY KEY,

    -- Identifica o tipo de alimentação
    tipo_alimentacao VARCHAR(50) NOT NULL
        CHECK (tipo_alimentacao IN (
            'amamentacao',
            'mamadeira',
            'solidos'
        )),

    -- Armazena o alimento, quando aplicável
    -- Na amamentação, esse campo permanece NULL
    alimento VARCHAR(150),

    -- Armazena a data e a hora do término da amamentação
    -- Permite NULL enquanto a amamentação não foi encerrada
    fim_amamentacao DATETIME,

    -- Armazena a quantidade ingerida
    -- Deve ser maior que zero quando preenchida
    quantidade REAL
        CHECK (quantidade > 0),

    -- Identifica a unidade da quantidade
    -- ml para líquidos e g para alimentos sólidos
    ml_ou_g VARCHAR(10)
        CHECK (ml_ou_g IN ('ml', 'g')),

    -- Identifica o lado utilizado na amamentação
    mama_lados VARCHAR(10)
        CHECK (mama_lados IN (
            'esquerda',
            'direita',
            'ambas'
        )),

    -- Identifica o nível de aceitação da alimentação
    aceitacao VARCHAR(20)
        CHECK (aceitacao IN (
            'tudo',
            'suficiente',
            'pouco'
        )),

    -- Armazena observações sobre a alimentação
    notas TEXT,

    -- Relaciona os detalhes ao acontecimento da rotina
    FOREIGN KEY (id_rotina)
        REFERENCES rotina(id_rotina)
);


-- =====================================================
-- TABELA SONO
-- Armazena os detalhes dos registros de sono
-- O início do sono fica armazenado em rotina.data_hora
-- =====================================================

CREATE TABLE IF NOT EXISTS sono (
    id_rotina INTEGER PRIMARY KEY,

    -- Armazena a data e a hora em que o sono terminou
    -- Permite NULL enquanto o bebê continua dormindo
    fim_sono DATETIME,

    -- Armazena observações sobre o sono
    notas TEXT,

    -- Relaciona os detalhes ao acontecimento da rotina
    FOREIGN KEY (id_rotina)
        REFERENCES rotina(id_rotina)
);


-- =====================================================
-- TABELA BANHO
-- Armazena os detalhes dos registros de banho
-- =====================================================

CREATE TABLE IF NOT EXISTS banho (
    id_rotina INTEGER PRIMARY KEY,

    -- Armazena observações sobre o banho
    notas TEXT,

    -- Relaciona os detalhes ao acontecimento da rotina
    FOREIGN KEY (id_rotina)
        REFERENCES rotina(id_rotina)
);


-- =====================================================
-- TABELA FRALDA
-- Armazena os detalhes das trocas de fralda
-- Permite registrar xixi, cocô ou ambos
-- =====================================================

CREATE TABLE IF NOT EXISTS fralda (
    id_rotina INTEGER PRIMARY KEY,

    -- Indica se houve xixi
    -- 0 = não e 1 = sim
    xixi INTEGER NOT NULL DEFAULT 0
        CHECK (xixi IN (0, 1)),

    -- Indica se houve cocô
    -- 0 = não e 1 = sim
    coco INTEGER NOT NULL DEFAULT 0
        CHECK (coco IN (0, 1)),

    -- Armazena observações sobre a troca de fralda
    notas TEXT,

    -- Impede o registro de uma troca sem nenhuma eliminação
    CHECK (xixi = 1 OR coco = 1),

    -- Relaciona os detalhes ao acontecimento da rotina
    FOREIGN KEY (id_rotina)
        REFERENCES rotina(id_rotina)
);
