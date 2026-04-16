# Programa 13: Ler limites inferior e superior e imprimir números pares no intervalo aberto e seu somatório
limite_inferior = int(input("Digite o limite inferior: "))
limite_superior = int(input("Digite o limite superior: "))

print(f"Números pares no intervalo aberto ({limite_inferior}, {limite_superior}):")
soma_pares = 0

for i in range(limite_inferior + 1, limite_superior):  # Intervalo aberto
    if i % 2 == 0:  # Se é par
        print(i)
        soma_pares += i

print(f"Somatório dos números pares: {soma_pares}")

