# Programa 15: Determinar se dois valores inteiros e positivos A e B são primos entre si
def mdc(a, b):
    """Calcula o máximo divisor comum entre dois números"""
    while b:
        a, b = b, a % b
    return a

A = int(input("Digite o valor de A (inteiro e positivo): "))
B = int(input("Digite o valor de B (inteiro e positivo): "))

if A <= 0 or B <= 0:
    print("Erro: Os números devem ser positivos!")
else:
    if mdc(A, B) == 1:
        print(f"{A} e {B} são primos entre si (MDC = 1)")
    else:
        print(f"{A} e {B} NÃO são primos entre si (MDC = {mdc(A, B)})")

