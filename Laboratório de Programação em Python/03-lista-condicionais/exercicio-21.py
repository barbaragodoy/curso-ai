# Exercício 21: Algoritmo para calcular crédito CEF baseado no saldo médio

# Lê o saldo médio do usuário
saldo_medio = float(input("Digite o saldo médio do último ano: R$ "))

# Calcula o valor do crédito baseado na tabela
if saldo_medio <= 500:
    percentual = 0
    valor_credito = 0
    mensagem = "Nenhum crédito"
elif saldo_medio <= 1000:
    percentual = 30
    valor_credito = saldo_medio * 0.30
    mensagem = "30% do valor do saldo médio"
elif saldo_medio <= 3000:
    percentual = 40
    valor_credito = saldo_medio * 0.40
    mensagem = "40% do valor do saldo médio"
else:  # saldo_medio > 3000
    percentual = 50
    valor_credito = saldo_medio * 0.50
    mensagem = "50% do valor do saldo médio"

print(f"Saldo médio: R$ {saldo_medio:.2f}")
print(f"Percentual: {percentual}%")
print(f"Valor do crédito: R$ {valor_credito:.2f}")
print(f"Observação: {mensagem}")
