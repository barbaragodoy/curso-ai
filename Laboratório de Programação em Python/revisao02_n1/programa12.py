# Programa 8: Receber dez números do usuário e imprimir a metade de cada número
print("Digite 10 números:")
for i in range(10):
    numero = float(input(f"Digite o {i+1}º número: "))
    metade = numero / 2
    print(f"A metade de {numero} é {metade:.2f}")

