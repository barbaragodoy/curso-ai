
ano = int(input('Digite o ano desejado: '))

if ano % 400 == 0:
    print('Bissexto Especial')

elif (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
    print('Bissexto')


else:
    print('Não Bissexto')