# Algoritmo que determina se um número inteiro é PAR ou ÍMPAR

# Lê um número inteiro do usuário
N = int(input("Digite um número inteiro: "))

# Verifica se o número é par ou ímpar usando o operador módulo (%)
if N % 2 == 0:
    print(f"O número {N} é PAR.")
else:
    print(f"O número {N} é ÍMPAR.")