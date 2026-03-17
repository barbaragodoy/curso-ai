#Bubble Sort

def bubbleSort(vet):
    # Índices i em ordem decrescente
    for i in range(len(vet) - 1, 0, -1):
        # Troca com o elemento da posição i
        for j in range(i):
            if vet[j] > vet[j + 1]:
                vet[j], vet[j + 1] = vet[j + 1], vet[j]

# Parte 1 – Utilizando função
valores = [64, 25, 12, 22, 11]
bubbleSort(valores)
print("Vetor ordenado usando função:", valores)

# Parte 2 – Sem utilizar função
vetor = [64, 25, 12, 22, 11]

for i in range(len(vetor) - 1, 0, -1):
    for j in range(i):
        if vetor[j] > vetor[j + 1]:
            vetor[j], vetor[j + 1] = vetor[j + 1], vetor[j]

print("Vetor ordenado sem função:", vetor)