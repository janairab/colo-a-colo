# Criar tabela Bebé
CREATE TABLE IF NOT EXISTS "bebe" (
	"id_bebe" INTEGER NOT NULL,
	"nome" VARCHAR NOT NULL,
	"data_nascimento" DATE NOT NULL,
	"sexo" VARCHAR NOT NULL,
	"id_cuidador" INTEGER NOT NULL,
	PRIMARY KEY("id_bebe"),
	FOREIGN KEY ("id_cuidador")
    REFERENCES "cuidador"("id_cuidador")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

# Criar tabela Cuidador
CREATE TABLE IF NOT EXISTS "cuidador" (
	"id_cuidador" INTEGER NOT NULL,
	"nome" VARCHAR NOT NULL,
	"email" VARCHAR NOT NULL UNIQUE,
	"data_nascimento" DATE NOT NULL,
	PRIMARY KEY("id_cuidador"),
	FOREIGN KEY ("id_cuidador") REFERENCES "bebe"("id_cuidador")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);


# Criar tabela registro_rotina
CREATE TABLE IF NOT EXISTS "registro_rotina" (
	"id_registro" INTEGER NOT NULL,
	"id_bebe" INTEGER NOT NULL,
	"tipo_registro" VARCHAR NOT NULL,
	"data_hora" DATETIME NOT NULL,
	"criado_em" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"notas" TEXT,
	PRIMARY KEY("id_registro"),
	FOREIGN KEY ("id_registro") REFERENCES "alimentacao"("id_registro")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id_registro") REFERENCES "fralda"("id_registro")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id_registro") REFERENCES "sono"("id_registro")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("id_registro") REFERENCES "banho"("id_registro")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

# Criar tabela alimentacao
CREATE TABLE IF NOT EXISTS "alimentacao" (
	"id_registro" INTEGER NOT NULL,
	"tipo_alimentacao" VARCHAR NOT NULL,
	"alimento" VARCHAR,
	"inicio_alimentacao" DATETIME,
	"fim_alimentacao" DATETIME,
	"quantidade" INTEGER,
	"ml_ou_gr" VARCHAR,
	"mama_lados" VARCHAR,
	"aceitacao" VARCHAR,
	"notas" TEXT,
	PRIMARY KEY ("id_registro"),
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);


# Criar tabela fralda
CREATE TABLE IF NOT EXISTS "fralda" (
	"id_registro" INTEGER NOT NULL,
	"miccao" VARCHAR,
	"coco" VARCHAR,
	"notas" TEXT,
	PRIMARY KEY ("id_registro"),
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);


# Criar tabela banho
CREATE TABLE IF NOT EXISTS "banho" (
	"id_registro" INTEGER NOT NULL,
	"notas" TEXT,
	PRIMARY KEY ("id_registro"),
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);

# Criar tabela sono
CREATE TABLE IF NOT EXISTS "sono" (
	"id_registro" INTEGER NOT NULL,
	"inicio_sono" DATETIME NOT NULL,
	"fim_sono" DATETIME,
	"notas" TEXT,
	PRIMARY KEY ("id_registro"),
	FOREIGN KEY ("id_registro")	
    REFERENCES "registro_rotina"("id_registro")
);
