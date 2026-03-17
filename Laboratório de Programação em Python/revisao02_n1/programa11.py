# Programa 7: Imprimir os 100 primeiros números ímpares
print("Os 100 primeiros números ímpares:")
contador = 0
numero = 1
while contador < 100:
    if numero % 2 == 1:  # Se é ímpar
        print(numero)
        contador += 1
    numero += 1

