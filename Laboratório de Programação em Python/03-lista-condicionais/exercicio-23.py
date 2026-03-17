# Exercício 23: Algoritmo que determina classe eleitoral

# Lê a idade do usuário
idade = int(input("Digite a idade: "))

# Determina a classe eleitoral
if idade < 16:
    classe = "não eleitor (abaixo de 16 anos)"
elif 16 <= idade < 18 or idade >= 65:
    classe = "eleitor facultativo (de 16 até 18 anos e maior de 65 anos, inclusive)"
else:  # 18 <= idade < 65
    classe = "eleitor obrigatório (entre a faixa de 18 e menor de 65 anos)"

print(f"Classe eleitoral: {classe}")
