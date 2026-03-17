# Exercício 19: Algoritmo que imprime quadrado do menor e raiz do maior

import math

# Lê dois números do usuário
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

# Determina o menor e maior número
if num1 < num2:
    menor = num1
    maior = num2
else:
    menor = num2
    maior = num1

# Calcula o quadrado do menor
quadrado_menor = menor ** 2

# Calcula a raiz quadrada do maior (se possível)
if maior >= 0:
    raiz_maior = math.sqrt(maior)
    print(f"Quadrado do menor número ({menor}): {quadrado_menor}")
    print(f"Raiz quadrada do maior número ({maior}): {raiz_maior}")
else:
    print(f"Quadrado do menor número ({menor}): {quadrado_menor}")
    print(f"Não é possível calcular a raiz quadrada do maior número ({maior}) pois é negativo.")
