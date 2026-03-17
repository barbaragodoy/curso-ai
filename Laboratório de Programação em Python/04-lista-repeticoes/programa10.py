# Programa 10: Imprimir todos os números de 1 até 100 e a média de todos eles
print("Números de 1 a 100:")
soma = 0
for i in range(1, 101):
    print(i)
    soma += i

media = soma / 100
print(f"\nA média de todos os números de 1 a 100 é: {media:.2f}")

