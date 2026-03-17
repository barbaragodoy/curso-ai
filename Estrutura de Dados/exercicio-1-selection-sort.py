#Selection Sort

# Parte 1 – Utilizando função:
def selectionSort(vet):
    for i in range(len(vet) - 1):
        menor = i
        for j in range(i + 1, len(vet)):
            if vet[j] < vet[menor]:
                menor = j
        # Troca apenas se necessário
        if menor != i:
            vet[i], vet[menor] = vet[menor], vet[i]

valores = [64, 25, 12, 22, 11]
selectionSort(valores)
print("Vetor ordenado usando Selection Sort (função):", valores)

# Parte 2 – Sem utilizar função:
vetor = [64, 25, 12, 22, 11]

for i in range(len(vetor) - 1):
    menor = i
    for j in range(i + 1, len(vetor)):
        if vetor[j] < vetor[menor]:
            menor = j
    if menor != i:
        vetor[i], vetor[menor] = vetor[menor], vetor[i]

print("Vetor ordenado usando Selection Sort (direto):", vetor)