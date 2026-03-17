# Exercício 6: Algoritmo que calcula raiz quadrada ou quadrado conforme o número

import math

# Lê um número do usuário
numero = float(input("Digite um número: "))

# Verifica se o número é positivo/zero ou negativo
if numero >= 0:
    raiz = math.sqrt(numero)
    print(f"O número {numero} é positivo ou zero.")
    print(f"Raiz quadrada: {raiz}")
else:
    quadrado = numero ** 2
    print(f"O número {numero} é negativo.")
    print(f"Quadrado: {quadrado}")
