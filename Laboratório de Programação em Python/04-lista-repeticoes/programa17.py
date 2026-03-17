# Programa 17: Determinar todos os divisores de um dado número N
N = int(input("Digite um número para encontrar seus divisores: "))

print(f"Divisores de {N}:")
divisores = []

for i in range(1, N + 1):
    if N % i == 0:
        divisores.append(i)
        print(i)

print(f"Total de divisores: {len(divisores)}")

