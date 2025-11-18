# Diagonal principal com 1 e demais com 0
# Declare uma matriz 5 x 5.
# Preencha com 1 a diagonal principal e com 0 os demais elementos.
# Ao final, escreva a matriz obtida.

matriz = []
for i in range(5):
    linha = []
    for j in range(5):
        if i == j:  # Diagonal principal
            linha.append(1)
        else:
            linha.append(0)
    matriz.append(linha)

print("Matriz 5x5 com diagonal principal = 1 e demais elementos = 0:")
for linha in matriz:
    print(linha)
