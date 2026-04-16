# Soma dos elementos da matriz
# Implemente um programa que calcule e retorne a soma dos elementos de uma matriz 5 x 5 de números inteiros.

matriz = []
print("Digite os elementos da matriz 5x5:")
for i in range(5):
    linha = []
    for j in range(5):
        elemento = int(input(f"Digite o elemento [{i}][{j}]: "))
        linha.append(elemento)
    matriz.append(linha)

# Calcula a soma dos elementos
soma = 0
for i in range(5):
    for j in range(5):
        soma += matriz[i][j]

print("\nMatriz:")
for linha in matriz:
    print(linha)

print(f"\nSoma dos elementos da matriz: {soma}")

