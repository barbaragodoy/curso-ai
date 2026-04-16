# Geração de matriz com fórmulas condicionais
# Implemente um programa capaz de gerar e imprimir uma matriz 10 x 10, onde cada elemento é calculado da seguinte forma:
# A[i][j] = 2i + 7j - 2, se i < j
# A[i][j] = 3i² - 1, se i = j
# A[i][j] = 4i³ - 5j² + 1, se i > j

matriz = []
for i in range(10):
    linha = []
    for j in range(10):
        if i < j:
            elemento = 2 * i + 7 * j - 2
        elif i == j:
            elemento = 3 * (i ** 2) - 1
        else:  # i > j
            elemento = 4 * (i ** 3) - 5 * (j ** 2) + 1
        linha.append(elemento)
    matriz.append(linha)

print("Matriz 10x10 gerada com fórmulas condicionais:")
for linha in matriz:
    print(linha)
