# Programa 12: Ler dez números inteiros e imprimir o maior e o menor número da lista
print("Digite 10 números inteiros:")

maior = None
menor = None

for i in range(10):
    numero = int(input(f"Digite o {i+1}º número: "))
    
    if maior is None or numero > maior:
        maior = numero
    if menor is None or numero < menor:
        menor = numero

print(f"O maior número é: {maior}")
print(f"O menor número é: {menor}")

