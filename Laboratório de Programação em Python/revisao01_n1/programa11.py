import math

numero = int(input('Digite o numero: '))

print("sqrt - Raiz quadrada")
print("pow2 - Elevar ao quadrado")
print("pow3 - Elevar ao cubo)")
print("log - Elevar ao cubo)")
print("exp - exponencial")


operacao = input('Digite a operação: ')

if operacao == 'sqrt':
    numero_final = math.sqrt(numero)
elif operacao == 'pow2':
    numero_final = (numero * numero)
elif operacao == 'pow3':
    numero_final = (numero * numero * numero)
elif operacao == 'log':
    numero_final = math.log(numero)
    if numero <= 0:
        print("Erro: logaritmo não pode ser calculado para números <= 0.")
        numero_final = None
    else:
        numero_final = math.log(numero)
elif operacao == 'exp':
    numero_final = math.exp(numero)


else:
    print('Resultado invalido')

print('O resultado é:', numero_final)