# Soma de linhas e colunas
# Implemente um programa que calcule a soma dos elementos de cada linha e de cada coluna de uma matriz
# e armazene os resultados em vetores.
# Ao final, exiba o valor do somatório das linhas e das colunas armazenados nos vetores.

linhas = int(input("Digite o número de linhas da matriz: "))
colunas = int(input("Digite o número de colunas da matriz: "))

matriz = []
print(f"\nDigite os elementos da matriz {linhas}x{colunas}:")
for i in range(linhas):
    linha = []
    for j in range(colunas):
        elemento = int(input(f"Digite o elemento [{i}][{j}]: "))
        linha.append(elemento)
    matriz.append(linha)

# Vetor para armazenar a soma de cada linha
soma_linhas = []
for i in range(linhas):
    soma = 0
    for j in range(colunas):
        soma += matriz[i][j]
    soma_linhas.append(soma)

# Vetor para armazenar a soma de cada coluna
soma_colunas = []
for j in range(colunas):
    soma = 0
    for i in range(linhas):
        soma += matriz[i][j]
    soma_colunas.append(soma)

print("\nMatriz:")
for linha in matriz:
    print(linha)

print(f"\nSoma de cada linha: {soma_linhas}")
print(f"Soma de cada coluna: {soma_colunas}")

