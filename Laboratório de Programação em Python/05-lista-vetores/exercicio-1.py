# Exercício 1: Programa com vetor A para armazenar 6 números inteiros

# Descrição do exercício:
# Faça um programa que contenha um vetor(lista) denominado A para armazenar 6
# números inteiros. O programa deve executar os seguintes passos:


# a) Atribuindo os valores ao vetor A
A = [1, 0, 5, -2, -5, 7]

# b) Calculando a soma das posições [0], [1] e [5]
soma = A[0] + A[1] + A[5]
print(f"Soma dos valores das posições [0], [1] e [5]: {soma}")

# c) Modificando o vetor na posição 4
A[4] = 100
print(f"Vetor modificado na posição 4: {A}")

# d) Mostrando cada valor do vetor A, um em cada linha
print("\nValores do vetor A:")
for i in range(len(A)):
    print(f"A[{i}] = {A[i]}")
