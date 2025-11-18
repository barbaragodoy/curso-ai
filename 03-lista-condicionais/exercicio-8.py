# Exercício 8: Algoritmo que verifica se um número é divisível por 5

# Lê um número do usuário
numero = int(input("Digite um número inteiro: "))

# Verifica se é divisível por 5
if numero % 5 == 0:
    print(f"O número {numero} é divisível por 5.")
else:
    print(f"O número {numero} não é divisível por 5.")
