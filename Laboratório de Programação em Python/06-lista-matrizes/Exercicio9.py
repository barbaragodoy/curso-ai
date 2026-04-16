# Total de vendas por mês, semana e ano
# Crie um algoritmo que carregue uma matriz 12 x 4 com os valores de vendas de uma loja,
# onde cada linha representa um mês do ano e cada coluna, uma semana do mês (considere 4 semanas por mês).
# Calcule e imprima:
# - O total vendido em cada mês do ano;
# - O total vendido em cada semana durante todo o ano;
# - O total vendido no ano.

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

vendas = []
print("Digite os valores de vendas (12 meses x 4 semanas):")
for i in range(12):
    print(f"\n{meses[i]}:")
    linha = []
    for j in range(4):
        valor = float(input(f"  Vendas da semana {j+1}: R$ "))
        linha.append(valor)
    vendas.append(linha)

# Calcula o total vendido em cada mês
total_por_mes = []
for i in range(12):
    soma = 0
    for j in range(4):
        soma += vendas[i][j]
    total_por_mes.append(soma)

# Calcula o total vendido em cada semana durante todo o ano
total_por_semana = []
for j in range(4):
    soma = 0
    for i in range(12):
        soma += vendas[i][j]
    total_por_semana.append(soma)

# Calcula o total vendido no ano
total_ano = sum(total_por_mes)

# Exibe os resultados
print("\n" + "="*60)
print("RELATÓRIO DE VENDAS")
print("="*60)

print("\nTotal vendido em cada mês do ano:")
for i in range(12):
    print(f"  {meses[i]}: R$ {total_por_mes[i]:.2f}")

print("\nTotal vendido em cada semana durante todo o ano:")
for j in range(4):
    print(f"  Semana {j+1}: R$ {total_por_semana[j]:.2f}")

print(f"\nTotal vendido no ano: R$ {total_ano:.2f}")

