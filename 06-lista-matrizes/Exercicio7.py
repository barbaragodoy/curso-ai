# Correção de prova com gabarito
# Implemente um programa que leia uma matriz 5 x 10 que representa as respostas de 5 alunos em 10 questões de múltipla escolha.
# Leia também um vetor de 10 posições contendo o gabarito (com respostas A, B, C, D ou E).
# O programa deve comparar as respostas de cada aluno com o gabarito e gerar um vetor resultado com a pontuação de cada aluno.

# Lê o gabarito
gabarito = []
print("Digite o gabarito (10 questões - A, B, C, D ou E):")
for i in range(10):
    resposta = input(f"Resposta da questão {i+1}: ").upper()
    while resposta not in ['A', 'B', 'C', 'D', 'E']:
        resposta = input(f"Resposta inválida! Digite A, B, C, D ou E para a questão {i+1}: ").upper()
    gabarito.append(resposta)

# Lê as respostas dos alunos
matriz_respostas = []
print("\nDigite as respostas dos 5 alunos (10 questões cada):")
for i in range(5):
    print(f"\nAluno {i+1}:")
    linha = []
    for j in range(10):
        resposta = input(f"Resposta da questão {j+1}: ").upper()
        while resposta not in ['A', 'B', 'C', 'D', 'E']:
            resposta = input(f"Resposta inválida! Digite A, B, C, D ou E para a questão {j+1}: ").upper()
        linha.append(resposta)
    matriz_respostas.append(linha)

# Calcula a pontuação de cada aluno
pontuacao = []
for i in range(5):
    pontos = 0
    for j in range(10):
        if matriz_respostas[i][j] == gabarito[j]:
            pontos += 1
    pontuacao.append(pontos)

# Exibe os resultados
print("\n" + "="*50)
print("RESULTADOS:")
print("="*50)
print(f"\nGabarito: {gabarito}\n")

for i in range(5):
    print(f"Aluno {i+1}: {pontuacao[i]} acertos de 10 questões")
    print(f"  Respostas: {matriz_respostas[i]}")

print(f"\nVetor de pontuação: {pontuacao}")

