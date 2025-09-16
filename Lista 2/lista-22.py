# ========================================
# LISTA 22 - Exercício de Cálculo de Área do Círculo
# Objetivo: Calcular a área de um círculo dado o raio
# ========================================

# Recebe o raio do círculo
raio = float(input("Digite o raio do círculo: "))

# Define o valor de pi (aproximação)
pi = 3.14159

# Calcula a área do círculo usando a fórmula: A = π × r²
area = pi * (raio ** 2)

# Exibe o resultado da área
print(f"A área do círculo é: {area:.2f}")