# Exercício 28: Algoritmo que verifica se três valores podem formar um triângulo

# Lê os três valores
A = float(input("Digite o primeiro valor (A): "))
B = float(input("Digite o segundo valor (B): "))
C = float(input("Digite o terceiro valor (C): "))

# Verifica se podem formar um triângulo
# Condição: a soma de dois lados deve ser maior que o terceiro lado
if (A + B > C) and (A + C > B) and (B + C > A):
    print("Os valores podem formar um triângulo.")
else:
    print("Os valores não podem formar um triângulo.")
