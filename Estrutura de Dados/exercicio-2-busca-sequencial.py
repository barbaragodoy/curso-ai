
# Exercício 2 — Busca Binária
# Encontre o Número no Vetor Ordenado

# Dado o vetor já ordenado:

numeros = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

def busca_binaria(lista, alvo):
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1

numero_busca = int(input("Digite o número alvo: "))
resultado = busca_binaria(numeros, numero_busca)
if resultado != -1:
    print(f"{numero_busca} encontrado na posição {resultado}")
else:
    print(f"{numero_busca} não encontrado")

   
    
