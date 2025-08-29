# ========================================
# LISTA 14 - Exercício de Cálculo de Idade em Dias
# Objetivo: Converter idade em anos, meses e dias para total de dias
# ========================================

# Leitura da idade em anos, meses e dias
anos = int(input("Digite a quantidade de anos: "))
meses = int(input("Digite a quantidade de meses: "))
dias = int(input("Digite a quantidade de dias: "))

# Calcula o total de dias (aproximado: 1 ano = 365 dias, 1 mês = 30 dias)
total_dias = (anos * 365) + (meses * 30) + dias

# Exibe o resultado total em dias
print(f"A idade total em dias é: {total_dias} dias")