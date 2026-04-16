# ========================================
# ARQUIVO DE AULA - Conceitos Básicos de Python
# Objetivo: Demonstrar diferentes tipos de entrada e saída
# ========================================

# Exemplo 1: Entrada e saída de texto (string)
nome = input ("Digite seu nome: ")
print ("Olá," , nome)

# Exemplo 2: Entrada de número inteiro e operação matemática
idade = int(input("Digite sua idade: "))
print ("Daqui a 5 anos, você terá", idade + 5, "anos.")

# Exemplo 3: Entrada de número decimal (float)
altura = float(input("Digite sua altura (em metros): "))
print ("Sua altura é" , altura, "metros")

# Exemplo 4: Concatenação de strings
cidade = input ("Digite sua cidade: ")
print ("Você mora em" , cidade + "!")

# Exemplo 5: Entrada de texto com comparação booleana
resposta = input ("Você gosta de Python? (sim/não): ").lower() == "sim"
print("Resposta:" , resposta)

