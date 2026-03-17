# Exercício 5: Programa para calcular média geral das notas de 15 alunos
# 
# Descrição do exercício:
# Faça um programa para ler a nota da prova de 15 alunos e armazene num
# vetor(lista), calcule e imprima a média geral.

# Criando lista vazia para armazenar as notas
notas = []

print("Digite as notas de 15 alunos:")

# Lendo as notas dos 15 alunos
for i in range(15):
    nota = float(input(f"Digite a nota do {i+1}º aluno: "))
    notas.append(nota)

# Calculando a média geral
soma_notas = sum(notas)
media_geral = soma_notas / len(notas)

# Imprimindo os resultados
print(f"\nNotas dos alunos: {notas}")
print(f"Soma das notas: {soma_notas}")
print(f"Média geral: {media_geral:.2f}")
