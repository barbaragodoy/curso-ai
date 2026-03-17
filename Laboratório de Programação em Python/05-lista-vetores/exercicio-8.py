# Exercício 8: Programa para calcular produto escalar entre dois conjuntos de números
# 
# Descrição do exercício:
# Implemente um programa que leia dois conjuntos de números reais, armazenando-
# os em vetor(lista)es. Após, calcule o produto escalar entre eles. Os conjuntos têm
# 5 elementos cada. Ao final, imprimir os dois conjuntos e o produto escalar, sendo
# que o produto escalar é dado por: x1 * y1 + x2 * y2 + ... + xn * yn.

# Criando listas vazias para armazenar os números
conjunto_x = []
conjunto_y = []

print("Digite os elementos do primeiro conjunto (X):")

# Lendo os 5 números do primeiro conjunto
for i in range(5):
    numero = float(input(f"Digite o {i+1}º número do conjunto X: "))
    conjunto_x.append(numero)

print("\nDigite os elementos do segundo conjunto (Y):")

# Lendo os 5 números do segundo conjunto
for i in range(5):
    numero = float(input(f"Digite o {i+1}º número do conjunto Y: "))
    conjunto_y.append(numero)

# Calculando o produto escalar
produto_escalar = 0
for i in range(5):
    produto_escalar += conjunto_x[i] * conjunto_y[i]

# Imprimindo os resultados
print(f"\nConjunto X: {conjunto_x}")
print(f"Conjunto Y: {conjunto_y}")
print(f"Produto escalar: {produto_escalar}")

# Mostrando o cálculo detalhado
print("\nCálculo detalhado:")
for i in range(5):
    print(f"x{i+1} * y{i+1} = {conjunto_x[i]} * {conjunto_y[i]} = {conjunto_x[i] * conjunto_y[i]}")
print(f"Soma total: {produto_escalar}")
