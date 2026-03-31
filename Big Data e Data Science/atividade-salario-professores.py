import pandas as pd

# Lê a planilha
arquivo = "salario_prof.xlsx"
df = pd.read_excel(arquivo)

# Renomeia as colunas
df.columns = ["UF", "Salario", "Regiao"]

# Converte salário para número
df["Salario"] = (
    df["Salario"]
    .astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)

df["Salario"] = pd.to_numeric(df["Salario"], errors="coerce")

# Estado com menor salário
estado_menor = df.loc[df["Salario"].idxmin()]

# Estado com maior salário
estado_maior = df.loc[df["Salario"].idxmax()]

# Cria ranking do maior para o menor salário
ranking = df.sort_values(by="Salario", ascending=False).reset_index(drop=True)
ranking.index = ranking.index + 1

# Busca a posição de Goiás
goias = ranking[ranking["UF"] == "GO"]

# Média salarial geral
media_geral = df["Salario"].mean()

# Média salarial por região
media_por_regiao = df.groupby("Regiao")["Salario"].mean()

# Maior salário por região
maior_por_regiao = df.groupby("Regiao")["Salario"].max()

# Menor salário por região
menor_por_regiao = df.groupby("Regiao")["Salario"].min()

# Região com maior média salarial
regiao_maior_media = media_por_regiao.idxmax()
valor_maior_media = media_por_regiao.max()

# Região com menor média salarial
regiao_menor_media = media_por_regiao.idxmin()
valor_menor_media = media_por_regiao.min()

# Exibe os resultados
print("ESTADO COM MENOR SALÁRIO:")
print(f"{estado_menor['UF']} - R$ {estado_menor['Salario']:.2f}")
print()

print("ESTADO COM MAIOR SALÁRIO:")
print(f"{estado_maior['UF']} - R$ {estado_maior['Salario']:.2f}")
print()

print("POSIÇÃO DE GOIÁS:")
if not goias.empty:
    posicao = goias.index[0]
    salario_goias = goias.iloc[0]["Salario"]
    print(f"Goiás está na {posicao}ª posição com salário de R$ {salario_goias:.2f}")
else:
    print("Goiás não foi encontrado na planilha.")
print()

print("MÉDIA SALARIAL GERAL:")
print(f"R$ {media_geral:.2f}")
print()

print("MÉDIA SALARIAL POR REGIÃO:")
print(media_por_regiao)
print()

print("MAIOR SALÁRIO POR REGIÃO:")
print(maior_por_regiao)
print()

print("MENOR SALÁRIO POR REGIÃO:")
print(menor_por_regiao)
print()

print("MÉDIA SALARIAL POR REGIÃO:")
print(media_por_regiao)
print()

print("REGIÃO COM MAIOR MÉDIA SALARIAL:")
print(f"{regiao_maior_media} - R$ {valor_maior_media:.2f}")
print()

print("REGIÃO COM MENOR MÉDIA SALARIAL:")
print(f"{regiao_menor_media} - R$ {valor_menor_media:.2f}")