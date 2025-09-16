# Algoritmo que lê dois valores inteiros, efetua a adição e apresenta o resultado se for maior que 10

# Lê dois valores inteiros do usuário
valor1 = int(input("Digite o primeiro valor inteiro: "))
valor2 = int(input("Digite o segundo valor inteiro: "))

# Efetua a adição
resultado = valor1 + valor2

# Verifica se o resultado é maior que 10 e apresenta
if resultado > 10:
    print(f"A soma de {valor1} + {valor2} = {resultado}")
    print(f"O resultado {resultado} é maior que 10.")
else:
    print(f"A soma de {valor1} + {valor2} = {resultado}")
    print(f"O resultado {resultado} não é maior que 10.")