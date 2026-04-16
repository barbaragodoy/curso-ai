# Exercício 34: Algoritmo que calcula dosagem de medicamento por idade e peso

# Lê idade e peso do paciente
idade = int(input("Digite a idade do paciente: "))
peso = float(input("Digite o peso do paciente (em kg): "))

# Calcula a dosagem baseada na idade e peso
if idade >= 12:
    # Adultos ou adolescentes desde 12 anos
    if peso >= 60:
        dosagem_mg = 1000
    else:
        dosagem_mg = 875
else:
    # Crianças e adolescentes abaixo de 12 anos
    if 5 <= peso <= 9:
        dosagem_mg = 125
    elif 9.1 <= peso <= 16:
        dosagem_mg = 250
    elif 16.1 <= peso <= 24:
        dosagem_mg = 375
    elif 24.1 <= peso <= 30:
        dosagem_mg = 500
    else:  # peso > 30
        dosagem_mg = 750

# Calcula a quantidade de gotas
# 500 mg por ml, 1 ml = 20 gotas
ml_necessario = dosagem_mg / 500
gotas_por_dose = ml_necessario * 20

print(f"Receita Médica:")
print(f"Idade: {idade} anos")
print(f"Peso: {peso} kg")
print(f"Dosagem: {dosagem_mg} mg")
print(f"Quantidade por dose: {gotas_por_dose:.1f} gotas")
