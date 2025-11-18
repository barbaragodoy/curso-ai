# Exercício 7: Algoritmo que verifica se um número é múltiplo de 3

# Lê um número do usuário
numero = int(input("Digite um número inteiro: "))

# Verifica se é múltiplo de 3
if numero % 3 == 0:
    print(f"O número {numero} é múltiplo de 3.")
else:
    print(f"O número {numero} não é múltiplo de 3.")
