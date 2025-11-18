# ========================================
# LISTA 23 - Exercício de Cálculo de Salário do Vendedor
# Objetivo: Calcular o salário final incluindo comissões
# ========================================

# Recebe os dados de vendas e salário
num_carros_vendidos = int(input("Digite o número de carros vendidos: "))
valor_total_vendas = float(input("Digite o valor total das vendas: "))
salario_fixo = float(input("Digite o salário fixo: "))
comissao_por_carro = float(input("Digite o valor da comissão por carro vendido: "))

# Calcula a comissão pelos carros vendidos
comissao_carros = num_carros_vendidos * comissao_por_carro

# Calcula a comissão sobre o valor total das vendas (5%)
comissao_vendas = valor_total_vendas * 0.05

# Calcula o salário final somando todas as comissões
salario_final = salario_fixo + comissao_carros + comissao_vendas

# Exibe o salário final calculado
print(f"O salário final do vendedor é R$: {salario_final:.2f}")