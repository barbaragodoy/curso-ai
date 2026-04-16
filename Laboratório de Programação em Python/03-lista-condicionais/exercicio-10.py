# Exercício 10: Algoritmo que imprime o menor e maior valor de dois números

# Lê dois números do usuário
A = float(input("Digite o primeiro número (A): "))
B = float(input("Digite o segundo número (B): "))

# Determina o menor e maior valor
if A > B:
    maior = A
    menor = B
else:
    maior = B
    menor = A

print(f"O menor valor é: {menor}")
print(f"O maior valor é: {maior}")
