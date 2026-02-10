import sqlite3
from datetime import date

def ranking_parcial(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nRanking dos 3 melhores alunos do curso: ")
	cursor.execute('''
	SELECT u.nome,
    	   COUNT(CASE WHEN ua.acerto = 1 THEN 1 END)
	FROM usuarios u
	LEFT JOIN usuario_curso uc ON u.id_usuario = uc.id_usuario
	LEFT JOIN atividades a ON a.id_curso = uc.id_curso
	LEFT JOIN usuario_atividade ua ON ua.id_atividade = a.id_atividade
                              AND ua.id_usuario = u.id_usuario
	WHERE uc.id_curso = ? AND u.tipo = 0
	GROUP BY u.id_usuario, u.nome
	ORDER BY COUNT (CASE WHEN ua.acerto = 1 THEN 1 end) DESC
	LIMIT 3;
	''', (curso,))
	resultados = cursor.fetchall()
	lugar = 1
	for item in resultados:
		print(f"\n{lugar}º - {item[0]} \n{item[1]} Estrelas")
		lugar+=1
	conexao.close()

def ranking_total(curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nRanking de todos os alunos do curso: ")
	cursor.execute('''
	SELECT u.nome,
    	   COUNT(CASE WHEN ua.acerto = 1 THEN 1 END),
    	   COUNT(CASE WHEN ua.status = 1 THEN 1 END)
	FROM usuarios u
	LEFT JOIN usuario_curso uc ON u.id_usuario = uc.id_usuario
	LEFT JOIN atividades a ON a.id_curso = uc.id_curso
	LEFT JOIN usuario_atividade ua ON ua.id_atividade = a.id_atividade
                              AND ua.id_usuario = u.id_usuario
	WHERE uc.id_curso = ? AND u.tipo = 0
	GROUP BY u.id_usuario, u.nome
	ORDER BY COUNT (CASE WHEN ua.acerto = 1 THEN 1 end) DESC;
	''', (curso,))
	resultados = cursor.fetchall()
	lugar=1
	for item in resultados:
		print(f"\n{lugar}º - {item[0]} \n{item[1]} Estrelas | {item[2]} Atividades feitas")
		lugar+=1
	conexao.close()
	
def progresso_diario(cpf,curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	hoje=str(date.today())
	print("\nSeu progresso diário no curso é de: ")
	cursor.execute('''
	SELECT COUNT (CASE WHEN ua.acerto = 1 THEN 1 end),
         COUNT (CASE WHEN ua.status = 1 THEN 1 end)
	FROM usuario_atividade ua
	INNER JOIN atividades a on ua.id_atividade = a.id_atividade
	INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
	WHERE ua.id_usuario =(CASE WHEN u.cpf = ? THEN u.id_usuario END) and a.id_curso= ? AND ua.data = ?;
				''',(cpf,curso,hoje,))
	resultados = cursor.fetchall()
	for item in resultados:
		if item[1] == 0:
			conexao.close()
			return print("\nNão foram realizadas nenhuma atividade hoje.")
		else:
			print(f"\n{item[0]} Estrelas recebidas e {item[1]} Atividades feitas hoje.")
	conexao.close()

def progresso_total(cpf,curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nSeu progresso total no curso é de: ")
	cursor.execute('''
  SELECT COUNT (CASE WHEN ua.acerto = 1 THEN 1 end),
         COUNT (CASE WHEN ua.status = 1 THEN 1 end),
         c.nome
  FROM usuario_atividade ua
  INNER JOIN atividades a on ua.id_atividade = a.id_atividade
  INNER JOIN cursos c ON a.id_curso = c.id_curso
  INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
  WHERE ua.id_usuario =(CASE WHEN u.cpf = ? THEN u.id_usuario END) and c.id_curso= ?;
''',(cpf,curso,))
	resultados = cursor.fetchall()
	for item in resultados:
		if item[2] is None :
			conexao.close()
			return print("\nNão foram realizadas nenhuma atividade no curso ainda.")
		else:
			print(f"\n{item[0]} Estrelas recebidas e {item[1]} Atividades feitas no total no curso de {item[2]}.")
	conexao.close()

def progresso_cursos(cpf):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	hoje=str(date.today())
	print("\nLista do progresso diário em todos os seus cursos: ")
	cursor.execute('''
	    SELECT c.nome,
  		   COUNT (CASE WHEN ua.acerto = 1 THEN 1 end),
           COUNT (CASE WHEN ua.status = 1 THEN 1 end)
	FROM cursos c
	LEFT JOIN atividades a on c.id_curso = a.id_curso
	LEFT JOIN usuario_atividade ua ON a.id_atividade = ua.id_atividade
    INNER JOIN usuarios u ON ua.id_usuario = u.id_usuario
	WHERE ua.data = ? AND ua.id_usuario = (CASE WHEN u.cpf = ? THEN u.id_usuario END)
	GROUP by c.nome
	ORDER BY c.nome ASC;
	''', (hoje,cpf,))
	resultados = cursor.fetchall()
	if not resultados:
		conexao.close()
		return print("\nNão foram realizadas nenhuma atividade hoje em nenhum dos cursos.")
	else:
		for item in resultados:
			print(f"\n{item[0]} - {item[1]} Estrelas recebidas e {item[2]} Atividades feitas hoje.")
	conexao.close()

def progresso_alunos():
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	hoje=str(date.today())
	print("\nLista do progresso diário de todos os alunos por curso: ")
	cursor.execute('''
	      SELECT c.nome,
    	   u.nome,
  		   COUNT (CASE WHEN ua.acerto = 1 THEN 1 end),
           COUNT (CASE WHEN ua.status = 1 THEN 1 end)
	FROM cursos c
	LEFT JOIN atividades a on c.id_curso = a.id_curso
	LEFT JOIN usuario_atividade ua ON a.id_atividade = ua.id_atividade
    LEFT JOIN usuarios u ON ua.id_usuario = u.id_usuario
	WHERE ua.data = ?
	GROUP by c.nome, u.nome
	ORDER BY c.nome ASC;
''',(hoje,))
	resultados = cursor.fetchall()
	if not resultados:
		conexao.close()
		return print("\nNão foram realizadas nenhuma atividade hoje por nenhum dos alunos.")
	else:
		for item in resultados:
			print(f"\n{item[0]} - {item[2]} Estrelas recebidas e {item[3]} Atividades feitas hoje por: \n{item[1]}")
	conexao.close()

def desempenho_curso():
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nDesempenho (em %) de acertos por curso: ")
	cursor.execute('''
	SELECT c.nome,
  		   COUNT (CASE WHEN ua.acerto = 1 THEN 1 end),
           COUNT (CASE WHEN ua.status = 1 THEN 1 end)
	FROM cursos c
	LEFT JOIN atividades a on c.id_curso = a.id_curso
	LEFT JOIN usuario_atividade ua ON a.id_atividade = ua.id_atividade
	GROUP by c.nome
	ORDER BY c.nome ASC;
	''')
	resultados = cursor.fetchall()
	for item in resultados:
			if item[2] == 0:
				print(f"\n{item[0]} - Sem atividades feitas.")
			else:
				calculo= (item[1]/item[2])*100
				print(f"\n{item[0]} - {calculo:.0f}% de acerto.")
	conexao.close()
	
def resetar_progresso(cpf,curso):
	conexao = sqlite3.connect('banco.db')
	cursor = conexao.cursor()
	print("\nResetando progresso... ")
	cursor.execute('''
	UPDATE usuario_atividade
   	SET status = 0
   	WHERE id_usuario = (SELECT id_usuario FROM usuarios WHERE cpf = ?)
   	AND id_atividade IN (
   		SELECT id_atividade
   		FROM atividades
  		WHERE id_curso = ?
   );
''',(cpf,curso,))
	conexao.commit()
	conexao.close()
	return print("\nProgresso resetado com sucesso.")