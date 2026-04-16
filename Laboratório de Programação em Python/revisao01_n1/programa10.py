
peso_pacote = float(input("Digite o peso do pacote (em kg): "))
distancia = float(input("Digite a distância (em km): "))


if peso_pacote <= 1:
    taxa_por_km = 5.00
elif peso_pacote <= 5:
    taxa_por_km = 10.00
else:
    taxa_por_km = 20.00


custo_total = taxa_por_km * distancia


print(f"\nPeso do pacote: {peso_pacote} kg")
print(f"Distância: {distancia} km")
print(f"Taxa por km: R$ {taxa_por_km:.2f}")
print(f"Custo total do frete: R$ {custo_total:.2f}")