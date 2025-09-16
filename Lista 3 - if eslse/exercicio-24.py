# Exercício 24: Algoritmo que determina categoria de nadador por idade

# Lê a idade do nadador
idade = int(input("Digite a idade do nadador: "))

# Determina a categoria
if 5 <= idade <= 7:
    categoria = "Infantil A"
elif 8 <= idade <= 10:
    categoria = "Infantil B"
elif 11 <= idade <= 13:
    categoria = "Juvenil A"
elif 14 <= idade <= 17:
    categoria = "Juvenil B"
elif idade >= 18:
    categoria = "Sênior"
else:
    categoria = "Idade não permitida para competição"

print(f"Categoria: {categoria}")
