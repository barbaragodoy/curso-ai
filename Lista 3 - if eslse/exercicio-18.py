# Exercício 18: Algoritmo que verifica em qual intervalo um número se encontra

# Lê um número do usuário
numero = float(input("Digite um número: "))

# Verifica em qual intervalo o número se encontra
if numero == 5:
    print(f"O número {numero} é igual a 5.")
elif numero == 200:
    print(f"O número {numero} é igual a 200.")
elif numero == 400:
    print(f"O número {numero} é igual a 400.")
elif 500 <= numero <= 1000:
    print(f"O número {numero} está no intervalo entre 500 e 1000 (inclusive).")
else:
    print(f"O número {numero} está fora dos escopos anteriores.")
