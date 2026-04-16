# ========================================
# LISTA 25 - Exercício de Média Ponderada
# Objetivo: Calcular média ponderada de três notas com pesos diferentes
# ========================================

# Recebe as três notas do usuário
nota1 = float(input("Insira a nota 1: "))
nota2 = float(input("Insira a nota 2: "))
nota3 = float(input("Insira a nota 3: "))

# Calcula a média ponderada: (nota1×2 + nota2×3 + nota3×5) / 10
resultado = ((nota1 * 2) + (nota2 * 3) + (nota3 * 5)) / 10

# Exibe o resultado da média ponderada
print ("Sua nota é: " , resultado)