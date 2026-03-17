# Exercício 13: Algoritmo que imprime o maior valor entre três números

# Lê três valores do usuário
A = float(input("Digite o primeiro valor (A): "))
B = float(input("Digite o segundo valor (B): "))
C = float(input("Digite o terceiro valor (C): "))

# Determina o maior valor
if A >= B and A >= C:
    maior = A
elif B >= A and B >= C:
    maior = B
else:
    maior = C

print(f"O maior valor é: {maior}")
