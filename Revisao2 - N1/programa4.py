n1 = float(input('Digite seu número: '))
n2 = float(input('Digite seu número: '))
n3 = float(input('Digite seu número: '))

maior = max(n1, n2, n3)
menor = min(n1, n2, n3)


if n1 != maior and n1 != menor:
    meio = n1
elif n2 != maior and n2 != menor:
    meio = n2
else:
    meio = n3



print(f"Maior: {maior}")
print(f"Meio: {meio}")
print(f"Menor: {menor}")