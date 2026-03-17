# Busca de elemento na matriz
# Implemente um programa que leia uma matriz 5 x 5 e um valor X.
# O programa deverá fazer uma busca desse valor na matriz e, ao final, escrever a localização
# (linha e coluna) do elemento ou uma mensagem informando "elemento não encontrado".

matriz = []
print("Digite os elementos da matriz 5x5:")
for i in range(5):
    linha = []
    for j in range(5):
        elemento = int(input(f"Digite o elemento [{i}][{j}]: "))
        linha.append(elemento)
    matriz.append(linha)

x = int(input("\nDigite o valor X a ser buscado na matriz: "))

# Busca o elemento na matriz
encontrado = False
linha_encontrada = -1
coluna_encontrada = -1

for i in range(5):
    for j in range(5):
        if matriz[i][j] == x:
            encontrado = True
            linha_encontrada = i
            coluna_encontrada = j
            break
    if encontrado:
        break

print("\nMatriz:")
for linha in matriz:
    print(linha)

if encontrado:
    print(f"\nElemento {x} encontrado na posição [{linha_encontrada}][{coluna_encontrada}]")
else:
    print(f"\nElemento {x} não encontrado na matriz.")

