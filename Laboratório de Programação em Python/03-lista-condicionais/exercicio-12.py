# Exercício 12: Algoritmo para verificar se empréstimo pode ser concedido

# Lê o salário bruto e valor da prestação
salario_bruto = float(input("Digite o salário bruto: R$ "))
valor_prestacao = float(input("Digite o valor da prestação: R$ "))

# Calcula 30% do salário bruto
limite_prestacao = salario_bruto * 0.30

# Verifica se o empréstimo pode ser concedido
if valor_prestacao <= limite_prestacao:
    print("Empréstimo pode ser concedido.")
    print(f"Valor da prestação: R$ {valor_prestacao:.2f}")
    print(f"Limite máximo (30% do salário): R$ {limite_prestacao:.2f}")
else:
    print("Empréstimo não pode ser concedido.")
    print(f"Valor da prestação: R$ {valor_prestacao:.2f}")
    print(f"Limite máximo (30% do salário): R$ {limite_prestacao:.2f}")
    print(f"Valor excedente: R$ {valor_prestacao - limite_prestacao:.2f}")
