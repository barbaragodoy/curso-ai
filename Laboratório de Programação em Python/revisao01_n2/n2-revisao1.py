# MATRIZ DE DADOS (tabela da prova)
dados = [
    ["Recife",       33, 35, 36, 34, 37],
    ["Salvador",     31, 32, 33, 32, 34],
    ["Rio de Janeiro",36, 38, 37, 39, 40],
    ["São Paulo",    28, 29, 30, 31, 29],
    ["Manaus",       34, 36, 37, 38, 36]
]

def processar(dados):
    maior_temp = -999
    cidade_mais_quente = ""
    ondas = []

    for linha in dados:
        cidade = linha[0]
        temps = linha[1:]

        media = sum(temps) / 5
        maior_da_cidade = max(temps)

        if maior_da_cidade > maior_temp:
            maior_temp = maior_da_cidade
            cidade_mais_quente = cidade

        if media > 35:
            ondas.append(cidade)
            print(f"Alerta: Onda de calor em {cidade}")

    return ondas, cidade_mais_quente, maior_temp


# ---- PROGRAMA PRINCIPAL ----

ondas, cidade_quente, maior_temp = processar(dados)

# média geral e total de medições
todas_temps = []
for linha in dados:
    todas_temps.extend(linha[1:])

media_geral = sum(todas_temps) / len(todas_temps)
total_medicoes = len(todas_temps)

print("\n==== RELATÓRIO FINAL ====\n")

for linha in dados:
    cidade = linha[0]
    temps = linha[1:]
    media = sum(temps) / 5
    maior_da_cidade = max(temps)
    situacao = "Onda de Calor" if media > 35 else "Normal"

    print(f"{cidade}:")
    print(f" Média: {media:.2f}")
    print(f" Maior temp.: {maior_da_cidade}")
    print(f" Situação: {situacao}\n")

print("Cidade mais quente:", cidade_quente)
print("Maior temperatura absoluta:", maior_temp)
print("Média geral das temperaturas:", round(media_geral, 2))
print("Total de medições:", total_medicoes)
