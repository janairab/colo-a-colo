/* Criar tabela Cuidador */
CREATE TABLE IF NOT EXISTS "cuidador" (
	"id_cuidador" INTEGER PRIMARY KEY,
	"nome" VARCHAR NOT NULL,
	"email" VARCHAR NOT NULL UNIQUE,
	"data_nascimento" DATE NOT NULL
);

/* Criar tabela Bebé */
CREATE TABLE IF NOT EXISTS "bebe" (
	"id_bebe" INTEGER PRIMARY KEY,
	"nome" VARCHAR NOT NULL,
	"data_nascimento" DATE NOT NULL,
	"sexo" VARCHAR NOT NULL,
	"id_cuidador" INTEGER NOT NULL,
	FOREIGN KEY ("id_cuidador")
    REFERENCES "cuidador"("id_cuidador")
);

/* Criar tabela registro_rotina */
CREATE TABLE IF NOT EXISTS "registro_rotina" (
	"id_registro" INTEGER PRIMARY KEY,
	"id_bebe" INTEGER NOT NULL,
	"tipo_registro" VARCHAR NOT NULL,
	"data_hora" DATETIME NOT NULL,
	"criado_em" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"notas" TEXT,
	FOREIGN KEY ("id_bebe")
    REFERENCES "bebe"("id_bebe")	
);

/* Criar tabela alimentacao */
CREATE TABLE IF NOT EXISTS "alimentacao" (
	"id_registro" INTEGER PRIMARY KEY,
	"tipo_alimentacao" VARCHAR NOT NULL,
	"alimento" VARCHAR,
	"inicio_alimentacao" DATETIME,
	"fim_alimentacao" DATETIME,
	"quantidade" INTEGER,
	"ml_ou_g" VARCHAR,
	"mama_lados" VARCHAR,
	"aceitacao" VARCHAR,
	"notas" TEXT,
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);


/* Criar tabela fralda */
CREATE TABLE IF NOT EXISTS "fralda" (
	"id_registro" INTEGER PRIMARY KEY,
	"miccao" VARCHAR,
	"coco" VARCHAR,
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
	"inicio_sono" DATETIME NOT NULL,
	"fim_sono" DATETIME,
	"notas" TEXT,
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);