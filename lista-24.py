# ========================================
# LISTA 24 - Exercício de Troca de Valores
# Objetivo: Trocar os valores de duas variáveis usando variável temporária
# ========================================

# Define os valores iniciais das variáveis
A = 10
B = 20

# Realiza a troca usando uma variável temporária
temp = A   # Guarda o valor de A temporariamente
A = B      # A recebe o valor de B
B = temp   # B recebe o valor que estava em A

# Exibe os valores finais após a troca
print("O valor final de A é:", A)
print("O valor final de B é:", B)