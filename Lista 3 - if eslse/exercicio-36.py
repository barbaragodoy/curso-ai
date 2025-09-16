# Exercício 36: Algoritmo que calcula preço da passagem por destino e tipo de viagem

# Lê o destino e tipo de viagem
print("Destinos disponíveis:")
print("1 - Região Norte")
print("2 - Região Nordeste")
print("3 - Região Centro-Oeste")
print("4 - Região Sul")

destino = int(input("Digite o número do destino (1-4): "))
tipo_viagem = input("A viagem inclui retorno? (s/n): ").lower()

# Define os preços baseados no destino
if destino == 1:  # Norte
    preco_ida = 500.00
    preco_ida_volta = 900.00
elif destino == 2:  # Nordeste
    preco_ida = 350.00
    preco_ida_volta = 650.00
elif destino == 3:  # Centro-Oeste
    preco_ida = 350.00
    preco_ida_volta = 600.00
elif destino == 4:  # Sul
    preco_ida = 300.00
    preco_ida_volta = 550.00
else:
    print("Destino inválido!")
    exit()

# Calcula o preço final
if tipo_viagem == 's':
    preco_final = preco_ida_volta
    tipo = "Ida e Volta"
else:
    preco_final = preco_ida
    tipo = "Ida"

print(f"Tipo de viagem: {tipo}")
print(f"Preço da passagem: R$ {preco_final:.2f}")
