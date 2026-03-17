# Exercício 27: Algoritmo que calcula valor da venda baseado no valor da compra

# Lê o valor da compra
valor_compra = float(input("Digite o valor da compra: R$ "))

# Calcula o valor da venda baseado na tabela
if valor_compra < 20:
    valor_venda = valor_compra * 1.45  # 45% de lucro
elif valor_compra < 50:
    valor_venda = valor_compra * 1.35  # 35% de lucro
elif valor_compra < 100:
    valor_venda = valor_compra * 1.25  # 25% de lucro
else:  # valor_compra >= 100
    valor_venda = valor_compra * 1.15  # 15% de lucro

print(f"Valor da compra: R$ {valor_compra:.2f}")
print(f"Valor da venda: R$ {valor_venda:.2f}")
