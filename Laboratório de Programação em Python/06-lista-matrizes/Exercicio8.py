# Soma de duas matrizes
# Leia duas matrizes A4x4 e B4x4 contendo valores inteiros.
# Calcule e imprima a matriz soma (A + B).

# Lê a matriz A
matriz_a = []
print("Digite os elementos da matriz A (4x4):")
for i in range(4):
    linha = []
    for j in range(4):
        elemento = int(input(f"A[{i}][{j}]: "))
        linha.append(elemento)
    matriz_a.append(linha)

# Lê a matriz B
matriz_b = []
print("\nDigite os elementos da matriz B (4x4):")
for i in range(4):
    linha = []
    for j in range(4):
        elemento = int(input(f"B[{i}][{j}]: "))
        linha.append(elemento)
    matriz_b.append(linha)

# Calcula a matriz soma
matriz_soma = []
for i in range(4):
    linha = []
    for j in range(4):
        soma = matriz_a[i][j] + matriz_b[i][j]
        linha.append(soma)
    matriz_soma.append(linha)

# Exibe os resultados
print("\n" + "="*50)
print("MATRIZ A:")
print("="*50)
for linha in matriz_a:
    print(linha)

print("\n" + "="*50)
print("MATRIZ B:")
print("="*50)
for linha in matriz_b:
    print(linha)

print("\n" + "="*50)
print("MATRIZ SOMA (A + B):")
print("="*50)
for linha in matriz_soma:
    print(linha)

