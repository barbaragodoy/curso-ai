# Exercício 16: Algoritmo que verifica divisibilidade por 10, 5 ou 2

# Lê um número do usuário
numero = int(input("Digite um número inteiro: "))

# Verifica divisibilidade
divisivel_por_10 = numero % 10 == 0
divisivel_por_5 = numero % 5 == 0
divisivel_por_2 = numero % 2 == 0

# Imprime o resultado
if divisivel_por_10:
    print(f"O número {numero} é divisível por 10.")
elif divisivel_por_5:
    print(f"O número {numero} é divisível por 5.")
elif divisivel_por_2:
    print(f"O número {numero} é divisível por 2.")
else:
    print(f"O número {numero} não é divisível por 10, 5 ou 2.")
