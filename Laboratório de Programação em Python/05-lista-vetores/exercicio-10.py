# Exercício 10: Programa para ler 10 números diferentes sem repetição
# 
# Descrição do exercício:
# Faça um programa para ler 10 números DIFERENTES a serem armazenados em
# um vetor(lista). Os dados deverão ser armazenados no vetor(lista) na ordem que
# forem sendo lidos, sendo que caso o usuário digite um número que já foi digitado
# anteriormente, o programa deverá pedir para ele digitar outro número. Note que
# cada valor digitado pelo usuário deve ser pesquisado no vetor(lista), verificando
# se ele existe entre os números que já foram fornecidos. Exibir na tela o vetor(lista)
# final que foi digitado, ou seja, sem nenhuma repetição.

# Criando lista vazia para armazenar os números únicos
numeros = []

print("Digite 10 números diferentes:")

# Lendo os 10 números diferentes
for i in range(10):
    while True:
        numero = int(input(f"Digite o {i+1}º número: "))
        
        # Verificando se o número já existe no vetor
        if numero in numeros:
            print(f"Número {numero} já foi digitado! Digite outro número.")
        else:
            numeros.append(numero)
            break

# Exibindo o vetor final
print(f"\nVetor final com números únicos: {numeros}")
print(f"Quantidade de números únicos: {len(numeros)}")

# Mostrando cada número com sua posição
print("\nNúmeros digitados:")
for i in range(len(numeros)):
    print(f"Posição {i}: {numeros[i]}")
