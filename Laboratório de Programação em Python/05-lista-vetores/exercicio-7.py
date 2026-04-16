# Exercício 7: Programa para ler vetor de 5 posições e código para mostrar ordem direta/inversa
# 
# Descrição do exercício:
# Faça um programa que leia um vetor(lista) de 5 posições para números reais e,
# depois, um código inteiro. Se o código lido for zero, finalize o programa; se for 1,
# mostre o vetor(lista) na ordem direta; se for 2, mostre o vetor(lista) na ordem
# inversa. Caso o código for diferente de 1 e 2 escreva uma mensagem informando
# que o código é inválido.

# Criando lista vazia para armazenar os números reais
vetor = []

print("Digite 5 números reais:")

# Lendo os 5 números reais
for i in range(5):
    numero = float(input(f"Digite o {i+1}º número real: "))
    vetor.append(numero)

# Lendo o código
print("\nDigite o código:")
print("0 - Finalizar programa")
print("1 - Mostrar vetor na ordem direta")
print("2 - Mostrar vetor na ordem inversa")
codigo = int(input("Código: "))

# Processando o código
if codigo == 0:
    print("Programa finalizado.")
elif codigo == 1:
    print(f"Vetor na ordem direta: {vetor}")
elif codigo == 2:
    vetor_inverso = vetor.copy()
    vetor_inverso.reverse()
    print(f"Vetor na ordem inversa: {vetor_inverso}")
else:
    print("Código inválido!")
