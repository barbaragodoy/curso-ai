# Exercício 17: Algoritmo que verifica se um número está entre 20 e 90

# Lê um número do usuário
numero = float(input("Digite um número: "))

# Verifica se está no intervalo (20 e 90 não estão incluídos)
if 20 < numero < 90:
    print(f"O número {numero} está compreendido entre 20 e 90.")
else:
    print(f"O número {numero} não está compreendido entre 20 e 90.")
