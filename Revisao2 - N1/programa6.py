preco = float(input('Informe o valor do produto: '))

print('1 → Dinheiro ou Pix')
print('2 → Cartão à vista')
print('3 → Cartão em 2x')
print('4 → Cartão em 3x ou mais')

forma_pagamento = int(input('Selecione a forma de pagamento: '))

if forma_pagamento == 1:
    valor_pagar = preco - (preco * 0.12)
elif forma_pagamento == 2:
    valor_pagar = preco - (preco * 0.8)
elif forma_pagamento == 3:
    valor_pagar = preco 
elif forma_pagamento == 4:
    valor_pagar = preco + (preco * 0.12)

else:
    print('Codigo invalido')

print(f'Valor a pagar é: {valor_pagar}')