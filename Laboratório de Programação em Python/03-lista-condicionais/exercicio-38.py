# Exercício 38: Algoritmo que verifica se IPVA vence no mês corrente

# Lê o mês atual e os dígitos da placa
mes_atual = int(input("Digite o número do mês atual (1-12): "))
placa = input("Digite os 4 dígitos da placa: ")

# Extrai o último dígito da placa
ultimo_digito = int(placa[-1])

# Determina o mês de vencimento do IPVA
if ultimo_digito == 1:
    mes_vencimento = 1
elif ultimo_digito == 2:
    mes_vencimento = 2
elif ultimo_digito == 3:
    mes_vencimento = 3
elif ultimo_digito == 4:
    mes_vencimento = 4
elif ultimo_digito == 5:
    mes_vencimento = 5
elif ultimo_digito == 6:
    mes_vencimento = 6
elif ultimo_digito == 7:
    mes_vencimento = 7
elif ultimo_digito == 8:
    mes_vencimento = 8
elif ultimo_digito == 9:
    mes_vencimento = 9
else:  # ultimo_digito == 0
    mes_vencimento = 10

# Verifica se o IPVA vence no mês corrente
if mes_atual == mes_vencimento:
    print(f"O IPVA da placa {placa} vence no mês {mes_atual} (mês corrente).")
else:
    print(f"O IPVA da placa {placa} vence no mês {mes_vencimento} (não é o mês corrente).")
