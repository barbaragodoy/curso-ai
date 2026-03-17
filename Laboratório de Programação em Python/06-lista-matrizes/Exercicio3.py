# Verificação de simetria
# Implemente um programa que verifique se uma matriz 2 x 3 é simétrica, ou seja, se é igual à sua transposta.
# Ao final, retorne se a matriz é simétrica ou não.

matriz = []
print("Digite os elementos da matriz 2x3:")
for i in range(2):
    linha = []
    for j in range(3):
        elemento = int(input(f"Digite o elemento [{i}][{j}]: "))
        linha.append(elemento)
    matriz.append(linha)

# Calcula a transposta (3x2)
transposta = []
for j in range(3):
    linha = []
    for i in range(2):
        linha.append(matriz[i][j])
    transposta.append(linha)

print("\nMatriz original (2x3):")
for linha in matriz:
    print(linha)

print("\nMatriz transposta (3x2):")
for linha in transposta:
    print(linha)

# Verifica se é simétrica (matriz original deve ser igual à transposta)
# Para uma matriz 2x3 ser simétrica, ela precisaria ser igual à sua transposta 3x2,
# o que é impossível. Mas vamos verificar se os elementos correspondem
simetrica = True
if len(matriz) != len(transposta) or len(matriz[0]) != len(transposta[0]):
    simetrica = False
else:
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] != transposta[i][j]:
                simetrica = False
                break
        if not simetrica:
            break

if simetrica:
    print("\nA matriz é simétrica.")
else:
    print("\nA matriz NÃO é simétrica (uma matriz 2x3 não pode ser simétrica, pois sua transposta é 3x2).")
