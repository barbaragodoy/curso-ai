# Exercício 5: Algoritmo que lê dois números, efetua adição e aplica regras específicas

# Lê dois números do usuário
num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))

# Efetua a adição
soma = num1 + num2

# Aplica as regras conforme o valor da soma
if soma > 20:
    resultado = soma + 8
    print(f"A soma é {soma} (maior que 20).")
    print(f"Resultado final: {resultado}")
else:
    resultado = soma - 5
    print(f"A soma é {soma} (menor ou igual a 20).")
    print(f"Resultado final: {resultado}")
