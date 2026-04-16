# Exercício 14: Algoritmo que imprime três valores em ordem ascendente

# Lê três valores do usuário
A = float(input("Digite o primeiro valor (A): "))
B = float(input("Digite o segundo valor (B): "))
C = float(input("Digite o terceiro valor (C): "))

# Ordena os valores em ordem ascendente
if A <= B <= C:
    menor, meio, maior = A, B, C
elif A <= C <= B:
    menor, meio, maior = A, C, B
elif B <= A <= C:
    menor, meio, maior = B, A, C
elif B <= C <= A:
    menor, meio, maior = B, C, A
elif C <= A <= B:
    menor, meio, maior = C, A, B
else:  # C <= B <= A
    menor, meio, maior = C, B, A

print(f"Valores em ordem ascendente: {menor}, {meio}, {maior}")
