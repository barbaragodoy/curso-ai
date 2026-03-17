# ========================================
# LISTA 21 - Exercício de Cálculo de Custo Final do Carro
# Objetivo: Calcular o custo final de um carro incluindo impostos e distribuidor
# ========================================

# Recebe o custo de fábrica do carro
custo_fabrica = float(input("Digite o custo de fábrica do carro: "))

# Define os percentuais de lucro do distribuidor e impostos
percentual_distribuidor = 0.28  # 28% para o distribuidor
percentual_impostos = 0.45      # 45% de impostos

# Calcula o valor que vai para o distribuidor
valor_distribuidor = custo_fabrica * percentual_distribuidor

# Calcula o valor dos impostos
valor_impostos = custo_fabrica * percentual_impostos

# Calcula o custo final somando todos os valores
custo_final = custo_fabrica + valor_distribuidor + valor_impostos

# Exibe o custo final formatado
print(f"O custo final ao consumidor é: R${custo_final:.2f}")