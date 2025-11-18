# Impressão formatada da matriz 3 x 3
# Crie um algoritmo que leia valores inteiros para uma matriz 3 x 3 e imprima a matriz final formatada,
# conforme o modelo mostrado no exemplo (em linhas e colunas).

matriz = []
print("Digite os elementos da matriz 3x3:")
for i in range(3):
    linha = []
    for j in range(3):
        elemento = int(input(f"Digite o elemento [{i}][{j}]: "))
        linha.append(elemento)
    matriz.append(linha)

# Imprime a matriz formatada
print("\nMatriz 3x3 formatada:")
print("-" * 25)
for i in range(3):
    print("|", end="")
    for j in range(3):
        print(f" {matriz[i][j]:4d} ", end="")
    print("|")
print("-" * 25)

