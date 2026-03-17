# Exercício 39: Algoritmo que calcula peso em diferentes planetas

# Lê o peso na Terra e o número do planeta
peso_terra = float(input("Digite seu peso na Terra (em kg): "))

print("Planetas disponíveis:")
print("1 - Mercúrio (gravidade: 0,37)")
print("2 - Vênus (gravidade: 0,88)")
print("3 - Marte (gravidade: 0,38)")
print("4 - Júpiter (gravidade: 2,64)")
print("5 - Saturno (gravidade: 1,15)")
print("6 - Urano (gravidade: 1,17)")

planeta = int(input("Digite o número do planeta (1-6): "))

# Define a gravidade relativa do planeta escolhido
if planeta == 1:
    gravidade_relativa = 0.37
    nome_planeta = "Mercúrio"
elif planeta == 2:
    gravidade_relativa = 0.88
    nome_planeta = "Vênus"
elif planeta == 3:
    gravidade_relativa = 0.38
    nome_planeta = "Marte"
elif planeta == 4:
    gravidade_relativa = 2.64
    nome_planeta = "Júpiter"
elif planeta == 5:
    gravidade_relativa = 1.15
    nome_planeta = "Saturno"
elif planeta == 6:
    gravidade_relativa = 1.17
    nome_planeta = "Urano"
else:
    print("Planeta inválido!")
    exit()

# Calcula o peso no planeta escolhido
peso_planeta = peso_terra * gravidade_relativa

print(f"Peso na Terra: {peso_terra:.2f} kg")
print(f"Peso em {nome_planeta}: {peso_planeta:.2f} kg")
