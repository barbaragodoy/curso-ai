# Exercício 6: Programa para ler 6 valores inteiros e mostrar na ordem inversa
# 
# Descrição do exercício:
# Crie um programa que leia 6 valores inteiros e, em seguida, mostre na tela os
# valores lidos na ordem inversa. Utilizar laço de repetição e vetor(lista).

# Criando lista vazia para armazenar os valores
valores = []

print("Digite 6 valores inteiros:")

# Lendo os 6 valores inteiros
for i in range(6):
    valor = int(input(f"Digite o {i+1}º valor inteiro: "))
    valores.append(valor)

# Mostrando os valores na ordem inversa usando laço de repetição
print(f"\nValores digitados: {valores}")
print("Valores na ordem inversa:")

for i in range(len(valores) - 1, -1, -1):
    print(f"Posição {i}: {valores[i]}")

# Alternativa usando reverse()
print("\nUsando método reverse():")
valores_inversos = valores.copy()
valores_inversos.reverse()
print(f"Valores na ordem inversa: {valores_inversos}")
