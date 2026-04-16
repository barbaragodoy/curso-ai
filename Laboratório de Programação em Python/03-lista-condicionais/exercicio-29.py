# Exercício 29: Algoritmo que verifica se três valores podem formar triângulo e determina o tipo

# Lê os três valores
A = float(input("Digite o primeiro valor (A): "))
B = float(input("Digite o segundo valor (B): "))
C = float(input("Digite o terceiro valor (C): "))

# Verifica se podem formar um triângulo
if (A + B > C) and (A + C > B) and (B + C > A):
    print("Os valores podem formar um triângulo.")
    
    # Determina o tipo do triângulo
    if A == B == C:
        tipo = "equilátero"
    elif A == B or A == C or B == C:
        tipo = "isósceles"
    else:
        tipo = "escaleno"
    
    print(f"Tipo do triângulo: {tipo}")
else:
    print("Os valores não podem formar um triângulo.")
