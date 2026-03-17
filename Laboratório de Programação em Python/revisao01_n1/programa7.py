#Solicite um ano ao usuário e informe se ele é bissexto.
ano = int(input('Informe o ano: '))


if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
    print('Bissexto')

else:
    print('Não Bissexto')

