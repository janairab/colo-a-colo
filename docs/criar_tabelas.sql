/* Criar tabela Cuidador */
CREATE TABLE IF NOT EXISTS "cuidador" (
	"id_cuidador" INTEGER PRIMARY KEY,
	"nome" VARCHAR(50) NOT NULL,
	"email" VARCHAR(50) NOT NULL UNIQUE,
	"data_nascimento" DATE NOT NULL,
	"password_hash" TEXT NOT NULL
);

/* Criar tabela Bebé */
CREATE TABLE IF NOT EXISTS "bebe" (
	"id_bebe" INTEGER PRIMARY KEY,
	"nome" VARCHAR(50) NOT NULL,
	"data_nascimento" DATE NOT NULL,
	"sexo" VARCHAR(20) NOT NULL,
	"id_cuidador" INTEGER NOT NULL,
	FOREIGN KEY ("id_cuidador")
    REFERENCES "cuidador"("id_cuidador")
);

/* Criar tabela registro_rotina */
CREATE TABLE IF NOT EXISTS "registro_rotina" (
	"id_registro" INTEGER PRIMARY KEY,
	"id_bebe" INTEGER NOT NULL,
	"tipo_registro" VARCHAR(50) NOT NULL
	CHECK (tipo_registro IN (
    'alimentacao',
    'sono',
    'banho',
    'fralda'
	)),
	"data_hora" DATETIME NOT NULL,
	"criado_em" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"notas" TEXT,
	FOREIGN KEY ("id_bebe")
    REFERENCES "bebe"("id_bebe")	
);

/* Criar tabela alimentacao */
CREATE TABLE IF NOT EXISTS "alimentacao" (
	"id_registro" INTEGER PRIMARY KEY,
	"tipo_alimentacao" VARCHAR(50) NOT NULL
	CHECK (tipo_alimentacao IN (
    'amamentacao',
    'mamadeira',
    'solidos'
	)),
	"alimento" VARCHAR(150),
	"fim_amamentacao" DATETIME,
	"quantidade" REAL
	CHECK (quantidade > 0),
	"ml_ou_g" VARCHAR(10)
	CHECK (ml_ou_g IN ('ml', 'g')),
	"mama_lados" VARCHAR(10),
	"aceitacao" VARCHAR(20),
	"notas" TEXT,
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);


/* Criar tabela fralda */
CREATE TABLE IF NOT EXISTS "fralda" (
	"id_registro" INTEGER PRIMARY KEY,
	"miccao" VARCHAR(25),
	"coco" VARCHAR(25),
	"notas" TEXT,
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);


/* Criar tabela banho*/
CREATE TABLE IF NOT EXISTS "banho" (
	"id_registro" INTEGER PRIMARY KEY,
	"notas" TEXT,
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);

/* Criar tabela sono */
CREATE TABLE IF NOT EXISTS "sono" (
	"id_registro" INTEGER PRIMARY KEY,
	"fim_sono" DATETIME,
	"notas" TEXT,
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);