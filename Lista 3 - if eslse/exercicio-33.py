# Exercício 33: Algoritmo que calcula f(x) = 1/(x-1)

# Lê o valor de x
x = float(input("Digite o valor de x: "))

# Verifica se x-1 é diferente de zero
if x - 1 != 0:
    fx = 1 / (x - 1)
    print(f"f({x}) = 1/({x}-1) = {fx}")
else:
    print(f"f({x}) = 1/({x}-1) = Indefinido (divisão por zero)")
