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

	INSERT OR IGNORE INTO usuarios (nome,email,cpf,senha,tipo)
    VALUES ('Ana Beatriz Ferreira', 'ana.ferreira@email.com.br', 52981734600,'Ana@4600',1),
('Carlos Eduardo Mendes', 'carlos.mendes@outlook.com', 38746195211,'Car@5211',0),
('Fernanda Lima Oliveira', 'fernanda.lima@gmail.com', 74125896322,'Fer@6322',1),
('Gustavo Henrique Souza', 'gustavo.souza@yahoo.com.br', 15935748633,'Gus@8633',2),
('Isabela Cristina Rocha', 'isabela.rocha@hotmail.com', 86420957144,'Isa@7144',0),
('João Pedro Almeida', 'joao.almeida@empresa.com', 24681357955,'Joa@7955',0),
('Larissa Manoela Costa', 'larissa.costa@provedor.net', 95175385266,'Lar@5266',0),
('Marcelo Augusto Dias', 'marcelo.dias@corporativo.br', 35795145677,'Mar@5677',0),
('Natália Regina Borges', 'natalia.borges@mail.com', 64209813488,'Nat@3488',0),
('Ricardo Antônio Nunes', 'ricardo.nunes@servidor.org', 13579246899,'Ric@6899',0);

	INSERT OR IGNORE INTO cursos (nome,horario)
    VALUES ('Programação',1),('Arquitetura',0);

	INSERT OR IGNORE INTO  usuario_curso(id_usuario,id_curso)
    VALUES (2,1), (4,2), (3,1),(6,1),(7,2),(3,2),(8,1),(9,2),(10,2),(11,1);

    INSERT OR IGNORE INTO  atividades (questao,a,b,c,d,dica,gabarito,id_curso)
    VALUES ('Em uma padaria, o padeiro fez 20 paezinhos para o café de manhã. E buscando por ingredientes, encontrou mais 4 pãezinhos do dia anterior, que decidiu juntar com os demais para vender na manhã. Quantos pãezinhos ele tinha disponível para venda naquele momento?','20','22','23','24','Cálculo Básico','d',1);

    INSERT OR IGNORE INTO atividades (questao,a,b,c,d,dica,gabarito,id_curso)
    VALUES ('20+2?','20','22','23','24','Cálculo Básico','b',1);

	INSERT OR IGNORE INTO atividades (questao,a,b,c,d,dica,gabarito,id_curso)
    VALUES ('O Joãozinho tem 18 anos. Durante uma entrevista de emprego, questionaram como seria o seu futuro em 5 anos? Daqui a 5 anos, quantos anos Joãozinho teria?','20','22','23','24','Cálculo Básico','c',1);

  	INSERT OR IGNORE INTO atividades (questao,a,b,c,d,dica,gabarito,id_curso)
    VALUES ('Quantos centímetros tem uma porta residencial?','210','220','238','240','Média brasileira de altura','a',2);

	INSERT OR IGNORE INTO atividades (questao,a,b,c,d,dica,gabarito,id_curso)
    VALUES ('Quantos metros cúbicos tem um hectare?','20.000','36.000','10.000','40.000','Cálculo Básico','c',2);

    INSERT OR IGNORE INTO atividades (questao,a,b,c,d,dica,gabarito,id_curso)
    VALUES ('25+2?','25','28','27','26','Cálculo Básico','c',2);

    INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (3,1,'2026-02-10',1,1);

   	INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (3,2,'2026-02-10',1,1);

    INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (3,3,'2026-02-10',0,1);

	INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (7,4,'2026-02-10',1,1);

	INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (3,5,'2026-02-10',0,1);

    INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (6,2,'2026-02-10',1,1);

    INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (6,3,'2026-02-10',1,1);

    INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (6,1,'2026-02-10',1,1);

    INSERT OR IGNORE INTO usuario_atividade (id_usuario,id_atividade,data,acerto,status)
    VALUES (7,5,'2026-02-10',0,1);

    """)

    conexao.commit()
    conexao.close()
