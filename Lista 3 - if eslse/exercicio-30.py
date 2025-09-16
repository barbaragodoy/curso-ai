# Exercício 30: Algoritmo que verifica triângulo retângulo e calcula ângulos

import math

# Lê os três valores
A = float(input("Digite o primeiro valor (A): "))
B = float(input("Digite o segundo valor (B): "))
C = float(input("Digite o terceiro valor (C): "))

# Verifica se podem formar um triângulo
if (A + B > C) and (A + C > B) and (B + C > A):
    print("Os valores podem formar um triângulo.")
    
    # Ordena os lados para encontrar a hipotenusa
    lados = [A, B, C]
    lados.sort()
    a, b, c = lados  # a e b são catetos, c é hipotenusa
    
    # Verifica se é triângulo retângulo (Teorema de Pitágoras)
    if abs(a**2 + b**2 - c**2) < 0.001:  # Tolerância para erros de ponto flutuante
        print("É um triângulo retângulo.")
        
        # Calcula os ângulos
        angulo_A = math.degrees(math.asin(a/c))
        angulo_B = math.degrees(math.asin(b/c))
        angulo_C = 90.0
        
        print(f"Ângulos internos:")
        print(f"Ângulo oposto ao lado {a}: {angulo_A:.2f}°")
        print(f"Ângulo oposto ao lado {b}: {angulo_B:.2f}°")
        print(f"Ângulo oposto ao lado {c}: {angulo_C:.2f}°")
    else:
        print("Não é um triângulo retângulo.")
else:
    print("Os valores não podem formar um triângulo.")
