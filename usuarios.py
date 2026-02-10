import sqlite3
import main
import progresso
import atividades

def curso_existe(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute("SELECT 1 FROM cursos WHERE id_curso = ?", (curso,))
	check_curso = cursor.fetchone()
	conexao.close()
	return check_curso is not None

def adicionar_curso(cpf):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nPara adicionar um curso preencha as informações a seguir: ")
	nome = input(f"\nDigite o nome do curso a ser adicionado: ")
	horario = (input("\nQual o horário do curso: \n1-Matutino \n2-Vespertino \n3-Noturno \n>"))
	if horario.isdigit() and len(horario)==1:
		opcao = int(horario)-1
		if opcao <= 2:
			cursor.execute("INSERT INTO cursos (nome,horario) VALUES (?,?)", (nome,opcao))
			cursor.execute("INSERT INTO usuario_curso (id_usuario,id_curso) VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),(SELECT id_curso FROM cursos WHERE nome = ?));", (cpf,nome))
			conexao.commit()
			conexao.close()
			return print(f"\nCurso {nome} adicionado a lista com sucesso.")
		else:
			return print(f"\nO número digitado não referencia nenhum dos horários possíveis")
	else:
		return print("Apenas números entre 1 a 3 são escolhas possíveis.")

def lista_cursos():
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nLista dos cursos: ")
	cursor.execute('''
    SELECT c.id_curso,
		   c.nome,
	       c.horario,
		   SUBSTR(u.nome, 1, INSTR(SUBSTR(u.nome, INSTR(u.nome, ' ') + 1), ' ') + INSTR(u.nome, ' ') - 1)
    FROM cursos c
    INNER JOIN usuario_curso uc ON c.id_curso = uc.id_curso
    INNER JOIN usuarios u ON uc.id_usuario = u.id_usuario
    WHERE u.tipo = 1
	ORDER BY c.id_curso ASC;
	''')
	resultados = cursor.fetchall()
	for linha in resultados:
		match linha[2]:
			case 0:
				print(f"\n{linha[0]}. Curso: {linha[1]} | Horário: Matutino | Professor(a): {linha[3]}")
			case 1:
				print(f"\n{linha[0]}. Curso: {linha[1]} | Horário: Vespertino | Professor(a): {linha[3]}")
			case 2:
				print(f"\n{linha[0]}. Curso: {linha[1]} | Horário: Noturno | Professor(a): {linha[3]}")

	conexao.close()

def email_existe(email):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
	check_email = cursor.fetchone()
	conexao.close()
	return check_email is not None

def cadastrar_usuario():
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nPara cadastrar um usuário preencha as informações a seguir: ")
	nome_completo = input("\nDigite o nome completo do(a) usuário(a): ")
	email = input("\nDigite o e-mail do(a) usuário(a): ")
	cpf = input("\nDigite o CPF do(a) usuário(a): (Apenas números) ")
	if not cpf.isdigit() or len(cpf)!=11:
		return print(f"CPF incorreto. Certifique-se de usar apenas 11 números.")
	if main.cpf_existe(cpf):
		conexao.close()
		return print(f"\nO CPF inserido já está cadastrado.")
	if email_existe(email):
		conexao.close()
		return print(f"\nO e-mail inserido já está cadastrado.")

	senha = (nome_completo[:3])+"@"+(str(cpf)[-4:])
	tipo = input("\nQual o tipo de usuário: \n1- Aluno \n2- Professor \n3- Coordenador \n>")
	if tipo.isdigit() and len(tipo)==1:
		opcao = int(tipo)-1
		if opcao == 0:
			print(f"\nQual curso, ou cursos, o aluno está matriculado? ")
			lista_cursos()
			escolha = input("\nDigite o número do curso em que o aluno está matriculado: ")
			if escolha.isdigit() and curso_existe(escolha):
				cursor.execute("INSERT INTO usuarios (nome,email,cpf,senha,tipo) VALUES (?,?,?,?,?)", (nome_completo,email,cpf,senha,opcao))
				cursor.execute("INSERT INTO usuario_curso (id_usuario,id_curso) VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),(?));", (cpf,escolha))
				conexao.commit()
				while True:
					alternativa = input(f"\nGostaria de adicionar outro curso? \n1- Sim   2-Não \n>")
					if alternativa.isdigit() and len(alternativa)==1:
						if alternativa == "1":
							print(f"\nQual curso há mais o aluno está matriculado? ")
							lista_cursos()
							escolha2 = input("\nDigite o número do curso em que o aluno está matriculado: ")
							if escolha2.isdigit() and curso_existe(escolha2) and escolha2!=escolha:
								cursor.execute("INSERT INTO usuario_curso (id_usuario,id_curso) VALUES ((SELECT id_usuario FROM usuarios WHERE cpf = ?),(?));", (cpf,escolha2))
								conexao.commit()
							else:
								print(f"\nApenas números de cursos ainda não adicionados entre os da lista são escolhas possíveis.")
						elif alternativa == "2":
							print(f"\nUsuário(a) {nome_completo} cadastrado(a) com sucesso.")
							break
						else:
							print(f"\nO número digitado não referencia nenhuma das opções possíveis.")
					else:
						print(f"\nApenas números entre 1 e 2 são escolhas possíveis.")
			else:
				return print(f"\nApenas números entre os da lista são escolhas possíveis.")
		elif opcao <=2:
			cursor.execute("INSERT INTO usuarios (nome,email,cpf,senha,tipo) VALUES (?,?,?,?,?)", (nome_completo,email,cpf,senha,opcao))
			conexao.commit()
			conexao.close()
			return print(f"\nUsuário(a) {nome_completo} cadastrado(a) com sucesso.")
		else:
			return print(f"\nO número digitado não referencia nenhum dos tipos possíveis ")
	else:
		return print(f"\nApenas números entre 1 a 3 são escolhas possíveis.")

def checar_uc(cpf,curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute('''SELECT 1 FROM usuario_curso uc
    INNER JOIN usuarios u ON u.id_usuario = uc.id_usuario
    WHERE uc.id_usuario = (CASE WHEN u.cpf = ? THEN u.id_usuario END) AND uc.id_curso = ?;
	''', (cpf,curso,))
	check_uc = cursor.fetchone()
	conexao.close()
	return check_uc is not None

def menu_usuario(cpf,tipo):
	while True:
		match tipo:
			case "1":
				print("\n--- Menu do Aluno ---")
				print("\nOpções do menu: \n1. Ver lista de cursos \n2. Ver progresso diário em todos os seus cursos. \n3. Deslogar")
				opcao = input("\nEscolha a opção do menu desejada: ")
				match opcao:
					case "1":
						print(f"\nAcessando lista de cursos...")
						return menu_lista(cpf,tipo)
					case "2":
						progresso.progresso_cursos(cpf)
						print(f"\nVoltando ao Menu do Aluno...")
					case "3":
						print(f"\nDeslogando...")
						return main.login()
					case _:
						print(f"\nApenas números entre 1 a 3 são escolhas possíveis.")
			
			case "2":
				print("\n--- Menu do Professor ---")
				print("\nOpções do menu: \n1. Ver lista de cursos \n2. Deslogar")
				opcao = input("\nEscolha a opção do menu desejada: ")
				match opcao:
					case "1":
						print(f"\nAcessando lista de cursos...")
						return menu_lista(cpf,tipo)
					case "2":
						print(f"\nDeslogando...")
						return main.login()
					case _:
						print(f"\nApenas números 1 e 2 são escolhas possíveis.")
			case "3":
				print("\n--- Menu do Coordenador ---")
				print("\nOpções do menu: \n1. Ver lista de cursos \n2. Cadastrar usuário. \n3. Deslogar")
				opcao = input("\nEscolha a opção do menu desejada: ")
				match opcao:
					case "1":
						print(f"\nAcessando lista de cursos...")
						return menu_lista(cpf,tipo)
					case "2":
						cadastrar_usuario()
					case "3":
						print(f"\nDeslogando...")
						return main.login()
					case _:
						print(f"\nApenas números entre 1 a 3 são escolhas possíveis.")

def menu_lista(cpf,tipo):
	while True:
		lista_cursos()
		match tipo:
			case "1":
				print("\n1. Selecionar curso \n2. Voltar")
				opcao = input("\nO que gostaria de fazer? ")
				match opcao:
					case "1":
						curso = input("\nDigite o número do curso desejado: ")
						if curso_existe(curso):
							if checar_uc(cpf,curso):
								print(f"\nAcessando opções do curso...")
								return menu_curso(cpf,tipo,curso)
							else:
								print(f"\nApenas os cursos em que está matriculado são selecionáveis.")
						else:
							print(f"\nApenas números entre os da lista são escolhas possíveis.")
					case "2":
						print(f"\nVoltando para o Menu do Aluno...")
						return menu_usuario(cpf,tipo)
					case _:
						print(f"\nApenas os números 1 e 2 são escolhas possíveis.")

			case "2":
				print("\n1. Selecionar curso \n2. Adicionar novo curso \n3. Voltar")
				opcao = input("\nO que gostaria de fazer? ")
				match opcao:
					case "1":
						curso = input("\nDigite o número do curso desejado: ")
						if curso_existe(curso):
							if checar_uc(cpf,curso):
								print(f"\nAcessando opções do curso...")
								return menu_curso(cpf,tipo,curso)
							else:
								print(f"\nApenas os cursos em que está lecionando são selecionáveis.")
						else:
							print(f"\nApenas números entre os da lista são escolhas possíveis.")
					case "2":
						adicionar_curso(cpf)
					case "3":
						print(f"\nVoltando para o Menu do Professor...")
						return menu_usuario(cpf,tipo)
					case _:
						print(f"\nApenas os números entre 1 a 3 são escolhas possíveis.")
			case "3":
				print("\n1. Selecionar curso \n2. Ver atividades feitas hoje por todos os alunos \n3. Ver desempenho por curso \n4. Voltar")
				opcao = input("\nO que gostaria de fazer? ")
				match opcao:
					case "1":
						curso = input("\nDigite o número do curso desejado: ")
						if curso_existe(curso):
							if checar_uc(cpf,curso):
								print(f"\nAcessando opções do curso...")
								return menu_curso(cpf,tipo,curso)
							else:
								print(f"\nApenas os cursos em que está matriculado são selecionáveis.")
						else:
							print(f"\nApenas números entre os da lista são escolhas possíveis.")
					case "2":
						progresso.progresso_alunos()
					case "3":
						progresso.desempenho_curso()
					case "4":
						print(f"\nVoltando para o Menu do Coordenador...")
						return menu_usuario(cpf,tipo)
					case _:
						print(f"\nApenas os números entre 1 a 4 são escolhas possíveis.")

def menu_curso(cpf,tipo,curso):
	while True:
		match tipo:
			case "1":
				print("\nOpções do curso: \n1. Selecionar atividade \n2.Ver seu progresso total \n3. Ver ranking dos 3 melhores alunos do curso \n4. Voltar")
				opcao = input("\nEscolha a opção desejada: ")
				match opcao:
					case "1":
						print(f"\nAcessando atividades do curso...")
						return menu_atividade(cpf,tipo,curso,(atividades.escolher_atividade(atividades.listar_atividades(curso))))
					case "2":
						print(f"\nAcessando o progresso total...")
						return menu_progresso(cpf,tipo,curso)
					case "3":
						progresso.ranking_parcial(curso)
						print(f"\nVoltando...")
					case "4":
						print(f"\nVoltando para a Lista de Cursos...")
						return menu_lista(cpf,tipo)
					case _:
						print(f"\nApenas os números entre 1 a 4 são escolhas possíveis.")
						
			case "2":
				atividades.listar_atividades(curso)
				print("\nOpções do curso: \n1. Adicionar atividade \n2. Deletar atividade \n3. Voltar")
				opcao = input("\nEscolha a opção desejada: ")
				match opcao:
					case "1":
						atividades.adicionar_atividade(curso)
					case "2":
						print("\nTem certeza disso? Essa decisão não pode ser desfeita. Todas as estrelas recebidas por essa atividade serão apagadas juntamente com ela.")
						confirmacao = input ("\n1. Sim \n2. Não")
						match confirmacao:
							case "1":
								atividades.deletar_atividade(atividades.escolher_atividade(atividades.listar_atividades(curso)))
							case "2":
								print(f"\nVoltando...")
							case _:
								print(f"\nApenas os números 1 e 2 são escolhas possíveis.")
					case "3":
						print(f"\nVoltando para a Lista de Cursos...")
						return menu_lista(cpf,tipo)
					case _:
						print(f"\nApenas os números entre 1 a 3 são escolhas possíveis.")
			case "3":
				print("\nOpções do curso: \n1. Ranking completo dos alunos no curso \n2. Voltar")
				opcao = input("\nEscolha a opção desejada: ")
				match opcao:
					case "1":
						progresso.ranking_total(curso)
					case "2":
						print(f"\nVoltando para a Lista de Cursos...")
						return menu_lista(cpf,tipo)
					case _:
						print(f"\nApenas os números 1 e 2 são escolhas possíveis.")


def menu_progresso(cpf,tipo,curso):
	while True:
		progresso.progresso_total(cpf,curso)
		print("\n1. Resetar progresso \n.2 Voltar")
		opcao = input("\nO que gostaria de fazer? ")
		match opcao:
			case "1":
				print("\nTem certeza disso? Essa decisão não pode ser desfeita, e não haverá mudança na quantidade de estrelas já recebidas.")
				confirmacao = input ("\n1. Sim \n2. Não")
				match confirmacao:
					case "1":
						progresso.resetar_progresso(cpf,curso)
					case "2":
						print(f"\nVoltando...")
					case _:
						print(f"\nApenas os números 1 e 2 são escolhas possíveis.")
			case "2":
				print(f"\nVoltando...")
				return menu_curso(cpf,tipo,curso)
			case _:
				print(f"\nApenas os números 1 e 2 são escolhas possíveis.")

def menu_atividade(cpf,tipo,curso,atividade):
	while True:
		atividades.mostrar_atividade(atividade)
		print("\n1. Responder \n2.Pedir dica \n.3 Voltar")
		opcao = input("\nO que gostaria de fazer? ")
		match opcao:
			case "1":
				resposta = input(f"\nQual opção deseja marcar como resposta? \nA \nB \nC \nD \n>").lower().strip()
				if len(resposta)==1:
					lista = ['a','b','c','d']
					if resposta in lista:
						atividades.realizar_atividade(cpf,atividade,resposta)
						progresso.progresso_diario(cpf,curso)
						return menu_curso(cpf,tipo,curso)
					else:
						print(f"\nApenas as letras de A a D são escolhas possíveis.")
				else:
					print(f"\nApenas uma das letras de A a D são escolhas possíveis.")
			case "2":
				atividades.pedir_dica(atividade)
			case "3":
				print(f"\nVoltando...")
				return menu_curso(cpf,tipo,curso)
			case _:
				print(f"\nApenas os números entre 1 e 3 são escolhas possíveis.")


menu_usuario("38746195211","1")