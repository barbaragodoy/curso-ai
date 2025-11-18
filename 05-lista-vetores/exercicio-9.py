# Exercício 9: Programa para analisar números pares e ímpares
# 
# Descrição do exercício:
# Implemente um programa que receba 10 números inteiros e mostre:
# • Os números pares digitados;
# • A soma dos números pares digitados;
# • Os números ímpares digitados;
# • A quantidade de números ímpares digitados;

# Criando lista vazia para armazenar os números
numeros = []

print("Digite 10 números inteiros:")

# Lendo os 10 números inteiros
for i in range(10):
    numero = int(input(f"Digite o {i+1}º número inteiro: "))
    numeros.append(numero)

# Separando números pares e ímpares
numeros_pares = []
numeros_impares = []

for numero in numeros:
    if numero % 2 == 0:
        numeros_pares.append(numero)
    else:
        numeros_impares.append(numero)

# Calculando a soma dos números pares
soma_pares = sum(numeros_pares)

# Calculando a quantidade de números ímpares
quantidade_impares = len(numeros_impares)

# Imprimindo os resultados
print(f"\nNúmeros digitados: {numeros}")
print(f"Números pares digitados: {numeros_pares}")
print(f"Soma dos números pares: {soma_pares}")
print(f"Números ímpares digitados: {numeros_impares}")
print(f"Quantidade de números ímpares: {quantidade_impares}")
