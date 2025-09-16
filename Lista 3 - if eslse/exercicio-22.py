# Exercício 22: Algoritmo que classifica pessoa por idade

# Lê a idade do usuário
idade = int(input("Digite a idade: "))

# Classifica a pessoa
if idade >= 65:
    classificacao = "pessoa idosa (idade superior ou igual a 65 anos)"
elif idade >= 18:
    classificacao = "maior de idade"
else:
    classificacao = "menor de idade"

print(f"Classificação: {classificacao}")
