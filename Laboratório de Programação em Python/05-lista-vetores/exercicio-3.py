# Exercício 3: Programa para encontrar maior e menor elemento em vetor de 20 posições
# 
# Descrição do exercício:
# Faça um programa que receba do usuário um vetor(lista) com 20 posições. Em
# seguida deverá ser impresso o maior e o menor elemento do vetor(lista).

# Criando lista vazia para armazenar os números
vetor = []

print("Digite 20 números:")

# Lendo os 20 números
for i in range(20):
    numero = float(input(f"Digite o {i+1}º número: "))
    vetor.append(numero)

# Encontrando o maior e menor elemento
maior = vetor[0]
menor = vetor[0]

for numero in vetor:
    if numero > maior:
        maior = numero
    if numero < menor:
        menor = numero

# Imprimindo os resultados
print(f"\nVetor digitado: {vetor}")
print(f"Maior elemento: {maior}")
print(f"Menor elemento: {menor}")
