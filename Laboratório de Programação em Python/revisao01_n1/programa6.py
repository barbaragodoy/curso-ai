produto = float(input('Digite o valor do produto: '))


print("\nEscolha a forma de pagamento:")
print("1 - À Vista em Dinheiro ou Pix (15% de desconto)")
print("2 - À Vista no cartão de crédito (10% de desconto)")
print("3 - Parcelado em 2x no cartão (sem juros)")
print("4 - Parcelado em 3x ou mais no cartão (com 10% de juros)")


codigo = int(input('Digite a forma de pagamento: '))

if codigo == 1:
    valor_final = produto - (produto * 0.15)
elif codigo == 2:
    valor_final = produto - (produto * 0.10)
elif codigo == 3:
    valor_final = produto
elif codigo == 4:
    valor_final = produto + (produto * 0.10)

else:
    print('Codigo invalido')

print('O valor final do produto será:', valor_final)