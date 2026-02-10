import sqlite3

def adicionar_atividade(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nPara adicionar uma atividade múltipla escolha preencha as informações a seguir: ")
	questao = input(f"\nDigite o texto da questão: ")
	a = input(f"\nPreencha as informações da alternativa A: ")
	b = input(f"\nPreencha as informações da alternativa B: ")
	c = input(f"\nPreencha as informações da alternativa C: ")
	d = input(f"\nPreencha as informações da alternativa D: ")
	dica = input(f"\nDigite uma dica para a atividade: ")
	gabarito = input(f"\nQual a respota da atividade? \nA \nB \nC \nD \n>").lower().strip()
	if len(gabarito)==1:
		lista = ['a','b','c','d']
		if gabarito in lista:
			cursor.execute("INSERT INTO atividades (questao,A,B,C,D,dica,gabarito,id_curso) VALUES (?,?,?,?,?,?,?,?)", (questao,a,b,c,d,dica,gabarito,curso))
			conexao.commit()
			conexao.close()
			return print(f"\nAtividade adicionada a lista com sucesso.")
		else:
			return print(f"\nA letra digitada não referencia nenhuma das alternativas possíveis")
	else:
		return print("Apenas letras de A a D são escolhas possíveis.")
	
def listar_atividades(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nLista de todas as atividades do curso: ")
	atividades = []
	cursor.execute('''
	SELECT c.nome,
    	   a.id_atividade,
           SUBSTR(a.questao,1,50)
    FROM atividades a
    INNER JOIN cursos c ON a.id_curso = c.id_curso
    WHERE c.id_curso = ?;
	''', (curso,))
	resultados = cursor.fetchall()
	lugar=1
	for item in resultados:
		atividades.append(item[1])
		print(f"\n{item[0]} \nAtividade {lugar}: {item[2]}...")
		lugar+=1
	conexao.close()
	return atividades

def escolher_atividade(atividades):
	escolha = input("\nQual das atividades gostaria de selecionar? ")
	if escolha.isdigit():
		opcao = int(escolha)-1
		if opcao in range(len(atividades)):
			resultado = atividades[opcao]
			return resultado
		else:
			print(f"\nO número inserido não referencia nenhuma atividade selecionada")
	else:
		print(f"\nApenas números são escolhar possíveis.")
		

def mostrar_atividade(atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    SELECT a.questao,
    	   a.a,
           a.b,
           a.c,
           a.d
    FROM atividades a
    WHERE a.id_atividade = ?;
	''', (atividade,))
	resultados = cursor.fetchall()
	for item in resultados:
		print(f"\nAtividade \n{item[0]} \n\na){item[1]} \n\nb){item[2]} \n\nc){item[3]} \n\nd){item[4]}")
	conexao.close()

def pedir_dica(atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    SELECT a.dica
    FROM atividades a
    WHERE a.id_atividade = ?;
''', (atividade,))
	resultado = cursor.fetchone()
	for item in resultado:
		print(f"\nDica: {item}")
	conexao.close()

def realizar_atividade(cpf,atividade,resposta):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	if atividade_feita(cpf,atividade):
		return repetir_atividade(cpf,atividade,resposta)
	cursor.execute('''
    SELECT a.gabarito
    FROM atividades a
    WHERE a.id_atividade = ?;
				''',(atividade,))
	gabarito = cursor.fetchone()
	if resposta in gabarito:
		cursor.execute(''' INSERT INTO usuario_atividade (id_usuario,id_atividade,acerto,status)
VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),?,?,?)''', (cpf,atividade,1,1))
		conexao.commit()
		conexao.close()
		return print(f"\nResposta Correta. Parabéns.")
	else:
		cursor.execute(''' INSERT INTO usuario_atividade (id_usuario,id_atividade,acerto,status)
VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),?,?,?)''', (cpf,atividade,0,1))
		conexao.commit()
		conexao.close()
		return print(f"\nResposta Incorreta. Sinto Muito.")

def atividade_feita(cpf,atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
	SELECT 1 FROM usuario_atividade ua
    INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
    WHERE ua.id_usuario =(CASE WHEN u.cpf = ? THEN u.id_usuario END) AND ua.id_atividade = ?;
	''', (cpf,atividade,))
	check_cpf = cursor.fetchone()
	conexao.close()
	return check_cpf is not None

def repetir_atividade(cpf,atividade,resposta):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''
    UPDATE usuario_atividade
    SET status = 1
    FROM usuarios
    WHERE usuario_atividade.id_atividade = ? AND usuario_atividade.id_usuario=(CASE WHEN usuarios.cpf = ? THEN usuarios.id_usuario END);
	''',(atividade,cpf,))
	conexao.commit()

	cursor.execute('''
	SELECT a.gabarito
    FROM atividades a
    WHERE a.id_atividade = ?;
	''', (atividade,))
	gabarito = cursor.fetchone()
	if resposta in gabarito:
		conexao.close()
		return print(f"\nResposta Correta. Parabéns.")
	else:
		conexao.close()
		return print(f"\nResposta Incorreta. Sinto Muito.")

def deletar_atividade(atividade):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nDeletando atividade...")
	cursor.execute('''
    DELETE FROM atividades
    WHERE id_atividade = ?;
''', (atividade,))
	conexao.commit()
	conexao.close()
	return print("\nAtividade deletada com sucesso.")