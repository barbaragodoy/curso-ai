# Exercício 20: Algoritmo para calcular IMC e determinar situação do peso

# Lê peso e altura do usuário
peso = float(input("Digite o peso (em kg): "))
altura = float(input("Digite a altura (em metros): "))

# Calcula o IMC
imc = peso / (altura ** 2)

# Determina a situação do peso
if imc < 20:
    situacao = "Abaixo do peso"
elif 20 <= imc < 25:
    situacao = "Peso Normal"
elif 25 <= imc < 30:
    situacao = "Sobre Peso"
elif 30 <= imc < 40:
    situacao = "Obeso"
else:  # imc >= 40
    situacao = "Obeso Mórbido"

print(f"IMC: {imc:.2f}")
print(f"Situação: {situacao}")
