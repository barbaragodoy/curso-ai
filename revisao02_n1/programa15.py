# Programa 11: Ler um número NUM, depois ler NUM números inteiros e imprimir o maior e o menor
NUM = int(input("Digite quantos números você quer ler: "))
print(f"Agora digite {NUM} números inteiros:")

maior = None
menor = None

for i in range(NUM):
    numero = int(input(f"Digite o {i+1}º número: "))
    
    if maior is None or numero > maior:
        maior = numero
    if menor is None or numero < menor:
        menor = numero

print(f"O maior número é: {maior}")
print(f"O menor número é: {menor}")

