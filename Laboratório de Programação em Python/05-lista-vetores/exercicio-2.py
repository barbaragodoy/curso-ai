# Exercício 2: Programa para ler números reais e calcular quadrados
# 
# Descrição do exercício:
# Implemente um programa que leia um conjunto de números reais armazenando-
# os em um vetor(lista). Após, calcule o quadrado dos componentes deste
# vetor(lista), armazenando o resultado em outro vetor(lista). Os conjuntos têm 10
# elementos cada. Ao final, imprima todos os vetores(listas).

# Criando listas vazias para armazenar os números
numeros = []
quadrados = []

print("Digite 10 números reais:")

# Lendo os 10 números reais
for i in range(10):
    numero = float(input(f"Digite o {i+1}º número: "))
    numeros.append(numero)

# Calculando o quadrado de cada número e armazenando em outro vetor
for numero in numeros:
    quadrado = numero ** 2
    quadrados.append(quadrado)

# Imprimindo os resultados
print("\nNúmeros originais:")
for i in range(len(numeros)):
    print(f"Posição {i}: {numeros[i]}")

print("\nQuadrados dos números:")
for i in range(len(quadrados)):
    print(f"Posição {i}: {quadrados[i]}")

print(f"\nVetor original: {numeros}")
print(f"Vetor dos quadrados: {quadrados}")
