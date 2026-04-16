# Exercício 25: Algoritmo que calcula valor do plano de saúde por idade

# Lê a idade da pessoa
idade = int(input("Digite a idade: "))

# Determina o valor do plano baseado na idade
if idade <= 10:
    valor = 30.00
elif 11 <= idade <= 29:
    valor = 60.00
elif 30 <= idade <= 45:
    valor = 120.00
elif 46 <= idade <= 59:
    valor = 150.00
elif 60 <= idade <= 65:
    valor = 250.00
else:  # idade > 65
    valor = 400.00

print(f"Valor do plano de saúde: R$ {valor:.2f}")
