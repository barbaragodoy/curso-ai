# Exercício 4: Programa para ler 15 valores e mostrar posição do maior e menor
# 
# Descrição do exercício:
# Fazer um programa para ler 15 valores e, em seguida, mostrar o valor e a posição
# onde se encontram o maior e o menor valor.

# Criando lista vazia para armazenar os valores
valores = []

print("Digite 15 valores:")

# Lendo os 15 valores
for i in range(15):
    valor = float(input(f"Digite o {i+1}º valor: "))
    valores.append(valor)

# Encontrando o maior e menor valor e suas posições
maior_valor = valores[0]
menor_valor = valores[0]
posicao_maior = 0
posicao_menor = 0

for i in range(len(valores)):
    if valores[i] > maior_valor:
        maior_valor = valores[i]
        posicao_maior = i
    if valores[i] < menor_valor:
        menor_valor = valores[i]
        posicao_menor = i

# Imprimindo os resultados
print(f"\nValores digitados: {valores}")
print(f"Maior valor: {maior_valor} (posição {posicao_maior})")
print(f"Menor valor: {menor_valor} (posição {posicao_menor})")
