import sqlite3

def criar_tabela():
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS "usuarios" (
        "id_usuario" INTEGER NOT NULL UNIQUE,
        "nome" VARCHAR(100) NOT NULL,
        "email" VARCHAR(150) NOT NULL UNIQUE,
        "cpf" INTEGER NOT NULL UNIQUE,
        "senha" VARCHAR(25) NOT NULL,
        "tipo" INTEGER NOT NULL,
        PRIMARY KEY("id_usuario")
    );

    CREATE TABLE IF NOT EXISTS "cursos" (
        "id_curso" INTEGER NOT NULL UNIQUE,
        "nome" VARCHAR(150) NOT NULL,
        "horario" INTEGER NOT NULL,
        PRIMARY KEY("id_curso")
    );

    CREATE TABLE IF NOT EXISTS "usuario_curso" (
        "id_usuario" INTEGER NOT NULL,
        "id_curso" INTEGER NOT NULL,
        FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_curso") REFERENCES "cursos"("id_curso")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "atividades" (
        "id_atividade" INTEGER NOT NULL UNIQUE,
        "questao" TEXT NOT NULL,
        "A" VARCHAR NOT NULL,
        "B" VARCHAR NOT NULL,
        "C" VARCHAR NOT NULL,
        "D" VARCHAR NOT NULL,
		"dica" VARCHAR NOT NULL,
        "gabarito" VARCHAR(1) NOT NULL,
        "id_curso" INTEGER NOT NULL,
        PRIMARY KEY("id_atividade"),
        FOREIGN KEY ("id_curso") REFERENCES "cursos"("id_curso")
        ON UPDATE NO ACTION ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS "usuario_atividade" (
        "id_usuario" INTEGER NOT NULL,
        "id_atividade" INTEGER NOT NULL,
        "data" DATE NOT NULL DEFAULT CURRENT_DATE,
        "acerto" BOOLEAN NOT NULL DEFAULT 0,
		"status" BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY ("id_usuario") REFERENCES "usuarios"("id_usuario")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
        FOREIGN KEY ("id_atividade") REFERENCES "atividades"("id_atividade")
        ON UPDATE NO ACTION ON DELETE CASCADE
    );

	INSERT OR IGNORE INTO usuarios (nome,email,cpf,senha,tipo)
    VALUES ('Admin','coordenacao@escola.br',12345678900,'Adm@8900',2);

    """)

    conexao.commit()
    conexao.close()
