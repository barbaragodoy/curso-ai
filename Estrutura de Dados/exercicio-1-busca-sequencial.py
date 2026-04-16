
#Exercício 1 — Busca Sequencial
#Procura de Nome na Lista de Presença

#Uma lista com nomes de alunos foi criada sem nenhuma ordem específica:

alunos = ["Lucas", "Mariana", "Ana", "Pedro", "João", "Beatriz", "Carlos"]

def busca_nome(lista, nome_procurado):
    
    for i in range(len(lista)):
        if lista[i] == nome_procurado:
            return i
    return -1

nome_busca = input("Digite o nome do aluno a buscar: ")
resultado = busca_nome(alunos, nome_busca)
if resultado != -1:
    print(f"{nome_busca} encontrada na posição {resultado}")
else:
    print(f"{nome_busca} não encontrado")

   
    
