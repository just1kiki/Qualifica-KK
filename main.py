import sqlite3
import banco
import usuarios

def checar_senha(cpf,senha):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	cursor.execute("SELECT 1 FROM usuarios WHERE cpf = ? AND senha = ?;", (cpf,senha,))
	check_senha = cursor.fetchone()
	conexao.close()
	return check_senha is not None

def login():
    banco.criar_tabela()
    while True:
        print("\n--- Login de Usuário ---")
        print("\nOpções de Login: \n1. Aluno \n2. Professor \n3. Coordenador \n4. Fechar")

        opcao = input("\nEscolha a opção de login desejada: ")

        match opcao:
            case "1":
                cpf_aluno = input("\nDigite o CPF (Apenas números): ")
                senha_aluno = input("\nDigite a senha: ")
                if usuarios.cpf_existe(cpf_aluno):
                    if checar_senha(cpf_aluno,senha_aluno):
                        print(f"\nLogin realizado com sucesso.\n\nEntrando no Menu Aluno...")
                        return repetir_login(usuarios.menu_usuario(cpf_aluno,opcao))
                    else:
                        print(f"\nSenha incorreta. Cheque os dados inseridos ou comunique um Coordenador responsável.")

                else:
                    print(f"\nCPF não cadastrado. Cheque os dados inseridos ou comunique um Coordenador responsável.")

            case "2":
                cpf_prof = input("\nDigite o CPF (Apenas números): ")
                senha_prof = input("\nDigite a senha: ")
                if usuarios.cpf_existe(cpf_prof):
                    if checar_senha(cpf_prof,senha_prof):
                        print(f"\nLogin realizado com sucesso.\n\nEntrando no Menu Professor...")
                        return repetir_login(usuarios.menu_usuario(cpf_prof,opcao))
                    else:
                        print(f"\nSenha incorreta. Cheque os dados inseridos ou comunique um Coordenador responsável.")

                else:
                    print(f"\nCPF não cadastrado. Cheque os dados inseridos ou comunique um Coordenador responsável.")
            case "3":
                cpf_coord = input("\nDigite o CPF (Apenas números): ")
                senha_coord = input("\nDigite a senha: ")
                if usuarios.cpf_existe(cpf_coord):
                    if checar_senha(cpf_coord,senha_coord):
                        print(f"\nLogin realizado com sucesso.\n\nEntrando no Menu Coordenador...")
                        return repetir_login(usuarios.menu_usuario(cpf_coord,opcao))
                    else:
                        print(f"\nSenha incorreta. Cheque os dados inseridos ou comunique outro Coordenador, ou TI responsável.")

                else:
                    print(f"\nCPF não cadastrado. Cheque os dados inseridos ou comunique outro Coordenador, ou TI responsável.")

            case "4":
                print("\nSaindo do menu de login...")
                break
            case _:
                print("\nOpção inválida. Tente novamente.")

def repetir_login(menu):
    if menu is True:
        login()

login()