# Exercício 4: Algoritmo para determinar se um número é POSITIVO, NEGATIVO ou NULO

# Lê um número do usuário
N = float(input("Digite um número: "))

# Verifica se o número é positivo, negativo ou nulo
if N > 0:
    print(f"O número {N} é POSITIVO.")
elif N < 0:
    print(f"O número {N} é NEGATIVO.")
else:
    print(f"O número {N} é NULO.")
