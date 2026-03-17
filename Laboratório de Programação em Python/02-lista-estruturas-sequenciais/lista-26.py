# ========================================
# LISTA 26 - Exercício de Algoritmo de Dígito Verificador
# Objetivo: Implementar algoritmo para gerar dígito verificador de conta
# ========================================

# Define o número da conta (exemplo: 235)
conta = 235

# Extrai cada dígito da conta usando divisão inteira e módulo
centena = conta // 100        # 235 // 100 = 2
dezena  = (conta // 10) % 10  # (235 // 10) % 10 = 23 % 10 = 3
unidade = conta % 10          # 235 % 10 = 5

# Inverte os dígitos: unidade vira centena, centena vira unidade
inverso = unidade * 100 + dezena * 10 + centena  # 5×100 + 3×10 + 2 = 532

# Soma o número original com o número invertido
soma = conta + inverso    # 235 + 532 = 767

# Extrai os dígitos da soma para cálculo ponderado
d1 = soma // 100         # 767 // 100 = 7
d2 = (soma // 10) % 10   # (767 // 10) % 10 = 76 % 10 = 6
d3 = soma % 10           # 767 % 10 = 7

# Calcula o resultado ponderado: d1×1 + d2×2 + d3×3
total = d1*1 + d2*2 + d3*3  # 7×1 + 6×2 + 7×3 = 7 + 12 + 21 = 40

# Calcula o dígito verificador (resto da divisão por 10)
digito_verificador = total % 10  # 40 % 10 = 0

# Exibe todos os resultados do algoritmo
print("Conta:", conta)
print("Inverso:", inverso)
print("Soma:", soma)
print("Resultado ponderado:", total)
print("Dígito verificador:", digito_verificador)


