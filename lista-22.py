

num_carros_vendidos = int(input("Digite o número de carros vendidos: "))
valor_total_vendas = float(input("Digite o valor total das vendas: "))
salario_fixo = float(input("Digite o salário fixo: "))
comissao_por_carro = float(input("Digite o valor da comissão por carro vendido: "))


comissao_carros = num_carros_vendidos * comissao_por_carro


comissao_vendas = valor_total_vendas * 0.05


salario_final = salario_fixo + comissao_carros + comissao_vendas


print(f"O salário final do vendedor é R$: {salario_final:.2f}")