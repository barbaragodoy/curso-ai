# Exercício 11: Algoritmo que verifica se um número é divisível por 3 e por 7

# Lê um número do usuário
numero = int(input("Digite um número inteiro: "))

# Verifica se é divisível por 3 e por 7
if numero % 3 == 0 and numero % 7 == 0:
    print(f"O número {numero} é divisível por 3 e por 7.")
else:
    print(f"O número {numero} não é divisível por 3 e por 7.")
