# Exercício 15: Algoritmo que imprime três valores em ordem descendente

# Lê três valores do usuário
A = float(input("Digite o primeiro valor (A): "))
B = float(input("Digite o segundo valor (B): "))
C = float(input("Digite o terceiro valor (C): "))

# Ordena os valores em ordem descendente
if A >= B >= C:
    maior, meio, menor = A, B, C
elif A >= C >= B:
    maior, meio, menor = A, C, B
elif B >= A >= C:
    maior, meio, menor = B, A, C
elif B >= C >= A:
    maior, meio, menor = B, C, A
elif C >= A >= B:
    maior, meio, menor = C, A, B
else:  # C >= B >= A
    maior, meio, menor = C, B, A

print(f"Valores em ordem descendente: {maior}, {meio}, {menor}")
